# 节点系统综合规范文档

## 1. 概述

本文档是 Story Factory 节点系统的综合规范，旨在为开发者提供一个清晰、统一的指南。经过多次重构和优化，目前的节点系统具备**智能布局**、**多层结构**和**统一配置**等核心特性，所有节点均基于 `BaseNodeTemplate` 模板和 `NodeFactory` 工厂进行构建，确保了高度的可维护性和扩展性。

---

## 2. 核心特性

- **✅ 智能布局系统**

  - 根据节点配置（是否同时包含输入和输出）自动选择**单侧**或**双侧**布局，避免不必要的空白区域。

- **✅ 多层内容结构**

  - 节点内容区域支持多个**内容层**，可用于展示复杂的节点逻辑和数据流。

- **✅ 统一配置中心**

  - 所有节点的配置（如连接点、图标、默认值）都集中在 `NodeFactory` 中管理，实现了**单一配置源**。

- **✅ 规范化的尺寸和样式**

  - 节点具有统一的尺寸规范和响应式设计，确保在不同设备上都有一致的视觉体验。

- **✅ 清晰的连接点对齐**
  - 连接点（Handle）与内容层精确对齐，直观地反映数据流向。

---

## 3. 架构设计

### 3.1. `BaseNodeTemplate.js` (基础模板)

- **位置**: `frontend/src/components/nodes/BaseNodeTemplate.js`
- **作用**: 提供所有节点的统一渲染逻辑和核心功能。
- **核心功能**:
  - 根据连接点配置自动选择布局。
  - 渲染左右两侧和多层内容。
  - 统一处理连接点（Handles）的渲染和对齐。
  - 内置数据验证和默认值处理。
  - 支持通过 props 自定义头部和内容区域。

### 3.2. `NodeFactory.js` (节点工厂)

- **位置**: `frontend/src/components/nodes/NodeFactory.js`
- **作用**: 作为所有节点的**统一配置中心**和实例化工厂。
- **核心功能**:
  - 集中管理所有节点类型的配置（连接点、图标、默认标签等）。
  - 提供创建和验证节点实例的静态方法。
  - 确保类型安全和数据一致性。

---

## 4. 智能布局系统

### 4.1. 布局规则

系统会根据一个节点是否同时拥有 `target` (输入) 和 `source` (输出) 类型的连接点来自动选择布局。

#### **双侧布局 (Bilateral)**

当节点**同时拥有**输入和输出时使用。

```
┌─────────────────────────────────────┐
│             节点头部                 │
├─────────────┬───────────────────────┤
│   左侧内容   │      右侧内容         │
│  (输入相关)  │      (输出相关)       │
│             │                       │
│  ┌─────────┐│ ┌─────────────────┐   │
│  │ 输入层 1 ││ │    输出层 1     │   │
│  └─────────┘│ └─────────────────┘   │
└─────────────┴───────────────────────┘
    ●           ●           ●
  输入1        输入2        输出1
```

#### **单侧布局 (Unilateral)**

当节点**只有**输入或**只有**输出时使用。

```
┌─────────────────────────────────────┐
│             节点头部                 │
├─────────────────────────────────────┤
│           单侧内容区域               │
│                                     │
│         ┌─────────────────┐         │
│         │     内容层      │         │
│         └─────────────────┘         │
│                                     │
└─────────────────────────────────────┘
                ●
              连接点
```

---

## 5. 节点配置与类型

### 5.1. 统一配置原则

1.  **单一配置源**: 所有节点的连接点、图标等配置均在 `NodeFactory.nodeConfigs` 中定义。
2.  **避免重复**: 节点组件本身不再定义连接点等配置信息。
3.  **统一管理**: 修改或添加节点类型只需在 `NodeFactory` 中进行。

### 5.2. 配置示例

```javascript
// NodeFactory.js
static nodeConfigs = {
    'text': {
        nodeType: 'text-node',
        handles: [
            { type: 'source', position: 'right', id: 'output' } // 只有输出 -> 单侧布局
        ],
        icon: '📝',
        defaultLabel: '文本',
    },
    'chapter': {
        nodeType: 'chapter-node',
        handles: [
            { type: 'target', position: 'left', id: 'input' },  // 既有输入
            { type: 'source', position: 'right', id: 'output' } // 也有输出 -> 双侧布局
        ],
        icon: '📖',
        defaultLabel: '章节',
    },
    // ... 其他节点配置
};
```

### 5.3. 内置节点类型

| 类型 (`type`) | 图标 | 布局类型 | 输入 | 输出 | 默认标签 |
| :------------ | :--: | :------- | :--: | :--: | :------- |
| `text`        |  📝  | 单侧     |  0   |  1   | 文本节点 |
| `chapter`     |  📖  | 双侧     |  1   |  1   | 章节节点 |
| `generate`    |  🤖  | 双侧     |  1   |  1   | 生成节点 |

