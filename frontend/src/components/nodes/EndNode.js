import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 结束节点组件 - 使用工厂模式配置
 * 连接点配置统一在NodeFactory中管理
 */
const EndNode = ({ data }) => {
    // 自定义头部内容
    const customHeader = (
        <div className="flex items-center gap-1">
            <span>⏹️</span>
            <span>{data.label || '结束节点'}</span>
        </div>
    );

    // 准备输入内容数据 - 结束节点只有输入
    const leftLayers = data.leftLayers || [
        { label: '结束输入', content: data.endInput || '结束输入' }
    ];

    // 合并数据
    const nodeData = {
        ...data,
        leftLayers,
        rightLayers: [] // 结束节点没有输出
    };

    return (
        <BaseNodeTemplate
            data={nodeData}
            nodeType="end-node"
            customHeader={customHeader}
        />
    );
};

export default EndNode;