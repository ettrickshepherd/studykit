# Plan Templates

Templates and structure for study plan construction.

## Plan YAML Frontmatter

Every plan file in `references/plans/<slug>.md` must have this frontmatter:

```yaml
---
project: <slug>
created: <YYYY-MM-DD>
deadline: <YYYY-MM-DD or "open-ended">
status: active
mode: <technical | knowledge | mixed>
language: <python | java | go | etc. | null>
topics: [<list of top-level topics>]
location: <absolute path to project directory>
hours_committed: <daily hours as decimal>
time_slots:
  weekday: "<HH:MM-HH:MM>"
  weekend: "<HH:MM-HH:MM>"
tags: [<searchable tags>]
---
```

## Plan Document Structure

```markdown
# <Project Name> — Study Plan

## The Commitment
[What the user agreed to: goals, timeline, daily hours, specific time slots]

## Learner Profile
[Summary from interview — current level, strengths, weaknesses, learning style, motivation]

## Content Acquisition Plan
[For each major topic, specify the content source method]

| Topic | Source | Notes |
|-------|--------|-------|
| Arrays | claude-generated | Strong coverage in training data |
| System Design | hybrid | Claude generates scenarios; user provides company-specific context |
| Evidence Law | user-provided | Requires course textbook |

Source types: claude-generated, user-provided, web-researched, inferred, hybrid

## Topic Dependency Graph
[Which topics must be learned before which. Can be a simple list or ASCII diagram.]

Example:
- Arrays → Two Pointers → Sliding Window
- Arrays → Binary Search
- Hashing (independent)
- Trees → Graphs → Dynamic Programming (partial)

## Day-by-Day Schedule

### Week 1: Foundations
| Day | Date | Time | Primary Topic | Review Topics | Mode | Difficulty |
|-----|------|------|---------------|---------------|------|------------|
| Mon | DD-MM | HH:MM-HH:MM | Arrays basics | — | Technical | Easy |
| Tue | DD-MM | HH:MM-HH:MM | Hashing | Arrays | Technical | Easy-Med |
| Wed | DD-MM | HH:MM-HH:MM | Two Pointers | Arrays, Hashing | Technical | Medium |
| Thu | DD-MM | HH:MM-HH:MM | — | — | REST | — |
| ... | | | | | | |

### Week 2: Building
[Continue pattern...]

### Final Week: Integration + Mock
[Diagnostic tests, timed practice, full mock exams]

## Spaced Repetition Plan
- Cards introduced: after each new topic
- Review cadence: interstitial during sessions (no dedicated SR blocks)
- Initial deck size: ~10-15 cards per topic
- Card types: recall, application, comparison, synthesis, edge cases

## Diagnostic Checkpoints
| Checkpoint | Day | Criteria for "On Track" |
|------------|-----|------------------------|
| End of Week 1 | Day 7 | 70%+ on arrays/hashing exercises, 15+ cards with ease > 2.3 |
| Mid-plan | Day N/2 | All foundation topics at "medium" difficulty, 60%+ SR accuracy |
| Pre-deadline | Day N-2 | Timed practice at target pace, 80%+ SR accuracy on core cards |

## Triage Strategy
If behind schedule, cut in this order (first = least critical):
1. [Lowest priority topic]
2. [Next lowest]
3. ...
N. [NEVER cut — this is non-negotiable]

## Motivation Architecture
Based on learner's stated motivators:
- Progress visibility: [how to show progress — streak, card count, exercise completion %]
- Variety: [how to prevent burnout — alternate topics, mix modes, change difficulty]
- Milestones: [specific achievements to mark — "completed all Easy arrays", "50 mature cards"]

## Claude's Capability Assessment
[Honest assessment from Phase 2]
- Reliable: [topics Claude can generate strong content for]
- Less reliable: [topics where Claude's knowledge may be thin/outdated]
- External sourcing needed: [topics requiring user materials or web research]
```

## learning-schedule.md Template

This is the LIVING document — updated every session.

```markdown
# Learning Schedule — <Project Name>
Last updated: DD-MM-YYYY

## This Week
| Day | Date | Time | Topics | Mode | Status |
|-----|------|------|--------|------|--------|
| Mon | DD-MM | HH:MM-HH:MM | Topic A, Topic B | Technical | completed |
| Tue | DD-MM | HH:MM-HH:MM | Topic C | Technical | missed |
| Wed | DD-MM | HH:MM-HH:MM | Topic C + catch-up | Technical | today |
| Thu | DD-MM | — | REST | — | — |
| Fri | DD-MM | HH:MM-HH:MM | Topic D | Knowledge | upcoming |
| Sat | DD-MM | HH:MM-HH:MM | Review + diagnostic | Mixed | upcoming |
| Sun | DD-MM | — | REST | — | — |

## Next Week
[Same format]

## Upcoming
[Remaining weeks in condensed format]

## Adjustments Log
- DD-MM: [What changed and why]
```

## progress-report.md Template

```markdown
# Progress Report — <Project Name>
Last updated: DD-MM-YYYY

## Current Status
- Day: X of Y
- Streak: N consecutive days
- Overall: [on track / behind by Z days / ahead by Z days]
- SR: N cards total, M mature (ease > 2.5, interval > 21), K due tomorrow
- Exercises: N completed out of M planned
- Weakest area: [topic]
- Strongest area: [topic]

## Active Concerns
- [Timing patterns, weak areas, environmental issues, anything the session skill should know]

## Session Log
| Date | Duration | Committed | Cards Reviewed | Cards Correct | Exercises | Notes |
|------|----------|-----------|---------------|---------------|-----------|-------|
| DD-MM | X min | Y min | N (Z%) | M | A/B | Brief note |

## Topic Mastery
| Topic | Mastery | Cards (mature/total) | Exercises (done/total) | Notes |
|-------|---------|---------------------|----------------------|-------|
```

## learner-context.md Template

```markdown
# Learner Context — <Project Name>
Last updated: DD-MM-YYYY

## Read This First
This document captures who this learner is in the context of THIS project.
Read it at the start of every session before plan, schedule, or cards.

## Explanation Style
- Preferred: [what works — e.g., "analogies before formal definitions", "code examples first"]
- Avoid: [what doesn't work — e.g., "long theoretical preambles"]

## Recurring Patterns
- [Common mistake types specific to this subject]
- [Confusions that keep coming back]
- [Explanations that clicked — record these for reuse]

## Confidence Calibration
- [Do they over- or under-rate their understanding?]
- [Topics where self-assessment diverges from actual performance]

## What Motivates Them (observed, not just stated)
- [What actually lit them up during sessions]
- [What killed momentum]

## Session-to-Session Notes
- [DD-MM]: [Notable observation — use their words where possible]
```
