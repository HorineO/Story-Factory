import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css'; // 引入样式文件

const GenerateNode = ({ data }) => {
    return (
        <div className="generate-node">
            <Handle type="target" position={Position.Top} />
            <div>{data.label}</div>
            {data.generatedText && <div className="node-text">{data.generatedText.length > 20 ? data.generatedText.substring(0, 20) + '...' : data.generatedText}</div>}
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
};

export default GenerateNode;