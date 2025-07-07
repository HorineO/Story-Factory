import React from 'react';
// import './ContextMenu.css'; // Tailwind migration: old styles removed

const ContextMenu = ({ top, left, right, bottom, onDelete, onClose, onDuplicate }) => {
    const positionStyles = {
        position: 'absolute',
        ...(top !== false && { top }),
        ...(left !== false && { left }),
        ...(right !== false && { right }),
        ...(bottom !== false && { bottom })
    };

    return (
        <div className="absolute bg-gray-700 border border-gray-600 rounded shadow-lg z-50 text-sm text-gray-200" style={positionStyles}>
            <div className="px-3 py-1 cursor-pointer hover:bg-gray-600" onClick={onDuplicate}>
                复制节点
            </div>
            <div className="px-3 py-1 cursor-pointer hover:bg-gray-600" onClick={onDelete}>
                删除
            </div>
        </div>
    );
};

export default ContextMenu;