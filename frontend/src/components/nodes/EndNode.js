import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

function EndNode({ data }) {
    return (
        <div className="node-base end-node">
            <div className="node-header">
                {data.label}
            </div>
            <div className="node-body">
                <Handle type="target" position={Position.Left} className="react-flow__handle-left" />
                <div>
                    <strong>{data.label}</strong>
                </div>
            </div>
        </div>
    );
}

export default EndNode;