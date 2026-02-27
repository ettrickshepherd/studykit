# Interview Guide

Structured questions for study plan creation. Phase 0 handles classification, identification, and timeline. This guide covers first-use onboarding and the remaining steps.

## First-Use Onboarding (only when no user-profile.md exists)

Before project-specific questions, establish who the person is. This only happens once.

### Personal Background
- "What's your name?"
- "What do you do? (profession, education, current role)"
- "How would you describe your general experience level with structured study?"

### Learning Style Discovery
- "How do you learn best? Pick what resonates: reading, doing exercises, flashcards, discussion/Socratic, teaching/explaining, or a mix."
- "What's worked for you before when studying something hard? What hasn't?"
- "Do you learn better in long focused sessions or short bursts?"
- "Do you prefer typing or speaking your answers?"

### Schedule and Environment
- "What timezone are you in?"
- "Where do you usually study? Is that environment reliable (quiet, no interruptions, good internet)?"
- "Do you have a backup study location?"
- "When are you typically free to study? Morning, afternoon, evening?"
- "What usually derails a planned study session?"

### Motivation
- "What motivates you to keep going when studying gets hard?"
- "What makes you quit?"

Write responses to `~/.claude/skills/study-plan/references/user-profile.md` using the template in the plan spec.

---

## Core Questions

Phase 0 has already established: what they're preparing for, target identified (company/role or exam name), background research agent launched, timeline known, urgency derived.

### Step 1 — Current State (all urgency levels)

1. "What's your current skill level in this area?" — Options:
   - Beginner (little to no experience)
   - Intermediate (know the basics, gaps in advanced topics)
   - Advanced (strong foundation, polishing / filling specific gaps)
   - Mixed (strong in some subtopics, weak in others)
2. "What specific subtopics are you strongest in?"
3. "What are you weakest in or most anxious about?"
4. "Do you have any materials already? (books, courses, notes, problem sets)"
5. "Should we start your first session with a diagnostic assessment to calibrate?"

### Step 2 — Focus (standard + deep, skip for urgent)

Scales with context. By now the background research agent should have results.

**For interview:**

Present research findings first: "Here's what I found about [Company] [Role] interviews — does this match what you've heard?" Confirm or correct before proceeding.

Then read the relevant reference files:
- Technical / coding → read `~/.claude/skills/study-plan/references/technical-interview.md`
- Oral / behavioral → read `~/.claude/skills/study-plan/references/oral-interview.md`
- Both → read both

AskUserQuestion (multiSelect): "What aspects of the interview are you preparing for?"
- Technical / coding
- Oral / behavioral

**For algorithmic prep:**
- "Which problem list do you want to work from?" (Blind 75 / Neetcode 150 / Grind 75 / Claude picks based on your level / I have my own list)
- "Which patterns are you already comfortable with?" (present the pattern list from `technical-interview.md`)
- "Which patterns feel weakest?" (these get prioritised)
- "Do you want timed practice from day 1, or build up to it?"

**For oral prep:**
- "Do you have stories/examples ready for behavioral questions, or starting from scratch?"
- "Any specific competencies you know they test? (leadership, conflict resolution, etc.)"
- "Do you want to practice out loud (typing responses) or build a story bank first?"

**For exam/cert:**

Present research findings: "Here's what I found about [Exam] — format, topics, weighting..." Confirm or correct.

- Known exam structure, topic weights
- Past attempts or mock results
- Which sections are you most/least confident in?

**For other:**
- Learning style preferences (if not covered in first-use onboarding)
- Specific goals / depth desired
- "What does success look like for you?"

### Step 3 — Schedule + Commitment (deep only)

1. "What specific time window works best each day? (e.g., '9-11 AM', 'after dinner')"
2. "Walk me through your week — is this consistent or does it vary by day?"
3. "Where will you study? Is the environment reliable?"
4. "What typically derails a planned session? (work overruns, social, energy)"
5. "What's the *actual minimum* you'll do on a bad day? Not the ideal — the floor."
6. "What days are genuinely unavailable?"
7. "Are there topics you're tempted to skip? (These often need the most work.)"

---

## Quick Mode (urgent)

Step 1 only. Skip Steps 2-3 — start studying. Background research agent results get incorporated into the first session or used to revise the plan after session 1.

For urgent interview/exam: the background agent is still running from Phase 0. If results arrive during Step 1, weave them in. If not, proceed without them — they'll inform the plan revision.

---

## Post-Interview Synthesis

After completing all steps:

1. Synthesise everything into a **Learner Profile** summary
2. Present it back to the user
3. Use AskUserQuestion to confirm: "Does this accurately capture your situation? Anything to correct or add?"
4. Iterate until they confirm

The confirmed profile feeds into Phase 2 (Research) and Phase 3 (Plan Construction).
