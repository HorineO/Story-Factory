/**
 * 该文件定义了一个用于可视化和编辑故事流程图的 React 组件。
 * 它处理节点和边的交互，并与后端数据进行同步。
 */
import React, { useState, useCallback } from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
} from 'reactflow';

import 'reactflow/dist/style.css';
import ContextMenu from './ContextMenu'; // 引入 ContextMenu 组件

const FlowCanvas = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode }) => {
    const [showContextMenu, setShowContextMenu] = useState(false);
    const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });
    const [nodeIdToDelete, setNodeIdToDelete] = useState(null);

    const handleNodeContextMenu = useCallback((event, node) => {
        event.preventDefault();
        setNodeIdToDelete(node.id);
        setContextMenuPosition({ x: event.clientX, y: event.clientY });
        setShowContextMenu(true);
    }, []);

    const handlePaneClick = useCallback(() => {
        setShowContextMenu(false);
    }, []);

    const handleDelete = useCallback(() => {
        if (nodeIdToDelete) {
            deleteNode(nodeIdToDelete);
            setShowContextMenu(false);
            setNodeIdToDelete(null);
        }
    }, [nodeIdToDelete, deleteNode]);

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onNodeContextMenu={handleNodeContextMenu}
                onPaneClick={handlePaneClick}
                fitView
            >
                <Controls />
                <MiniMap />
                <Background variant="dots" gap={12} size={1} />
            </ReactFlow>
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