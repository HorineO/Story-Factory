import React from 'react';
import './ContextMenu.css';

const ContextMenu = ({ top, left, right, bottom, onDelete, onClose, onDuplicate }) => {
    const positionStyles = {
        position: 'absolute',
        ...(top !== false && { top }),
        ...(left !== false && { left }),
        ...(right !== false && { right }),
        ...(bottom !== false && { bottom })
    };

    return (
        <div className="context-menu" style={positionStyles}>
            <div className="menu-item" onClick={onDuplicate}>
                复制节点
            </div>
            <div className="menu-item" onClick={onDelete}>
                删除
            </div>
        </div>
    );
};

export default ContextMenu;