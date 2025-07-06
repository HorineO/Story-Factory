/**
 * @file 定义了文件操作的自定义 hook
 * @description 提供项目文件的保存和打开功能
 */

const useFileOperations = ({ nodes, edges, setNodesAndEdges }) => {
    const handleSave = () => {
        const filename = window.prompt("Enter filename (e.g., my_project):", "project");
        if (filename) {
            const flowData = { nodes, edges };
            const json = JSON.stringify(flowData);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${filename}.storyfactory`;
            a.click();
            URL.revokeObjectURL(url);
        }
    };

    const handleOpen = () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.storyfactory';
        input.onchange = (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const flowData = JSON.parse(e.target.result);
                        setNodesAndEdges(flowData.nodes || [], flowData.edges || []);
                    } catch (error) {
                        console.error("Error parsing .storyfactory file:", error);
                        alert("Error opening file. Please ensure it's a valid .storyfactory file.");
                    }
                };
                reader.readAsText(file);
            }
        };
        input.click();
    };

    return { handleSave, handleOpen };
};

export default useFileOperations; 