import React from 'react';

const NewNodeTab = ({ onDragStart }) => {
    return (
        <div>
            <div className="dndnode" onDragStart={(event) => onDragStart(event, 'default')} draggable>
                Default Node
            </div>
            {/* 可以添加更多类型的节点 */}
        </div>
    );
};

export default NewNodeTab;