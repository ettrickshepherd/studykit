# Technical Interview Reference

Read this reference when the study plan context is interview prep + technical. It covers the assessment landscape, algorithmic pattern taxonomy, primitive extraction, and problem list references.

## Assessment Types

### Algorithmic (LeetCode-style)
- Pattern-based problem solving under time constraints
- Typical format: 1-2 problems, 45-60 min
- Evaluated on: correctness, optimal approach, code quality, edge cases, communication
- Prep approach: pattern recognition → timed practice → primitive extraction → SR cards

### Online Assessments (OA)
- Platforms: CodeSignal, HackerRank, Karat, Codility, LeetCode OA
- Typically 2-4 problems, 60-120 min, no IDE assistance
- Often auto-graded with hidden test cases
- Prep approach: practice under platform constraints, time management across problems

### System Design
- Architecture and scalability questions (senior+ roles)
- Typical format: 1 question, 45-60 min, open-ended
- Evaluated on: requirements gathering, component breakdown, trade-offs, scalability reasoning
- Prep approach: component-by-component study, practice drawing systems, learn estimation

### Pair Programming / Live Coding
- Solve a problem with an interviewer observing or collaborating
- Evaluated on: communication, thinking aloud, collaboration, handling feedback
- Prep approach: practice narrating thought process while coding

### Take-Home Projects
- Build something in 2-8 hours (sometimes longer)
- Evaluated on: architecture, code quality, testing, documentation, polish
- Prep approach: project structure templates, time-boxing, knowing when "good enough" is done

### CS Fundamentals
- OS: processes, threads, memory, scheduling, synchronization
- Networking: TCP/UDP, HTTP, DNS, load balancing, CDNs
- Databases: SQL vs NoSQL, indexing, transactions, CAP theorem, sharding
- Concurrency: locks, semaphores, deadlock, race conditions
- Prep approach: concept review → SR cards for definitions and trade-offs

### Domain-Specific
- ML/AI: model selection, training pipelines, evaluation metrics, MLOps
- Data Engineering: ETL, data modeling, streaming, batch processing
- Security: OWASP, auth patterns, encryption, threat modeling
- Mobile: platform-specific patterns, lifecycle, performance
- Prep approach: varies — identify the specific domain requirements from role research

---

## Pattern Taxonomy (Algorithmic)

The ~15 core patterns that cover the majority of interview problems. During onboarding, ask which the user is comfortable with and which feel weakest.

### Two Pointer
- **What**: Two indices moving through a sorted/structured array
- **Signals**: sorted array, "find pair that sums to X", "remove duplicates in-place"
- **Key primitives**: pointer initialization, movement rules, termination condition
- **Difficulty curve**: Easy (Two Sum II) → Medium (3Sum) → Hard (Trapping Rain Water)

### Sliding Window
- **What**: Variable or fixed-size window over a sequence
- **Signals**: "longest substring with...", "minimum window containing...", contiguous subarray
- **Key primitives**: window expansion, contraction condition, tracking window state (hash map/counter)
- **Difficulty curve**: Easy (Max Avg Subarray) → Medium (Longest Substring Without Repeating) → Hard (Minimum Window Substring)

### Binary Search
- **What**: Halving search space on sorted/monotonic data
- **Signals**: sorted array, "find minimum/maximum that satisfies...", search space with monotonic property
- **Key primitives**: mid calculation, boundary update logic, left vs right bias, search space definition
- **Difficulty curve**: Easy (Binary Search) → Medium (Search in Rotated Array) → Hard (Median of Two Sorted Arrays)

### BFS / Breadth-First Search
- **What**: Level-by-level exploration of graphs/trees
- **Signals**: "shortest path in unweighted graph", "level order", "minimum steps"
- **Key primitives**: queue, visited set, level tracking, neighbor enumeration
- **Difficulty curve**: Easy (Flood Fill) → Medium (Number of Islands) → Hard (Word Ladder)

### DFS / Depth-First Search
- **What**: Explore as deep as possible before backtracking
- **Signals**: "all paths", "connected components", "detect cycle", tree traversals
- **Key primitives**: recursion/stack, visited tracking, pre/in/post-order, backtracking cleanup
- **Difficulty curve**: Easy (Max Depth of Tree) → Medium (Course Schedule) → Hard (Word Search II)

