import React from 'react';

const LeftPanel = () => {
    return (
        <div
            className="left-panel"
            style={{
                width: '250px',
                backgroundColor: 'rgb(75, 75, 75)',
                borderRight: '1px solid #ddd',
                border: '1px solid rgb(46, 46, 46)',
                padding: '10px'
            }}
        >
            <div style={{ textAlign: 'center', padding: '20px', color: '#666' }}>
                {/* 这里是左侧面板, 功能面板区域 */}
                空白面板区域
            </div>
        </div>
    );
};

export default LeftPanel;