---
name: strongs-doctor
description: >
  Expert assistant for diagnosing and fixing Strong's concordance issues in the Raamattu Nyt project.
  Use when (1) debugging infinite loops or performance issues with Strong's lookups,
  (2) validating lexicon data against authoritative sources,
  (3) checking KJV verses point to correct Strong's numbers,
  (4) fixing corrupted kjv_strongs_words data,
  (5) auditing strongs_lexicon entries for format/content issues,
  or (6) troubleshooting Strong's search functionality.
  Triggers: strongs issue, lexicon error, infinite loop strongs, strongs validation,
  kjv strongs, fix strongs, lexicon fix.
---

# Strongs Doctor

Diagnose and fix all Strong's concordance and lexicon issues in the Raamattu Nyt Bible application.

## CRITICAL: bible_schema Usage

**All Strong's tables and RPC functions reside in `bible_schema`, NOT `public`.**

### Supabase Client Queries

```typescript
// WRONG - looks in public schema, will fail with "function not found"
const { data } = await supabase.rpc("search_verses_by_strongs", { ... });

// CORRECT - explicitly specify bible_schema
const { data } = await (supabase as any)
  .schema("bible_schema")
  .rpc("search_verses_by_strongs", { ... });

// WRONG - table query without schema
const { data } = await supabase.from("strongs_lexicon").select("*");

// CORRECT - with schema prefix
const { data } = await (supabase as any)
  .schema("bible_schema")
  .from("strongs_lexicon")
  .select("*");
```

### PostgREST Nested Selects Issue

Complex nested selects with `!inner` joins often fail silently in `bible_schema` due to PostgREST relationship inference issues. **Solution: Use RPC functions instead.**

Example: `search_verses_by_strongs(p_strongs_number, p_limit)` handles the complex join logic server-side.

### SQL Queries

Always prefix table names with `bible_schema.`:

```sql
-- WRONG
SELECT * FROM strongs_lexicon WHERE strongs_number = 'G25';

-- CORRECT
SELECT * FROM bible_schema.strongs_lexicon WHERE strongs_number = 'G25';
```

## Quick Diagnosis Checklist

When a Strong's issue is reported, check these in order:

1. **Infinite Loop?** - Check LexiconCard useEffect dependencies and async state updates
2. **Wrong Data?** - Verify strongs_number format (H/G prefix, leading zeros)
3. **Missing Data?** - Check if strongs_lexicon entry exists
4. **Corrupted KJV?** - Check for David's Psalm corruption pattern
5. **Performance?** - Check for missing indexes or N+1 queries

## Database Schema

### strongs_lexicon (14,197 entries)

Primary lexicon data for Hebrew (H) and Greek (G) Strong's numbers.

```sql
-- Key columns
strongs_number TEXT PRIMARY KEY  -- 'H1', 'G26', etc.
language TEXT                     -- 'H' or 'G'
lemma TEXT                        -- Original word meaning
transliterations TEXT[]           -- Phonetic representations
pronunciations TEXT[]             -- Pronunciation guides
part_of_speech TEXT
definition_short TEXT
definition_lit TEXT
definition_long TEXT
derivation TEXT                   -- Cross-refs like "from [[G123]]" or "(h0085)"
notes TEXT
see_also TEXT[]                   -- Related Strong's numbers
compare TEXT[]                    -- Comparison Strong's numbers
```

### kjv_strongs_words (939,793 entries)

Word-by-word Strong's mappings for KJV Bible.

```sql
verse_id UUID REFERENCES bible_schema.verses(id)
word_order INTEGER
word_text TEXT
strongs_number TEXT               -- Can be NULL for punctuation
PRIMARY KEY (verse_id, word_order)
```

## Common Issues & Fixes

### Issue 1: Infinite Loop in LexiconCard

**Symptoms:** Browser freezes, excessive API calls, memory usage spikes

**Root Cause:** Async state updates in useEffect triggering re-renders

