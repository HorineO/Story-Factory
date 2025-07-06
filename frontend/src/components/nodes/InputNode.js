import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const InputNode = ({ data }) => {
    return (
        <div className="input-node">
            <Handle type="source" position={Position.Bottom} className="react-flow__handle-bottom" />
            <div>{data.label}</div>
            {data.text && <div className="node-text">{data.text.length > 20 ? data.text.substring(0, 20) + '...' : data.text}</div>}
        </div>
    );
};

export default InputNode;