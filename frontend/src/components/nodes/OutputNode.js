import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const OutputNode = ({ data }) => {
    return (
        <div className="output-node">
            <Handle type="target" position={Position.Top} className="react-flow__handle-top" />
            <div>{data.label}</div>
            {data.text && <div className="node-text">{data.text.length > 20 ? data.text.substring(0, 20) + '...' : data.text}</div>}
        </div>
    );
};

export default OutputNode;