/**
 * @file HelpMenu.js
 * @description 帮助相关的导航菜单组件
 */
import React from 'react';

const HelpMenu = ({ onNavigate }) => {
    return (
        <li className="dropdown">
            <button className="dropbtn">帮助</button>
            <div className="dropdown-content">
                <button onClick={() => onNavigate('/about')}>关于</button>
            </div>
        </li>
    );
};

export default HelpMenu; 