/**
 * @file 定义了一个 React 导航栏组件。
 * @description 该组件包含应用标题和导航链接。
 */
import React from 'react';
import './NavigationBar.css'; // 导入CSS文件

const NavigationBar = () => {
    return (
        <nav className="navbar">
            <ul className="nav-links">
                <li><a href="/">主页</a></li>
                <li><a href="/about">关于</a></li>
            </ul>
        </nav>
    );
};

export default NavigationBar;