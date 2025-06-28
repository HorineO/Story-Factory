import React from 'react';
import { Handle, Position } from 'reactflow';

function StartNode({ data }) {
    return (
        <div className="node-base start-node">
            <div className="node-header">
                {data.label}
            </div>
            <div className="node-body">
                <Handle type="source" position={Position.Right} />
                <div>
                    <strong>{data.label}</strong>
                </div>
            </div>
        </div>
    );
}

export default StartNode;