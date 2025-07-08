/**
 * @file App.js
 * @description React 应用的主组件，负责定义应用的整体结构和路由。
 * 它集成了导航栏和主页组件。
 */
import React, { useEffect, Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import useStore from './stores/useStore';

// 路由级代码分割：按需加载 HomePage 及其依赖
const HomePage = React.lazy(() => import('./pages/HomePage'));
const App = () => {
    const initSocketListeners = useStore((state) => state.initSocketListeners);

    useEffect(() => {
        initSocketListeners();
    }, [initSocketListeners]);

    return (
        <Router>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
                <div style={{ flexGrow: 1, overflow: 'hidden' }}>
                    {/* 使用 Suspense 处理懒加载组件的加载状态 */}
                    <Suspense fallback={<div className="flex items-center justify-center h-full">Loading...</div>}>
                        <Routes>
                            <Route path="/" element={<HomePage />} />
                            <Route path="/about" element={<div>关于页面</div>} /> {/* 示例关于页面 */}
                        </Routes>
                    </Suspense>
                </div>
            </div>
        </Router>
    );
};

export default App;