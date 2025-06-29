/**
 * @file 定义了应用的主页组件。
 * @description 该组件集成了流程图画布和相关工具，用于展示和编辑流程图。
 */
// frontend/src/pages/HomePage.js
// 此文件作为Homepage应用程序的主入口点，负责导入和组合各个模块。
import React, { useState, useEffect } from 'react';
import { io } from "socket.io-client";
import { ReactFlowProvider } from 'reactflow';
import useStore from '../stores/useStore';
import FlowCanvas from '../components/FlowCanvas';
import NavigationBar from '../components/NavigationBar';

import '../pages/HomePage.css';

const HomePage = () => {
    const { nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode, updateNodeStatus, fetchNodesAndEdges, setNodesAndEdges, initSocketListeners, setActiveTab } = useStore();

    useEffect(() => {
        fetchNodesAndEdges();
    }, [fetchNodesAndEdges]);
    const [selectedNodeId, setSelectedNodeId] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        initSocketListeners();
    }, [initSocketListeners]);

    useEffect(() => {
        if (selectedNodeId) {
            const node = nodes.find(n => n.id === selectedNodeId);
            setSelectedNode(node);
        } else {
            setSelectedNode(null);
        }
    }, [selectedNodeId, nodes]);

    const onNodeClick = (event, node) => {
        setSelectedNodeId(node.id);
        setActiveTab('tab4'); // 切换到节点属性标签页
        console.log('HomePage - selectedNode after click:', nodes.find(n => n.id === node.id));
    };

    const onPaneClick = () => {
        setSelectedNodeId(null);
        console.log('HomePage - selectedNode after pane click: null');
    };

    const handleSave = () => {
        const filename = window.prompt("Enter filename (e.g., my_project):", "project");
        if (filename) {
            const flowData = { nodes, edges };
            const json = JSON.stringify(flowData);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${filename}.storyfactory`;
            a.click();
            URL.revokeObjectURL(url);
        }
    };

    const handleOpen = () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.storyfactory';
        input.onchange = (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const flowData = JSON.parse(e.target.result);
                        // Assuming useStore has a way to set nodes and edges
                        // This might need adjustment based on the actual useStore implementation
                        // For now, let's assume it has setNodes and setEdges
                        setNodesAndEdges(flowData.nodes || [], flowData.edges || []);
                    } catch (error) {
                        console.error("Error parsing .storyfactory file:", error);
                        alert("Error opening file. Please ensure it's a valid .storyfactory file.");
                    }
                };
                reader.readAsText(file);
            }
        };
        input.click();
    };

    return (
        <ReactFlowProvider>
            <NavigationBar onSave={handleSave} onOpen={handleOpen} />
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
