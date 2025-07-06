import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 开始节点组件
 * 使用BaseNodeTemplate规范化实现
 */
const StartNode = ({ data }) => {
    // 定义连接点配置 - 开始节点只有输出
    const handles = [
        { type: 'source', position: 'right', id: 'output' }
    ];

    // 自定义头部内容
    const customHeader = (
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span>▶️</span>
            <span>{data.label || '开始'}</span>
        </div>
    );

    // 自定义主体内容
    const customBody = (
        <div className="node-text">
            {data.content || data.text || '开始节点'}
        </div>
    );

    return (
        <BaseNodeTemplate
            data={data}
            nodeType="start-node"
            handles={handles}
            customHeader={customHeader}
            customBody={customBody}
        />
    );
};

export default StartNode;