**Location:** `apps/raamattu-nyt/src/components/LexiconCard.tsx:219-232`

**Problem Pattern:**
```typescript
// PROBLEMATIC: forEach with async can cause cascading state updates
Object.entries(textsToProcess).forEach(async ([key, text]) => {
  const processed = await parseAndRenderStrongsText(text);
  setProcessedTexts((prev) => ({ ...prev, [key]: processed }));
});
```

**Fix:** Batch state updates or use Promise.all:
```typescript
const processAll = async () => {
  const results: Record<string, string> = {};
  await Promise.all(
    Object.entries(textsToProcess).map(async ([key, text]) => {
      results[key] = await parseAndRenderStrongsText(text);
    })
  );
  setProcessedTexts(results);
};
processAll();
```

### Issue 2: Strong's Number Format Mismatches

**Symptoms:** "No lexicon data found", missing definitions

**Root Cause:** Inconsistent formats - `H0085` vs `H85`, `g123` vs `G123`

**Normalization Required:**
```typescript
// Normalize: remove leading zeros, uppercase prefix
const normalizedNumber = num.replace(/^([HG])0+/, "$1").toUpperCase();
// H0085 → H85
// g123 → G123
```

**Validation Regex:**
```typescript
const isValidStrongsNumber = (num: string): boolean => {
  return /^[GH]\d+$/i.test(num.trim());
};
```

### Issue 3: Corrupted kjv_strongs_words Data

**Symptoms:** Wrong Strong's numbers, "David_s" text, duplicate entries

**Known Corruption:** ~1,500 entries with punctuation mapped to H1732/H8416

**Detection Query:**
```sql
-- Find corrupted entries (punctuation with Strong's numbers)
SELECT word_text, strongs_number, COUNT(*)
FROM bible_schema.kjv_strongs_words
WHERE word_text IN ('.', ',', ';', ':', '?', '')
  AND strongs_number IS NOT NULL
GROUP BY word_text, strongs_number
ORDER BY COUNT(*) DESC;
```

**Fix Migration Pattern:**
```sql
-- Delete corrupted entries where punctuation has Strong's numbers
DELETE FROM bible_schema.kjv_strongs_words
WHERE word_text IN ('.', ',', ';', ':', '?', '')
  AND strongs_number IS NOT NULL;
```

### Issue 4: Cross-Reference Parsing Errors

**Symptoms:** Links not working, wrong Strong's displayed

**Formats in derivation/notes fields:**
- `[[H1234]]` - Bracket format
- `(h0085)` - Parentheses format (lowercase, with leading zeros)
- `from g0025` - Plain text format

**Parsing Logic:**
```typescript
// Bracket format: [[H1234]]
const bracketMatches = text.match(/\[\[([GH]\d+)\]\]/g) || [];

// Parentheses format: (h0085)
const parenMatches = text.match(/\(([gh]\d+)\)/gi) || [];
```

### Issue 5: Performance Issues

**Symptoms:** Slow searches, timeouts, high database load

**Root Causes:**
1. Sequential pattern searches (7 patterns tried one by one)
2. No caching of fetchStrongsName results
3. N+1 queries for reference names

**Check Indexes:**
```sql
-- Ensure indexes exist
SELECT indexname FROM pg_indexes
WHERE tablename = 'kjv_strongs_words' AND schemaname = 'bible_schema';

-- Should have index on strongs_number
CREATE INDEX IF NOT EXISTS idx_kjv_strongs_words_strongs_number
ON bible_schema.kjv_strongs_words(strongs_number);
```

## Validation Against External Sources

### OpenScriptures Reference

The authoritative open-source Strong's data: https://github.com/openscriptures/strongs

**Validation Points:**
1. **Number Range:** H1-H8674 (Hebrew), G1-G5624 (Greek)
2. **Required Fields:** strongs_number, lemma, definition_short
3. **Cross-Reference Format:** Must reference valid Strong's numbers

### Validation Query

