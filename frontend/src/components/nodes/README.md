# 节点系统规范文档

## 概述

本项目的节点系统已经进行了规范化改进，所有节点现在都基于 `BaseNodeTemplate` 实现，确保了一致性和可维护性。

## 架构设计

### 1. BaseNodeTemplate (基础模板)

- **位置**: `BaseNodeTemplate.js`
- **作用**: 提供统一的节点渲染逻辑
- **特性**:
  - 数据验证和默认值处理
  - 统一的 Handle 渲染
  - 支持自定义头部和主体
  - 错误处理和类型验证

### 2. NodeFactory (节点工厂)

- **位置**: `NodeFactory.js`
- **作用**: 统一创建和验证节点实例
- **特性**:
  - 集中管理节点配置
  - 数据验证
  - 默认值处理
  - 类型安全

### 3. 具体节点实现

所有节点都使用 `BaseNodeTemplate` 实现，包括：

- `StartNode.js` - 开始节点
- `EndNode.js` - 结束节点
- `TextNode.js` - 文本节点
- `ChapterNode.js` - 章节节点
- `GenerateNode.js` - 生成节点

## 节点类型配置

### 支持的节点类型

| 类型     | 图标 | 输入 | 输出 | 默认标签 | 默认内容 |
| -------- | ---- | ---- | ---- | -------- | -------- |
| start    | ▶️   | ❌   | ✅   | 开始     | 开始节点 |
| end      | ⏹️   | ✅   | ❌   | 结束     | 结束节点 |
| text     | 📝   | ✅   | ✅   | 文本     | 文本内容 |
| chapter  | 📖   | ✅   | ✅   | 章节     | 章节内容 |
| generate | 🤖   | ✅   | ✅   | 生成     | 生成内容 |

## 使用方法

### 1. 使用工厂模式 (推荐)

```javascript
import { NodeFactory } from "./NodeTypes";

// 创建节点组件
const MyComponent = () => {
  const nodeData = {
    label: "我的节点",
    content: "节点内容",
  };

  return NodeFactory.createNode("text", nodeData);
};
```

### 2. 使用传统模式 (向后兼容)

```javascript
import nodeTypes from "./NodeTypes";

// 使用传统方式
const MyComponent = () => {
  const nodeData = { label: "我的节点", content: "节点内容" };
  const TextNodeComponent = nodeTypes.text_legacy;

  return <TextNodeComponent data={nodeData} />;
};
```

### 3. 创建自定义节点

```javascript
import React from "react";
import BaseNodeTemplate from "./BaseNodeTemplate";

const CustomNode = ({ data }) => {
  const handles = [
    { type: "target", position: "left", id: "input" },
    { type: "source", position: "right", id: "output" },
  ];

  const customHeader = (
    <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
      <span>🎯</span>
      <span>{data.label}</span>
    </div>
  );

  return (
    <BaseNodeTemplate
      data={data}
      nodeType="text-node" // 使用现有样式
      handles={handles}
      customHeader={customHeader}
    />
  );
};
```

## 数据规范

### 标准数据字段

```javascript
const nodeData = {
  label: "节点标题", // 显示在头部
  content: "节点内容", // 显示在主体 (推荐)
  text: "节点内容", // 兼容字段
  // ... 其他自定义字段
};
```

### 数据验证

```javascript
import { NodeFactory } from "./NodeTypes";

const validation = NodeFactory.validateNodeData("text", nodeData);
if (!validation.isValid) {
  console.error("节点数据验证失败:", validation.errors);
}
```

## 样式系统

### CSS 类名规范

- `.node-base` - 基础节点样式
- `.text-node` - 文本节点样式
- `.chapter-node` - 章节节点样式
- `.generate-node` - 生成节点样式
- `.start-node` - 开始节点样式
- `.end-node` - 结束节点样式

### 自定义样式

```css
/* 添加新的节点类型样式 */
.custom-node {
  --node-border-color: #ff6b6b;
  --node-header-bg: #ff6b6b;
}

.custom-node .node-header {
  background-color: var(--node-header-bg);
}
```

## 最佳实践

### 1. 数据一致性

- 优先使用 `content` 字段存储节点内容
- 提供有意义的默认值
- 验证必需字段

### 2. 错误处理

- 使用 `NodeFactory.validateNodeData()` 验证数据
- 处理未知节点类型
- 提供用户友好的错误信息

### 3. 性能优化

- 避免在节点组件中进行复杂计算
- 使用 `React.memo` 优化渲染性能
- 合理使用 `useCallback` 和 `useMemo`

### 4. 扩展性

- 通过 `NodeFactory.nodeConfigs` 添加新节点类型
- 使用 `BaseNodeTemplate` 创建自定义节点
- 保持向后兼容性

## 迁移指南

### 从旧版本迁移

1. **更新导入语句**:

   ```javascript
   // 旧版本
   import { Handle, Position } from "reactflow";
   import "./NodeStyles.css";

   // 新版本
   import BaseNodeTemplate from "./BaseNodeTemplate";
   ```

2. **重构节点组件**:

   ```javascript
   // 旧版本
   const MyNode = ({ data }) => (
     <div className="node-base text-node">
       <Handle type="source" position={Position.Right} />
       <div className="node-header">{data.label}</div>
       <div className="node-body">{data.content}</div>
     </div>
   );

   // 新版本
   const MyNode = ({ data }) => (
     <BaseNodeTemplate
       data={data}
       nodeType="text-node"
       handles={[{ type: "source", position: "right" }]}
     />
   );
   ```

3. **使用工厂模式**:
   ```javascript
   // 推荐方式
   const MyNode = ({ data }) => NodeFactory.createNode("text", data);
   ```

## 故障排除

### 常见问题

1. **节点不显示**: 检查 `nodeType` 是否正确
2. **Handle 位置错误**: 验证 `handles` 配置
3. **样式不生效**: 确认 CSS 类名是否正确
4. **数据不显示**: 检查数据字段名称

### 调试技巧

```javascript
// 启用调试模式
console.log("节点数据:", data);
console.log("节点类型:", nodeType);
console.log("Handle配置:", handles);

// 使用工厂验证
const validation = NodeFactory.validateNodeData(type, data);
console.log("验证结果:", validation);
```
