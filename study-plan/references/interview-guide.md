# Interview Guide

Structured interview questions for study plan creation. Number of rounds scales with urgency (Phase 0 triage).

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
- "Where do you usually study? Is that environment reliable (quiet, no interruptions, good internet)?"
- "Do you have a backup study location?"
- "When are you typically free to study? Morning, afternoon, evening?"
- "What usually derails a planned study session?"

### Motivation
- "What motivates you to keep going when studying gets hard?"
- "What makes you quit?"

Write responses to `~/.claude/skills/study-plan/references/user-profile.md` using the template in the plan spec.

---

## Project-Specific Interview Rounds

### Round 1 — Who and What (all urgency levels)

Use AskUserQuestion for each:

1. "What are you trying to learn?" (free text — let them describe in their own words)
2. "What's the context?" — Options:
   - Interview prep
   - Exam / certification
   - Professional development
   - Personal interest
   - Other
3. "What's your timeline?" — Get a specific date or "open-ended"
4. "How many hours per day can you realistically commit?" — Emphasise *realistically*

### Round 2 — Current State (standard + deep)

1. "What's your current skill level in this area?" — Options:
   - Beginner (little to no experience)
   - Intermediate (know the basics, gaps in advanced topics)
   - Advanced (strong foundation, polishing / filling specific gaps)
   - Mixed (strong in some subtopics, weak in others)
2. "What specific subtopics are you strongest in?"
3. "What are you weakest in or most anxious about?"
4. "Do you have any materials already? (books, courses, notes, problem sets)"
5. "Should we start your first session with a diagnostic assessment to calibrate?"

### Round 3 — Learning Style (standard + deep)

Skip if first-use onboarding already covered this. Otherwise:

1. "How do you learn best?" (same options as onboarding)
2. "For this specific topic, what study approach appeals to you?"
3. "Do you learn better in long sessions or short bursts?"
4. "What keeps you engaged vs. what makes you zone out?"

### Round 4 — Schedule and Environment (deep only)

1. "What specific time window works best each day? (e.g., '9-11 AM', 'after dinner')"
2. "Walk me through your week — is this consistent or does it vary by day?"
   - Monday: ___
   - Tuesday: ___
   - (etc.)
3. "Where will you study? Is the environment reliable?"
4. "Do you have backup locations?"
5. "What typically derails a planned session? (work overruns, social, energy)"

### Round 5 — Honest Commitment (deep only)

Frame this carefully — not shaming, realistic triage:

1. "What's the *actual minimum* you'll do on a bad day? Not the ideal — the floor."
2. "What days are genuinely unavailable?"
3. "Are there topics you're tempted to skip? (These often need the most work.)"
4. "What does success look like for you — minimum viable vs. ideal?"
5. "If you look at the last week of your life: how many of those study time slots would you *actually* have used?" — Force honest reflection.

---

## Post-Interview Synthesis

After completing all rounds:

1. Synthesise everything into a **Learner Profile** summary
2. Present it back to the user
3. Use AskUserQuestion to confirm: "Does this accurately capture your situation? Anything to correct or add?"
4. Iterate until they confirm

The confirmed profile feeds into Phase 2 (Research) and Phase 3 (Plan Construction).

---

## Quick Mode (Urgent) — Compressed Interview

Single round, all essential questions:

1. "What topic and what level?"
2. "What language? (for technical)"
3. "How many hours do you have today?"
4. "What's the most important thing to cover?"
5. "Any materials you have open right now?"

Get answers → skip research → generate lean plan → start studying within 10-15 minutes.
