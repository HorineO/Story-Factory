import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

const NewNodeTab = ({ onDragStart }) => {
    const [isBasicNodesCollapsed, setIsBasicNodesCollapsed] = useState(false);
    const { t } = useTranslation();

    // 根据节点类型返回颜色类
    const typeClasses = (type) => {
        switch (type) {
            case 'text':
                return 'bg-cyan-600 border-cyan-600';
            case 'chapter':
                return 'bg-purple-700 border-purple-700';
            case 'generate':
                return 'bg-yellow-400 border-yellow-400 text-black';
            case 'start':
                return 'bg-green-600 border-green-600';
            case 'end':
                return 'bg-red-600 border-red-600';
            default:
                return 'bg-gray-800 border-gray-700';
        }
    };

    return (
        <div>
            <div
                className="bg-gray-800 text-white px-4 py-2 cursor-pointer rounded mb-2 font-bold flex justify-between items-center hover:bg-gray-700 select-none"
                onClick={() => setIsBasicNodesCollapsed(!isBasicNodesCollapsed)}
            >
                <span>{t('newNode.basicNodes')}</span>
                <span>{isBasicNodesCollapsed ? '▼' : '▲'}</span>
            </div>
            {!isBasicNodesCollapsed && (
                <div className="py-1 border-t border-gray-700">
                    {[
                        { type: 'generate', label: t('newNode.generateNode') },
                        { type: 'text', label: t('newNode.textNode') },
                        { type: 'chapter', label: t('newNode.chapterNode') },
                        { type: 'start', label: t('newNode.startNode') },
                        { type: 'end', label: t('newNode.endNode') },
                    ].map((node) => (
                        <div
                            key={node.type}
                            data-type={node.type}
                            draggable
                            onDragStart={(event) => onDragStart(event, node.type)}
                            className={`text-white px-4 py-2 mb-2 rounded cursor-grab active:cursor-grabbing font-bold transition hover:opacity-90 border focus:outline-none focus-visible:ring focus-visible:ring-white/50 ${typeClasses(node.type)}`}
                        >
                            {node.label}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default NewNodeTab;