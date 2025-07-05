/**
 * @file FileMenu.js
 * @description 文件操作相关的导航菜单组件
 */
import React from 'react';

const FileMenu = ({ onSave, onOpen }) => {
    return (
        <li className="dropdown">
            <button className="dropbtn">文件</button>
            <div className="dropdown-content">
                <button>新建节点项目文件</button>
                <button onClick={onOpen}>打开节点项目文件</button>
                <button onClick={onSave}>保存节点项目文件</button>
            </div>
        </li>
    );
};

export default FileMenu; 