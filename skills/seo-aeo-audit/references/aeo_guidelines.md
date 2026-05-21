# Answer Engine Optimization (AEO) Guidelines

Use these guidelines to audit and optimize assets for AI search engines, answer engines (e.g., Perplexity, ChatGPT Search, Gemini, Claude, and Google AI Overviews), and featured snippets.

---

## 1. Answer-First Formatting (The "AI Snack")

Answer engines prioritize text that directly solves a query in the first few sentences.

- **Standalone Summaries**:
  - Place a concise summary (40–60 words) at the very beginning of the page or under each major heading.
  - The summary should answer the "who, what, where, why, or how" directly and unambiguously.
  - Avoid introductory filler or conversational fluff in these summaries (e.g., instead of "In this article, we will explore...", write "Answer Engine Optimization (AEO) is the practice of optimizing content to be easily extracted by AI search engines...").
- **Clear Definitions**:
  - Use declarative sentence structures: `[Entity] is [Definition] because [Key Context].`

---

## 2. Information Structure and Scannability

AI engines synthesize and pull structured facts.

- **Lists & Tables**:
  - Whenever describing steps, rankings, or comparisons, format them as structured bulleted lists, numbered lists, or HTML tables.
  - Keep lists clean and parallel in structure (e.g., start each bullet with a verb or noun consistently).
- **Standalone Headers**:
  - Phrased as questions or specific search queries (e.g., `## What is AEO?` rather than `## AEO Overview`).
  - The content directly beneath the header must answer the header's question immediately.

---

## 3. Structured Data (JSON-LD Schema)

Schema acts as an explicit knowledge graph that AI crawlers use to map relationships between entities without guessing.

- **Essential Schema Types**:
  - `FAQPage`: Links specific questions (`Question`) to answers (`Answer`). Excellent for capturing direct Q&A blocks.
  - `Article` / `BlogPosting` / `NewsArticle`: Defines the author, publisher, date published, and primary content.
  - `Person`: For authors and executives. Must link to external authority profiles (`sameAs`) such as LinkedIn, Wikipedia, or Twitter.
  - `Organization`: Defines the business entity, logo, contact points, and official social handles.
  - `Product`: For products, including price, reviews, and availability details.
- **Rules**:
  - Schema must be valid JSON-LD.
  - No parsing errors or missing required fields.
  - Information in the schema must match the visible text on the page exactly (to prevent search engine penalty).

---

## 4. E-E-A-T & Entity Alignment (Authority)

AI models need to verify the source of information to ensure accuracy and limit hallucinations.

- **Entity Consistency**:
  - Maintain a clean, consistent brand description and author name across all platforms (socials, crunchbase, official site, etc.) to minimize "semantic drift".
- **Source Citations**:
  - Back up claims with outbound links to primary sources, research papers, or government domains.
  - Cite the specific organization or research name in the anchor text (e.g., "According to the Pew Research Center study...").
- **Author Bios**:
  - Link author names on articles to dedicated bio pages that describe their credentials and link to external authority sources.

---

## 5. Conversational Query Mapping (PAA)

- **Targeting PAA (People Also Ask)**:
  - Audit Google's PAA boxes for target keywords. Include these exact questions as H2/H3 headers on the page.
  - Write dedicated 50-word answers directly beneath them.
- **Natural Language Intent**:
  - Optimize for voice searches and conversational search queries (e.g., long-tail, natural phrases).
