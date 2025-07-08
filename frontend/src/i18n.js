import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            'nav': {
                'home': 'Home',
                'file': 'File',
                'edit': 'Edit',
                'help': 'Help',
                'about': 'About',
                'saveFile': 'Save Node Project',
                'openFile': 'Open Node Project',
                'newFile': 'New Node Project',
                'undo': 'Undo (Ctrl+Z)',
                'redo': 'Redo (Ctrl+Y)',
                'cut': 'Cut',
                'copy': 'Copy',
                'paste': 'Paste',
                'newNode': 'New Node',
            },
            'leftPanel': {
                'newNode': 'New Node',
                'nodeProps': 'Node Properties',
                'directory': 'Directory',
                'other': 'Other'
            },
            'nodeProps': {
                'header': 'Node Properties',
                'id': 'ID',
                'type': 'Type',
                'textContent': 'Text Content',
                'generate': 'Generate',
                'generating': 'Generating...',
                'generatePreview': 'Generated Content Preview',
                'chapterPreview': 'Chapter Content Preview',
                'selectPrompt': 'Please select a node to view its properties.',
                'generateFail': 'Generate content failed: {{msg}}'
            },
            'newNode': {
                'basicNodes': 'Basic Nodes',
                'generateNode': 'Generate Node',
                'textNode': 'Text Node',
                'chapterNode': 'Chapter Node',
                'startNode': 'Start Node',
                'endNode': 'End Node'
            },
            'directory': {
                'content': 'Directory content'
            },
            'otherTab': {
                'content': 'Other content'
            }
        }
    },
    zh: {
        translation: {
            'nav': {
                'home': '主页',
                'file': '文件',
                'edit': '编辑',
                'help': '帮助',
                'about': '关于',
                'saveFile': '保存节点项目文件',
                'openFile': '打开节点项目文件',
                'newFile': '新建节点项目文件',
                'undo': '撤销(Ctrl+Z)',
                'redo': '重做(Ctrl+Y)',
                'cut': '剪切',
                'copy': '复制',
                'paste': '粘贴',
                'newNode': '新建节点',
            },
            'leftPanel': {
                'newNode': '新建节点',
                'nodeProps': '节点属性',
                'directory': '目录',
                'other': '其他'
            },
            'nodeProps': {
                'header': '节点属性',
                'id': 'ID',
                'type': '类型',
                'textContent': '文本内容',
                'generate': '生成',
                'generating': '生成中...',
                'generatePreview': '生成内容预览',
                'chapterPreview': '章节内容预览',
                'selectPrompt': '请选择一个节点以查看其属性。',
                'generateFail': '生成内容失败: {{msg}}'
            },
            'newNode': {
                'basicNodes': '基础节点',
                'generateNode': '生成节点',
                'textNode': '文本节点',
                'chapterNode': '章节节点',
                'startNode': '开始节点',
                'endNode': '结束节点'
            },
            'directory': {
                'content': '目录内容'
            },
            'otherTab': {
                'content': '其他内容'
            }
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        lng: 'zh', // 默认语言，可在后续通过 UI 切换
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false
        }
    });

export default i18n; 