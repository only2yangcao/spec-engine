# Step 4b: 测试场景 + 交付契约
> ⚠️ 本步骤产出物是「测试场景 + CONTRACT.md」，不是代码。如果你发现自己正在写实现代码，立即停止并回到本步骤。

**预计耗时**：30分钟-1小时 | **人类角色**：🔍 审计者 + 🎯 指挥官

## 为什么这步需要更多人类投入

Beck 的洞察：测试用例是对下游 AI 最高质量的 prompt。没有测试的 AI 编程就像没有损失函数的训练——你在做随机搜索。在这一步多花30分钟，下游执行的首次通过率从 60% 拉到 90%+。

同时，CONTRACT.md 定义了规格包的"使用说明"——约束和验收维度需要人类确认。

## 测试场景生成

**AI 做什么**：
1. 基于 SPEC.md v1.0 + DESIGN.md v1.0，为每个 Use Case 生成 **Given-When-Then** 场景：
   ```
   Given: [前置条件 — 引用 DESIGN.md 中的具体数据结构和状态]
   When:  [用户行为 — 引用 DESIGN.md 中的具体 API 端点]
   Then:  [期望结果 — 引用 DESIGN.md 中的具体响应体和错误码]
   ```
2. 包含正常路径和异常路径（空输入、错误输入、边界条件）
3. 特别关注**圆桌审查中被暴露的盲区**和 **DESIGN.md 中的业务规则**——为每条业务规则至少设计一个测试

**人类做什么**：
1. **审核每一个 Then**——这是价值判断，不能委托。Then 定义了"什么是正确的"。
2. 补充 AI 遗漏的边界条件——你比 AI 更了解你的用户会怎么"误用"产品

## CONTRACT.md 生成

**AI 做什么**：
生成交付契约。CONTRACT.md **不提取四文件的内容**，而是描述四文件的**使用方式**。

CONTRACT.md 回答四个问题：

**一、交付物清单**
列出规格包中的每个文件及其角色（一句话定义，不复制内容）。

**二、阅读协议**
定义下游执行者应该按什么顺序、以什么方式消费这些文件：

| 阶段 | 读什么 | 目的 |
|---|---|---|
| 理解意图 | SPEC.md 全文 | 建立"为什么做、做成什么样"的完整认知 |
| 理解边界 | ARCHITECTURE.md 全文 | 明确技术栈、架构模式、不可逾越的约束 |
| 精确实现 | DESIGN.md 逐章节 | 每实现一个模块前，精读对应章节；逐字遵守 |
| 风格对齐 | CONVENTIONS.md 通读一次 | 执行全程保持风格一致 |

核心原则：DESIGN.md 是**逐字级约束**，SPEC 和 ARCHITECTURE 是**语义级约束**。

**三、执行约束（MUST / MUST NOT / WHEN AMBIGUOUS）**
明确下游执行者的硬约束——必须做什么、不能做什么、四文件之间有矛盾时的优先级。

**四、验收维度**
定义实现完成后按哪些维度验收、判定标准是什么、不通过时输出什么格式的偏离报告。

CONTRACT.md 的结构参见 `references/contract-template.md`。

**人类做什么**：审阅 Contract 的约束和验收维度，确认无遗漏。

## 产出 Artifact

- **测试场景文档** — Given-When-Then 的人类可读版本
- **CONTRACT.md** — 交付契约

## Step 4 完成后的交付包

Step 4b 结束时，规格包完整定型：

**单模块模式**：
```
规格包/
├── SPEC.md          — 产品规约（做什么、为什么）
├── DESIGN.md        — 技术契约（精确怎么做）
├── ARCHITECTURE.md  — 架构约束（技术栈、系统边界）
├── CONVENTIONS.md   — 风格规范（命名、格式、结构）
├── CONTRACT.md      — 交付契约（使用说明、约束、验收维度）
└── tests/           — 测试场景（Given-When-Then）
```

**多模块模式**：目录结构详见 `references/step-2.5-module-split.md` 合并阶段，额外包含 SHARED_SCHEMA.md、INTERFACE_REGISTRY.md、modules/ 和 tests/integration/。

---

## ✅ 完成 Checklist

- [ ] 产出物已生成：测试场景 + CONTRACT.md
- [ ] 进度图已展示
- [ ] 门控检查已执行（展示 🚦 格式）
- [ ] 进度已保存到 `userdata/spec-builder-progress.json`
- [ ] 未生成任何实现代码
