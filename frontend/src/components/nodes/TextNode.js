import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

const TextNode = ({ data }) => {
    return (
        <div className="node-base text-node">
            <div className="node-header">
                {data.label}
            </div>
            <div className="node-body">
                {/* Node-specific content can go here */}
                Text Node Content
            </div>
            <Handle type="source" position={Position.Right} className="react-flow__handle-right" />
        </div>
    );
};

export default TextNode;