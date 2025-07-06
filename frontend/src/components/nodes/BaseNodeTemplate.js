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
    data,
    nodeType = 'default-node',
    handles = [],
    showHeader = true,
    showBody = true,
    customHeader,
    customBody,
    additionalClasses = ''
}) => {
    // 获取Position枚举
    const getPosition = (pos) => {
        switch (pos) {
            case 'top': return Position.Top;
            case 'right': return Position.Right;
            case 'bottom': return Position.Bottom;
            case 'left': return Position.Left;
            default: return Position.Right;
        }
    };

    // 获取连接点CSS类名
    const getHandleClass = (pos) => {
        switch (pos) {
            case 'top': return 'react-flow__handle-top';
            case 'right': return 'react-flow__handle-right';
            case 'bottom': return 'react-flow__handle-bottom';
            case 'left': return 'react-flow__handle-left';
            default: return 'react-flow__handle-right';
        }
    };

    return (
        <div className={`node-base ${nodeType} ${additionalClasses}`}>
            {/* 渲染连接点 */}
            {handles.map((handle, index) => (
                <Handle
                    key={handle.id || index}
                    type={handle.type}
                    position={getPosition(handle.position)}
                    className={getHandleClass(handle.position)}
                    id={handle.id}
                />
            ))}

            {/* 渲染头部 */}
            {showHeader && (
                <div className="node-header">
                    {customHeader || data.label || 'Node'}
                </div>
            )}

            {/* 渲染主体 */}
            {showBody && (
                <div className="node-body">
                    {customBody || (
                        <div className="node-text">
                            {data.content || data.text || 'Node content'}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default BaseNodeTemplate; 