import React, { useEffect, useState } from 'react';
import useStore from '../../stores/useStore';
import { API_BASE_URL } from '../../config';
import { useTranslation } from 'react-i18next';

const NodePropertiesTab = () => {
    const { t } = useTranslation();
    const selectedNode = useStore((state) => state.selectedNode);
    const updateNodeText = useStore((state) => state.updateNodeText);
    const updateNodeGenerate = useStore((state) => state.updateNodeGenerate);
    const [nodeText, setNodeText] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    useEffect(() => {
        console.log('NodePropertiesTab - selectedNode changed:', selectedNode);
        if (selectedNode && selectedNode.type === 'text') {
            setNodeText(selectedNode.data.text || '');
        } else if (selectedNode && selectedNode.type === 'generate') {
            setNodeText(selectedNode.data.generate || '');
        } else if (selectedNode && selectedNode.type === 'chapter') {
            setNodeText(selectedNode.data.chapterText || ''); // Assuming chapterText will be stored in node data
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
        <div className="p-2 text-white">
            {selectedNode ? (
                <div>
                    <h3 className="text-lg font-bold mb-2">{t('nodeProps.header')}</h3>
                    <p className="mb-1">{t('nodeProps.id')}: {selectedNode.id}</p>
                    <p className="mb-2">{t('nodeProps.type')}: {selectedNode.type}</p>
                    {selectedNode.type === 'text' && (
                        <div className="mt-2">
                            <label htmlFor="nodeText" className="block mb-1">{t('nodeProps.textContent')}:</label>
                            <textarea
                                id="nodeText"
                                value={nodeText}
                                onChange={handleTextChange}
                                className="w-full min-h-[100px] bg-gray-800 text-white border border-gray-600 p-2 box-border"
                            />
                        </div>
                    )}
                    {selectedNode.type === 'generate' && (
                        <div className="mt-2">
                            <button
                                className="btn-primary mb-2"
                                onClick={async () => {
                                    setIsGenerating(true);
                                    try {
                                        const response = await fetch(`${API_BASE_URL}/api/generate/`, {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json',
                                            },
                                            body: JSON.stringify({ user_content: selectedNode.data.text }), // Send data.text directly
                                        });
                                        if (!response.ok) {
                                            throw new Error(`HTTP error! status: ${response.status}`);
                                        }
                                        const data = await response.json();
                                        // Assuming the API returns an object with a 'generated_text' field
                                        const generatedContent = data.generated_text || 'No content generated.';
                                        updateNodeGenerate(selectedNode.id, generatedContent); // Update the node's generate field
                                        setNodeText(generatedContent); // Update local state for preview
                                    } catch (error) {
                                        console.error('Error generating content:', error);
                                        alert(t('nodeProps.generateFail', { msg: error.message }));
                                    } finally {
                                        setIsGenerating(false);
                                    }
                                }}
                            >
                                {isGenerating ? (
                                    <span className="inline-flex items-center">
                                        <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                                        {t('nodeProps.generating')}
                                    </span>
                                ) : t('nodeProps.generate')}
                            </button>
                            <label htmlFor="generatedTextPreview" className="block mb-1">{t('nodeProps.generatePreview')}:</label>
                            <textarea
                                id="generatedTextPreview"
                                value={nodeText} // Use nodeText for preview
                                readOnly
                                className="w-full min-h-[150px] bg-gray-800 text-white border border-gray-600 p-2 resize-y"
                            />
                        </div>
                    )}
                    {selectedNode.type === 'chapter' && (
                        <div className="mt-2">
                            <label htmlFor="chapterTextPreview" className="block mb-1">{t('nodeProps.chapterPreview')}:</label>
                            <textarea
                                id="chapterTextPreview"
                                value={nodeText} // Use nodeText for preview
                                readOnly
                                className="w-full min-h-[150px] bg-gray-800 text-white border border-gray-600 p-2 resize-y"
                            />
                        </div>
                    )}
                    <p>数据: {JSON.stringify(selectedNode.data)}</p>
                </div>
            ) : (
                <p>{t('nodeProps.selectPrompt')}</p>
            )}
        </div>
    );
};

export default NodePropertiesTab;
