# Session Workflow — Detailed Reference

Step-by-step session flow for `/study-session`. The SKILL.md has the overview; this reference has the details.

## Session Timeline

```
[0 min]     Greeting + load data (background)
[1-2 min]   Session brief
[2-5 min]   Pre-session daily note written
[5 min+]    Main session begins
             ├── Interstitial SR cards woven throughout
             ├── New material (knowledge: teach + cards, technical: exercise files)
             └── Progress checks at midpoint and checkpoints
[last 10 min] Session wrap-up
             ├── After-report in daily note
             ├── Update progress-report.md
             ├── Update learning-schedule.md (if adjustments)
             ├── Update learner-context.md (if notable)
             ├── Update _index.json last_session
             └── Git commit
```

## Data Loading Order

At session start, read files in this priority:

1. **`learner-context.md`** — WHO they are for this project (read FIRST, always)
2. **`user-profile.md`** (from `~/.claude/skills/study-plan/references/`) — WHO they are globally
3. **`learning-schedule.md`** — WHAT's planned for today
4. **`progress-report.md`** — WHERE they stand overall
5. **Yesterday's daily note** — WHAT happened last time
6. **`data/sessions.json`** — streak, timing patterns
7. **`data/cards.json`** — due cards count

## Session Brief Template

Short version (< 45 min session):
> "Day 8 of 14. 12 cards due. Today: binary search review."

Full version (> 45 min session):
> "Day 8 of 14. You're on track — completed 7 of 14 planned sessions.
>
> **Today's schedule** (09:00-11:00): Dynamic Programming — intro to memoization + 2 exercises.
> **Cards due**: 18 (3 overdue from yesterday)
> **Yesterday**: Completed arrays exercises (8/10 correct, 85 min). Noted confusion on sliding window edge cases.
> **Adjustment**: Moved 5 overdue DP cards to today's review queue."

## Interstitial SR — Insertion Strategy

The goal is 3-5 review items per hour, woven naturally:

| Insertion Point | When to Use | Example |
|----------------|-------------|---------|
| Concept warm-up | Before teaching new topic | "Before we start DP, what do you remember about recursion?" |
| Post-explanation | After teaching, before exercise | "Quick check — what's the difference between memoization and tabulation?" |
| Exercise transition | Between exercises | "While you shift gears — [review card from different topic]" |
| Struggle pivot | After user hits a wall | Switch to confidence-builder from strong area |
| Random | Keep them on their toes | "Pop quiz — [card from any topic]" |

## AskUserQuestion Patterns for SR

### Open Recall (default)

```
Question: "[card front text]"
Options:
1. "I know this"    → Must use notes (n key) to describe answer
2. "Partially"      → Use notes to describe what they know
3. "No idea"        → Optional notes, or just select
```

After they respond, reveal the answer and state your quality assessment:
- "Correct — you nailed the key insight. [quality 5]"
- "Right direction but you missed [X]. [quality 3]"
- "That's wrong. The answer is [X]. Here's why: [explanation]. [quality 1]"

### Self-Rating Probe (every 5-8 items)

```
Question: "Quick self-check: how are you feeling about [topic]?"
Options:
1. "Solid — could explain to someone"
2. "Getting there — know pieces, connections shaky"
3. "Struggling — keep forgetting or mixing up"
4. "Lost — need this re-taught"
```

Use their response to calibrate: if they say "solid" but SR data shows < 70% accuracy, note the calibration gap in `learner-context.md`.

## Writing to Daily Notes

### Timing: After EVERY task

Not at the end. Not in batches. After every SR batch (3-5 cards) and every exercise. This protects against context compaction.

### SR Batch Note Format
```markdown
### SR Review (HH:MM)
- Cards reviewed: 5
- Correct: 3/5 (60%)
- Topics: arrays (2), hashing (2), binary-search (1)
- Notable: Confused merge sort stability with quicksort again — 3rd time
- Cards updated: c012 (quality 2), c015 (quality 4), c018 (quality 5), c023 (quality 1), c031 (quality 4)
```

### Exercise Note Format
```markdown
### Exercise: Two Sum (HH:MM)
- Topic: arrays / two-pointer
- Difficulty: easy
- Time: 8 min (expected: 20 min)
- Result: Correct, clean solution
- Notes: Good edge case handling. Would pass interview timing.
- Comparison: First attempt at this pattern — strong start
```

## Structured Review Process

When triggers are met (see SKILL.md), replace normal session flow:

1. **Pull data**: Read `progress-report.md` + `data/sessions.json` + `data/cards.json`
2. **State facts plainly**:
   - "In the last 10 days: 4 sessions of 8 planned. Avg duration 52 min vs 120 committed. SR accuracy dropped 78% → 61%."
   - OR: "Completed 12 days of material in 8 days. SR 94%. Exercises averaging 8 min vs 20 min expected."
3. **Diagnose**: Ask targeted questions based on direction
4. **Reassess**: What's achievable? What changes?
5. **Propose**: Specific revised terms — user must agree
6. **Update**: `learning-schedule.md`, `progress-report.md`, plan frontmatter
7. **Checkpoint**: "Let's check in again in 3 days."

## Git Commit Pattern

After every session:
```bash
cd <project-dir> && git add daily-notes/ data/ progress-report.md learning-schedule.md learner-context.md exercises/ && git commit -m "Session DD-MM-YYYY: [1-line summary]"
```

Include `exercises/` only if new files were created. Don't add `plan.md` (immutable) or `materials/` (user-managed).
