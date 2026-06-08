# The Unofficial Guide — Project 1


---

## Domain

My system covers UCF off-campus student housing. The knowledge base focuses on Reddit discussions where students share firsthand experiences about apartment complexes near the University of Central Florida, including pricing, bugs, mold, maintenance, safety, parking, shuttle access, noise, roommate issues, and management quality.

This knowledge is valuable because official apartment websites usually only show marketing information such as amenities, floor plans, and prices. They do not clearly show what students actually experience after moving in. Reddit comments are useful because they include informal, honest student opinions that are hard to find through official channels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Off campus student housing? | Reddit Thread | https://www.reddit.com/r/ucf/comments/1r26j8e/off_campus_student_housing/ |
| 2 | Best off-campus housing? | Reddit Thread | https://www.reddit.com/r/ucf/comments/1e7dmvz/best_offcampus_housing/ |
| 3 | good off-campus apartments for under $1100 a month? | Reddit Thread | https://www.reddit.com/r/ucf/comments/1cyjuti/good_offcampus_apartments_for_under_1100_a_month/ |
| 4 | UCF Off-Campus Housing | Reddit Thread | https://www.reddit.com/r/ucf/comments/wakpw4/ucf_offcampus_housing/ |
| 5 | Best Off-Campus housing w/ no car? | Reddit Thread | https://www.reddit.com/r/ucf/comments/17wu3wl/best_offcampus_housing_w_no_car/ |
| 6 | Which off campus housing should I move in? | Reddit Thread | https://www.reddit.com/r/ucf/comments/1kohehb/which_off_campus_housing_should_i_move_in/ |
| 7 | Best "not too modern looking" off campus near UCF? | Reddit Thread | https://www.reddit.com/r/ucf/comments/1hz8vtr/best_not_too_modern_looking_off_campus_near_ucf/ |
| 8 | Is off-campus housing really that bad? | Reddit Thread | https://www.reddit.com/r/ucf/comments/kq046u/is_offcampus_housing_really_that_bad_should_i_go/ |
| 9 | Off campus housing | Reddit Thread | https://www.reddit.com/r/ucf/comments/1tzgl6l/off_campus_housing/ |
| 10 | WHICH DO I CHOOSE | Reddit Thread | https://www.reddit.com/r/ucf/comments/1t6n7es/which_do_i_choose/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
One Reddit comment per chunk. Comments under 30 characters were dropped or merged with nearby context. Comments longer than 600 characters were split into smaller paragraph-based chunks.

**Overlap:**
0 characters for normal comment-based chunks. For comments longer than 600 characters that needed to be split, I used a 100-character overlap.

**Why these choices fit your documents:**
My documents are Reddit discussion threads, so individual comments are the natural unit of meaning. Most comments contain one student’s opinion, recommendation, warning, or personal experience about a specific apartment complex. Chunking by comment keeps apartment names, pricing, maintenance complaints, safety concerns, and shuttle information together.

Before chunking, I stripped metadata headers such as SOURCE_TYPE and DOCUMENT_ID, removed structural labels, removed Reddit boilerplate such as Upvote, Downvote, Reply, vote counts, ads, and AutoModerator text, and split the remaining content on comment-author boundaries.

Fixed character chunking could split useful context apart or combine unrelated apartment comments into one chunk. Very short comments such as “yes” or “thanks” do not carry enough meaning for semantic search, so they were removed or merged. Very long comments were split so that each embedding stayed focused.

**Final chunk count:**
236

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 through the Sentence Transformers library.

**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it runs locally, does not require an API key, is fast, and works well for short text such as Reddit comments. Its 256-token input limit is not a major issue for this project because my chunks are based on short comments, but it would matter more for longer documents.

If this system were deployed for real users and cost was not a constraint, I would consider a larger embedding model for better semantic accuracy. A larger model might better understand housing-specific terms such as “individual leasing,” “4x4,” “shuttle route,” and “maintenance response.” However, larger models may increase latency, cost, and memory usage. I would also consider multilingual support because UCF has a diverse student population, but accuracy on student housing questions would be my main priority.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt instructs the model to answer using only the provided CONTEXT, never outside or general knowledge. If the retrieved context does not contain relevant information, the model must respond with the exact phrase: “I don't have enough information on that.” The prompt also includes a comparison rule: if the user asks to compare two options but the context only supports one side, the model must say it cannot make a confident comparison instead of inventing a conclusion.

