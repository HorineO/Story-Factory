import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 章节节点组件 - 使用工厂模式配置
 * 连接点配置统一在NodeFactory中管理
 */
const ChapterNode = ({ data }) => {
    // 自定义头部内容
    const customHeader = (
        <div className="flex items-center gap-1">
            <span>📖</span>
            <span>{data.label || '章节节点'}</span>
        </div>
    );

    // 准备左右两侧的内容层数据
    const leftLayers = data.leftLayers || [
        { label: '章节输入', content: data.inputContent || '输入章节内容' }
    ];

    const rightLayers = data.rightLayers || [
        { label: '章节输出', content: data.outputContent || '输出章节内容' }
    ];

    // 合并数据
    const nodeData = {
        ...data,
        leftLayers,
        rightLayers
    };

    return (
        <BaseNodeTemplate
            data={nodeData}
            nodeType="chapter-node"
            customHeader={customHeader}
        />
    );
};

export default ChapterNode;