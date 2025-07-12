export default {
    text: {
        nodeType: 'text-node',
        handles: [
            { type: 'source', position: 'right', id: 'output' }
        ],
        icon: '📝',
        defaultLabel: '文本',
        defaultContent: '文本内容'
    },
    chapter: {
        nodeType: 'chapter-node',
        handles: [
            { type: 'target', position: 'left', id: 'input' },
            { type: 'source', position: 'right', id: 'output' }
        ],
        icon: '📖',
        defaultLabel: '章节',
        defaultContent: '章节内容'
    },
    generate: {
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