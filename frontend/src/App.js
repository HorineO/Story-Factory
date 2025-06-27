/**
 * @file App.js
 * @description React 应用的主组件，负责定义应用的整体结构和路由。
 * 它集成了导航栏和主页组件。
 */
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import HomePage from './pages/HomePage';
const App = () => {

    return (
        <Router>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
                <div style={{ flexGrow: 1, overflow: 'hidden' }}>
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <HomePage />
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