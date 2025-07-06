import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 示例自定义节点组件 - 展示多层结构
 * 使用BaseNodeTemplate规范化实现
 */
const ExampleCustomNode = ({ data }) => {
    // 定义连接点配置 - 多层输入和输出
    const handles = [
        // 左侧输入连接点
        {
            type: 'target',
            position: 'left',
            id: 'input-1',
            label: '输入1',
            layerIndex: 0
        },
        {
            type: 'target',
            position: 'left',
            id: 'input-2',
            label: '输入2',
            layerIndex: 1
        },
        {
            type: 'target',
            position: 'left',
            id: 'input-3',
            label: '输入3',
            layerIndex: 2
        },
        // 右侧输出连接点
        {
            type: 'source',
            position: 'right',
            id: 'output-1',
            label: '输出1',
            layerIndex: 0
        },
        {
            type: 'source',
            position: 'right',
            id: 'output-2',
            label: '输出2',
            layerIndex: 1
        }
    ];

    // 自定义头部内容
    const customHeader = (
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span>🔧</span>
            <span>{data.label || '示例节点'}</span>
        </div>
    );

    // 准备左右两侧的多层内容数据
    const leftLayers = data.leftLayers || [
        { label: '输入层1', content: data.input1 || '输入内容1' },
        { label: '输入层2', content: data.input2 || '输入内容2' },
        { label: '输入层3', content: data.input3 || '输入内容3' }
    ];

    const rightLayers = data.rightLayers || [
        { label: '输出层1', content: data.output1 || '输出内容1' },
        { label: '输出层2', content: data.output2 || '输出内容2' }
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
            nodeType="text-node" // 使用文本节点样式
            handles={handles}
            customHeader={customHeader}
        />
    );
};

export default ExampleCustomNode; 