import React, { useEffect, useRef } from 'react';
import './ContextMenu.css'; // 导入CSS文件

const ContextMenu = ({ x, y, onDelete, onClose }) => {
    const menuRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                onClose();
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [onClose]);

    return (
        <div
            ref={menuRef}
            className="context-menu" // 添加CSS类名
            style={{
                position: 'absolute',
                top: y,
                left: x,
            }}
        >
            <div
                className="menu-item" // 添加CSS类名
                onClick={onDelete}
            >
                删除节点
            </div>
        </div>
    );
};

export default ContextMenu;