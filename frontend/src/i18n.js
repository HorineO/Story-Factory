import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            'nav': {
                'home': 'Home',
                'file': 'File',
                'edit': 'Edit',
                'help': 'Help'
            }
        }
    },
    zh: {
        translation: {
            'nav': {
                'home': '主页',
                'file': '文件',
                'edit': '编辑',
                'help': '帮助'
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