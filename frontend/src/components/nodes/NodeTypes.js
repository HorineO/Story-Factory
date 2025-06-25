import DefaultNode from './DefaultNode';
import InputNode from './InputNode';
import OutputNode from './OutputNode';
import GenerateNode from './GenerateNode';

const nodeTypes = {
    default: DefaultNode,
    input: InputNode,
    output: OutputNode,
    generate: GenerateNode,
};

export default nodeTypes;