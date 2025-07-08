import NodeFactory from './NodeFactory';

// 使用工厂模式创建节点组件
const createNodeComponent = (type) => {
    return ({ data }) => NodeFactory.createNode(type, data);
};

// 节点类型映射 - 统一使用工厂模式
const nodeTypes = {
    generate: createNodeComponent('generate'),
    text: createNodeComponent('text'),
    chapter: createNodeComponent('chapter'),
};

// 导出工厂类，供其他组件使用
export { NodeFactory };

export default nodeTypes;