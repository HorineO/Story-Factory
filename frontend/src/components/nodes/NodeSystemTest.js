import React from 'react';
import NodeStyleTest from './NodeStyleTest';

/**
 * 节点系统测试页面
 * 用于验证重构后的节点样式和功能
 */
const NodeSystemTest = () => {
    return (
        <div className="page-container">
            <div className="card-container">
                <h1 className="page-title">
                    节点系统重构测试
                </h1>
                <div className="info-box">
                    <h2 className="text-white text-lg mb-2">
                        测试说明
                    </h2>
                    <p className="text-content">
                        本页面展示了重构后的节点系统，包括：
                    </p>
                    <ul className="text-content-list mt-2.5">
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