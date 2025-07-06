import React from 'react';
import { NodeFactory } from './NodeTypes';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 节点系统测试组件
 * 用于验证规范化后的节点系统是否正常工作
 */
const NodeSystemTest = () => {
    // 测试数据
    const testData = {
        label: '测试节点',
        content: '这是一个测试节点内容',
        text: '兼容性测试文本'
    };

    // 测试所有节点类型
    const testAllNodeTypes = () => {
        const types = NodeFactory.getSupportedTypes();
        return types.map(type => {
            const config = NodeFactory.getNodeConfig(type);
            const validation = NodeFactory.validateNodeData(type, testData);

            return (
                <div key={type} style={{ margin: '10px', padding: '10px', border: '1px solid #ccc' }}>
                    <h4>测试节点类型: {type}</h4>
                    <p>配置: {JSON.stringify(config, null, 2)}</p>
                    <p>验证结果: {validation.isValid ? '✅ 通过' : '❌ 失败'}</p>
                    {validation.errors.length > 0 && (
                        <p>错误: {validation.errors.join(', ')}</p>
                    )}
                    <div style={{ transform: 'scale(0.8)', transformOrigin: 'top left' }}>
                        {NodeFactory.createNode(type, testData)}
                    </div>
                </div>
            );
        });
    };

    // 测试数据验证
    const testDataValidation = () => {
        const testCases = [
            { type: 'text', data: {}, expected: false },
            { type: 'text', data: { label: '有标签' }, expected: true },
            { type: 'text', data: { content: '有内容' }, expected: true },
            { type: 'text', data: { text: '有文本' }, expected: true },
            { type: 'unknown', data: { label: '未知类型' }, expected: false }
        ];

        return testCases.map((testCase, index) => {
            const validation = NodeFactory.validateNodeData(testCase.type, testCase.data);
            const passed = validation.isValid === testCase.expected;

            return (
                <div key={index} style={{
                    margin: '5px',
                    padding: '5px',
                    border: `1px solid ${passed ? 'green' : 'red'}`,
                    backgroundColor: passed ? '#e8f5e8' : '#ffe8e8'
                }}>
                    <p>测试 {index + 1}: {passed ? '✅' : '❌'}</p>
                    <p>类型: {testCase.type}</p>
                    <p>数据: {JSON.stringify(testCase.data)}</p>
                    <p>期望: {testCase.expected ? '通过' : '失败'}</p>
                    <p>实际: {validation.isValid ? '通过' : '失败'}</p>
                    {validation.errors.length > 0 && (
                        <p>错误: {validation.errors.join(', ')}</p>
                    )}
                </div>
            );
        });
    };

    // 测试BaseNodeTemplate
    const testBaseNodeTemplate = () => {
        const testCases = [
            {
                name: '标准节点',
                props: {
                    data: { label: '标准节点', content: '标准内容' },
                    nodeType: 'text-node',
                    handles: [
                        { type: 'target', position: 'left', id: 'input' },
                        { type: 'source', position: 'right', id: 'output' }
                    ]
                }
            },
            {
                name: '自定义头部',
                props: {
                    data: { label: '自定义头部', content: '自定义内容' },
                    nodeType: 'chapter-node',
                    handles: [{ type: 'source', position: 'right' }],
                    customHeader: <div style={{ color: 'red' }}>🔴 自定义头部</div>
                }
            },
            {
                name: '自定义主体',
                props: {
                    data: { label: '自定义主体', content: '自定义内容' },
                    nodeType: 'generate-node',
                    handles: [{ type: 'target', position: 'left' }],
                    customBody: <div style={{ color: 'blue' }}>🔵 自定义主体内容</div>
                }
            },
            {
                name: '无效数据',
                props: {
                    data: null,
                    nodeType: 'invalid-type',
                    handles: [{ type: 'invalid', position: 'invalid' }]
                }
            }
        ];

        return testCases.map((testCase, index) => (
            <div key={index} style={{ margin: '10px', padding: '10px', border: '1px solid #ddd' }}>
                <h4>{testCase.name}</h4>
                <div style={{ transform: 'scale(0.8)', transformOrigin: 'top left' }}>
                    <BaseNodeTemplate {...testCase.props} />
                </div>
            </div>
        ));
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h2>节点系统测试</h2>

            <h3>1. 工厂模式测试</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                {testAllNodeTypes()}
            </div>

            <h3>2. 数据验证测试</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '10px' }}>
                {testDataValidation()}
            </div>

            <h3>3. BaseNodeTemplate测试</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                {testBaseNodeTemplate()}
            </div>

            <h3>4. 系统信息</h3>
            <div style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
                <p><strong>支持的节点类型:</strong> {NodeFactory.getSupportedTypes().join(', ')}</p>
                <p><strong>总节点类型数量:</strong> {NodeFactory.getSupportedTypes().length}</p>
                <p><strong>BaseNodeTemplate版本:</strong> 2.0 (规范化版本)</p>
            </div>
        </div>
    );
};

export default NodeSystemTest; 