import React from 'react';
import TextNode from './TextNode';
import ChapterNode from './ChapterNode';
import GenerateNode from './GenerateNode';
import StartNode from './StartNode';
import EndNode from './EndNode';
import ExampleCustomNode from './ExampleCustomNode';

/**
 * 节点样式测试组件
 * 用于展示重构后的节点样式和功能
 */
const NodeStyleTest = () => {
    // 测试数据
    const testData = {
        // 双侧节点数据（有输入有输出）
        textNodeData: {
            label: '文本节点',
            leftLayers: [
                { label: '文本输入', content: '输入文本内容' }
            ],
            rightLayers: [
                { label: '文本输出', content: '输出文本内容' }
            ]
        },

        chapterNodeData: {
            label: '章节节点',
            leftLayers: [
                { label: '章节输入', content: '输入章节内容' }
            ],
            rightLayers: [
                { label: '章节输出', content: '输出章节内容' }
            ]
        },

        generateNodeData: {
            label: '生成节点',
            leftLayers: [
                { label: '生成输入', content: '输入生成提示' }
            ],
            rightLayers: [
                { label: '生成输出', content: '输出生成内容' }
            ]
        },

        // 单侧节点数据（只有输入或只有输出）
        startNodeData: {
            label: '开始节点',
            rightLayers: [
                { label: '开始输出', content: '开始输出' }
            ]
        },

        endNodeData: {
            label: '结束节点',
            leftLayers: [
                { label: '结束输入', content: '结束输入' }
            ]
        },

        // 多层节点数据
        multiLayerData: {
            label: '多层示例节点',
            leftLayers: [
                { label: '输入层1', content: '输入内容1' },
                { label: '输入层2', content: '输入内容2' },
                { label: '输入层3', content: '输入内容3' }
            ],
            rightLayers: [
                { label: '输出层1', content: '输出内容1' },
                { label: '输出层2', content: '输出内容2' }
            ]
        }
    };

    const containerStyle = {
        padding: '20px',
        backgroundColor: '#1a1a1a',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
    };

    const sectionStyle = {
        backgroundColor: '#2a2a2a',
        padding: '20px',
        borderRadius: '8px',
        border: '1px solid #444'
    };

    const titleStyle = {
        color: '#fff',
        fontSize: '18px',
        fontWeight: 'bold',
        marginBottom: '15px',
        borderBottom: '2px solid #555',
        paddingBottom: '8px'
    };

    const gridStyle = {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        marginTop: '15px'
    };

    const nodeContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        padding: '10px',
        backgroundColor: '#333',
        borderRadius: '6px',
        border: '1px solid #555'
    };

    return (
        <div style={containerStyle}>
            <h1 style={{ color: '#fff', textAlign: 'center', marginBottom: '30px' }}>
                节点样式重构测试
            </h1>

            {/* 双侧节点类型（有输入有输出） */}
            <div style={sectionStyle}>
                <h2 style={titleStyle}>双侧节点类型（有输入有输出）</h2>
                <p style={{ color: '#ccc', marginBottom: '15px' }}>
                    这些节点既有输入又有输出，使用左右两侧布局
                </p>
                <div style={gridStyle}>
                    <div style={nodeContainerStyle}>
                        <TextNode data={testData.textNodeData} />
                    </div>
                    <div style={nodeContainerStyle}>
                        <ChapterNode data={testData.chapterNodeData} />
                    </div>
                    <div style={nodeContainerStyle}>
                        <GenerateNode data={testData.generateNodeData} />
                    </div>
                </div>
            </div>

            {/* 单侧节点类型（只有输入或只有输出） */}
            <div style={sectionStyle}>
                <h2 style={titleStyle}>单侧节点类型（只有输入或只有输出）</h2>
                <p style={{ color: '#ccc', marginBottom: '15px' }}>
                    这些节点只有输入或只有输出，使用单侧布局，更加简洁
                </p>
                <div style={gridStyle}>
                    <div style={nodeContainerStyle}>
                        <StartNode data={testData.startNodeData} />
                    </div>
                    <div style={nodeContainerStyle}>
                        <EndNode data={testData.endNodeData} />
                    </div>
                </div>
            </div>

            {/* 多层结构节点 */}
            <div style={sectionStyle}>
                <h2 style={titleStyle}>多层结构节点</h2>
                <p style={{ color: '#ccc', marginBottom: '15px' }}>
                    展示支持多层输入输出的节点，每个连接点与对应的内容层平行对齐
                </p>
                <div style={gridStyle}>
                    <div style={nodeContainerStyle}>
                        <ExampleCustomNode data={testData.multiLayerData} />
                    </div>
                </div>
            </div>

            {/* 功能说明 */}
            <div style={sectionStyle}>
                <h2 style={titleStyle}>重构功能说明</h2>
                <div style={{ color: '#ccc', lineHeight: '1.6' }}>
                    <h3 style={{ color: '#fff', marginBottom: '10px' }}>主要改进：</h3>
                    <ul style={{ paddingLeft: '20px' }}>
                        <li><strong>智能布局：</strong>根据节点类型自动选择单侧或双侧布局</li>
                        <li><strong>规范尺寸：</strong>统一节点大小，提供更好的视觉一致性</li>
                        <li><strong>单侧优化：</strong>只有输入或输出的节点使用单侧布局，避免空白区域</li>
                        <li><strong>多层结构支持：</strong>每个区域可以包含多个内容层，支持复杂的节点逻辑</li>
                        <li><strong>连接点对齐：</strong>左侧的每个端点与对应的内容层平行，右侧相同</li>
                        <li><strong>响应式设计：</strong>节点大小和布局会根据内容自动调整</li>
                        <li><strong>视觉增强：</strong>更好的阴影、边框和悬停效果</li>
                        <li><strong>连接点标签：</strong>支持为连接点添加标签，提高可读性</li>
                    </ul>

                    <h3 style={{ color: '#fff', marginTop: '20px', marginBottom: '10px' }}>布局规则：</h3>
                    <ul style={{ paddingLeft: '20px' }}>
                        <li><strong>双侧布局：</strong>当节点既有输入又有输出时使用</li>
                        <li><strong>单侧布局：</strong>当节点只有输入或只有输出时使用</li>
                        <li><strong>尺寸规范：</strong>最小宽度160px，最大宽度280px，响应式调整</li>
                        <li><strong>内容显示：</strong>单层内容使用简化显示，多层内容使用标准显示</li>
                    </ul>

                    <h3 style={{ color: '#fff', marginTop: '20px', marginBottom: '10px' }}>使用方法：</h3>
                    <ul style={{ paddingLeft: '20px' }}>
                        <li>通过 <code>leftLayers</code> 和 <code>rightLayers</code> 数组定义内容层</li>
                        <li>通过 <code>handles</code> 数组定义连接点，使用 <code>layerIndex</code> 指定对应层</li>
                        <li>每个连接点可以添加 <code>label</code> 属性显示标签</li>
                        <li>支持自定义头部和左右两侧内容</li>
                        <li>组件会自动判断使用单侧还是双侧布局</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default NodeStyleTest; 