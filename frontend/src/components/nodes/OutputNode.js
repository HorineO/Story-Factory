import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const OutputNode = ({ data }) => {
    return (
        <div className="node-base output-node">
            <Handle type="target" position={Position.Left} className="react-flow__handle-left" />
            <div className="node-header">
                {data.label || 'Output'}
            </div>
            <div className="node-body">
                <div className="node-text">
                    {data.text || 'Output content'}
                </div>
            </div>
            <Handle type="source" position={Position.Right} className="react-flow__handle-right" />
        </div>
    );
};

export default OutputNode;