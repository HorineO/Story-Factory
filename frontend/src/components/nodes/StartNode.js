import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 开始节点组件 - 使用工厂模式配置
 * 连接点配置统一在NodeFactory中管理
 */
const StartNode = ({ data }) => {
    // 自定义头部内容
    const customHeader = (
        <div className="flex items-center gap-1">
            <span>▶️</span>
            <span>{data.label || '开始节点'}</span>
        </div>
    );

    // 准备输出内容数据 - 开始节点只有输出
    const rightLayers = data.rightLayers || [
        { label: '开始输出', content: data.startOutput || '开始输出' }
    ];

    // 合并数据
    const nodeData = {
        ...data,
        leftLayers: [], // 开始节点没有输入
        rightLayers
    };

    return (
        <BaseNodeTemplate
            data={nodeData}
            nodeType="start-node"
            customHeader={customHeader}
        />
    );
};

export default StartNode;