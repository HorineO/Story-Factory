/**
 * @file 定义了应用的主页组件。
 * @description 该组件集成了流程图画布和相关工具，用于展示和编辑流程图。
 */
// frontend/src/pages/HomePage.js
// 此文件作为Homepage应用程序的主入口点，负责导入和组合各个模块。
import React, { useState, useEffect } from 'react';
import { io } from "socket.io-client";
import { ReactFlowProvider } from 'reactflow';
import useFlowData from '../hooks/useFlowData';
import FlowCanvas from '../components/FlowCanvas';

import '../pages/HomePage.css';

const HomePage = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode, updateNodeStatus }) => {
    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        const socket = io('http://localhost:5000');
        socket.on('node_status_push', (data) => {
            updateNodeStatus(data.nodeId, data.status);
        });
        return () => socket.disconnect();
    }, [updateNodeStatus]);

    const onNodeClick = (event, node) => {
        setSelectedNode(node);
    };

    const onPaneClick = () => {
        setSelectedNode(null);
    };

    return (
        <ReactFlowProvider>
            <FlowCanvas
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                deleteNode={deleteNode}
                onNodeClick={onNodeClick}
                onPaneClick={onPaneClick}
                selectedNode={selectedNode}
            />
        </ReactFlowProvider>
    );
};

export default HomePage;