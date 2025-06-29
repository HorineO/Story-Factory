import React, { useEffect, useState } from 'react';
import useStore from '../../stores/useStore';

const NodePropertiesTab = ({ selectedNode }) => {
    const updateNodeText = useStore((state) => state.updateNodeText);
    const [nodeText, setNodeText] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    useEffect(() => {
        console.log('NodePropertiesTab - selectedNode changed:', selectedNode);
        if (selectedNode && selectedNode.type === 'text') {
            setNodeText(selectedNode.data.text || '');
        } else if (selectedNode && selectedNode.type === 'generate') {
            setNodeText(selectedNode.data.text || selectedNode.data.generatedText || ''); // Support both data.text and data.generatedText
        } else if (selectedNode && selectedNode.type === 'chapter') {
            setNodeText(selectedNode.data.chapterText || ''); // Assuming chapterText will be stored in node data
        }
        else {
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
                    {selectedNode.type === 'generate' && (
                        <div style={{ marginTop: '10px' }}>
                            <button
                                onClick={async () => {
                                    setIsGenerating(true);
                                    try {
                                        const response = await fetch('http://127.0.0.1:5000/api/generate/basic_straight', {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json',
                                            },
                                            body: JSON.stringify({ nodeId: selectedNode.id }), // Pass node ID if needed by backend
                                        });
                                        if (!response.ok) {
                                            throw new Error(`HTTP error! status: ${response.status}`);
                                        }
                                        const data = await response.json();
                                        // Assuming the API returns an object with a 'generated_text' field
                                        const generatedContent = data.generated_text || 'No content generated.';
                                        updateNodeText(selectedNode.id, generatedContent); // Update the node's text
                                        setNodeText(generatedContent); // Update local state for preview
                                    } catch (error) {
                                        console.error('Error generating content:', error);
                                        alert('生成内容失败: ' + error.message);
                                    } finally {
                                        setIsGenerating(false);
                                    }
                                }}
                                style={{
                                    padding: '8px 15px',
                                    backgroundColor: '#007bff',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    marginBottom: '10px'
                                }}
                            >
                                {isGenerating ? (
                                    <span style={{ display: 'inline-flex', alignItems: 'center' }}>
                                        <span style={{
                                            display: 'inline-block',
                                            width: '16px',
                                            height: '16px',
                                            border: '2px solid rgba(255,255,255,0.3)',
                                            borderRadius: '50%',
                                            borderTopColor: 'white',
                                            animation: 'spin 1s linear infinite',
                                            marginRight: '8px'
                                        }}></span>
                                        生成中...
                                    </span>
                                ) : '生成'}
                            </button>
                            <label htmlFor="generatedTextPreview" style={{ display: 'block', marginBottom: '5px' }}>生成内容预览:</label>
                            <textarea
                                id="generatedTextPreview"
                                value={nodeText} // Use nodeText for preview
                                readOnly
                                style={{
                                    width: '100%',
                                    minHeight: '150px',
                                    backgroundColor: '#333',
                                    color: 'white',
                                    border: '1px solid #555',
                                    padding: '5px',
                                    boxSizing: 'border-box',
                                    resize: 'vertical'
                                }}
                            />
                        </div>
                    )}
                    {selectedNode.type === 'chapter' && (
                        <div style={{ marginTop: '10px' }}>
                            <label htmlFor="chapterTextPreview" style={{ display: 'block', marginBottom: '5px' }}>章节内容预览:</label>
                            <textarea
                                id="chapterTextPreview"
                                value={nodeText} // Use nodeText for preview
                                readOnly
                                style={{
                                    width: '100%',
                                    minHeight: '150px',
                                    backgroundColor: '#333',
                                    color: 'white',
                                    border: '1px solid #555',
                                    padding: '5px',
                                    boxSizing: 'border-box',
                                    resize: 'vertical'
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

// Add CSS animation
const styles = document.createElement('style');
styles.textContent = `
@keyframes spin {
    to { transform: rotate(360deg); }
}
`;
document.head.appendChild(styles);