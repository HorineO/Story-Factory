from __future__ import annotations

"""FastAPI version of the backend application.

This file sets up a FastAPI app that exposes the same REST endpoints and
Socket.IO events as the previous Flask implementation so that the
frontend remains fully compatible.  You can run it directly with
`python backend/fastapi_app.py` or via uvicorn: `uvicorn backend.fastapi_app:app`.
"""

import os
from typing import Any, Dict, Optional

import socketio
from fastapi import (
    APIRouter,
    Body,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.services import (
    EdgeService,
    GenerationService,
    NodeService,
    WorkflowExecutionService,
)

# ---------------------------------------------------------------------------
# Initialise core components
# ---------------------------------------------------------------------------

# Socket.IO server (ASGI mode for FastAPI)
sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins=settings.socketio_cors
)

# FastAPI instance that will handle HTTP requests
_fastapi = FastAPI(
    title="Story Factory API",
    version="1.0.0",
    debug=settings.debug,
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url=f"{settings.api_prefix}/docs",
)

# Allow cross-origin requests from anywhere (adjust for production)
_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the React static build (if available)
if os.path.isdir(settings.static_folder):
    _fastapi.mount(
        "/",
        StaticFiles(directory=settings.static_folder, html=True),
        name="static",
    )

# ---------------------------------------------------------------------------
# Dependency-free service layer singletons
# ---------------------------------------------------------------------------
node_service = NodeService()
edge_service = EdgeService()
generation_service = GenerationService()
workflow_service = WorkflowExecutionService()

# ---------------------------------------------------------------------------
# REST routers under /api prefix
# ---------------------------------------------------------------------------
api_router = APIRouter(prefix=settings.api_prefix)

# -- Nodes -------------------------------------------------------------------
nodes_router = APIRouter(prefix="/nodes", tags=["nodes"])

@nodes_router.get("/")
async def get_nodes():
    return node_service.get_all_nodes()


@nodes_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_node(node_data: Dict[str, Any] = Body(...)):
    new_node = node_service.create_node(node_data)
    await sio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
    return new_node


@nodes_router.delete("/{node_id}")
async def delete_node(node_id: str):
    if node_service.delete_node(node_id):
        await sio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return {"message": f"Node {node_id} deleted"}
    raise HTTPException(status_code=404, detail=f"Node {node_id} not found")


@nodes_router.put("/{node_id}")
async def update_node(node_id: str, node_data: Dict[str, Any] = Body(...)):
    updated = node_service.update_node(node_id, node_data)
    if updated:
        await sio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return updated
    raise HTTPException(status_code=404, detail=f"Node {node_id} not found")


@nodes_router.put("/{node_id}/text")
async def update_node_text(node_id: str, text_body: Dict[str, Any] = Body(...)):
    text = text_body.get("text", "")
    updated = node_service.update_node_text(node_id, text)
    if updated:
        await sio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return updated
    raise HTTPException(status_code=404, detail=f"Node {node_id} not found")


@nodes_router.post("/{node_id}/generate")
async def generate_from_node(node_id: str):
    try:
        generated_text, target_id, source_id = generation_service.generate_text_from_connected_node(node_id)
        if not generated_text:
            raise HTTPException(status_code=404, detail="No connected source node found")
        node_service.update_node_text(node_id, generated_text)
        return {
            "generated_text": generated_text,
            "node_id": target_id,
            "source_node_id": source_id,
        }
    except HTTPException:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@nodes_router.post("/{node_id}/execute")
async def execute_node(node_id: str, data: Optional[Dict[str, Any]] = Body(default=None)):
    input_data = (data or {}).get("input_data", {})
    result = workflow_service.execute_node(node_id, input_data)
    if result.get("status") == "completed":
        await sio.emit(
            "node_executed",
            {"node_id": node_id, "success": True, "output": result.get("output")},
        )
    else:
        await sio.emit(
            "node_execution_error",
            {"node_id": node_id, "error": result.get("error", "Unknown error")},
        )
    return result

# -- Edges -------------------------------------------------------------------
edges_router = APIRouter(prefix="/edges", tags=["edges"])

@edges_router.get("/")
async def get_edges():
    return edge_service.get_all_edges()


@edges_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_edge(edge_data: Dict[str, Any] = Body(...)):
    try:
        new_edge = edge_service.create_edge(edge_data)
        await sio.emit("edges_update", {"edges": edge_service.get_all_edges()})
        return new_edge
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@edges_router.put("/{edge_id}")
async def update_edge(edge_id: str, edge_data: Dict[str, Any] = Body(...)):
    updated = edge_service.update_edge(edge_id, edge_data)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail=f"Edge {edge_id} not found")


