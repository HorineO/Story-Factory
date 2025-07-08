import React from 'react';
import NodeStyleTest from './NodeStyleTest';

/**
 * 节点系统测试页面
 * 用于验证重构后的节点样式和功能
 */
const NodeSystemTest = () => {
    return (
        <div className="page-container">
            <div className="max-w-[1200px] mx-auto bg-panelbg rounded-lg p-5 shadow-lg">
                <h1 className="text-white text-center mb-8 text-2xl font-bold">
                    节点系统重构测试
                </h1>

                <div className="bg-surfacebg p-4 rounded-md mb-5 border border-borderlight">
                    <h2 className="text-white text-lg mb-2">
                        测试说明
                    </h2>
                    <p className="text-gray-300 leading-relaxed">
                        本页面展示了重构后的节点系统，包括：
                    </p>
                    <ul className="text-gray-300 leading-relaxed list-disc pl-5 mt-2.5">
                        <li>左右两侧布局的节点设计</li>
                        <li>多层结构支持</li>
                        <li>连接点与内容层平行对齐</li>
                        <li>增强的视觉效果和交互</li>
                        <li>响应式设计</li>
                    </ul>
                </div>

                <NodeStyleTest />
            </div>
        </div>
    );
};

export default NodeSystemTest; 