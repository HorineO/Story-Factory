import React from 'react';
import './TabPanel.css';
import useStore from '../stores/useStore';

const TabPanel = ({ tabs }) => {
    const activeTab = useStore((state) => state.activeTab);
    const setActiveTab = useStore((state) => state.setActiveTab);

    return (
        <div className="tab-panel">
            <div className="tab-headers">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`tab-header ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            <div className="tab-content">
                {tabs.map(tab => (
                    <div
                        key={tab.id}
                        className={`tab-pane ${activeTab === tab.id ? 'active' : ''}`}
                    >
                        {tab.content}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TabPanel;