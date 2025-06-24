/**
 * 该文件定义了一个用于可视化和编辑故事流程图的 React 组件。
 * 它处理节点和边的交互，并与后端数据进行同步。
 */
import React from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
} from 'reactflow';

import 'reactflow/dist/style.css';

const FlowCanvas = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect }) => {
    return (
        <div style={{ width: '100%', height: '100%' }}>
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

export default FlowCanvas;