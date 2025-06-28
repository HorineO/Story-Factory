import React from 'react';

const NodePropertiesTab = ({ selectedNode }) => {
    return (
        <div style={{ padding: '10px', color: 'white' }}>
            {selectedNode ? (
                <div>
                    <h3>节点属性</h3>
                    <p>ID: {selectedNode.id}</p>
                    <p>类型: {selectedNode.type}</p>
                    <p>数据: {JSON.stringify(selectedNode.data)}</p>
                    {/* 在这里可以添加更多节点属性的显示和编辑逻辑 */}
                </div>
            ) : (
                <p>请选择一个节点以查看其属性。</p>
            )}
        </div>
    );
};

export default NodePropertiesTab;