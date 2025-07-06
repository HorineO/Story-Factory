import GenerateNode from './GenerateNode';
import TextNode from './TextNode';
import ChapterNode from './ChapterNode';
import StartNode from './StartNode';
import EndNode from './EndNode';

const nodeTypes = {
    generate: GenerateNode,
    text: TextNode,
    chapter: ChapterNode,
    start: StartNode,
    end: EndNode,
};

export default nodeTypes;