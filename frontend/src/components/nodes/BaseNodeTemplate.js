import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

/**
 * 通用节点组件模板 - 使用工厂模式配置
 * 用于快速创建新的节点类型
 * 
 * @param {Object} props
 * @param {Object} props.data - 节点数据
 * @param {string} props.data.label - 节点标签
 * @param {Array} props.data.leftLayers - 左侧内容层数组
 * @param {Array} props.data.rightLayers - 右侧内容层数组
 * @param {string} props.nodeType - 节点类型 (对应CSS类名)
 * @param {Array} props.handles - 连接点配置数组 (可选，如果不提供则从工厂获取)
 * @param {Object} props.handles[].type - 连接点类型 ('source' | 'target')
 * @param {string} props.handles[].position - 连接点位置 ('left' | 'right')
 * @param {string} props.handles[].id - 连接点ID
 * @param {string} props.handles[].label - 连接点标签
 * @param {number} props.handles[].layerIndex - 连接点对应的层索引
 * @param {boolean} props.showHeader - 是否显示头部 (默认: true)
 * @param {React.ReactNode} props.customHeader - 自定义头部内容
 * @param {React.ReactNode} props.customLeftContent - 自定义左侧内容
 * @param {React.ReactNode} props.customRightContent - 自定义右侧内容
 * @param {string} props.additionalClasses - 额外的CSS类名
 */
const BaseNodeTemplate = ({
    data = {},
    nodeType = 'text-node',
    handles = null,
    showHeader = true,
    customHeader,
    customLeftContent,
    customRightContent,
    additionalClasses = ''
}) => {
    // 数据验证和默认值处理
    const validatedData = {
        label: data?.label || '节点',
        leftLayers: data?.leftLayers || [],
        rightLayers: data?.rightLayers || [],
        ...data
    };

    // 验证nodeType
    const validNodeTypes = ['text-node', 'chapter-node', 'generate-node', 'start-node', 'end-node'];
    const validatedNodeType = validNodeTypes.includes(nodeType) ? nodeType : 'text-node';

    // 如果没有提供handles，尝试从工厂获取
    let finalHandles = handles;
    if (!finalHandles) {
        // 动态导入NodeFactory以避免循环依赖
        try {
            const NodeFactory = require('./NodeFactory').default;
            const nodeTypeKey = validatedNodeType.replace('-node', '');
            const config = NodeFactory.getNodeConfig(nodeTypeKey);
            if (config && config.handles) {
                finalHandles = config.handles;
            }
        } catch (error) {
            console.warn('无法从工厂获取handles配置:', error);
            finalHandles = [];
        }
    }

    // 获取Position枚举
    const getPosition = (pos) => {
        const positionMap = {
            'left': Position.Left,
            'right': Position.Right
        };
        return positionMap[pos] || Position.Right;
    };

    // 验证handles配置
    const validatedHandles = (finalHandles || []).filter(handle => {
        const isValidType = ['source', 'target'].includes(handle.type);
        const isValidPosition = ['left', 'right'].includes(handle.position);
        return isValidType && isValidPosition;
    });

    // 分离左右两侧的连接点
    const leftHandles = validatedHandles.filter(handle => handle.position === 'left');
    const rightHandles = validatedHandles.filter(handle => handle.position === 'right');

    // 判断节点类型
    const hasInput = leftHandles.length > 0;
    const hasOutput = rightHandles.length > 0;
    const isSingleSide = !hasInput || !hasOutput; // 只有输入或只有输出

    // 渲染内容层
    const renderContentLayers = (layers, side) => {
        if (!layers || layers.length === 0) {
            return (
                <div className="node-single-layer">
                    {side === 'left' ? '输入内容' : '输出内容'}
                </div>
            );
        }

        return layers.map((layer, index) => (
            <div key={index} className="node-content-layer">
                {layer.label || layer.content || `${side === 'left' ? '输入' : '输出'} ${index + 1}`}
            </div>
        ));
    };

    // 渲染单侧内容
    const renderSingleContent = (layers, side) => {
        if (!layers || layers.length === 0) {
            return (
                <div className="node-single-layer">
                    {side === 'left' ? '输入内容' : '输出内容'}
                </div>
            );
        }

        // 如果只有一层，使用简化显示
        if (layers.length === 1) {
            return (
                <div className="node-single-layer">
                    {layers[0].label || layers[0].content || `${side === 'left' ? '输入' : '输出'}内容`}
                </div>
            );
        }

        // 多层时使用标准显示
        return layers.map((layer, index) => (
            <div key={index} className="node-content-layer">
                {layer.label || layer.content || `${side === 'left' ? '输入' : '输出'} ${index + 1}`}
            </div>
        ));
    };

    // 渲染连接点
    const renderHandles = (handles, side) => {
        const layers = side === 'left' ? validatedData.leftLayers : validatedData.rightLayers;
        const maxLayers = Math.max(layers.length, 1);

        return handles.map((handle, index) => {
            // 计算连接点的垂直位置，与内容层对齐
            const layerIndex = handle.layerIndex !== undefined ? handle.layerIndex : index;
            const layerCount = Math.max(layers.length, 1);
            const topPercentage = layerCount > 1
                ? (layerIndex / (layerCount - 1)) * 100
                : 50;

            return (
                <div
                    key={handle.id || `${handle.type}-${handle.position}-${index}`}
                    style={{
                        position: 'absolute',
                        top: `${topPercentage}%`,
                        transform: 'translateY(-50%)',
                        pointerEvents: 'all'
                    }}
                >
                    <Handle
                        type={handle.type}
                        position={getPosition(handle.position)}
                        id={handle.id}
                        style={{
                            width: '10px',
                            height: '10px',
                            background: '#555',
                            border: '2px solid #888',
                            borderRadius: '50%',
                            transition: 'all 0.2s ease'
                        }}
                    />
                    {handle.label && (
                        <div className={`handle-label handle-label-${handle.position}`}>
                            {handle.label}
                        </div>
                    )}
                </div>
            );
        });
    };

    return (
        <div className={`node-base ${validatedNodeType} ${additionalClasses}`}>
            {/* 连接点容器 */}
            <div className="node-handles-container">
                {/* 左侧连接点 */}
                {hasInput && (
                    <div className="node-left-handles">
                        {renderHandles(leftHandles, 'left')}
                    </div>
                )}
                {/* 右侧连接点 */}
                {hasOutput && (
                    <div className="node-right-handles">
                        {renderHandles(rightHandles, 'right')}
                    </div>
                )}
            </div>

            {/* 渲染头部 */}
            {showHeader && (
                <div className="node-header">
                    {customHeader || validatedData.label}
                </div>
            )}

            {/* 渲染主体 - 根据节点类型选择布局 */}
            <div className="node-body">
                {isSingleSide ? (
                    // 单侧布局 - 只有输入或只有输出
                    <div className="node-single-content">
                        {customLeftContent || customRightContent ||
                            renderSingleContent(
                                hasInput ? validatedData.leftLayers : validatedData.rightLayers,
                                hasInput ? 'left' : 'right'
                            )}
                    </div>
                ) : (
                    // 双侧布局 - 既有输入又有输出
                    <>
                        {/* 左侧内容 */}
                        <div className="node-left-content">
                            {customLeftContent || renderContentLayers(validatedData.leftLayers, 'left')}
                        </div>
                        {/* 右侧内容 */}
                        <div className="node-right-content">
                            {customRightContent || renderContentLayers(validatedData.rightLayers, 'right')}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default BaseNodeTemplate; 