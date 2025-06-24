/**
 * @file App.js
 * @description React 应用的主组件，负责定义应用的整体结构和路由。
 * 它集成了导航栏和主页组件。
 */
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavigationBar from './components/NavigationBar';
import HomePage from './pages/HomePage';
import useFlowData from './hooks/useFlowData'; // 引入 useFlowData

const App = () => {
    const { nodes, edges, onNodesChange, onEdgesChange, onConnect, deleteNode } = useFlowData(); // 解构 deleteNode

    return (
        <Router>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
                <NavigationBar />
                <div style={{ flexGrow: 1, overflow: 'hidden' }}>
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <HomePage
                                    nodes={nodes}
                                    edges={edges}
                                    onNodesChange={onNodesChange}
                                    onEdgesChange={onEdgesChange}
                                    onConnect={onConnect}
                                    deleteNode={deleteNode} // 传递 deleteNode prop
                                />
                            }
                        />
                        <Route path="/about" element={<div>关于页面</div>} /> {/* 示例关于页面 */}
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;