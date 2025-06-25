import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const InputNode = ({ data }) => {
    return (
        <div className="input-node">
            <Handle type="source" position={Position.Bottom} />
            <div>{data.label}</div>
        </div>
    );
};

export default InputNode;