```sql
-- Find entries outside valid range
SELECT strongs_number FROM bible_schema.strongs_lexicon
WHERE (
  (strongs_number LIKE 'H%' AND CAST(SUBSTRING(strongs_number FROM 2) AS INTEGER) > 8674)
  OR
  (strongs_number LIKE 'G%' AND CAST(SUBSTRING(strongs_number FROM 2) AS INTEGER) > 5624)
);

-- Find entries with invalid cross-references
SELECT strongs_number, see_also
FROM bible_schema.strongs_lexicon
WHERE see_also IS NOT NULL
  AND array_length(see_also, 1) > 0
  AND NOT EXISTS (
    SELECT 1 FROM bible_schema.strongs_lexicon sl2
    WHERE sl2.strongs_number = ANY(see_also)
  );
```

## KJV Verse Verification

Verify KJV Strong's mappings are correct:

```sql
-- Sample verification: Check word matches expected Strong's meaning
SELECT
  ksw.verse_id,
  ksw.word_text,
  ksw.strongs_number,
  sl.lemma,
  sl.definition_short
FROM bible_schema.kjv_strongs_words ksw
JOIN bible_schema.strongs_lexicon sl ON sl.strongs_number = ksw.strongs_number
WHERE ksw.strongs_number = 'G26'  -- agape (love)
LIMIT 10;
```

## Key Files

| File | Purpose |
|------|---------|
| `apps/raamattu-nyt/src/lib/strongsSearchService.ts` | Strong's search logic |
| `apps/raamattu-nyt/src/components/LexiconCard.tsx` | Lexicon display component |
| `apps/raamattu-nyt/src/components/search/StrongsSearchSection.tsx` | Search UI |
| `apps/raamattu-nyt/src/components/summary/StrongsSelectorModal.tsx` | Selection modal |

## Diagnostic Workflow

### Step 1: Identify the Issue Type

```
User reports "Strong's not working"
│
├─ Infinite loop/freeze → Check LexiconCard useEffect
├─ Wrong/missing data → Check number format, check lexicon entry exists
├─ Performance issue → Check indexes, check for N+1 queries
└─ Display issue → Check cross-reference parsing
```

### Step 2: Gather Data

```sql
-- Check if Strong's number exists in lexicon
SELECT * FROM bible_schema.strongs_lexicon WHERE strongs_number = 'G26';

-- Check KJV word mappings
SELECT * FROM bible_schema.kjv_strongs_words WHERE strongs_number = 'G26' LIMIT 10;

-- Check for null Strong's numbers (should only be punctuation)
SELECT COUNT(*) FROM bible_schema.kjv_strongs_words WHERE strongs_number IS NULL;
```

### Step 3: Apply Fix

Based on issue type, apply appropriate fix from the Common Issues section above.

### Step 4: Verify Fix

```sql
-- After fix, verify data integrity
SELECT
  COUNT(*) as total,
  COUNT(DISTINCT strongs_number) as unique_strongs,
  COUNT(*) FILTER (WHERE strongs_number IS NULL) as null_count
FROM bible_schema.kjv_strongs_words;
```

## Article/Particle Detection

Common grammatical words that should be displayed with subdued styling:

**Greek Articles:**
- G3588 (the) - definite article, appears 18,109 times
- G2532 (and) - conjunction, 8,180 times
- G846 (he/she/it) - pronoun, 5,381 times
- G1161 (but/and) - conjunction, 2,448 times
- G1722 (in) - preposition, 2,114 times
- G1519 (into) - preposition

**Hebrew Particles:**
- H853 (untranslatable object marker)
- H3068 (YHWH/LORD) - 5,163 times

## External Lexicon APIs

For validation against external sources:

- **Bible SDK:** https://biblesdk.com/ - REST API with Strong's data
- **Complete Study Bible API:** RapidAPI - includes Strong's, lexicons
- **OpenScriptures:** https://github.com/openscriptures/strongs - raw data files
