import React, { useEffect, useRef } from 'react';

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
            style={{
                position: 'absolute',
                top: y,
                left: x,
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px',
                boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                zIndex: 1000,
                padding: '8px 0',
            }}
        >
            <div
                style={{
                    padding: '8px 12px',
                    cursor: 'pointer',
                    '&:hover': {
                        backgroundColor: '#f0f0f0',
                    },
                }}
                onClick={onDelete}
            >
                删除节点
            </div>
        </div>
    );
};

export default ContextMenu;