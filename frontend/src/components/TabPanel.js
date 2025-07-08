import React from 'react';
import clsx from 'clsx';
// import './TabPanel.css'; // Tailwind migration: old styles removed
import useStore from '../stores/useStore';

const TabPanel = ({ tabs }) => {
    const activeTab = useStore((state) => state.activeTab);
    const setActiveTab = useStore((state) => state.setActiveTab);

    return (
        <div className="flex flex-col h-full">
            <div className="flex border-b border-gray-700 bg-gray-700 whitespace-nowrap overflow-x-auto">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={clsx('tab-btn',
                            activeTab === tab.id ? 'bg-gray-600 text-white border-b-2 border-blue-500' : 'text-gray-300 hover:bg-gray-600')}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            <div className="flex-grow p-2 bg-gray-600 text-gray-200 overflow-y-auto">
                {tabs.map(tab => (
                    <div
                        key={tab.id}
                        className={`${activeTab === tab.id ? 'block h-full' : 'hidden'}`}
                    >
                        {tab.content}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TabPanel;