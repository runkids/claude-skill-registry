---
name: skill-logging
description: セッションごとの動作結果と期待値の乖離を記録し、改善の証跡を残すための手続き。
---

# Skill: 動作ログ記録 (Logging)

## 概要
毎セッションの終了時、または重要なタスクの完了時に、その実行結果を客観的に記録する。

## Instructions
1. **ログファイルの特定**: `development_logs/session_logs.md` (または指定された場所) に追記する。
2. **記録項目**: 以下のフォーマットで記述すること。

---
### Session Log: [YYYY-MM-DD] [Session ID/Topic]
- **Goal (期待値)**: このセッションで何を達成しようとしたか。
- **Result (実際の結果)**: 何が起こったか（成功/失敗/部分的成功）。
- **Expectation Gap (乖離)**: 期待と何が違ったか。具体的（例：pmMode が Skill を無視した、Mode の切り替えが遅い等）に記述。
- **Action for Improvement**: 次回どう修正するか。
---

3. **project_state の更新**: 完了したタスクを `project_state.md` に反映し、次の課題を更新する。
