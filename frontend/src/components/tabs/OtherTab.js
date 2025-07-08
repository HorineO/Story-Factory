import React from 'react';
import { useTranslation } from 'react-i18next';

const OtherTab = () => {
    const { t } = useTranslation();
    return (
        <div>{t('otherTab.content')}</div>
    );
};

export default OtherTab;