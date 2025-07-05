/**
 * @file 定义了一个 React 导航栏组件。
 * @description 该组件包含应用标题和导航链接。
 */
import React from 'react';
import { useNavigate } from 'react-router-dom'; // 导入 useNavigate
import './NavigationBar.css'; // 导入CSS文件
import FileMenu from './nav/FileMenu';
import EditMenu from './nav/EditMenu';
import HelpMenu from './nav/HelpMenu';

const NavigationBar = ({ onSave, onOpen }) => {
    const navigate = useNavigate(); // 获取 navigate 函数

    const handleNavigation = (path) => {
        navigate(path); // 使用 navigate 进行路由跳转
    };

    return (
        <nav className="navbar">
            <ul className="nav-links">
                <li><button onClick={() => handleNavigation('/')}>主页</button></li>
                <FileMenu onSave={onSave} onOpen={onOpen} />
                <EditMenu />
                <HelpMenu onNavigate={handleNavigation} />
            </ul>
        </nav>
    );
};

export default NavigationBar;