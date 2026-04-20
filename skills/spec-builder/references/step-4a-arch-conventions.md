# Step 4a: 架构 + 规范
> ⚠️ 本步骤产出物是「ARCHITECTURE.md + CONVENTIONS.md」，不是代码。如果你发现自己正在写实现代码，立即停止并回到本步骤。

**预计耗时**：15-30分钟 | **人类角色**：🔍 审计者

## 定位

这一步的两个产出物（ARCHITECTURE.md + CONVENTIONS.md）大部分内容可以从 SPEC + DESIGN 中**自动提取**，人类只需快速审阅确认。认知负荷远低于 Step 3c 和 Step 4b。

## ARCHITECTURE.md 生成

**AI 做什么**：
基于 SPEC.md 的技术约束和 DESIGN.md 的技术决策，生成 ARCHITECTURE.md。这不是重新设计——而是把散落在 SPEC 和 DESIGN 中的架构决策**集中到一个文件**，明确：

- **技术栈**：语言/框架/数据库/运行时的精确版本
- **系统边界**：模块划分、前后端分离策略、进程边界
- **部署模式**：部署目标（Serverless / VPS / Container）、环境配置
- **关键架构决策**：为什么选 X 而不是 Y（如果在 DESIGN.md 的设计决策附录中已有，直接引用）

**人类做什么**：快速审阅，确认与 SPEC/DESIGN 中的决策一致。

## CONVENTIONS.md 生成

**AI 做什么**：
基于技术栈和项目类型，生成 CONVENTIONS.md，覆盖：

- **命名规则**：变量/函数/文件/目录的命名约定
- **目录结构**：项目目录组织方式
- **代码格式**：缩进/引号/分号等风格约定
- **提交规范**：Git commit message 格式

**人类做什么**：快速审阅，按个人偏好调整。

## 产出 Artifact

- **ARCHITECTURE.md** — 架构约束文档
- **CONVENTIONS.md** — 风格规范文档

---

## ✅ 完成 Checklist

- [ ] 产出物已生成：ARCHITECTURE.md + CONVENTIONS.md
- [ ] 进度图已展示
- [ ] 门控检查已执行（展示 🚦 格式）
- [ ] 进度已保存到 `userdata/spec-builder-progress.json`
- [ ] 未生成任何实现代码
