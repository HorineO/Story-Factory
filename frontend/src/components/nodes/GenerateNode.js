import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

const GenerateNode = ({ data }) => {
    return (
        <div className="node-base generate-node">
            <Handle type="target" position={Position.Left} className="react-flow__handle-left" />
            <div className="node-header">
                {data.label}
            </div>
            <div className="node-body">
                {/* Node-specific content can go here */}
                Generate Node Content
            </div>
            <Handle type="source" position={Position.Right} className="react-flow__handle-right" />
        </div>
    );
};

export default GenerateNode;