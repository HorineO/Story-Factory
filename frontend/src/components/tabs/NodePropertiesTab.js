import React, { useState, useEffect } from 'react';
import { useReactFlow } from 'reactflow';
import './NodePropertiesTab.css'; // 导入CSS文件

const NodePropertiesTab = ({ selectedNode }) => {
    const { setNodes } = useReactFlow();
    const [nodeLabel, setNodeLabel] = useState('');
    const [nodeText, setNodeText] = useState(''); // 新增状态用于文本输入框
    const [generatedText, setGeneratedText] = useState(''); // 新增状态用于生成结果预览

    useEffect(() => {
        if (selectedNode) {
            setNodeLabel(selectedNode.data?.label || '');
            setNodeText(selectedNode.data?.text || ''); // 初始化文本输入框的值
            setGeneratedText(selectedNode.data?.generatedText || ''); // 初始化生成结果预览
        } else {
            setNodeLabel('');
            setNodeText('');
            setGeneratedText('');
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

    const handleTextChange = (event) => {
        const newText = event.target.value;
        setNodeText(newText);
        if (selectedNode) {
            setNodes((nds) =>
                nds.map((node) =>
                    node.id === selectedNode.id
                        ? { ...node, data: { ...node.data, text: newText } }
                        : node
                )
            );
        }
    };

    const handleGenerateClick = () => {
        // 模拟生成文本，实际应用中会调用后端API
        const newGeneratedText = `这是根据输入节点文本 "${nodeText}" 生成的内容。`;
        setGeneratedText(newGeneratedText);
        if (selectedNode) {
            setNodes((nds) =>
                nds.map((node) =>
                    node.id === selectedNode.id
                        ? { ...node, data: { ...node.data, generatedText: newGeneratedText } }
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

            {selectedNode.type === 'input' && ( // 只有当节点类型是 'input' 时才显示文本输入框
                <div>
                    <label htmlFor="nodeText">文本内容:</label>
                    <textarea
                        id="nodeText"
                        value={nodeText}
                        onChange={handleTextChange}
                        rows="5" // 初始行数
                        style={{ resize: 'vertical' }} // 允许垂直调整大小
                    />
                </div>
            )}

            {selectedNode.type === 'generate' && (
                <div>
                    <button onClick={handleGenerateClick}>生成</button>
                    <textarea
                        readOnly
                        value={generatedText}
                        placeholder="生成结果预览"
                        rows="5" // 初始行数
                        style={{ resize: 'vertical' }} // 允许垂直调整大小
                    />
                </div>
            )}

            {selectedNode.type === 'output' && ( // 只有当节点类型是 'output' 时才显示文本预览框
                <div>
                    <label htmlFor="nodeText">文本内容:</label>
                    <textarea
                        id="nodeText"
                        value={nodeText}
                        readOnly // 设置为只读
                        rows="5" // 初始行数
                        style={{ resize: 'vertical' }} // 允许垂直调整大小
                    />
                </div>
            )}
            {/* 可以根据需要添加更多属性 */}
        </div>
    );
};

export default NodePropertiesTab;