---
name: seo-aeo-audit
description: Audits client digital assets (HTML files, websites, articles, schemas, URLs) for traditional SEO and AEO (Answer Engine Optimization) compliance. Use this skill whenever a user asks to audit client assets, inspect page structure, validate JSON-LD schemas, optimize content for AI search queries, or run search/answer engine checks.
---

# SEO & AEO Audit Agent

This skill guides you through auditing and optimizing client digital assets (such as local website directories, articles, templates, or live URLs) for both **Search Engine Optimization (SEO)** and **Answer Engine Optimization (AEO)**.

AEO focuses on preparing assets to be consumed, cited, and recommended by AI-driven search models (e.g., Perplexity, ChatGPT Search, Google AI Overviews, Gemini, and Claude).

---

## Decision Tree: Choosing Your Audit Path

```
                                  [Start Audit]
                                        │
                         How are assets provided?
                         ┌──────────────┴──────────────┐
                    [Local Directory/Files]         [Live URL]
                         │                             │
               Identify HTML files               Verify URL availability
                         │                             │
                         └──────────────┬──────────────┘
                                        ▼
                        Run Automated Scanning Script:
                  python scripts/audit_assets.py --src/--url
                                        │
                                        ▼
                        Review Raw Results in JSON
                                        │
                                        ▼
                         Compile Client HTML Dashboard:
                    python scripts/generate_report.py
                                        │
                                        ▼
                          [Iterative Manual Review]
                Analyze complex E-E-A-T and Entity structures
```

---

## Tooling & Automation

This skill includes bundled Python scripts to speed up structural audits and client reports:

- **Auditor Script**: `scripts/audit_assets.py`  
  *Usage*: Scans files or fetches URLs to evaluate SEO parameters (title, description, headings, images, canonical, robots meta) and AEO parameters (concise answer summaries, schema types, lists/tables). Saves data to a JSON file.
- **Report Compiler**: `scripts/generate_report.py`  
  *Usage*: Reads the JSON audit findings and compiles a premium, responsive HTML dashboard report featuring gauge scores, error logs, and dynamic filter tools.

---

## Step-by-Step Audit Workflow

### Step 1: Run Structural Scanning

Execute the auditor script against the target files or URL. Note: The script utilizes Python's built-in libraries, meaning no additional package installations are required.

**Scan local directory:**
```bash
python scripts/audit_assets.py --src /path/to/website/folder --output findings.json
```

**Scan a single HTML file:**
```bash
python scripts/audit_assets.py --src /path/to/page.html --output findings.json
```

**Scan a live website URL:**
```bash
python scripts/audit_assets.py --url https://client-site.com --output findings.json
```

### Step 2: Compile the Client Dashboard

Once the findings are saved in `findings.json`, compile the executive HTML dashboard:

```bash
python scripts/generate_report.py --input findings.json --output client_audit_dashboard.html
```

Proffer the resulting dashboard path to the user so they can open it in a browser.

### Step 3: Perform Contextual Analysis (E-E-A-T & Intent)

Automated scripts cannot verify subjective E-E-A-T signals or conceptual alignment. You must manually check the following:

#### 1. Entity and E-E-A-T Verification
- **Authorship**: Inspect the `<script type="application/ld+json">` tags. Look for a `Person` schema. Does it contain a `sameAs` array linking to established external entities (e.g., LinkedIn profile, Wikidata page, or official bio page)?
- **Brand Consistency**: Confirm that the client brand name, spelling, and description match exactly across their site and their Crunchbase, LinkedIn, or external reference links.
- **Reference Citations**: Verify that claims made in the articles cite primary sources (such as research databases, academic papers, or .edu/.gov URLs) using descriptive anchor text.

#### 2. Answer-First Snippets (The "AI Snack")
- Ensure that each key informational page or sub-heading begins with a direct, standalone summary of **40 to 60 words**.
- Check that this summary is free of filler language (e.g., replace "In this section we will discuss X" with "X is a Y defined by Z").

#### 3. Conversational Intent Mapping
- Perform search queries related to the asset's keywords and check "People Also Ask" (PAA) boxes.
- Match those PAA questions exactly to heading structures (`<h2>` or `<h3>`) and check if the page provides immediate, concise answers directly beneath them.

---

## Detailed Evaluation Criteria

Review the attached guidelines for specific audit definitions:
- **Traditional SEO**: [seo_guidelines.md](file://references/seo_guidelines.md)
- **Answer Engine Optimization**: [aeo_guidelines.md](file://references/aeo_guidelines.md)
