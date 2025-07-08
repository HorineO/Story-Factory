import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 文本节点组件 - 使用工厂模式配置
 * 连接点配置统一在NodeFactory中管理
 */
const TextNode = ({ data }) => {
    // 自定义头部内容
    const customHeader = (
        <div className="flex-center">
            <span>📝</span>
            <span>{data.label || '文本节点'}</span>
        </div>
    );

    // 准备左右两侧的内容层数据
    const leftLayers = data.leftLayers || [
        { label: '文本输入', content: data.inputText || '输入文本内容' }
    ];

    const rightLayers = data.rightLayers || [
        { label: '文本输出', content: data.outputText || '输出文本内容' }
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
            nodeType="text-node"
            customHeader={customHeader}
        />
    );
};

export default TextNode;