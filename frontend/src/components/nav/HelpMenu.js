/**
 * @file HelpMenu.js
 * @description 帮助相关的导航菜单组件
 */
import React from 'react';
import { useTranslation } from 'react-i18next';

const HelpMenu = ({ onNavigate }) => {
    const { t } = useTranslation();
    return (
        <li className="relative group">
            <button className="btn-secondary">{t('nav.help')}</button>
            <div className="absolute left-0 mt-1 hidden w-40 max-h-72 overflow-y-auto rounded-md bg-gray-700 shadow-lg z-10 group-hover:block">
                <button className="dropdown-item" onClick={() => onNavigate('/about')}>{t('nav.about')}</button>
            </div>
        </li>
    );
};

export default HelpMenu; 