import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

const ChapterNode = ({ data }) => {
    return (
        <div className="chapter-node">
            <Handle type="target" position={Position.Left} />
            <div>{data.label}</div>
            <Handle type="source" position={Position.Right} />
        </div>
    );
};

export default ChapterNode;