# skills/project-management/agile-leadership-skill.md
---
name: "Agile Project Orchestration"
description: "Directing the Swarm and managing state."
---

## The Roadmap
* **File**: `ROADMAP.md`
* **Format**: Checkboxes for tasks `[ ]`, assigned to specific agents (`@Quant`).

## Dynamic Configuration
* **Source of Truth**: `project_state/runtime_rules.json`.
* **Change Management**:
    1.  Receive Request (e.g., "Tighten Stops").
    2.  Validate with `@Psych` (Is this emotional?).
    3.  Update JSON.
    4.  Broadcast "Config Reload" signal to `@Quant`.

## Meeting Protocol
* **Standup**: When initialized, check status of all subsystems (API, DB, UI).
* **Retrospective**: After a trading session, trigger `@MLEng` to process `lessons_learned.json`.