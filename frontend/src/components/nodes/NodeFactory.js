import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';

/**
 * 节点工厂类
 * 用于统一创建和验证节点实例
 */
class NodeFactory {
    // 节点类型配置
    static nodeConfigs = {
        'start': {
            nodeType: 'start-node',
            handles: [{ type: 'source', position: 'right', id: 'output' }],
            icon: '▶️',
            defaultLabel: '开始',
            defaultContent: '开始节点'
        },
        'end': {
            nodeType: 'end-node',
            handles: [{ type: 'target', position: 'left', id: 'input' }],
            icon: '⏹️',
            defaultLabel: '结束',
            defaultContent: '结束节点'
        },
        'text': {
            nodeType: 'text-node',
            handles: [
                { type: 'source', position: 'right', id: 'output' }
            ],
            icon: '📝',
            defaultLabel: '文本',
            defaultContent: '文本内容'
        },
        'chapter': {
            nodeType: 'chapter-node',
            handles: [
                { type: 'target', position: 'left', id: 'input' },
                { type: 'source', position: 'right', id: 'output' }
            ],
            icon: '📖',
            defaultLabel: '章节',
            defaultContent: '章节内容'
        },
        'generate': {
            nodeType: 'generate-node',
            handles: [
                { type: 'target', position: 'left', id: 'input' },
                { type: 'source', position: 'right', id: 'output' }
            ],
            icon: '🤖',
            defaultLabel: '生成',
            defaultContent: '生成内容'
        }
    };

    /**
     * 创建节点组件
     * @param {string} type - 节点类型
     * @param {Object} data - 节点数据
     * @returns {React.Component} 节点组件
     */
    static createNode(type, data = {}) {
        const config = this.nodeConfigs[type];

        if (!config) {
            console.warn(`未知的节点类型: ${type}，使用默认文本节点`);
            return this.createNode('text', data);
        }

        // 合并默认数据
        const nodeData = {
            label: data.label || config.defaultLabel,
            content: data.content || data.text || config.defaultContent,
            ...data
        };

        // 创建自定义头部
        const customHeader = (
            <div className="flex-center">
                <span>{config.icon}</span>
                <span>{nodeData.label}</span>
            </div>
        );

        // 创建自定义主体 - 为生成节点和文本节点使用固定描述文字
        let customBody;
        if (type === 'start') {
            customBody = (
                <div className="node-text">
                    开始节点
                </div>
            );
        } else if (type === 'generate') {
            customBody = (
                <div className="node-text">
                    生成内容
                </div>
            );
        } else if (type === 'text') {
            customBody = (
                <div className="node-text">
                    文本内容
                </div>
            );
        } else if (type === 'chapter') {
            customBody = (
                <div className="node-text">
                    章节内容
                </div>
            );
        } else if (type === 'end') {
            customBody = (
                <div className="node-text">
                    结束节点
                </div>
            );
        } else {
            customBody = (
                <div className="node-text">
                    {nodeData.content}
                </div>
            );
        }

        return (
            <BaseNodeTemplate
                data={nodeData}
                nodeType={config.nodeType}
                handles={config.handles}
                customHeader={customHeader}
                customBody={customBody}
            />
        );
    }

    /**
     * 验证节点数据
     * @param {string} type - 节点类型
     * @param {Object} data - 节点数据
     * @returns {Object} 验证结果
     */
    static validateNodeData(type, data) {
        const config = this.nodeConfigs[type];
        const errors = [];

        if (!config) {
            errors.push(`未知的节点类型: ${type}`);
            return { isValid: false, errors };
        }

        // 验证必需字段
        if (!data.label && !data.content && !data.text) {
            errors.push('节点缺少内容');
        }

        return {
            isValid: errors.length === 0,
            errors,
            config
        };
    }

    /**
     * 获取所有支持的节点类型
     * @returns {Array} 节点类型数组
     */
    static getSupportedTypes() {
        return Object.keys(this.nodeConfigs);
    }

    /**
     * 获取节点配置
     * @param {string} type - 节点类型
     * @returns {Object} 节点配置
     */
    static getNodeConfig(type) {
        return this.nodeConfigs[type] || null;
    }
}

export default NodeFactory; 