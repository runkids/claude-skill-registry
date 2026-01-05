---
name: clarity-gate
description: Pre-ingestion verification for epistemic quality in RAG systems. Use when reviewing documents before they enter knowledge bases, checking if claims could be misinterpreted as facts, or validating that hypotheses are clearly marked. Triggers on "clarity gate", "check for hallucination risks", "can an LLM read this safely", "review for equivocation", "verify document clarity", "pre-ingestion check".
---

# Clarity Gate v1.6

**Purpose:** Pre-ingestion verification system that enforces epistemic quality before documents enter RAG knowledge bases.

**Core Question:** "If another LLM reads this document, will it mistake assumptions for facts?"

**Core Principle:** *"Detection finds what is; enforcement ensures what should be. In practice: find the missing uncertainty markers before they become confident hallucinations."*

**Prior Art:** This skill builds on proven patterns from enterprise gates (Adlib, pharma QMS) and detection tools (UnScientify, HedgeHog). Our contribution is open-source epistemic enforcement. See [docs/PRIOR_ART.md](docs/PRIOR_ART.md).

**Origin:** Part of [Stream Coding](https://github.com/frmoretto/stream-coding) methodology. Clarity Gate is the mandatory checkpoint before code generation. This standalone version enables verification without the full methodology.

---

## The Key Distinction

Existing tools like UnScientify and HedgeHog **detect** uncertainty markers already present in text ("Is uncertainty expressed?").

Clarity Gate **enforces** their presence where epistemically required ("Should uncertainty be expressed but isn't?").

| Tool Type | Question | Example |
|-----------|----------|---------|
| **Detection** | "Does this text contain hedges?" | UnScientify finds "may", "possibly" |
| **Enforcement** | "Should this claim be hedged but isn't?" | Clarity Gate flags "Revenue will be $50M" |

---

## Critical Limitation

> **Clarity Gate verifies FORM, not TRUTH.**
>
> This skill checks whether claims are properly marked as uncertain--it cannot verify if claims are actually true. 
>
> **Risk:** An LLM can hallucinate facts INTO a document, then "pass" Clarity Gate by adding source markers to false claims.
>
> **Solution:** HITL (Human-In-The-Loop) verification is **MANDATORY** before declaring PASS.

---

## When to Use

- Before ingesting documents into RAG systems
- Before sharing documents with other AI systems
- After writing specifications, state docs, or methodology descriptions
- When a document contains projections, estimates, or hypotheses
- Before publishing claims that haven't been validated
- When handing off documentation between LLM sessions

---

## The 9 Verification Points

### Epistemic Checks (Core Focus: Points 1-4)

**1. HYPOTHESIS vs FACT LABELING**
Every claim must be clearly marked as validated or hypothetical.

**Check:** Are projections, estimates, and assumptions explicitly labeled?

| Fails | Passes |
|-------|--------|
| "Our architecture outperforms competitors" | "Our architecture outperforms competitors [benchmark data in Table 3]" |
| "The model achieves 40% improvement" | "The model achieves 40% improvement [measured on dataset X]" |

**Fix:** Add markers: "PROJECTED:", "HYPOTHESIS:", "UNTESTED:", "(estimated)", "~", "?"

---

**2. UNCERTAINTY MARKER ENFORCEMENT**
Forward-looking statements require qualifiers.

**Check:** Do predictions and projections have explicit uncertainty markers?

| Fails | Passes |
|-------|--------|
| "Revenue will be $50M by Q4" | "Revenue is **projected** to be $50M by Q4" |
| "The feature will reduce churn" | "The feature is **expected** to reduce churn" |

**Fix:** Add "projected", "estimated", "expected", "designed to", "intended to"

---

**3. ASSUMPTION VISIBILITY**
Implicit assumptions that affect interpretation must be explicit.

**Check:** Are hidden conditions and constraints stated?

| Fails | Passes |
|-------|--------|
| "The system scales linearly" | "The system scales linearly [assuming <1000 concurrent users]" |
| "Response time is 50ms" | "Response time is 50ms [under standard load conditions]" |

**Fix:** Add bracketed conditions: "[assuming X]", "[under conditions Y]", "[when Z]"

---

**4. AUTHORITATIVE-LOOKING UNVALIDATED DATA**
Tables with specific percentages and checkmarks look like measured data.

**Check:** Could a reader mistake this table/chart for empirical results?

**Red flag:** 
| Approach | Accuracy | Success Rate |
|----------|----------|--------------|
| Method A | 89% | 66% |
| Method B | 95% | 100% |

**Fix:** Add "(guess)", "(est.)", "?" to numbers. Change checkmarks to question marks for unvalidated items. Add explicit warning: "PROJECTED VALUES - NOT MEASURED"

---

### Data Quality Checks (Complementary: Points 5-7)

**5. DATA CONSISTENCY**
Scan for conflicting numbers, dates, or facts within the document.

**Check:** Does the same metric appear with different values?

**Red flag:** "500 users" in one section, "750 users" in another

**Fix:** Reconcile conflicts or explicitly note the discrepancy with explanation.

---

**6. IMPLICIT CAUSATION**
Claims that imply causation without evidence.

**Check:** Does the document claim X causes Y without validation?

**Red flag:** "Shorter prompts improve response quality" (plausible but unproven)

**Fix:** Reframe as hypothesis: "Shorter prompts MAY improve response quality (hypothesis, not validated)"

---

**7. FUTURE STATE AS PRESENT**
Describing planned/hoped outcomes as if already achieved.

**Check:** Are future goals written in present tense?

**Red flag:** "The system processes 10,000 requests per second" (when it hasn't been built)

**Fix:** Use future/conditional: "The system is DESIGNED TO process..." or "TARGET: 10,000 rps"

---

### Verification Routing (Points 8-9)

**8. TEMPORAL COHERENCE**
Document dates and timestamps must be internally consistent and plausible.

**Check:** Are dates coherent with each other and with the present?

| Fails | Passes |
|-------|--------|
| "Last Updated: December 2024" (when current date is December 2025) | "Last Updated: December 2025" |
| v1.0.0 dated 2024-12-23, v1.1.0 dated 2024-12-20 (out of order) | Versions in chronological order |
| "Deployed in Q3 2025" in a doc from Q1 2025 (future as fact) | "PLANNED: Q3 2025" |
| "Current CEO is X" (when X left 2 years ago) | "As of Dec 2025, CEO is Y" |

**Sub-checks:**
1. **Document date vs current date**: Is "Last Updated" in the future or suspiciously stale (>6 months)?
2. **Internal chronology**: Are version numbers, event dates in logical sequence?
3. **Reference freshness**: Do "current", "now", "today" claims need staleness markers?

**Fix:** 
- Update dates to current
- Add "as of [date]" qualifiers to time-sensitive claims
- Flag stale "current" claims for review

**Scope boundaries:**
- ✅ IN: Catching wrong years, chronological inconsistencies, stale markers
- ❌ OUT: Judging if timelines are "reasonable" (subjective), verifying events happened on stated dates (HITL)

---

**9. EXTERNALLY VERIFIABLE CLAIMS**
Specific numbers that could be fact-checked should be flagged for verification.

**Check:** Does the document contain pricing, statistics, rates, or competitor claims without sources?

**Red flags:**

| Type | Example | Risk |
|------|---------|------|
| Pricing | "Costs ~$0.005 per call" | API pricing changes; may be outdated or wrong |
| Statistics | "Papers average 15-30 equations" | Sounds plausible but may be wildly off |
| Rates/ratios | "40% of researchers use X" | Specific % needs citation |
| Competitor claims | "No competitor offers Y" | May be outdated or incorrect |
| Industry facts | "The standard is X" | Standards evolve |

**Why this matters:**
These claims are dangerous because they:
1. Look authoritative (specific numbers)
2. Sound plausible (common-sense estimates)
3. Are verifiable (unlike opinions)
4. Are often wrong (pricing changes, statistics misremembered)

An LLM ingesting "costs ~$0.005" will confidently repeat this—even if actual cost is 10x different.

**Fix options:**
1. Add source: "~$0.005 (Gemini pricing, Dec 2025)"
2. Add uncertainty: "~$0.005 (estimated, verify current pricing)"
3. Route to verification: Flag for HITL or external search
4. Generalize: "low cost per call" instead of specific number

| Before | After |
|--------|-------|
| "Costs ~$0.005 per call" | "Costs ~$0.001 per call (Gemini 2.0 Flash, Dec 2025)" |
| "Papers average 15-30 equations" | "Papers contain varying numbers of equations (varies significantly by field)" |
| "All competitors use PDFs" | "Most competitors process PDFs (based on Dec 2025 review)" |
| "The API returns results in 50ms" | "The API returns results in ~50ms (internal benchmark, Nov 2025)" |

---

## The Verification Hierarchy

The key insight: **not all claims can be verified the same way.**

```
Claim Extracted --> Does Source of Truth Exist?
                           |
           +---------------+---------------+
           YES                             NO
           |                               |
   Tier 1: Automated              Tier 2: HITL
   Consistency & Verification     Two-Round Verification
           |                               |
   PASS / BLOCK                   Round A → Round B → APPROVE / REJECT
```

### Tier 1: Automated Consistency & Verification

**A. Internal Consistency (Ready Now)**

Checks for contradictions *within* a document--no external systems required.

| Check Type | Example |
|------------|---------|
| Figure vs. Text | Figure shows B=0.33, text claims B=0.73 |
| Abstract vs. Body | Abstract claims "40% improvement," body shows 28% |
| Table vs. Prose | Table lists 5 features, text references 7 |
| Numerical consistency | Revenue stated as $47M in one section, $49M in another |

This is the **core capability**--solvable, generic, and valuable. A document with conflicting claims becomes a "trusted source of confusion"--the model confidently reports one value, unaware they conflict.

**B. External Verification (Extension Interface)**

For claims that *can* be verified against structured sources:

| Claim Type | Source | Implementation |
|------------|--------|----------------|
| "Q3 revenue was $47M" | Financial system | User provides connector |
| "Feature deployed Oct 15" | Git commits | User provides API |
| "Customer count: 2,847" | CRM | User provides query |

**Note:** External verification requires bespoke integration for each data source. Clarity Gate provides the *interface* for verification hooks; users implement connectors for their specific systems.

---

### Tier 2: Two-Round HITL Verification -- MANDATORY

The value isn't having humans review data--every team does that. The value is **intelligent routing**: the system detects *which* specific claims need human review, and *what kind of review* each needs.

**Why two rounds?** Different claims need different types of verification:

| Claim Type | What Human Checks | Cognitive Load |
|------------|-------------------|----------------|
| LLM found source, human witnessed | "Did I interpret correctly?" | Low (quick scan) |
| Human's own data | "Is this actually true?" | High (real verification) |
| No source found | "Is this actually true?" | High (real verification) |

Mixing these in one table creates checkbox fatigue—human rubber-stamps everything instead of focusing attention where it matters.

---

**Step 0: Request Source of Truth**

Before extracting claims, ask:

> "Do you have a Source of Truth document for this project?
> (e.g., project state record, verified metrics, status tracker)
>
> If yes, please share it -- I'll use it to verify claims.
> If no, I'll present claims for two-round verification."

---

## Two-Round HITL Classification

How to assign claims to Round A or Round B:

```
Claim Extracted
      │
      ▼
Was source found in THIS session?
      │
      ├─── YES ────► Was human present/active?
      │                    │
      │              ├─ YES ──► ROUND A (Derived)
      │              │
      │              └─ NO/UNCLEAR ──► ROUND B (True HITL)
      │
      └─── NO ─────► Is this human's own data?
                           │
                     ├─ YES ──► ROUND B with note "your data"
                     │
                     └─ NO ──► ROUND B with note "no source found"
```

### Classification Rules

| Condition | Round | Rationale |
|-----------|-------|-----------|
| Source found in session, human active | **A** | Human witnessed, just confirm interpretation |
| Source found in session, human unclear | **B** | Can't assume human saw it |
| Human's own data (experiments, metrics) | **B** | Only human can confirm their data |
| No source found | **B** | High hallucination risk |
| Conflicting sources | **B** | Needs human judgment |
| Extrapolation/inference | **B** | LLM reasoning, not fact |
| Cross-session claim | **B** | Context may be lost |

**Default behavior:** When uncertain, assign to Round B.

---

## Round A: Derived Data Confirmation

Claims where LLM found a source AND human was present in the session.

**Purpose:** Confirm interpretation, not truth. Human already saw the source.

**Format:** Simple list (no table needed—lower visual weight for quick scan)

```
## Derived Data Confirmation

These claims came from sources found in this session:

- o3 prices cut 80% June 2025 (OpenAI blog)
- Opus 4.5 is $5/$25 (Anthropic pricing page)
- Google free tier cut Dec 7 (GCP changelog)

Reply "confirmed" or flag any I misread.
```

**Human action:** Quick scan, reply "confirmed" or flag extraction errors.

---

## Round B: True HITL Verification

Claims where:
- No source was found
- Source is human's own data/experiment
- LLM is extrapolating or inferring
- Conflicting sources found
- Session context unclear

**Purpose:** Verify truth. Human may NOT have seen this or it may not exist.

**Format:** Full table with True/False confirmation

```
## HITL Verification Required

These claims need your verification:

| # | Claim | Why HITL Needed | Human Confirms |
|---|-------|-----------------|----------------|
| 1 | Benchmark scores (Haiku 100%, Flash 75%→100%) | Your experiment data | [ ] True / [ ] False |
| 2 | 500 employees deployed | No source found | [ ] True / [ ] False |

Please respond with confirmation or corrections.
```

**Human action:** Actually verify each claim.

---

## Edge Cases

### 1. Long conversation - did human see the search?

**Problem:** In a 2-hour session, human may have stepped away when a search happened.

**Solution:** If uncertain, default to Round B. Add note: "Source found earlier in session - please confirm you saw this."

### 2. Human uploaded a document - is that "their data"?

**Problem:** Human uploads a PDF. LLM extracts claims. Are these "derived" or "HITL"?

**Solution:** 
- If LLM is extracting what PDF says → Round A (confirm interpretation)
- If LLM is claiming PDF content is TRUE → Round B (human must verify the source)

### 3. Mixed provenance

**Problem:** Claim combines searched data + inference.

**Example:** "At current prices ($0.15/1M), this would cost ~$450/month"
- Price: searched (Round A)
- Monthly cost: calculated (could be wrong)

**Solution:** Split into components or assign to higher round (B).

### 4. No claims need Round B

**Problem:** All claims are derived from sources in session.

**Solution:** Skip Round B section entirely. Output:

```
## HITL Verification Required

No claims require full HITL verification - all claims derived from sources found in this session.

Please confirm Derived Data above, then PASS can be declared.
```

---

## Quick Scan Checklist

Run through document looking for these patterns:

| Pattern | Action |
|---------|--------|
| Specific percentages (89%, 73%, etc.) | Add source or mark as estimate |
| Comparison tables | Add "PROJECTED" header + uncertainty markers |
| "Achieves", "delivers", "provides" | Check if validated; if not, use "designed to", "intended to" |
| Checkmarks | Verify these are actually confirmed |
| "100%" anything | Almost always needs qualification |
| Time/cost savings claims | Mark as projected unless measured |
| "The model recognizes/understands/knows" | Mark as hypothesis about LLM behavior |
| "Always", "never", "guarantees" | Check if absolute claim is warranted |
| **Case studies / customer names** | **Round B - verify with human** |
| **Production deployments** | **Round B - verify with human** |
| **Measured outcomes** | **Round B - verify with human** |
| "Last Updated: [date]" | Check against current date (Point 8) |
| Version numbers with dates | Verify chronological order (Point 8) |
| "Current", "now", "today", "as of" | Flag for staleness check (Point 8) |
| Year in document ≠ current year | Verify intentional vs error (Point 8) |
| **"$X.XX" or "~$X" (pricing)** | **⚠️ Flag for external verification (Point 9)** |
| **"averages", "typically", "on average"** | **⚠️ Flag for source/citation (Point 9)** |
| **"X% of", "X per Y" (rates/ratios)** | **⚠️ Flag for source/citation (Point 9)** |
| **Competitor capability claims** | **⚠️ Flag for external verification (Point 9)** |
| **"All X", "No X", "Every X"** | **⚠️ Flag absolutes for verification (Point 9)** |

---

## Output Format

After running Clarity Gate, report:

```
## Clarity Gate Results

**Issues Found:** [number]

### Critical (will cause hallucination)
- [issue + location + fix]

### Warning (could cause equivocation)  
- [issue + location + fix]

### Temporal (date/time issues)
- [issue + location + fix]

### Passed (Points 1-9)
- [what was already clear]

---

## Externally Verifiable Claims

| # | Claim | Type | Suggested Verification |
|---|-------|------|------------------------|
| 1 | [specific claim] | Pricing / Statistic / Competitor | [where to verify] |

**Verification status:** ⬜ Pending / ✅ Verified / ❌ Incorrect

---

## Derived Data Confirmation

These claims came from sources found in this session:

- [claim] ([source])
- [claim] ([source])

Reply "confirmed" or flag any I misread.

---

## HITL Verification Required

These claims need your verification:

| # | Claim | Why HITL Needed | Human Confirms |
|---|-------|-----------------|----------------|
| 1 | [claim] | [reason] | [ ] True / [ ] False |

---

**Would you like me to produce an annotated version of this document with the fixes applied?**

---

**Verdict:** PENDING CONFIRMATION
```

**Confirmation flow:**

1. Human confirms Round A: "confirmed" (or flags issues)
2. Human confirms Round B: "1 true, 2 false" (or provides corrections)
3. Only after both rounds confirmed:

```
**Verdict:** PASS (HITL confirmed [date])
```

**If user requests annotation:**

Produce the complete document with all fixes applied inline:
- Uncertainty markers added
- Assumptions made visible
- Projections labeled
- Unverified claims marked

This creates a **Clarity-Gated Document (CGD)** ready for RAG ingestion or handoff to other LLM systems.

---

## Severity Levels

| Level | Definition | Action |
|-------|------------|--------|
| **CRITICAL** | LLM will likely treat hypothesis as fact | Must fix before use |
| **WARNING** | LLM might misinterpret | Should fix |
| **TEMPORAL** | Date/time inconsistency detected | Verify and update |
| **VERIFIABLE** | Specific claim that could be fact-checked | Route to HITL or external search |
| **ROUND A** | Derived from witnessed source | Quick confirmation |
| **ROUND B** | Requires true verification | Cannot pass without confirmation |
| **PASS** | Clearly marked, no ambiguity, verified | No action needed |

---

## What This Skill Does NOT Do

- Does not classify document types (use Stream Coding for that)
- Does not restructure documents 
- Does not add deep links or references
- Does not evaluate writing quality
- **Does not check factual accuracy autonomously** (requires HITL for factual claims)

**This skill verifies:** 
1. (Points 1-4) Epistemic quality: Are claims properly qualified?
2. (Points 5-7) Data quality: Is the document internally consistent?
3. (Points 8-9) Verification routing: Are temporal and verifiable claims flagged?
4. (Two-Round HITL) Truth verification: Has a human confirmed factual claims?

---

## Example Fixes

**Before:** "The new architecture reduces latency by 40%"
**After:** "The new architecture is PROJECTED to reduce latency by ~40% (UNTESTED)"

**Before:** "Method B is the superior approach"
**After:** "HYPOTHESIS: Method B may be more efficient (not yet validated through comparative testing)"

**Before:** 
| Method | Success Rate |
|--------|--------------|
| Ours | 100% |

**After:**
| Method | Success Rate (ESTIMATED) |
|--------|--------------------------|
| Ours | ~100%? (assumes ideal conditions) |

**Before:** "Users prefer the new interface"
**After:** "HYPOTHESIS: Users may prefer the new interface (based on 3 informal interviews, no formal study)"

**Before:** "Deployed to 500+ employees at Acme Corp with zero data leaks"
**After (if HITL reveals this was only a demo):** "Demo presented to Acme Corp. NO production deployment. Zero data leaks is a design goal, not a measured outcome."

---

## HITL Failure Case Study

**What happened:**

1. LLM wrote document about a project
2. Included "Enterprise deployment: 500+ employees, zero PII leaks, 6 months production"
3. Ran Clarity Gate points 1-7
4. Added "(client-reported)" marker to claims
5. Declared PASS

**The problem:**
- The client only saw a demo--there was NO production deployment
- The LLM misinterpreted past conversations
- Adding "(client-reported)" made a FALSE claim look MORE credible
- Clarity Gate verified the FORM but not the TRUTH

**What Two-Round HITL would have caught:**

```
## HITL Verification Required

| # | Claim | Why HITL Needed | Human Confirms |
|---|-------|-----------------|----------------|
| 1 | Deployed to 500+ employees | No source found | [ ] True / [ ] False |
| 2 | Zero PII leaks in 6 months production | No source found | [ ] True / [ ] False |
| 3 | 80% adoption rate achieved | Your data | [ ] True / [ ] False |

Human response: "All FALSE - Client only saw a demo. None of this happened."
```

**Lesson:** Without HITL, Clarity Gate can make false claims WORSE by adding authoritative-looking source markers. Two-round HITL ensures human attention is focused on claims that actually need verification.

---

## Source of Truth Template (Adaptable)

If the human doesn't have a Source of Truth, suggest creating one:

```
# [Subject] - Source of Truth
Last Updated: [date]
Owner: [name/team]
Status: [current state]

## Verified Data
| Item | Value | Context | Verified Date |
|------|-------|---------|---------------|
| [what] | [measured value] | [conditions, source, method] | [when] |

## Status Tracker
| Item | Status | Notes |
|------|--------|-------|
| [what] | [None / Planned / In Progress / Completed / N/A] | [details] |

## Stakeholders / Relationships
| Entity | Relationship | Status |
|--------|--------------|--------|
| [who] | [type] | [current state] |

## Sources
| Claim | Source Type | Reference |
|-------|-------------|-----------|
| [claim] | Internal | [internal doc] |
| [claim] | External | [citation] |
| [claim] | None | Unverified |

## Open Items
| ID | Priority | Description | Status |
|----|----------|-------------|--------|
```

---

## Related

- **[Source of Truth Creator](https://github.com/frmoretto/source-of-truth-creator)** -- Create documents (use before verification)
- **[Stream Coding](https://github.com/frmoretto/stream-coding)** -- Full documentation-first methodology
- **Author:** Francesco Marinoni Moretto

---

## Changelog

### v1.6 (2025-12-31)
- **ADDED:** Two-Round HITL verification system
  - Round A: Derived Data Confirmation (claims from sources found in session)
  - Round B: True HITL Verification (claims needing actual verification)
- **ADDED:** Classification logic for round assignment
- **ADDED:** Edge cases documentation (long conversations, uploaded docs, mixed provenance)
- **UPDATED:** Output format to show both rounds
- **UPDATED:** Severity levels to include ROUND A and ROUND B
- **CHANGED:** Round A uses simple list format (lighter weight for quick scan)
- **CHANGED:** Round B uses full table format (structure aids real verification)
- **RATIONALE:** Reduces cognitive load by matching verification type to claim provenance. Human knows *what kind of thinking* is needed at each step. Focuses real attention on claims that actually need it.

### v1.5 (2025-12-28)
- **ADDED:** Point 8 - Temporal Coherence check
  - Document date vs current date validation
  - Internal chronology verification
  - Staleness detection for "current" claims
  - Scope boundaries (IN: wrong years, chronological issues; OUT: subjective timelines)
- **ADDED:** Point 9 - Externally Verifiable Claims check
  - Pricing/cost claim flagging
  - Statistical generalization detection  
  - Competitor claim routing
  - Fix options: add source, add uncertainty, route to verification, generalize
- **EXPANDED:** HITL categories to include pricing, statistics, competitor claims, time-sensitive facts
- **ADDED:** New severity levels "TEMPORAL" and "VERIFIABLE"
- **ADDED:** Quick Scan patterns for temporal and verifiable claims
- **ADDED:** Output section for Externally Verifiable Claims with verification status tracking
- **RESTRUCTURED:** Points now grouped as Epistemic (1-4), Data Quality (5-7), Verification Routing (8-9)
- **MOTIVATION:** Production use revealed "confident plausible falsehoods" (correct form, wrong facts) passing review. External validation caught pricing errors (10x off) and statistic errors (7x off) that had proper uncertainty markers but were factually incorrect.

### v1.4 (2025-12-23)
- Added: Annotation offer after verification ("Would you like me to produce an annotated version?")
- Added: CGD (Clarity-Gated Document) output mode
- Bridges gap between checker and annotator functionality

### v1.3 (2025-12-21)
- Restructured: Points grouped into "Epistemic Checks (1-4)" and "Data Quality Checks (5-7)"
- Added: Detection vs enforcement distinction in intro
- Added: Tier 1A (Internal Consistency) vs Tier 1B (External Verification) framework
- Updated: HITL reframed as "Intelligent Routing" with 96% efficiency example
- Added: "Trusted source of confusion" explanation for internal consistency value
- Added: Prior Art reference

### v1.2 (2025-12-21)
- Added: Step 0 in HITL - Request Source of Truth before verification
- Added: Source of Truth Template (adaptable to any domain)
- Added: Source Types table (Internal, External, None)

### v1.1 (2025-12-21)
- Added: HITL Fact Verification (mandatory)
- Added: Critical Limitation section explaining FORM vs TRUTH
- Added: HITL Failure Case Study
- Added: "Source in Doc" column to HITL table
- Updated: Output format to require HITL confirmation before PASS
- Updated: Severity levels to include "HITL REQUIRED"

### v1.0 (2025-11)
- Initial release with 6-point verification

---

**Version:** 1.6
**Scope:** Pre-ingestion verification for RAG systems and LLM document handoff
**Time:** 5-15 minutes (verification) + HITL response time (varies)
**Output:** List of issues + fixes + externally verifiable claims table + two-round HITL confirmation + optional annotated document (CGD), then PASS verdict
