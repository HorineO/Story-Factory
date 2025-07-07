/**
 * @file 定义了一个 React 导航栏组件。
 * @description 该组件包含应用标题和导航链接。
 */
import React from 'react';
import { useNavigate } from 'react-router-dom'; // 导入 useNavigate
// import './NavigationBar.css'; // Tailwind migration: old styles removed
import FileMenu from './nav/FileMenu';
import EditMenu from './nav/EditMenu';
import HelpMenu from './nav/HelpMenu';

const NavigationBar = ({ onSave, onOpen }) => {
    const navigate = useNavigate(); // 获取 navigate 函数

    const handleNavigation = (path) => {
        navigate(path); // 使用 navigate 进行路由跳转
    };

    return (
        <nav className="w-full bg-gray-700 border border-black px-5 py-1 text-white box-border">
            <ul className="flex items-center space-x-1">
                <li><button className="px-2 py-1 text-xs text-white rounded-md hover:bg-white/10" onClick={() => handleNavigation('/')}>主页</button></li>
                <FileMenu onSave={onSave} onOpen={onOpen} />
                <EditMenu />
                <HelpMenu onNavigate={handleNavigation} />
            </ul>
        </nav>
    );
};

export default NavigationBar;