---

## 6. 尺寸与样式规范

### 6.1. 节点尺寸

- **最小宽度**: `160px` (桌面端), `140px` (移动端)
- **最大宽度**: `280px` (桌面端), `240px` (移动端)
- **最小高度**: `40px` (双侧), `35px` (单侧)

### 6.2. 内容层尺寸

- **标准层高度**: `18px`
- **单层显示高度**: `20px`
- **内边距**: `4px` 到 `8px` 不等，根据布局类型调整。

---

## 7. 使用方法

### 7.1. 创建标准节点

通过 `NodeFactory` 可以方便地创建节点。

```javascript
import { NodeFactory } from "./NodeFactory"; // 注意路径

// 创建一个双侧布局的节点
const chapterNode = NodeFactory.createNode("chapter", {
  label: "第一章",
  leftLayers: [{ label: "输入", content: "故事背景" }],
  rightLayers: [{ label: "输出", content: "章节内容" }],
});

// 创建一个单侧布局的节点
const textNode = NodeFactory.createNode("text", {
  label: "开场白",
  rightLayers: [{ label: "输出", content: "从前有座山..." }],
});
```

### 7.2. 创建自定义节点

可以利用 `BaseNodeTemplate` 快速创建符合规范的自定义节点。

```javascript
import React from "react";
import BaseNodeTemplate from "./BaseNodeTemplate";

const CustomNode = ({ data }) => {
  // 1. 定义连接点，BaseNodeTemplate 会据此自动选择布局
  const handles = [
    {
      type: "target",
      position: "left",
      id: "input-1",
      label: "输入1",
      layerIndex: 0,
    },
    {
      type: "source",
      position: "right",
      id: "output-1",
      label: "输出1",
      layerIndex: 0,
    },
  ];

  // 2. (可选) 定义自定义头部
  const customHeader = (
    <div style={{ color: "blue" }}>
      <span>🎨</span>
      <span>{data.label}</span>
    </div>
  );

  // 3. 渲染基础模板
  return (
    <BaseNodeTemplate
      data={data}
      handles={handles}
      customHeader={customHeader}
    />
  );
};
```

---

## 8. 数据结构

### 8.1. 节点数据 (`data`)

```javascript
const nodeData = {
  label: "节点标题", // 显示在头部
  leftLayers: [
    // 左侧内容层 (输入)
    {
      label: "层标签",
      content: "层内容",
    },
  ],
  rightLayers: [
    // 右侧内容层 (输出)
    {
      label: "层标签",
      content: "层内容",
    },
  ],
  // ... 其他自定义字段
};
```

### 8.2. 连接点配置 (`handles`)

```javascript
const handleConfig = {
  type: "target", // 'target' (输入) 或 'source' (输出)
  position: "left", // 'left' 或 'right'
  id: "unique-handle-id", // 唯一ID
  label: "连接点标签", // (可选) 显示在连接点旁的标签
  layerIndex: 0, // (重要) 对应内容层的索引，用于垂直对齐
};
```

---

## 9. 最佳实践与迁移指南

### 9.1. 最佳实践

- 根据节点功能选择合适的连接点配置，充分利用智能布局。
- 对于多层内容的节点，使用清晰的 `label` 和 `content` 描述。
- 设计新节点时，优先复用 `BaseNodeTemplate`。

### 9.2. 向后兼容与迁移

- **兼容性**: 系统仍兼容旧的数据结构（如只使用 `data.content`），但强烈建议迁移到新的 `leftLayers` 和 `rightLayers` 格式以获得完整功能。
- **迁移建议**:
  1.  将旧的 `content` 字段迁移到 `leftLayers` 和/或 `rightLayers`。
  2.  为连接点（Handles）配置添加 `layerIndex` 属性以确保正确对齐。
  3.  考虑为连接点添加 `label` 以提高可读性。

---

## 10. 历史重构概要

<details>
<summary>点击展开查看节点系统的演进历史</summary>

### 节点样式重构 (V1)

- **目标**: 解决早期节点样式单一、缺乏结构化布局的问题。
- **核心改进**:
  - 引入**左右两侧布局**，用于区分输入和输出。
  - 增加了**多层结构**支持，允许节点展示更复杂的信息。
  - 建立了连接点与内容层的**对齐机制**。
  - 重构了 CSS，并引入了响应式设计。
- **主要产物**: `REFACTOR_SUMMARY.md`

### 节点样式优化 (V2)

- **目标**: 基于用户反馈，解决布局不智能、尺寸不统一的问题。
- **核心改进**:
  - 引入**智能布局系统**，根据连接点自动选择单侧或双侧布局。
  - 制定了严格的**节点尺寸规范**，统一了视觉风格。
  - 优化了单层和多层内容的显示样式，提升了信息密度。
- **主要产物**: `OPTIMIZATION_SUMMARY.md`
</details>
