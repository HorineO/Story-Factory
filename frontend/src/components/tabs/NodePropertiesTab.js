import React, { useState, useEffect } from 'react';
import { useReactFlow } from 'reactflow';
import './NodePropertiesTab.css'; // 导入CSS文件

const NodePropertiesTab = ({ selectedNode }) => {
    const { setNodes } = useReactFlow();
    const [nodeLabel, setNodeLabel] = useState('');

    useEffect(() => {
        if (selectedNode) {
            setNodeLabel(selectedNode.data?.label || '');
        } else {
            setNodeLabel('');
        }
    }, [selectedNode]);

    const handleLabelChange = (event) => {
        const newLabel = event.target.value;
        setNodeLabel(newLabel);
        if (selectedNode) {
            setNodes((nds) =>
                nds.map((node) =>
                    node.id === selectedNode.id
                        ? { ...node, data: { ...node.data, label: newLabel } }
                        : node
                )
            );
        }
    };

    if (!selectedNode) {
        return <div className="node-properties-tab no-node-selected">选择节点，就可以修改节点属性了</div>;
    }

    return (
        <div className="node-properties-tab" style={{ height: '100%' }}>
            <h3>节点属性</h3>
            <div>
                <label htmlFor="nodeLabel">显示名称:</label>
                <input
                    id="nodeLabel"
                    type="text"
                    value={nodeLabel}
                    onChange={handleLabelChange}
                />
            </div>
            {/* 可以根据需要添加更多属性 */}
        </div>
    );
};

export default NodePropertiesTab;