import DefaultNode from './DefaultNode';
import InputNode from './InputNode';
import OutputNode from './OutputNode';
import GenerateNode from './GenerateNode';
import TextNode from './TextNode';
import ChapterNode from './ChapterNode';
import StartNode from './StartNode';
import EndNode from './EndNode';

const nodeTypes = {
    default: DefaultNode,
    input: InputNode,
    output: OutputNode,
    generate: GenerateNode,
    text: TextNode,
    chapter: ChapterNode,
    start: StartNode,
    end: EndNode,
};

export default nodeTypes;