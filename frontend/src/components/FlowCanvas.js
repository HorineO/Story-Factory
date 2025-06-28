/**
 * 该文件定义了一个用于可视化和编辑故事流程图的 React 组件。
 * 它处理节点和边的交互，并与后端数据进行同步。
 */
import React, { useState, useCallback, useMemo, useRef } from 'react';
import LeftPanel from './LeftPanel'; // 引入左侧面板组件
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    useReactFlow,
} from 'reactflow';
import nodeTypes from './nodes/NodeTypes';
import useStore from '../stores/useStore'; // 引入 useStore

import 'reactflow/dist/style.css';
import ContextMenu from './ContextMenu'; // 引入 ContextMenu 组件

const FlowCanvas = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode, onNodeClick, onPaneClick, selectedNode }) => {
    const reactFlowInstance = useReactFlow();
    const flowRef = useRef(null);
    const [menu, setMenu] = useState(null);
    const addNode = useStore((state) => state.addNode); // 从 store 中获取 addNode 函数

    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback(async (event) => { // 将 onDrop 设为 async
        event.preventDefault();

        const type = event.dataTransfer.getData('application/reactflow');
        if (typeof type === 'undefined' || !type) {
            return;
        }

        const position = reactFlowInstance.screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
        });

        const newNodeData = { // 更改变量名以避免与 addNode 返回的 newNode 冲突
            type,
            position,
            data: { label: `${type} Node` },
        };

        const newNode = await addNode(newNodeData); // 调用 addNode 并等待其完成
        if (newNode) {
            reactFlowInstance.setNodes((nds) => nds.concat(newNode));
        }
    }, [reactFlowInstance, addNode]); // 添加 addNode 到依赖数组

    const handleNodeContextMenu = useCallback((event, node) => {
        event.preventDefault();

        const pane = flowRef.current.getBoundingClientRect();
        setMenu({
            id: node.id,
            top: event.clientY < pane.height - 200 && event.clientY,
            left: event.clientX < pane.width - 200 && event.clientX,
            right: event.clientX >= pane.width - 200 && pane.width - event.clientX,
            bottom: event.clientY >= pane.height - 200 && pane.height - event.clientY,
        });
    }, []);

    const handlePaneClickInternal = useCallback(() => {
        setMenu(null);
        if (onPaneClick) {
            onPaneClick();
        }
    }, [onPaneClick]);

    const handleNodeClickInternal = useCallback((event, node) => {
        if (onNodeClick) {
            onNodeClick(event, node);
        }
    }, [onNodeClick]);

    const handleDelete = useCallback(() => {
        if (menu?.id) {
            deleteNode(menu.id);
            setMenu(null);
        }
    }, [menu, deleteNode]);

    const handleDuplicate = useCallback(() => {
        if (menu?.id) {
            // Get the latest nodes directly from the store
            const currentNodes = useStore.getState().nodes;
            const nodeToDuplicate = currentNodes.find(n => n.id === menu.id);
            if (nodeToDuplicate) {
                const newNode = {
                    ...nodeToDuplicate,
                    id: `node_${Date.now()}`,
                    position: {
                        x: nodeToDuplicate.position.x + 50,
                        y: nodeToDuplicate.position.y + 50,
                    }
                };
                reactFlowInstance.setNodes(nds => nds.concat(newNode));
                setMenu(null);
            }
        }
    }, [menu, reactFlowInstance]);

    return (
        <div style={{ display: 'flex', flexDirection: 'row', width: '100%', height: '100%' }}>
            <LeftPanel selectedNode={selectedNode} />

            <div style={{ flex: 1 }}>
                <ReactFlow
                    ref={flowRef}
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onNodeContextMenu={handleNodeContextMenu}
                    onPaneClick={handlePaneClickInternal}
                    onNodeClick={handleNodeClickInternal}
                    onDragOver={onDragOver}
                    onDrop={onDrop}
                    nodeTypes={useMemo(() => nodeTypes, [])}
                    fitView
                    style={{ backgroundColor: '#282c34' }}
                    proOptions={{ hideAttribution: true }}
                >
                    <Controls />
                    <MiniMap style={{ opacity: 0.85 }} />
                    <Background variant="dots" gap={12} size={1} color="#cccccc" />
                </ReactFlow>
            </div>

            {menu && (
                <ContextMenu
                    {...menu}
                    onDelete={handleDelete}
                    onDuplicate={handleDuplicate}
                    onClose={() => setMenu(null)}
                />
            )}
        </div>
    );
};

export default FlowCanvas;