import React from 'react';
import { Handle, Position } from 'reactflow';

// 颜色映射：节点类型 -> Tailwind 边框/头部背景
const typeStyles = {
    text: { border: 'border-cyan-600', headerBg: 'bg-cyan-600' },
    chapter: { border: 'border-purple-700', headerBg: 'bg-purple-700' },
    generate: { border: 'border-yellow-400', headerBg: 'bg-yellow-400 text-black' },
};

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
    const validNodeTypes = ['text-node', 'chapter-node', 'generate-node'];
    const validatedNodeType = validNodeTypes.includes(nodeType) ? nodeType : 'text-node';

    const typeKey = validatedNodeType.replace('-node', '');
    const colorStyle = typeStyles[typeKey] || { border: 'border-gray-500', headerBg: 'bg-gray-600' };

    // 公共 Tailwind 样式常量
    const baseClasses = `rounded-md shadow-lg text-xs text-gray-200 overflow-hidden min-w-[160px] max-w-[280px] flex flex-col transition-all duration-300 bg-gray-800 border-2 ${colorStyle.border} ${additionalClasses}`;
    const headerClasses = `px-2 py-1 font-bold flex items-center justify-center min-h-[24px] border-b border-white/10 ${colorStyle.headerBg}`;
    const bodyClasses = 'flex min-h-[40px] bg-gray-700';
    const leftContentClasses = 'flex-1 p-1.5 flex-col-center border-r border-white/10';
    const rightContentClasses = 'flex-1 p-1.5 flex-col-center';
    const singleContentClasses = 'flex-1 p-2 flex-col-center justify-center items-center';
    const contentLayerClass = 'px-1.5 py-1 bg-white/5 rounded border border-white/10 min-h-[18px] flex items-center text-[11px] text-gray-400 transition hover:bg-white/10 hover:border-white/20 break-words';
    const singleLayerClass = 'px-2 py-1 bg-white/5 rounded border border-white/10 min-h-[20px] flex items-center justify-center text-[11px] text-gray-400 text-center break-words';

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
                <div className={singleLayerClass}>
                    {side === 'left' ? '输入内容' : '输出内容'}
                </div>
            );
        }

        return layers.map((layer, index) => (
            <div key={index} className={contentLayerClass}>
                {layer.label || layer.content || `${side === 'left' ? '输入' : '输出'} ${index + 1}`}
            </div>
        ));
    };

    // 渲染单侧内容
    const renderSingleContent = (layers, side) => {
        if (!layers || layers.length === 0) {
            return (
                <div className={singleLayerClass}>
                    {side === 'left' ? '输入内容' : '输出内容'}
                </div>
            );
        }

        // 如果只有一层，使用简化显示
        if (layers.length === 1) {
            return (
                <div className={singleLayerClass}>
                    {layers[0].label || layers[0].content || `${side === 'left' ? '输入' : '输出'}内容`}
                </div>
            );
        }

        // 多层时使用标准显示
        return layers.map((layer, index) => (
            <div key={index} className={contentLayerClass}>
                {layer.label || layer.content || `${side === 'left' ? '输入' : '输出'} ${index + 1}`}
            </div>
        ));
    };

    // 渲染连接点
    const renderHandles = (handles, side) => {
        const layers = side === 'left' ? validatedData.leftLayers : validatedData.rightLayers;

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
                    className="absolute -translate-y-1/2 pointer-events-auto"
                    style={{ top: `${topPercentage}%` }}
                >
                    <Handle
                        type={handle.type}
                        position={getPosition(handle.position)}
                        id={handle.id}
                        className="w-[10px] h-[10px] bg-gray-600 border-2 border-gray-400 rounded-full transition duration-200"
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
        <div className={baseClasses}>
            {/* 连接点容器 */}
            <div className="absolute inset-0 pointer-events-none">
                {/* 左侧连接点 */}
                {hasInput && (
                    <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-around pointer-events-none">
                        {renderHandles(leftHandles, 'left')}
                    </div>
                )}
                {/* 右侧连接点 */}
                {hasOutput && (
                    <div className="absolute right-0 top-0 bottom-0 flex flex-col justify-around pointer-events-none">
                        {renderHandles(rightHandles, 'right')}
                    </div>
                )}
            </div>

            {/* 渲染头部 */}
            {showHeader && (
                <div className={headerClasses}>
                    {customHeader || validatedData.label}
                </div>
            )}

            {/* 渲染主体 - 根据节点类型选择布局 */}
            <div className={bodyClasses}>
                {isSingleSide ? (
                    // 单侧布局 - 只有输入或只有输出
                    <div className={singleContentClasses}>
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
                        <div className={leftContentClasses}>
                            {customLeftContent || renderContentLayers(validatedData.leftLayers, 'left')}
                        </div>
                        {/* 右侧内容 */}
                        <div className={rightContentClasses}>
                            {customRightContent || renderContentLayers(validatedData.rightLayers, 'right')}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default BaseNodeTemplate; 