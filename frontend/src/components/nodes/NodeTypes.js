import NodeFactory from './NodeFactory';
import GenerateNode from './GenerateNode';
import TextNode from './TextNode';
import ChapterNode from './ChapterNode';
import StartNode from './StartNode';
import EndNode from './EndNode';

// 使用工厂模式创建节点组件
const createNodeComponent = (type) => {
    return ({ data }) => NodeFactory.createNode(type, data);
};

// 节点类型映射 - 支持工厂模式和传统模式
const nodeTypes = {
    // 工厂模式 - 推荐使用
    generate: createNodeComponent('generate'),
    text: createNodeComponent('text'),
    chapter: createNodeComponent('chapter'),
    start: createNodeComponent('start'),
    end: createNodeComponent('end'),

    // 传统模式 - 保持向后兼容
    generate_legacy: GenerateNode,
    text_legacy: TextNode,
    chapter_legacy: ChapterNode,
    start_legacy: StartNode,
    end_legacy: EndNode,
};

// 导出工厂类，供其他组件使用
export { NodeFactory };

export default nodeTypes;