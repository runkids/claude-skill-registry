---
name: skill-meta-evaluation
description: プロジェクト運営プロセスが、定義された契約（Contract）や設計思想（Reference）に準拠していたかをメタ的に評価する手続き。
---

# Skill: メタ評価 (Meta Evaluation)

## 概要
成果物の品質（QA担当）ではなく、pmMode による「進行・判断・指揮」のプロセス自体が、システムの憲法（docs/system-definition.md）に適合していたかを監査・採点する。

## Instructions

1. **セッション履歴の分析**:
   - `development_logs/` や直前の会話履歴を参照し、pmMode の立ち振る舞いを確認する。

2. **チェックリスト評価**:
   以下の観点で評価を行う。
   - **Mode 選定**: タスクに対して適切な Mode を選んだか？（例: 実装を pm 自身でやろうとしなかったか？）
   - **契約遵守**: 各 Mode の `Forbidden Actions` を踏んでいないか？
   - **自律性**: ユーザーに聞くべきでない些細な判断を自律的に行えたか？ 逆に、勝手な仕様変更をしなかったか？
   - **記録**: `project_state.md` は適切に更新されたか？

3. **レポート出力**:
   - **Score**: A (Ideal) / B (Acceptable) / C (Violation)
   - **Findings**: 具体的な遵守点と違反点。
   - **Recommendation**: 次回に向けて pmMode が修正すべき行動指針。

## Input
- 対象セッションのログ、または実行履歴。

## Output
- 構造化された Markdown 形式の監査レポート。
