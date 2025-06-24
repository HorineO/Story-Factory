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