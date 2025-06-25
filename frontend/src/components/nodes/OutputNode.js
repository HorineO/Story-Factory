import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const OutputNode = ({ data }) => {
    return (
        <div className="output-node">
            <Handle type="target" position={Position.Top} />
            <div>{data.label}</div>
        </div>
    );
};

export default OutputNode;