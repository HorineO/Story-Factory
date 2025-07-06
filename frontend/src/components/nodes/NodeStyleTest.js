import React from 'react';
import TextNode from './TextNode';
import ChapterNode from './ChapterNode';
import GenerateNode from './GenerateNode';
import StartNode from './StartNode';
import EndNode from './EndNode';
import ExampleCustomNode from './ExampleCustomNode';
import './NodeStyles.css';

/**
 * 节点样式测试组件
 * 用于展示所有节点类型的样式效果
 */
const NodeStyleTest = () => {
    const testData = {
        text: { label: 'Text Node', text: 'This is a text node with some content' },
        chapter: { label: 'Chapter Node', content: 'Chapter content here' },
        generate: { label: 'Generate Node', content: 'AI generation node' },
        start: { label: 'Start Node', content: 'Story beginning' },
        end: { label: 'End Node', content: 'Story ending' },
        custom: { label: 'Custom Node', content: 'Custom content', status: 'active' }
    };

    const containerStyle = {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        padding: '20px',
        backgroundColor: '#1a1a1a',
        minHeight: '100vh'
    };

    const nodeContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '10px'
    };

    const labelStyle = {
        color: '#ffffff',
        fontSize: '14px',
        fontWeight: 'bold',
        textAlign: 'center'
    };

    return (
        <div style={containerStyle}>
            <div style={nodeContainerStyle}>
                <div style={labelStyle}>Text Node</div>
                <TextNode data={testData.text} />
            </div>

            <div style={nodeContainerStyle}>
                <div style={labelStyle}>Chapter Node</div>
                <ChapterNode data={testData.chapter} />
            </div>

            <div style={nodeContainerStyle}>
                <div style={labelStyle}>Generate Node</div>
                <GenerateNode data={testData.generate} />
            </div>

            <div style={nodeContainerStyle}>
                <div style={labelStyle}>Start Node</div>
                <StartNode data={testData.start} />
            </div>

            <div style={nodeContainerStyle}>
                <div style={labelStyle}>End Node</div>
                <EndNode data={testData.end} />
            </div>

            <div style={nodeContainerStyle}>
                <div style={labelStyle}>Custom Node (Template)</div>
                <ExampleCustomNode data={testData.custom} />
            </div>
        </div>
    );
};

export default NodeStyleTest; 