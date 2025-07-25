/**
 * 该文件定义了一个用于可视化和编辑故事流程图的 React 组件。
 * 它处理节点和边的交互，并与后端数据进行同步。
 */
import React, { useCallback } from 'react';
import LeftPanel from './LeftPanel'; // 引入左侧面板组件
import './FlowCanvas.css'; // 引入样式文件
import useStore from '../stores/useStore'; // 引入 useStore
import ReactFlowWrapper from './flow/ReactFlowWrapper';
import ContextMenuHandler from './flow/ContextMenuHandler';

const FlowCanvas = () => {
    const {
        nodes,
        edges,
        onNodesChange,
        onEdgesChange,
        onConnect,
        deleteNode,
        onNodeClick,
        onPaneClick,
        selectedNode
    } = useStore();

    return (
        <div className="flow-container">
            <LeftPanel />

            <div className="flow-canvas-wrapper">
                <ReactFlowWrapper
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onNodeClick={onNodeClick}
                    onPaneClick={onPaneClick}
                />
            </div>

            <ContextMenuHandler
                deleteNode={deleteNode}
            />
        </div>
    );
};

export default FlowCanvas;