import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
} from 'reactflow';

import 'reactflow/dist/style.css';
import './HomePage.css';

const App = () => {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        const fetchNodesAndEdges = async () => {
            try {
                const nodesResponse = await fetch('/api/nodes');
                const nodesData = await nodesResponse.json();
                setNodes(nodesData);

                const edgesResponse = await fetch('/api/edges');
                const edgesData = await edgesResponse.json();
                setEdges(edgesData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchNodesAndEdges();
    }, [setNodes, setEdges]);

    const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

    return (
        <div style={{ width: '100vw', height: '100vh' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
            >
                <Controls />
                <MiniMap />
                <Background variant="dots" gap={12} size={1} />
            </ReactFlow>
        </div>
    );
};

export default App;