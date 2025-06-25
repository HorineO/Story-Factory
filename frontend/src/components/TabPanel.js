import React, { useState } from 'react';
import './TabPanel.css'; // Assuming you'll create this CSS file

const TabPanel = ({ tabs }) => {
    const [activeTab, setActiveTab] = useState(tabs[0].id);

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