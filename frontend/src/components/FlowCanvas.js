/**
 * 该文件定义了一个用于可视化和编辑故事流程图的 React 组件。
 * 它处理节点和边的交互，并与后端数据进行同步。
 */
import React, { useState, useCallback } from 'react';
import LeftPanel from './LeftPanel'; // 引入左侧面板组件
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    useReactFlow,
} from 'reactflow';
import nodeTypes from './nodes/NodeTypes';

import 'reactflow/dist/style.css';
import ContextMenu from './ContextMenu'; // 引入 ContextMenu 组件

const FlowCanvas = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode, onNodeClick, onPaneClick, selectedNode }) => {
    const reactFlowInstance = useReactFlow();
    const [showContextMenu, setShowContextMenu] = useState(false);
    const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });
    const [nodeIdToDelete, setNodeIdToDelete] = useState(null);

    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback((event) => {
        event.preventDefault();

        const type = event.dataTransfer.getData('application/reactflow');

        // check if the dropped element is valid
        if (typeof type === 'undefined' || !type) {
            return;
        }

        const position = reactFlowInstance.screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
        });

        const newNode = {
            id: `node_${Date.now()}`,
            type,
            position,
            data: { label: `${type} Node` },
        };

        reactFlowInstance.setNodes((nds) => nds.concat(newNode));
    }, [reactFlowInstance]);

    const handleNodeContextMenu = useCallback((event, node) => {
        event.preventDefault();
        setNodeIdToDelete(node.id);
        setContextMenuPosition({ x: event.clientX, y: event.clientY });
        setShowContextMenu(true);
    }, []);

    const handlePaneClickInternal = useCallback(() => {
        setShowContextMenu(false);
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
        if (nodeIdToDelete) {
            deleteNode(nodeIdToDelete);
            setShowContextMenu(false);
            setNodeIdToDelete(null);
        }
    }, [nodeIdToDelete, deleteNode]);

    return (
        <div style={{ display: 'flex', flexDirection: 'row', width: '100%', height: '100%' }}>
            {/* 使用独立左侧面板组件 */}
            <LeftPanel selectedNode={selectedNode} />

            {/* 右侧流程图区域 */}
            <div style={{ flex: 1 }}>
                <ReactFlow
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
                    nodeTypes={nodeTypes}
                    fitView
                    style={{ backgroundColor: '#e0e0e0' }}
                    proOptions={{ hideAttribution: true }}
                >
                    <Controls />
                    <MiniMap style={{ opacity: 0.85 }} />
                    <Background variant="dots" gap={12} size={1} />
                </ReactFlow>
            </div>

            {showContextMenu && (
                <ContextMenu
                    x={contextMenuPosition.x}
                    y={contextMenuPosition.y}
                    onDelete={handleDelete}
                    onClose={() => setShowContextMenu(false)}
                />
            )}
        </div>
    );
};

export default FlowCanvas;