import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 生成节点组件 - 使用工厂模式配置
 * 连接点配置统一在NodeFactory中管理
 */
const GenerateNode = ({ data }) => {
    // 自定义头部内容
    const customHeader = (
        <div className="flex items-center gap-1">
            <span>🤖</span>
            <span>{data.label || '生成节点'}</span>
        </div>
    );

    // 准备左右两侧的内容层数据
    const leftLayers = data.leftLayers || [
        { label: '生成输入', content: data.inputPrompt || '输入生成提示' }
    ];

    const rightLayers = data.rightLayers || [
        { label: '生成输出', content: data.outputContent || '输出生成内容' }
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
            nodeType="generate-node"
            customHeader={customHeader}
        />
    );
};

export default GenerateNode;