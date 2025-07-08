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