import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 示例自定义节点
 * 展示如何使用BaseNodeTemplate创建新的节点类型
 */
const ExampleCustomNode = ({ data }) => {
    // 定义连接点配置
    const handles = [
        { type: 'target', position: 'left', id: 'input' },
        { type: 'source', position: 'right', id: 'output' }
    ];

    // 自定义头部内容
    const customHeader = (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🚀</span>
            <span>{data.label || 'Custom Node'}</span>
        </div>
    );

    // 自定义主体内容
    const customBody = (
        <div style={{ padding: '4px' }}>
            <div className="node-text">{data.content || 'Custom content'}</div>
            {data.status && (
                <div style={{
                    fontSize: '10px',
                    color: data.status === 'active' ? '#28a745' : '#dc3545',
                    marginTop: '2px'
                }}>
                    Status: {data.status}
                </div>
            )}
        </div>
    );

    return (
        <BaseNodeTemplate
            data={data}
            nodeType="text-node" // 使用现有的节点类型样式
            handles={handles}
            customHeader={customHeader}
            customBody={customBody}
            additionalClasses="node-compact" // 使用工具类
        />
    );
};

export default ExampleCustomNode; 