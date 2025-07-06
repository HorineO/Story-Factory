import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 结束节点组件
 * 使用BaseNodeTemplate规范化实现
 */
const EndNode = ({ data }) => {
    // 定义连接点配置 - 结束节点只有输入
    const handles = [
        { type: 'target', position: 'left', id: 'input' }
    ];

    // 自定义头部内容
    const customHeader = (
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span>⏹️</span>
            <span>{data.label || '结束'}</span>
        </div>
    );

    // 自定义主体内容 - 只显示简短的描述文字
    const customBody = (
        <div className="node-text">
            结束节点
        </div>
    );

    return (
        <BaseNodeTemplate
            data={data}
            nodeType="end-node"
            handles={handles}
            customHeader={customHeader}
            customBody={customBody}
        />
    );
};

export default EndNode;