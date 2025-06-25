/**
 * @file 定义了一个 React 导航栏组件。
 * @description 该组件包含应用标题和导航链接。
 */
import React from 'react';
import { useNavigate } from 'react-router-dom'; // 导入 useNavigate
import './NavigationBar.css'; // 导入CSS文件

const NavigationBar = () => {
    const navigate = useNavigate(); // 获取 navigate 函数

    const handleNavigation = (path) => {
        navigate(path); // 使用 navigate 进行路由跳转
    };

    return (
        <nav className="navbar">
            <ul className="nav-links">
                <li><button onClick={() => handleNavigation('/')}>主页</button></li>
                <li><button onClick={() => handleNavigation('/edit')}>编辑</button></li>
                <li className="dropdown">
                    <button className="dropbtn">帮助</button>
                    <div className="dropdown-content">
                        <button onClick={() => handleNavigation('/about')}>关于</button>
                    </div>
                </li>
            </ul>
        </nav>
    );
};

export default NavigationBar;