import React from 'react';
import BaseNodeTemplate from './BaseNodeTemplate';
import nodeSpecs from '../../config/nodeSpecs';

/**
 * 节点工厂类
 * 用于统一创建和验证节点实例
 */
class NodeFactory {
    // 引入外部配置，便于前后端共享与集中维护
    static nodeConfigs = nodeSpecs;

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

        // 合并默认数据，并动态构建左右内容层，便于 UI 实时展示 I/O 数据
        const nodeData = {
            label: data.label || config.defaultLabel,
            content: data.content || data.text || config.defaultContent,
            ...data
        };

        // 不再在工厂中人为构造 leftLayers/rightLayers，交由 BaseNodeTemplate 根据 handles 决定占位显示

        // 创建自定义头部
        const customHeader = (
            <div className="flex-center">
                <span>{config.icon}</span>
                <span>{nodeData.label}</span>
            </div>
        );

        // 创建自定义主体 - 为生成节点和文本节点使用固定描述文字
        let customBody;
        if (type === 'generate') {
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