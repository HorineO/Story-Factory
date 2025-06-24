import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavigationBar from './components/NavigationBar';
import HomePage from './pages/HomePage';

const App = () => {
    return (
        <Router>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
                <NavigationBar />
                <div style={{ flexGrow: 1, overflow: 'hidden' }}>
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/about" element={<div>关于页面</div>} /> {/* 示例关于页面 */}
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;