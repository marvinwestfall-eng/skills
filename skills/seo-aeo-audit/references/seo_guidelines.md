# Traditional SEO Audit Guidelines

Use these guidelines to evaluate website assets for traditional search engine visibility, indexability, and user experience.

---

## 1. Title Tags and Meta Descriptions

Title tags and meta descriptions are the primary visual interfaces in search engine result pages (SERPs).

### Title Tags (`<title>`)
- **Length**: 50–60 characters (to avoid truncation in SERPs).
- **Format**: `Primary Keyword - Secondary Keyword | Brand Name` or `Title | Brand Name`.
- **Requirements**:
  - Exactly one `<title>` tag per page.
  - Must be unique across the entire site.
  - Must accurately describe the page content.
  - Avoid keyword stuffing.

### Meta Descriptions (`<meta name="description">`)
- **Length**: 110–160 characters.
- **Format**: A compelling, active call-to-action summary that encourages user clicks.
- **Requirements**:
  - Must include the target primary keyword naturally.
  - Unique to each page.
  - No duplicate description text across pages.

---

## 2. Heading Structure (Semantic Hierarchy)

Search engine crawlers use heading tags (`<h1>` to `<h6>`) to understand the structure and topic depth of a page.

- **H1 Header**:
  - Exactly one `<h1>` per page.
  - Represents the main topic or title of the content.
  - Should contain the primary target keyword.
- **Subheadings (H2, H3, H4)**:
  - Must follow a logical, descending nested order (e.g., do not skip from H2 to H4).
  - Use H2s for main sections, H3s for subsections under an H2.
  - Avoid using headings for styling; use CSS instead.

---

## 3. URLs and Canonicalization

- **URL Structure**:
  - Clean, user-friendly, and lowercase (e.g., `/services/seo-aeo-audit` instead of `/services.php?id=43&lang=en`).
  - Use hyphens (`-`) instead of underscores (`_`) or spaces (`%20`).
- **Canonical Tags (`<link rel="canonical">`)**:
  - Every indexable page must contain a self-referencing canonical URL.
  - Prevents duplicate content issues caused by query parameters (e.g., UTM tracking links).

---

## 4. Media and Image Optimization

- **Alt Text (`alt` attribute)**:
  - Every `<img>` tag must have an `alt` attribute.
  - For decorative images, use an empty alt attribute (`alt=""`).
  - For content-relevant images, describe the image contextually and include key phrases if relevant.
- **File Names**:
  - Descriptive, lowercase, hyphenated file names (e.g., `seo-audit-report-dashboard.jpg`).
- **Responsive Images**:
  - Use `srcset` or modern image formats (WebP, AVIF) to improve page speed.

---

## 5. Links (Internal and External)

- **Anchor Text**:
  - Must be descriptive and context-rich (avoid "click here" or "read more").
  - Example: Use "download our AEO audit checklist" instead of "click here to download".
- **Broken Links**:
  - Audit for `404` pages or invalid URLs.
- **Outbound Links**:
  - Link to high-authority external sources when referencing claims.
  - Set `rel="noopener noreferrer"` for security on external links opening in new tabs.

---

## 6. Technical Crawlability and Indexability

- **Robots Meta Tag**:
  - Verify that important pages are indexable (`<meta name="robots" content="index, follow">`).
  - Verify that utility or private pages are set to `noindex`.
- **Robots.txt & Sitemap**:
  - Ensure the page is listed in the `sitemap.xml`.
  - Ensure the user agents for search engines are not blocked from indexing key pages in `robots.txt`.
