# CONTRACT.md — 交付契约

## 项目
- 名称: [项目名]
- 版本: [版本号]
- 生成日期: [日期]

---

## 一、交付物

| 文件 | 角色 |
|---|---|
| SPEC.md | 产品规约——做什么、为什么、用户故事 |
| DESIGN.md | 技术契约——数据结构、API、枚举、业务规则、外部依赖 |
| ARCHITECTURE.md | 架构约束——技术栈、系统边界、部署模式 |
| CONVENTIONS.md | 风格规范——命名、目录结构、代码格式 |
| tests/ | 测试场景——Given-When-Then 格式的验收用例 |

**多模块模式额外交付物**（如适用）：

| 文件 | 角色 |
|---|---|
| SHARED_SCHEMA.md | 跨模块共享数据模型——权威模块、字段定义、消费关系 |
| INTERFACE_REGISTRY.md | 模块间接口注册表——v2 带类型契约 + 一致性状态 |
| modules/[name]/SPEC.md | 模块级产品规约 |
| modules/[name]/DESIGN.md | 模块级技术契约 |
| tests/integration/ | 跨模块集成测试场景 |

---

## 二、阅读协议

**阅读顺序**：SPEC → ARCHITECTURE → DESIGN → CONVENTIONS

| 阶段 | 读什么 | 目的 |
|---|---|---|
| 理解意图 | SPEC.md 全文 | 建立"为什么做、做成什么样"的完整认知 |
| 理解边界 | ARCHITECTURE.md 全文 | 明确技术栈、架构模式、不可逾越的技术约束 |
| 精确实现 | DESIGN.md 逐章节 | 每实现一个模块前，精读对应章节；字段名/类型/枚举值/API签名/业务规则逐字遵守 |
| 风格对齐 | CONVENTIONS.md 通读一次 | 执行全程保持风格一致 |

**核心原则**：

- **DESIGN.md 是逐字级约束**——其中定义的任何标识符、类型、枚举值，在实现中必须完全一致，不可重命名、不可改类型、不可增减枚举值
- **SPEC.md 和 ARCHITECTURE.md 是语义级约束**——理解意图后可以灵活实现，但不可超出范围
- **CONVENTIONS.md 是风格级约束**——尽量遵守，允许因技术原因做出合理偏离（需说明理由）

---

## 三、执行约束

### MUST
1. DESIGN.md 中定义的标识符（字段名、枚举值、端点路径、错误码）必须在实现中逐字使用
2. DESIGN.md 中定义的每条业务规则必须全部实现，不可遗漏
3. 遇到四文件未覆盖的实现细节，暂停并提出，不可自行补全
4. 每完成一个模块，对照 DESIGN.md 对应章节做一次自检

### MUST NOT
1. 不可引入四文件未提及的外部依赖
2. 不可对 SPEC.md 定义的功能范围做加法或减法
3. 不可修改 DESIGN.md 中已定义的数据结构
4. 不可在未获确认的情况下变更 ARCHITECTURE.md 中的技术栈选型

### WHEN AMBIGUOUS
当四文件之间存在矛盾或模糊地带时，优先级为：

**DESIGN.md > SPEC.md > ARCHITECTURE.md > CONVENTIONS.md**

遇到矛盾时应暂停并报告，而非自行选择。

---

## 四、验收维度

实现完成后，按以下四个维度验收：

| 维度 | 验收方法 | 判定标准 |
|---|---|---|
| **功能完整性** | 逐条核对 SPEC.md 中的 User Story | 每条 US 都有对应实现，无遗漏无多余 |
| **实现精度** | 逐项比对 DESIGN.md 的定义与实际实现 | 字段/API/枚举/规则 100% 一致 |
| **风格合规** | 抽检是否符合 CONVENTIONS.md | 命名、结构、格式无系统性偏离 |
| **测试通过** | 执行 tests/ 中的 Given-When-Then 场景 | 全部场景通过 |
| **模块间集成**（多模块） | 校验接口调用匹配注册表、共享实体匹配 SHARED_SCHEMA | 全部接口 ✅ 已校验，无字段漂移 |

### 偏离报告格式

验收不通过时，输出偏离报告：

```
## 偏离报告

### 偏离项 1
- 维度: [功能完整性 / 实现精度 / 风格合规 / 测试通过]
- 具体项: [哪条 User Story / 哪个字段 / 哪条规则 / 哪个测试]
- 期望值: [四文件中的定义]
- 实际值: [实现中的实际情况]
- 严重度: [必须修正 / 建议修正 / 可接受]
- 修正方向: [建议的修正方式]

### 偏离项 2
...
```

---

## 五、下游实现路径参考

本规格包可由以下方式消费（非穷举）：

### 路径 A：AI Coding
推荐将四文件映射为 OpenSpec change，通过 propose → apply → archive 流程执行。
- ARCHITECTURE.md + CONVENTIONS.md → openspec/project.md + AGENTS.md
- SPEC.md → openspec/specs/{capability}/spec.md
- DESIGN.md → openspec/changes/{feature}/design.md

### 路径 B：Skill 生成
将 SPEC.md 作为功能定义，DESIGN.md 作为实现规范，生成 Skill 文件。

### 路径 C：专业文档生成
将 SPEC.md 作为内容大纲，DESIGN.md 中的业务规则作为精确内容源。

### 路径 D：其他
根据下游系统的输入规范，从四文件中提取对应信息。
