import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 章节节点组件
 * 使用BaseNodeTemplate规范化实现
 */
const ChapterNode = ({ data }) => {
    // 定义连接点配置 - 章节节点有输入和输出
    const handles = [
        { type: 'target', position: 'left', id: 'input' },
        { type: 'source', position: 'right', id: 'output' }
    ];

    // 自定义头部内容
    const customHeader = (
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span>📖</span>
            <span>{data.label || '章节'}</span>
        </div>
    );

    // 自定义主体内容
    const customBody = (
        <div className="node-text">
            {data.content || data.text || '章节内容'}
        </div>
    );

    return (
        <BaseNodeTemplate
            data={data}
            nodeType="chapter-node"
            handles={handles}
            customHeader={customHeader}
            customBody={customBody}
        />
    );
};

export default ChapterNode;