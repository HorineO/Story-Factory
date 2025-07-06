/**
 * @file NodeStateManager.js
 * @description 管理节点的状态和选择的组件
 */
import React, { useState, useEffect } from 'react';
import useStore from '../stores/useStore';

const NodeStateManager = ({ children }) => {
    const {
        nodes,
        edges,
        onNodesChange,
        onEdgesChange,
        onConnect,
        deleteNode,
        fetchNodesAndEdges,
        initSocketListeners,
        setActiveTab
    } = useStore();

    const [selectedNodeId, setSelectedNodeId] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);

    // 初始化数据
    useEffect(() => {
        fetchNodesAndEdges();
    }, [fetchNodesAndEdges]);

    // 初始化WebSocket监听
    useEffect(() => {
        initSocketListeners();
    }, [initSocketListeners]);

    // 处理选中节点的状态更新
    useEffect(() => {
        if (selectedNodeId) {
            const node = nodes.find(n => n.id === selectedNodeId);
            setSelectedNode(node);
        } else {
            setSelectedNode(null);
        }
    }, [selectedNodeId, nodes]);

    // 节点点击处理
    const onNodeClick = (event, node) => {
        setSelectedNodeId(node.id);
        setActiveTab('tab4'); // 切换到节点属性标签页
        console.log('NodeStateManager - selectedNode after click:', nodes.find(n => n.id === node.id));
    };

    // 画布点击处理
    const onPaneClick = () => {
        setSelectedNodeId(null);
        console.log('NodeStateManager - selectedNode after pane click: null');
    };

    // 构建传递给子组件的属性
    const nodeProps = {
        nodes,
        edges,
        onNodesChange,
        onEdgesChange,
        onConnect,
        deleteNode,
        onNodeClick,
        onPaneClick,
        selectedNode
    };

    return children(nodeProps);
};

export default NodeStateManager; 