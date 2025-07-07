/**
 * @file HelpMenu.js
 * @description 帮助相关的导航菜单组件
 */
import React from 'react';

const HelpMenu = ({ onNavigate }) => {
    return (
        <li className="relative group">
            <button className="px-2 py-1 text-xs text-white rounded-md hover:bg-white/10 focus:outline-none focus-visible:ring focus-visible:ring-white/50">帮助</button>
            <div className="absolute left-0 mt-1 hidden w-40 max-h-72 overflow-y-auto rounded-md bg-gray-700 shadow-lg z-10 group-hover:block">
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate focus:outline-none focus-visible:ring focus-visible:ring-white/50" onClick={() => onNavigate('/about')}>关于</button>
            </div>
        </li>
    );
};

export default HelpMenu; 