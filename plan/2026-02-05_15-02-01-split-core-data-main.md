---
mode: plan
cwd: /Users/lifcc/Desktop/code/AI/tools/claude-skill-registry
task: Split functionality into core/data, keep main merged, unify layout and naming
complexity: complex
planning_method: builtin
created_at: 2026-02-05T15:02:08+08:00
---

# Plan: Split core/data with unified layout

🎯 任务概述
在不拆主仓库的前提下，把“采集与逻辑”沉到 core、把“数据”沉到 data，主仓库作为两者的合并产物，三库持续同步。统一目录结构为 `skills/{category}/{name}`，统一冲突命名为 `{name}-{owner}-{repo}`，不要求向后兼容，且不可移除任何 skill。

📋 执行计划
1. 现状审计：统计三库的脚本、目录布局、冲突命名与产物差异，明确要保留/替换的脚本清单与行为基线。
2. 统一规则模块化：在 core 中抽出“命名/冲突/归一化”公共函数（不使用 `__dup`），明确优先级策略与稳定命名规则。
3. 调整 core 脚本：让 `download_v2.py`、`sync_and_download.py`、`clone_and_import.py` 与索引构建按新规则输出到 `skills/{category}/{name}`。
4. 迁移 data：按新命名规则重命名目录，补齐主仓库独有数据，更新元数据字段（含 `dir_name`），确保无大小写冲突。
5. 更新 main：用 core 脚本 + data 数据重建主仓库布局，移除扁平 `skills/data` 产物与过期脚本；主仓库 README 反映新的三库关系与布局。
6. 同步机制：提供一键同步脚本（或 GitHub Actions）让 main 从 core+data 合并生成，保证三库持续一致。
7. 重建索引与回归：在 core/main 运行索引与 registry 构建，核对计数、冲突、路径规则；运行完整测试或关键脚本回归。
8. 提交与推送：按库分别提交（core/data/main）并推送，记录关键变更点与回滚方式。

⚠️ 风险与注意事项
- 目录重命名会造成路径大规模变动，需保证生成规则稳定且可复现。
- 主/数据仓库之间存在差集，需先补齐再迁移，避免“丢技能”。
- 不向后兼容会导致历史引用失效，应在 README/文档明确说明。
- 同步脚本是三库一致性的关键，需避免人工手工修改导致漂移。

📎 参考
- `scripts/download_v2.py`
- `scripts/clone_and_import.py`
- `scripts/sync_and_download.py`