**How source attribution is surfaced in the response:**
Source attribution is attached programmatically, not generated freely by the LLM. After retrieval, the code collects the source filename from each retrieved chunk, removes duplicate filenames while preserving order, and returns those sources alongside the answer. The interface displays them in a “Retrieved from” panel, so every response is tied back to the documents used as context.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which apartment complex is most commonly recommended for students without a car? | Knights Circle because of its proximity to campus, shuttle access, and walkability. | The system said there was not enough information to determine the answer. | Partially relevant | Inaccurate |
| 2 | What concerns do students commonly mention about Northgate Lakes? | Mold issues, unreliable internet, small rooms, dirty units, and maintenance concerns. | The system mentioned dirty units, small rooms, strange smells, and negative experiences, but missed mold and internet issues. | Relevant | Partially accurate |
| 3 | Which apartment complexes are frequently described as affordable options under approximately $1,100 per month? | Tivoli, Mercury 3100, Riverwind, College Station, and some Orion units. | The system identified College Station and house rentals but missed several other affordable options. | Partially relevant | Partially accurate |
| 4 | What do students say about living at Plaza on University? | Good location and amenities, but complaints about noise, parking, maintenance, elevators, and pests. | The system described Plaza as having good amenities and location but noted management issues and mixed experiences. | Relevant | Accurate |
| 5 | Is Knights Circle or Accolade better for a student who wants a quiet apartment? | The documents do not provide enough evidence for a confident comparison. | The system correctly said it could not confidently compare the two apartments. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which apartment complex is most commonly recommended for students without a car?

**What the system returned:**
The system responded that it did not have enough information to determine which apartment complex was most commonly recommended for students without a car.

**Root cause (tied to a specific pipeline stage):**
This failure was primarily caused by the retrieval and grounding stages working together too conservatively. The relevant information was spread across multiple Reddit threads and multiple comments rather than appearing as one explicit statement. Although the retrieved chunks contained recommendations for Knights Circle, the grounding prompt required strong evidence before making a conclusion. As a result, the model refused to synthesize several related comments into a single answer.

**What you would change to fix it:**
I would adjust the grounding prompt to allow the model to synthesize consistent evidence across multiple retrieved chunks while still preventing the use of outside knowledge. I would also experiment with increasing top-k retrieval from 5 to 7 so more supporting comments can be retrieved for questions that require aggregation.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning document forced me to think carefully about chunking before writing any code. By deciding on comment-based chunking in advance, I avoided using a generic fixed-character splitter that would have separated apartment names from the experiences being described. The evaluation plan also gave me concrete questions to test retrieval quality before adding generation.

**One way your implementation diverged from the spec, and why:**
My original plan included context-aware merging of very short comments. During implementation, I simplified this by dropping comments under approximately 30 characters because reliable automatic merging was more complex than expected and provided little additional value. I also used simple character-based splitting for unusually long comments instead of sentence-aware splitting, which was easier to implement within the project timeline.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Documents section, Chunking Strategy section, and Architecture diagram from planning.md.
- *What it produced:* A document ingestion and chunking script that loaded Reddit text files and split content into chunks.
- *What I changed or overrode:* The first version split documents on blank lines, which fragmented several Reddit comments into incomplete chunks. I directed a rewrite that split on comment-author boundaries instead, preserving complete comments as the primary chunking unit.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach, grounding requirements, and evaluation questions.
- *What it produced:* A grounding prompt that required the model to answer only from retrieved context and refuse unsupported questions.
- *What I changed or overrode:* The initial grounding prompt was too strict and refused some answerable questions. I revised it to allow synthesis across multiple retrieved comments while maintaining the rule against using outside knowledge and adding a comparison guard for unsupported comparisons.
