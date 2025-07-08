import React from 'react';
import { useTranslation } from 'react-i18next';

const DirectoryTab = () => {
    const { t } = useTranslation();
    return (
        <div>{t('directory.content')}</div>
    );
};

export default DirectoryTab;