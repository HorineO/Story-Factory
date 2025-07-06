import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const DefaultNode = ({ data }) => {
    return (
        <div className="node-base default-node">
            <Handle type="target" position={Position.Top} className="react-flow__handle-top" />
            <div className="node-header">
                {data.label || 'Default Node'}
            </div>
            <div className="node-body">
                <div className="node-text">
                    {data.content || 'Default content'}
                </div>
            </div>
            <Handle type="source" position={Position.Bottom} className="react-flow__handle-bottom" />
        </div>
    );
};

export default DefaultNode;