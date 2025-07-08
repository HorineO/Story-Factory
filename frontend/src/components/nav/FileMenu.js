/**
 * @file FileMenu.js
 * @description 文件操作相关的导航菜单组件
 */
import React from 'react';
import { useTranslation } from 'react-i18next';

const FileMenu = ({ onSave, onOpen }) => {
    const { t } = useTranslation();
    return (
        <li className="relative group">
            <button className="btn text-white">{t('nav.file')}</button>
            <div className="absolute left-0 mt-1 hidden w-40 max-h-72 overflow-y-auto rounded-md bg-gray-700 shadow-lg z-10 group-hover:block">
                <button className="dropdown-item" onClick={() => {/* todo create new file */ }}>{t('nav.newFile')}</button>
                <button className="dropdown-item" onClick={onOpen}>{t('nav.openFile')}</button>
                <button className="dropdown-item" onClick={onSave}>{t('nav.saveFile')}</button>
            </div>
        </li>
    );
};

export default FileMenu; 