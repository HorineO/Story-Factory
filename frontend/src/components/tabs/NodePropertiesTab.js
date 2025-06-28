import React, { useEffect, useState } from 'react';
import useStore from '../../stores/useStore';

const NodePropertiesTab = ({ selectedNode }) => {
    const updateNodeText = useStore((state) => state.updateNodeText);
    const [nodeText, setNodeText] = useState('');

    useEffect(() => {
        console.log('NodePropertiesTab - selectedNode changed:', selectedNode);
        if (selectedNode && selectedNode.type === 'text') {
            setNodeText(selectedNode.data.text || '');
        } else {
            setNodeText('');
        }
    }, [selectedNode]);

    const handleTextChange = (event) => {
        const newText = event.target.value;
        setNodeText(newText);
        console.log('NodePropertiesTab - nodeText changed:', newText);
        if (selectedNode) {
            updateNodeText(selectedNode.id, newText);
        }
    };

    return (
        <div style={{ padding: '10px', color: 'white' }}>
            {selectedNode ? (
                <div>
                    <h3>节点属性</h3>
                    <p>ID: {selectedNode.id}</p>
                    <p>类型: {selectedNode.type}</p>
                    {selectedNode.type === 'text' && (
                        <div style={{ marginTop: '10px' }}>
                            <label htmlFor="nodeText" style={{ display: 'block', marginBottom: '5px' }}>文本内容:</label>
                            <textarea
                                id="nodeText"
                                value={nodeText}
                                onChange={handleTextChange}
                                style={{
                                    width: '100%',
                                    minHeight: '100px',
                                    backgroundColor: '#333',
                                    color: 'white',
                                    border: '1px solid #555',
                                    padding: '5px',
                                    boxSizing: 'border-box'
                                }}
                            />
                        </div>
                    )}
                    <p>数据: {JSON.stringify(selectedNode.data)}</p>
                </div>
            ) : (
                <p>请选择一个节点以查看其属性。</p>
            )}
        </div>
    );
};

export default NodePropertiesTab;