### Topological Sort
- **What**: Linear ordering of directed acyclic graph nodes
- **Signals**: "order of dependencies", "course prerequisites", "build order"
- **Key primitives**: in-degree counting, BFS with queue (Kahn's), DFS with post-order
- **Difficulty curve**: Medium (Course Schedule) → Medium (Course Schedule II) → Hard (Alien Dictionary)

### Union Find
- **What**: Track connected components with efficient merge/find
- **Signals**: "connected components", "redundant connection", grouping by equivalence
- **Key primitives**: parent array, find with path compression, union by rank
- **Difficulty curve**: Medium (Number of Provinces) → Medium (Redundant Connection) → Hard (Accounts Merge)

### Heap / Priority Queue
- **What**: Efficiently track min/max elements
- **Signals**: "kth largest/smallest", "merge k sorted", "median from stream"
- **Key primitives**: heapify, push/pop, two-heap pattern (min + max)
- **Difficulty curve**: Easy (Kth Largest) → Medium (Top K Frequent) → Hard (Merge K Sorted Lists)

### Backtracking
- **What**: Build candidates incrementally, abandon on constraint violation
- **Signals**: "all combinations", "all permutations", "generate all valid...", constraint satisfaction
- **Key primitives**: choice-explore-unchoice, pruning conditions, avoiding duplicates
- **Difficulty curve**: Medium (Subsets) → Medium (Combination Sum) → Hard (N-Queens)

### Dynamic Programming
- **What**: Optimal substructure + overlapping subproblems
- **Signals**: "minimum/maximum cost", "number of ways", "can you reach...", optimization over sequence
- **Key primitives**: subproblem definition, recurrence relation, base cases, memoization vs tabulation, state dimensions
- **Difficulty curve**: Easy (Climbing Stairs) → Medium (Coin Change) → Hard (Edit Distance)

### Greedy
- **What**: Locally optimal choices lead to globally optimal solution
- **Signals**: "minimum number of intervals", scheduling, "can you complete..."
- **Key primitives**: sorting by key criterion, greedy choice proof (exchange argument), interval handling
- **Difficulty curve**: Easy (Assign Cookies) → Medium (Jump Game) → Hard (Task Scheduler)

### Divide and Conquer
- **What**: Split problem, solve halves, combine
- **Signals**: "merge sort variant", "count inversions", recursive structure
- **Key primitives**: split strategy, combine logic, base case
- **Difficulty curve**: Medium (Sort an Array) → Medium (Count of Smaller Numbers After Self) → Hard (Reverse Pairs)

### Monotonic Stack
- **What**: Stack maintaining increasing or decreasing order
- **Signals**: "next greater element", "largest rectangle in histogram", "daily temperatures"
- **Key primitives**: push/pop invariant, what the stack stores (index vs value), direction of scan
- **Difficulty curve**: Easy (Next Greater Element I) → Medium (Daily Temperatures) → Hard (Largest Rectangle in Histogram)

### Trie
- **What**: Prefix tree for string operations
- **Signals**: "prefix search", "autocomplete", "word dictionary with wildcards"
- **Key primitives**: node structure (children dict + is_end), insert/search/startsWith
- **Difficulty curve**: Medium (Implement Trie) → Medium (Add and Search Word) → Hard (Word Search II)

### Bit Manipulation
- **What**: Operations at the bit level
- **Signals**: "single number", "power of two", "XOR trick", "count bits"
- **Key primitives**: XOR properties, bit shifting, masks, Brian Kernighan's algorithm
- **Difficulty curve**: Easy (Single Number) → Medium (Counting Bits) → Hard (Maximum XOR of Two Numbers)

### Interval Merging
- **What**: Operations on ranges/intervals
- **Signals**: "merge overlapping", "insert interval", "meeting rooms"
- **Key primitives**: sort by start, overlap detection, merge logic
- **Difficulty curve**: Easy (Meeting Rooms) → Medium (Merge Intervals) → Hard (Insert Interval)

---

## Problem List References

Named sets the user can choose from during onboarding. Claude knows these lists — the reference just names them so the interview can offer them.

| List | Size | Focus | Best for |
|------|------|-------|----------|
| Blind 75 | 75 | Core patterns, high frequency | Short timelines (1-3 weeks), general prep |
| Neetcode 150 | 150 | Expanded Blind 75, better coverage | Medium timelines (3-6 weeks) |
| Grind 75 | 75 | Customizable by hours available | Flexible timelines, structured progression |
| Sean Prashad LC Patterns | ~170 | Organized strictly by pattern | Pattern-focused learners |
| Company-tagged problems | varies | Filtered by company frequency | Targeting a specific company |

During onboarding: "Which problem list do you want to work from?" or "How much time do you have? I'll recommend a list."

---

## Primitive Extraction Guide

After the user solves a problem (or studies a concept), extract the **transferable building blocks** and generate SR cards for those. The cards are about the primitives, not the specific problem.

### Algorithmic Example
**Problem**: Two Sum (LC 1)
**Primitives extracted**:
1. Hash map for O(1) complement lookup
2. Single-pass pattern: check-then-store vs store-then-check
3. Time/space trade-off: O(n) time + O(n) space vs O(n^2) brute force

**Cards generated**:
- "When should you use a hash map for complement searching?" → "When you need O(1) lookup of whether a target value exists. Classic in pair/sum problems."
- "What's the single-pass trick for Two Sum-style problems?" → "Check if complement exists in map BEFORE inserting current element. Avoids using an element twice."

### System Design Example
**Problem**: Design a URL shortener
**Primitives extracted**:
1. Base62 encoding for compact representation
2. Hash collision handling strategies
3. Read-heavy cache strategy (cache-aside pattern)
4. Counter vs hash-based ID generation trade-offs

### CS Fundamentals Example
**Topic**: Process vs Thread
**Primitives extracted**:
1. Shared memory model (threads share heap, separate stack)
2. Context switch cost (process > thread due to TLB flush)
3. Isolation trade-off (process crash doesn't kill siblings; thread crash can)

---

## Timing Benchmarks

| Assessment Type | Difficulty | Expected Solve Time | Interview Budget |
|----------------|-----------|-------------------|-----------------|
| Algorithmic | Easy | 10-15 min | 15-20 min |
| Algorithmic | Medium | 20-30 min | 25-35 min |
| Algorithmic | Hard | 30-45 min | 40-50 min |
| System Design | — | N/A | 45-60 min |
| OA (per problem) | Mixed | 15-30 min | Platform-specific |

During exercise evaluation: "You solved this in M minutes. In a real interview, you'd have ~N. [assessment]."
