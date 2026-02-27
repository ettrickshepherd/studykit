# Oral Interview Reference

Read this reference when the study plan context is interview prep + oral/behavioral. Covers behavioral, case, competency, and culture-fit interview formats.

## Assessment Types

### Behavioral (STAR Method)
- **Format**: "Tell me about a time when..." questions
- **Structure**: Situation → Task → Action → Result
- **Evaluated on**: specificity, impact quantification, ownership, self-awareness
- **Common themes**: leadership, conflict resolution, failure handling, collaboration, ambiguity, prioritization
- **Prep approach**: build a story bank (8-12 strong stories), map each to multiple competencies, practice concise delivery

### Case Interviews
- **Format**: open-ended business problems, often consulting-style
- **Frameworks**: market sizing, profitability analysis, M&A evaluation, new market entry
- **Evaluated on**: structured thinking, estimation skill, synthesis, ability to ask good questions
- **Prep approach**: learn 3-4 frameworks, practice estimation, practice synthesizing under pressure

### Competency-Based
- **Format**: role-specific scenarios — "How would you handle..."
- **Differs from behavioral**: asks about hypothetical situations, not past experiences
- **Evaluated on**: domain knowledge, judgment, reasoning process, alignment with role requirements
- **Prep approach**: understand the role deeply, prepare domain vocabulary, build concrete example bank

### Culture Fit / Values
- **Format**: company-specific values probing — "Which of our values resonates most?"
- **Varies by company**: Amazon (Leadership Principles), Google (Googleyness), Netflix (Culture Deck)
- **Evaluated on**: authentic alignment, not rehearsed answers
- **Prep approach**: research company values, identify genuine connections to personal experience, prepare 2-3 specific examples per value

### Presentation / Pitch
- **Format**: present past work, defend design decisions, pitch an idea
- **Evaluated on**: clarity, structure, handling questions, depth of understanding
- **Prep approach**: structure a narrative arc, anticipate questions, practice concise explanation at multiple detail levels

---

## Primitive Extraction for Oral Prep

Same concept as technical — extract transferable building blocks, generate SR cards.

### Behavioral Primitives
- **STAR structure**: how to frame any experience into a clear narrative
- **Impact quantification**: "I improved X by Y%" vs "I made things better"
- **Ownership language**: "I decided" vs "the team decided" — when to use each
- **Failure narratives**: how to present failures as growth (what happened, what you learned, what changed)
- **Scope signaling**: demonstrating awareness of business impact, not just task completion
- **Brevity discipline**: 2-3 minutes per answer, not 10

### Case Primitives
- **Framework selection**: matching the right framework to the problem type
- **Market sizing estimation**: top-down vs bottom-up, sanity checks, order of magnitude
- **Profitability tree**: revenue × volume - costs, decomposed
- **Synthesis under pressure**: summarizing findings and recommending a course of action

### Competency Primitives
- **Domain vocabulary**: using the right terms naturally (not forced)
- **Concrete examples bank**: specific situations ready to deploy
- **Bridging**: connecting personal experience to role requirements explicitly

---

## Practice Format

### Behavioral Practice
1. Claude presents a behavioral question (themed to target competency)
2. User types their STAR response
3. Claude evaluates:
   - **Structure**: Is STAR clear? Situation concise? Action specific?
   - **Specificity**: Concrete details or vague generalities?
   - **Impact**: Quantified result? Business-level awareness?
   - **Length**: Appropriate for interview (2-3 min spoken ≈ 150-300 words typed)?
   - **Ownership**: Clear personal contribution?
4. Feedback is direct: "Your situation setup was too long — 4 sentences max. The action was strong but you didn't quantify the result."
5. SR cards generated for: the competency being tested, the question pattern, which story from their bank fits

### Case Practice
1. Claude presents a case scenario
2. User works through it step by step (typing their reasoning)
3. Claude evaluates framework choice, estimation quality, synthesis
4. SR cards for framework steps and estimation techniques

### Competency Practice
1. Claude presents a "How would you handle..." scenario relevant to the role
2. User describes their approach
3. Claude evaluates against role expectations (informed by background research)
4. SR cards for domain-specific concepts and judgment patterns

---

## Company-Specific Research

Same pipeline as technical interviews. When user provides company + role:

1. Launch background Explore subagent to research:
   - Company values and leadership principles
   - Glassdoor/Blind interview reports for this role
   - Known question themes and emphasis areas
   - Interview round structure (how many behavioral rounds, who conducts them)
   - Any company-specific formats (Amazon's "bar raiser", Google's "Googleyness" round)

2. Present findings: "Here's what I found about [Company]'s behavioral interview process — does this match what you've heard?"

3. Tailor the practice:
   - Weight questions toward the company's known emphasis areas
   - Use the company's vocabulary (e.g., Amazon Leadership Principles by name)
   - Adjust story bank to emphasize relevant competencies

---

## Story Bank

During onboarding for oral prep, help the user build a **story bank** — 8-12 strong personal experiences that can be adapted to multiple question types.

For each story, record:
- **Title**: short name for reference ("The migration project", "The difficult stakeholder")
- **STAR summary**: 2-3 sentence version
- **Competencies it covers**: [leadership, conflict, technical depth, etc.]
- **Companies/roles it fits**: based on their values emphasis
- **Strength**: what makes this story good
- **Risk**: what could go wrong if asked to go deeper

Store in `learner-context.md` under a "## Story Bank" section. SR cards reference stories by title: "Which story best demonstrates [competency]?" → "[story title] — because [reason]."
