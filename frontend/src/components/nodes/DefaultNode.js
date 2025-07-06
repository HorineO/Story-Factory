import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const DefaultNode = ({ data }) => {
    return (
        <div className="default-node">
            <Handle type="target" position={Position.Top} className="react-flow__handle-top" />
            <div>{data.label}</div>
            <Handle type="source" position={Position.Bottom} className="react-flow__handle-bottom" />
        </div>
    );
};

export default DefaultNode;