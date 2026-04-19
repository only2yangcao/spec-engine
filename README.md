# Spec Engine - AI 工程自动交付框架

Spec Engine 是一个 AI 驱动的软件工程自动交付框架，通过多角色协作实现从需求规格到代码交付的全流程自动化。

## 核心概念

框架通过定义专业化的 AI 角色，模拟真实的软件开发团队协作流程：

| 角色 | 职责 | 文件 |
|------|------|------|
| 项目经理 | 流程管理、任务分配、进度把控 | `prompts/AGENTS.md` |
| 系统架构师 | 需求理解、工程化任务拆解 | `agents/system-architect.md` |
| 测试工程师 | 测试用例设计、测试验证 | `agents/qa.md` |
| 研发工程师 | 编码实现、单元测试 | `agents/code_developer.md` |
| 代码审核员 | 代码质量审查、测试执行 | `agents/code_reviewer.md` |



## 文件驱动长上下文

框架采用**文件驱动**的协作模式，所有角色通过读写约定的文件进行协作，确保流程可追踪、可中断、可恢复。

### 状态文件 state.json

`state.json` 是流程的单一真相来源，**只有项目经理可以修改**。

```
{
  "version": "v001-user-auth",
  "currentStep": "Step6",
  "currentTask": "Task-003",
  "steps": {
    "Step0": { "status": "completed", "timestamp": "2026-04-19T10:00:00Z" },
    "Step1": { "status": "completed", "timestamp": "2026-04-19T10:05:00Z" },
    "Step2": { "status": "completed", "timestamp": "2026-04-19T10:30:00Z" },
    "Step3": { "status": "completed", "timestamp": "2026-04-19T10:45:00Z", "reviewDecision": "approved" },
    "Step4": { "status": "completed", "timestamp": "2026-04-19T11:30:00Z" },
    "Step5": { "status": "completed", "timestamp": "2026-04-19T11:45:00Z", "reviewDecision": "approved" },
    "Step6": { "status": "in_progress", "currentPhase": "Phase1" },
    "Step7": { "status": "pending" },
    "Step8": { "status": "pending" }
  },
  "tasks": {
    "Task-001": { "status": "completed", "reviewRounds": 1, "fixCycles": 0 },
    "Task-002": { "status": "completed", "reviewRounds": 1, "fixCycles": 1 },
    "Task-003": { "status": "in_progress", "reviewRounds": 0, "fixCycles": 0 },
    "Task-004": { "status": "pending" },
    "Task-005": { "status": "pending" }
  },
  "metadata": {
    "createdAt": "2026-04-19T10:00:00Z",
    "lastUpdated": "2026-04-19T12:00:00Z",
    "interruptedAt": "2026-04-19T12:05:00Z",
    "interruptionReason": "user_paused"
  }
}
```

### 各环节的文件契约

| 步骤 | 输入文件 | 输出文件 | 读写角色 |
|------|----------|----------|----------|
| Step1 需求初始化 | (用户需求) | `spec/SPEC.md`<br>`spec/ARCHITECTURE.md`<br>`spec/CONVENTIONS.md`<br>`spec/TEST-SCENARIOS.md` | 项目经理 |
| Step2 任务拆解 | `spec/*.md` | `tasks/task-*.md`<br>`tasks/task-report.md` | 系统架构师 |
| Step3 审查节点1 | `tasks/task-report.md` | `report.json` (审查记录) | 项目经理 + 用户 |
| Step4 测试验证 | `tasks/task-*.md`<br>`spec/*.md` | `tests/Test*.java`<br>`tests/test-report.md` | 测试工程师 |
| Step5 审查节点2 | `tests/test-report.md` | `report.json` (审查记录) | 项目经理 + 用户 |
| Step6 Phase1 编码 | `tasks/task-{N}.md` | (源代码变更) | 研发工程师 |
| Step6 Phase2 审查 | `tasks/task-{N}.md`<br>`tests/Test*.java` | `reviews/review-task-{N}.md` | 代码审核员 |
| Step6 Phase3 AI审查 | `reviews/review-task-{N}.md` | `reviews/review-report.md`<br>更新 `state.json` | 项目经理 |
| Step7 审查节点3 | `reviews/review-report.md` | `report.json` (审查记录) | 项目经理 + 用户 |
| Step8 项目汇报 | 所有文件 | `report.json` (最终总结) | 项目经理 |


