import React from 'react';
import NodeStyleTest from './NodeStyleTest';

/**
 * 节点系统测试页面
 * 用于验证重构后的节点样式和功能
 */
const NodeSystemTest = () => {
    return (
        <div style={{
            backgroundColor: '#1a1a1a',
            minHeight: '100vh',
            padding: '20px'
        }}>
            <div style={{
                maxWidth: '1200px',
                margin: '0 auto',
                backgroundColor: '#2a2a2a',
                borderRadius: '8px',
                padding: '20px',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)'
            }}>
                <h1 style={{
                    color: '#fff',
                    textAlign: 'center',
                    marginBottom: '30px',
                    fontSize: '24px',
                    fontWeight: 'bold'
                }}>
                    节点系统重构测试
                </h1>

                <div style={{
                    backgroundColor: '#333',
                    padding: '15px',
                    borderRadius: '6px',
                    marginBottom: '20px',
                    border: '1px solid #555'
                }}>
                    <h2 style={{
                        color: '#fff',
                        fontSize: '18px',
                        marginBottom: '10px'
                    }}>
                        测试说明
                    </h2>
                    <p style={{ color: '#ccc', lineHeight: '1.6' }}>
                        本页面展示了重构后的节点系统，包括：
                    </p>
                    <ul style={{
                        color: '#ccc',
                        lineHeight: '1.6',
                        paddingLeft: '20px',
                        marginTop: '10px'
                    }}>
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