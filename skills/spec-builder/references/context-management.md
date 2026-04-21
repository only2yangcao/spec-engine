# 上下文窗口管理策略

> ⚠️ 本策略的目标是确保全流程对话质量不退化。这不是一个步骤，而是贯穿整个流程的运行机制。

## 为什么需要这个策略

一个完整的 spec-builder 流程（Step 0→6）在单 Session 中会消耗大量上下文窗口：

| 阶段 | 累计消耗估算 |
|---|---|
| SKILL.md + 前 2 步 | ~10-15K tokens |
| Step 3a（6-10 轮追问） | ~25-35K tokens |
| Step 3b-3c（圆桌 + 设计） | ~45-55K tokens |
| Step 4a-4b（架构 + 测试） | ~65-80K tokens |
| 多模块模式（3 模块） | ~120-180K tokens |

当上下文超过 50K tokens 后，AI 的指令遵循能力开始退化——忘记展示进度图、忽略门控检查、格式漂移、甚至忘记不能写代码。超过 100K 则可能丢失早期对话中的关键决策。

## 策略一：上下文摘要压缩

### 触发时机

每个门控检查点，在展示 🚦 格式之后，AI 必须同时执行上下文摘要。

### 摘要格式

在门控检查中追加一个 📝 上下文摘要区块：

```
🚦 门控检查：Step N → Step M
✅ 产出物：[artifact]
✅ 用户确认：[状态]
✅ 进入条件：[状态]

📝 上下文摘要（截至 Step N）：
- 项目：[一句话描述]
- 关键决策：[每条一行]
- 已产出 Artifact：[文件名 + 核心内容摘要]
- 待解决问题：[如有]
- 下一步需要的输入：[前置信息]
→ 已写入 progress.json
```

### 写入 progress.json 的摘要结构

在 spec-builder-progress.json 中增加 context_summary 字段：

```json
{
  "project_name": "...",
  "current_step": "Step N",
  "context_summary": {
    "one_liner": "一句话描述项目",
    "key_decisions": [
      { "step": "1", "decision": "目标用户是独立开发者" },
      { "step": "3a", "decision": "技术栈选定 Next.js + SQLite" }
    ],
    "artifacts_summary": {
      "SPEC.md": "v0.1 已生成，3 处 [AI 建议] 标注"
    },
    "open_questions": ["是否需要多语言支持"],
    "next_step_context": "进入 3b，关注 [AI 建议] 标注"
  }
}
```

### 摘要在后续步骤中的作用

进入新步骤时：
1. 先读取 progress.json 中的 context_summary
2. 基于摘要理解项目上下文，不依赖翻阅完整对话历史
3. 如果摘要信息不足，读取对应的 artifact 文件

原则：**依赖 artifact + 摘要，不依赖对话历史**。

## 策略二：推荐分段点（分 Session 执行）

### 自然分段点

| 分段点 | 位置 | 前序产出 | 新 Session 加载什么 |
|---|---|---|---|
| A | Step 3a 完成后 | 意图清单 + SPEC v0.1 | SKILL.md + SPEC.md + progress.json |
| B | Step 3c 完成后 | SPEC v1.0 + DESIGN v1.0 | SKILL.md + SPEC + DESIGN + progress.json |
| C | Step 4b 完成后 | 完整规格包 | SKILL.md + 全部 artifact + progress.json |

### Token 消耗对比

| 模式 | 最大单 Session 消耗 |
|---|---|
| 不分段 | ~65-80K（后期质量退化） |
| 在 A 断一次 | ~35-40K（质量稳定） |
| 在 A + B 断两次 | ~25-30K（最优质量） |

### AI 何时主动建议分段

1. **对话轮数超过 20 轮**
2. **即将进入 Step 3c 或 Step 4**（产出密集区）
3. **多模块模式的模块间切换**

### 分段建议措辞

```
💡 分段建议
当前已完成 Step [N]，对话已进行 [X] 轮。
建议在此暂停：后续步骤需要生成大量文档，新 Session 能确保最优质量。
所有 artifact 已持久化，progress.json 已保存完整摘要。

恢复方式：开新 Session → 说"继续 spec-builder" → 自动从 Step [M] 继续。
也可选择在当前 Session 继续——说"继续"即可。
```

## 策略三：恢复加载协议

### 新 Session 恢复时的加载顺序

```
1. 读取 progress.json → 获取 context_summary + 当前步骤
2. 读取已完成的 artifact 文件
3. 加载当前步骤的 reference 文件
4. 向用户展示恢复摘要
```

恢复摘要格式：

```
🔄 项目恢复：[项目名]
📝 概述：[one_liner]
📍 上次停在：Step [N]
📦 已完成 Artifact：[列表]
🔑 关键决策：[摘要]
❓ 待解决：[open_questions]
→ 从 Step [M] 继续。确认？
```

### 恢复时不需要加载的内容

- 之前步骤的 reference 文件（已通过 artifact 固化结论）
- 完整的对话历史（已通过 context_summary 压缩）
- 已完成步骤的中间讨论过程

### 恢复后的上下文消耗

| 加载项 | Token |
|---|---|
| SKILL.md | ~4K |
| progress.json + 摘要 | ~1K |
| Artifact 文件 | ~5-10K |
| 当前步骤 reference | ~1.5K |
| **总计** | **~12-17K** |

恢复后有 80%+ 上下文窗口可用于当前步骤的深度交互。

## 多模块模式的特殊处理

强烈推荐每个模块一个 Session：

```
Session 1: Step 0 → 1 → 2 → 2.5（拆分）
Session 2: 模块 A（3a → 3b → 3c → 4b）
Session 3: 模块 B（3a → 3b → 3c → 4b）
Session 4: 合并 → 5 → 6
```

模块切换时额外写入：模块级 artifact 路径、暴露接口（更新 INTERFACE_REGISTRY.md）、依赖校验结果、依赖关系。

下一模块启动时加载：全局 SPEC + 全局 ARCH + SHARED_SCHEMA + INTERFACE_REGISTRY + 当前模块执行计划。不加载前序模块的完整 SPEC/DESIGN。
