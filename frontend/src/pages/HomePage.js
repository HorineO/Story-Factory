/**
 * @file 定义了应用的主页组件。
 * @description 该组件集成了流程图画布和相关工具，用于展示和编辑流程图。
 */
// frontend/src/pages/HomePage.js
// 此文件作为Homepage应用程序的主入口点，负责导入和组合各个模块。
import React from 'react';
import useFlowData from '../hooks/useFlowData';
import FlowCanvas from '../components/FlowCanvas';

import '../pages/HomePage.css';

const HomePage = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode }) => {

    return (
        <FlowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            deleteNode={deleteNode}
        />
    );
};

export default HomePage;