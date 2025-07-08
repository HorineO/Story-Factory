/**
 * @file EditMenu.js
 * @description 编辑操作相关的导航菜单组件
 */
import React from 'react';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';

const EditMenu = () => {
    const { t } = useTranslation();
    return (
        <li className="relative group">
            <button className="btn text-white">{t('nav.edit')}</button>
            <div className="absolute left-0 mt-1 hidden w-40 max-h-72 overflow-y-auto rounded-md bg-gray-700 shadow-lg z-10 group-hover:block">
                <button className="dropdown-item">{t('nav.undo')}</button>
                <button className="dropdown-item">{t('nav.redo')}</button>
                <button className={clsx('dropdown-item')}>{t('nav.cut')}</button>
                <button className="dropdown-item">{t('nav.copy')}</button>
                <button className="dropdown-item">{t('nav.paste')}</button>
                <button className="dropdown-item">{t('nav.newNode')}</button>
            </div>
        </li>
    );
};

export default EditMenu; 