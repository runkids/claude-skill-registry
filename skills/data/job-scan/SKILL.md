---
name: job-scan
description: Parse a job posting into structured requirements. Extracts must-haves, nice-to-haves, and company signals for fit analysis.
argument-hint: [job-url-or-file]
---

# Job Scan Workflow

**Load and execute:** `workflows/job-scan/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Obtains job posting content (URL, file, or pasted text)
2. Extracts company information and role details
3. Detects duplicate postings and offers re-validation for previously scanned roles
4. Categorizes requirements into MUST-HAVE and NICE-TO-HAVE
5. Calculates fit score against your corpus and constraints
6. Saves parsed posting to `research/openings/`
7. **Updates company profile** with a link to this opening (if profile exists in `research/companies/{industry}/`)

**Company Profile Integration:** When you scan a job from a company you've profiled via `company-discovery`, the analysis is automatically linked in that company's "Tracked Openings" section. This builds a per-company view of all opportunities you've investigated.

Follow all steps exactly as written. Embody Scout's analytical approach throughout.

$ARGUMENTS
