/**
 * @file FlowControls.js
 * @description 封装流程图控件，如迷你地图、控制按钮和背景
 */
import React from 'react';
import { Controls, MiniMap, Background } from 'reactflow';

const FlowControls = () => {
    return (
        <>
            <Controls />
            <MiniMap className="minimap" />
            <Background variant="dots" gap={12} size={1} color="#cccccc" />
        </>
    );
};

export default FlowControls; 