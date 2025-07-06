import React from 'react';
import { Handle, Position } from 'reactflow';
import './NodeStyles.css';

/**
 * 通用节点组件模板
 * 用于快速创建新的节点类型
 * 
 * @param {Object} props
 * @param {Object} props.data - 节点数据
 * @param {string} props.data.label - 节点标签
 * @param {string} props.data.content - 节点内容
 * @param {string} props.nodeType - 节点类型 (对应CSS类名)
 * @param {Array} props.handles - 连接点配置数组
 * @param {Object} props.handles[].type - 连接点类型 ('source' | 'target')
 * @param {string} props.handles[].position - 连接点位置 ('top' | 'right' | 'bottom' | 'left')
 * @param {string} props.handles[].id - 连接点ID (可选)
 * @param {boolean} props.showHeader - 是否显示头部 (默认: true)
 * @param {boolean} props.showBody - 是否显示主体 (默认: true)
 * @param {React.ReactNode} props.customHeader - 自定义头部内容
 * @param {React.ReactNode} props.customBody - 自定义主体内容
 * @param {string} props.additionalClasses - 额外的CSS类名
 */
const BaseNodeTemplate = ({
    data = {},
    nodeType = 'text-node',
    handles = [],
    showHeader = true,
    showBody = true,
    customHeader,
    customBody,
    additionalClasses = ''
}) => {
    // 数据验证和默认值处理
    const validatedData = {
        label: data?.label || '节点',
        content: data?.content || data?.text || '节点内容',
        ...data
    };

    // 验证nodeType
    const validNodeTypes = ['text-node', 'chapter-node', 'generate-node', 'start-node', 'end-node'];
    const validatedNodeType = validNodeTypes.includes(nodeType) ? nodeType : 'text-node';

    // 获取Position枚举
    const getPosition = (pos) => {
        const positionMap = {
            'top': Position.Top,
            'right': Position.Right,
            'bottom': Position.Bottom,
            'left': Position.Left
        };
        return positionMap[pos] || Position.Right;
    };

    // 获取连接点CSS类名
    const getHandleClass = (pos) => {
        const classMap = {
            'top': 'react-flow__handle-top',
            'right': 'react-flow__handle-right',
            'bottom': 'react-flow__handle-bottom',
            'left': 'react-flow__handle-left'
        };
        return classMap[pos] || 'react-flow__handle-right';
    };

    // 验证handles配置
    const validatedHandles = handles.filter(handle => {
        const isValidType = ['source', 'target'].includes(handle.type);
        const isValidPosition = ['top', 'right', 'bottom', 'left'].includes(handle.position);
        return isValidType && isValidPosition;
    });

    return (
        <div className={`node-base ${validatedNodeType} ${additionalClasses}`}>
            {/* 渲染连接点 */}
            {validatedHandles.map((handle, index) => (
                <Handle
                    key={handle.id || `${handle.type}-${handle.position}-${index}`}
                    type={handle.type}
                    position={getPosition(handle.position)}
                    className={getHandleClass(handle.position)}
                    id={handle.id}
                />
            ))}

            {/* 渲染头部 */}
            {showHeader && (
                <div className="node-header">
                    {customHeader || validatedData.label}
                </div>
            )}

            {/* 渲染主体 */}
            {showBody && (
                <div className="node-body">
                    {customBody || (
                        <div className="node-text">
                            {validatedData.content}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default BaseNodeTemplate; 