## 断点恢复机制

框架支持从任意断点处恢复执行，无需从头开始。


## 工作流程

```
Step0: 版本检查
   ↓
Step1: 需求初始化
   ↓
Step2: [工程化任务拆解] ← (系统架构师) ──┐
   │                                            │ 自查循环
   └────────────────────────────────────────────┘ (最多3轮)
   ↓
Step3: [人工审查] 节点1
   ↓
Step4: [工程化测试验证] ← (测试工程师) ─────┐
   │                                            │ 自查循环
   └────────────────────────────────────────────┘ (需求/边界/异常覆盖率达标)
   ↓
Step5: [人工审查] 节点2
   ↓
Step6: 编码->代码验收 (循环执行每个任务)
   ├─ Phase1: [工程化编码] ← (研发工程师)
   │   ├─ Check A (函数级): 编码→检查→修复 (无限次编译修复/最多3次测试修复)
   │   └─ Check B (Commit级): 完成→检查→修复 (最多2轮)
   ├─ Phase2: [工程化代码审查] ← (代码审核员)
   └─ Phase3: AI审查
         ├─ 通过 → 下一任务
         └─ 不通过 → 返回 Phase1 修复 (最多2轮)
   ↓
Step7: [人工审查] 节点3
   ↓
Step8: [项目汇报]
```

#### 不确定性协议
| 情况 | 处理方式 |
|------|---------|
| 确定 | 直接实现 |
| 可推断 | 实现 + 注释 `INFERRED: [依据]` |
| 不确定 | 最简实现 + 注释 `SPEC_UNCLEAR: [方案列表]` |
| 新依赖/接口变更 | 不实现，注释 `NEEDS_HUMAN: [描述]` |


## 安装使用

将本项目直接安装到目标工程的 `.claude` 目录下（**不要**创建 spec-engine 层）：

```bash
# 在目标工程根目录下
mkdir -p .claude
cd .claude

# 将 spec-engine 的内容复制到 .claude 目录
# agents/、prompts/、skills/ 等直接放在 .claude 下
```

目录结构应该是：
```
your-project/
└── .claude/
    ├── agents/
    ├── prompts/
    ├── skills/
    └── ...
```

重要步骤：设置output-style
> 这一步可以避免非常多主agent失控的问题

步骤
```
1.  Claude code cli启动后，输入/config  
2.  选择Output style，按空格
3.  选择spec-executor-style，保存
4.  重启Claude code cli
5.  输入 "你好"
```

## 版本管理目录结构

框架会在项目根目录下创建 `.spec-versions/` 目录用于多版本管理：

```
.spec-versions/
└── v001-user-auth/
    ├── spec/
    │   ├── ARCHITECTURE.md      # 架构约束
    │   ├── CONVENTIONS.md       # 风格约束
    │   ├── SPEC.md              # 需求规约
    │   └── TEST-SCENARIOS.md    # 测试验收场景
    ├── tasks/
    │   ├── task-001.md
    │   ├── task-002.md
    │   └── task-report.md       # 任务拆解报告
    ├── tests/
    │   ├── TestTask001.java
    │   ├── TestTask002.java
    │   ├── v001UserAuth.java    # 综合测试
    │   └── test-report.md
    ├── reviews/
    │   ├── review-task-001.md
    │   ├── review-task-002.md
    │   └── review-report.md
    ├── report.json               # 过程进展汇报
    └── state.json                # 流程进展状态
```



## Claude Code 设置小tips

1. 提高上下文自动压缩阈值

`/context`可以查看当前的上下文大小，默认80%触发压缩


2. 状态栏显示 Context 大小

prompt
```
帮我修改状态栏格式，显示context大小
```
设置成功后，cli下方会显示当前context大小。

配置后重启 Claude Code 即可生效。

## 许可证

MIT License
