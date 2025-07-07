/**
 * @file EditMenu.js
 * @description 编辑操作相关的导航菜单组件
 */
import React from 'react';

const EditMenu = () => {
    return (
        <li className="relative group">
            <button className="px-2 py-1 text-xs text-white rounded-md hover:bg-white/10">编辑</button>
            <div className="absolute left-0 mt-1 hidden w-40 max-h-72 overflow-y-auto rounded-md bg-gray-700 shadow-lg z-10 group-hover:block">
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate">撤销(Ctrl+Z)</button>
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate">重做(Ctrl+Y)</button>
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate">剪切(Ctrl+X)</button>
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate">复制(Ctrl+C)</button>
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate">粘贴(Ctrl+V)</button>
                <button className="block w-full text-left px-4 py-1 text-xs text-white hover:bg-white/10 truncate">新建节点</button>
            </div>
        </li>
    );
};

export default EditMenu; 