@edges_router.delete("/{edge_id}")
async def delete_edge(edge_id: str):
    if edge_service.delete_edge(edge_id):
        return {"message": f"Edge {edge_id} deleted"}
    raise HTTPException(status_code=404, detail=f"Edge {edge_id} not found")


@edges_router.delete("/related_to/{node_id}")
async def delete_related_edges(node_id: str):
    if edge_service.delete_related_to_node(node_id):
        await sio.emit("edges_update", {"edges": edge_service.get_all_edges()})
        return {"message": f"Edges related to node {node_id} deleted"}
    return {"message": "No edges were deleted"}

# -- Generate ----------------------------------------------------------------
generate_router = APIRouter(prefix="/generate", tags=["generate"])

@generate_router.post("/")
async def generate_text(payload: Dict[str, Any] = Body(...)):
    user_content = payload.get("user_content")
    if not user_content:
        raise HTTPException(status_code=400, detail="user_content is required")
    generated_text = generation_service.generate_text(user_content)
    return {"generated_text": generated_text}


@generate_router.post("/basic_straight")
async def generate_text_basic_straight(payload: Dict[str, Any] = Body(...)):
    node_id = payload.get("nodeId")
    if not node_id:
        raise HTTPException(status_code=400, detail="nodeId is required")
    generated_text, target_id, source_id = generation_service.generate_text_from_connected_node(node_id)
    if not generated_text:
        raise HTTPException(status_code=404, detail="No connected source node found")
    return {
        "generated_text": generated_text,
        "node_id": target_id,
        "source_node_id": source_id,
    }

# -- Workflow ----------------------------------------------------------------
workflow_router = APIRouter(prefix="/workflow", tags=["workflow"])

@workflow_router.post("/execute")
async def execute_workflow(payload: Optional[Dict[str, Any]] = Body(default=None)):
    start_node_id = (payload or {}).get("start_node_id")
    result = workflow_service.execute_workflow(start_node_id)
    if result.get("success"):
        await sio.emit(
            "workflow_completed",
            {
                "success": True,
                "executed_nodes": list(result.get("executed_nodes", {}).keys()),
            },
        )
    else:
        await sio.emit(
            "workflow_error",
            {
                "error": result.get("error", "Unknown error"),
                "executed_nodes": list(result.get("executed_nodes", {}).keys()),
            },
        )
    return result


@workflow_router.get("/status")
async def get_workflow_status():
    return workflow_service.get_execution_status()

# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------
api_router.include_router(nodes_router)
api_router.include_router(edges_router)
api_router.include_router(generate_router)
api_router.include_router(workflow_router)
_fastapi.include_router(api_router)

# ---------------------------------------------------------------------------
# Socket.IO event handlers (equivalent to Flask version)
# ---------------------------------------------------------------------------

@sio.event
async def connect(sid, environ):  # type: ignore[override]
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):  # type: ignore[override]
    print(f"Client disconnected: {sid}")


@sio.on("node_status_update")
async def handle_node_status_update(sid, data):
    node_id = data.get("nodeId")
    status = data.get("status")
    if node_id and status:
        node_service.update_node_status(node_id, status)
    await sio.emit("node_status_push", data)


@sio.on("nodes_update_request")
async def handle_nodes_update_request(sid):
    # Send latest nodes only to the requesting client
    await sio.emit("nodes_update", {"nodes": node_service.get_all_nodes()}, room=sid)


@sio.on("edges_update_request")
async def handle_edges_update_request(sid):
    await sio.emit("edges_update", {"edges": edge_service.get_all_edges()}, room=sid)


@sio.on("node_move")
async def handle_node_move(sid, data):
    node_id = data.get("nodeId")
    x = data.get("x")
    y = data.get("y")
    if node_id is None or x is None or y is None:
        return
    updated_node = node_service.update_node_position(node_id, x, y)
    if updated_node:
        # 仅推送单节点位置变化，减少前端拖动时的多余刷新
        await sio.emit(
            "node_updated",
            {"nodeId": node_id, "x": updated_node["position"]["x"], "y": updated_node["position"]["y"]},
            skip_sid=sid,
        )

# ---------------------------------------------------------------------------
# Combine FastAPI & Socket.IO into a single ASGI app that uvicorn can serve
# ---------------------------------------------------------------------------
app = socketio.ASGIApp(sio, other_asgi_app=_fastapi)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.fastapi_app:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
    ) 