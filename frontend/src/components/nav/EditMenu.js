/**
 * @file EditMenu.js
 * @description 编辑操作相关的导航菜单组件
 */
import React from 'react';

const EditMenu = () => {
    return (
        <li className="dropdown">
            <button className="dropbtn">编辑</button>
            <div className="dropdown-content">
                <button>撤销(Ctrl+Z)</button>
                <button>重做(Ctrl+Y)</button>
                <button>剪切(Ctrl+X)</button>
                <button>复制(Ctrl+C)</button>
                <button>粘贴(Ctrl+V)</button>
                <button>新建节点</button>
            </div>
        </li>
    );
};

export default EditMenu; 