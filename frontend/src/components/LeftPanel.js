import React from 'react';

const LeftPanel = () => {
    return (
        <div
            className="left-panel"
            style={{
                width: '250px',
                backgroundColor: '#f0f0f0',
                borderRight: '1px solid #ddd',
                padding: '10px'
            }}
        >
            <div style={{ textAlign: 'center', padding: '20px', color: '#666' }}>
                功能面板区域
            </div>
        </div>
    );
};

export default LeftPanel;