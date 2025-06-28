import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

const ChapterNode = ({ data }) => {
    return (
        <div className="node-base chapter-node">
            <Handle type="target" position={Position.Left} className="react-flow__handle-left" />
            <div className="node-header">
                {data.label}
            </div>
            <div className="node-body">
                {/* Node-specific content can go here */}
                Chapter Node Content
            </div>
            <Handle type="source" position={Position.Right} className="react-flow__handle-right" />
        </div>
    );
};

export default ChapterNode;