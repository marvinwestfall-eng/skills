#!/usr/bin/env python3
import os
import sys
import json
import re
import argparse
import html.parser
import urllib.request
import urllib.parse

class AssetParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.meta_description = None
        self.meta_robots = None
        self.canonical_url = None
        self.title_text = ""
        self.headings = []
        self.images = []
        self.links = []
        self.json_ld_contents = []
        self.paragraphs = []
        self.lists_count = 0
        self.tables_count = 0
        
        # State trackers
        self.in_json_ld = False
        self.current_json_ld = ""
        self.in_heading = False
        self.current_heading_tag = None
        self.current_heading_text = ""
        self.in_link = False
        self.current_link_href = None
        self.current_link_text = ""
        self.in_paragraph = False
        self.current_paragraph_text = ""

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        
        if tag == 'meta':
            name = attr_dict.get('name', '').lower()
            prop = attr_dict.get('property', '').lower()
            content = attr_dict.get('content', '')
            if name == 'description' or prop == 'og:description':
                if not self.meta_description:
                    self.meta_description = content
            elif name == 'robots':
                self.meta_robots = content
        elif tag == 'link':
            rel = attr_dict.get('rel', '').lower()
            if rel == 'canonical':
                self.canonical_url = attr_dict.get('href', '')
        elif tag == 'img':
            src = attr_dict.get('src', '')
            alt = attr_dict.get('alt') # None if missing, or string
            self.images.append({"src": src, "alt": alt})
        elif tag in ['ul', 'ol', 'dl']:
            self.lists_count += 1
        elif tag == 'table':
            self.tables_count += 1
        elif tag == 'script':
            type_attr = attr_dict.get('type', '')
            if type_attr == 'application/ld+json':
                self.in_json_ld = True
                self.current_json_ld = ""
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = True
            self.current_heading_tag = tag
            self.current_heading_text = ""
        elif tag == 'a':
            self.in_link = True
            self.current_link_href = attr_dict.get('href', '')
            self.current_link_text = ""
        elif tag == 'p':
            self.in_paragraph = True
            self.current_paragraph_text = ""

    def handle_data(self, data):
        if self.current_tag == 'title':
            self.title_text += data
        elif self.in_json_ld:
            self.current_json_ld += data
        elif self.in_heading:
            self.current_heading_text += data
        elif self.in_link:
            self.current_link_text += data
        elif self.in_paragraph:
            self.current_paragraph_text += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_json_ld:
            self.json_ld_contents.append(self.current_json_ld)
            self.in_json_ld = False
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.in_heading:
            self.headings.append({"tag": tag, "text": self.current_heading_text.strip()})
            self.in_heading = False
        elif tag == 'a' and self.in_link:
            self.links.append({"href": self.current_link_href, "text": self.current_link_text.strip()})
            self.in_link = False
        elif tag == 'p' and self.in_paragraph:
            txt = self.current_paragraph_text.strip()
            if txt:
                self.paragraphs.append(txt)
            self.in_paragraph = False
        self.current_tag = None

def analyze_asset(content, source_name):
    parser = AssetParser()
    try:
        parser.feed(content)
    except Exception as e:
        return {
            "source": source_name,
            "error": f"Failed to parse HTML: {str(e)}",
            "seo_score": 0,
            "aeo_score": 0,
            "metrics": {},
            "recommendations": ["Ensure the file contains valid HTML markup."]
        }

    # Evaluate metrics
    seo_score = 100
    aeo_score = 100
    recommendations = []
    metrics = {}

    # 1. Title tag analysis
    title_text = parser.title_text.strip()
    title_len = len(title_text)
    if not title_text:
        seo_score -= 20
        aeo_score -= 10
        metrics["title"] = {"text": "", "length": 0, "status": "error", "message": "Title tag is missing or empty."}
        recommendations.append("Add a descriptive <title> tag to the page.")
    elif title_len < 10 or title_len > 60:
        seo_score -= 5
        status = "warning"
        msg = f"Title length is {title_len} chars (recommended: 10-60)."
        metrics["title"] = {"text": title_text, "length": title_len, "status": status, "message": msg}
        recommendations.append(f"Optimize title tag length (currently {title_len} chars; recommend 10-60).")
    else:
        metrics["title"] = {"text": title_text, "length": title_len, "status": "pass", "message": "Title is optimized."}

    # 2. Meta description analysis
    meta_desc = parser.meta_description or ""
    meta_desc_len = len(meta_desc.strip())
    if not meta_desc:
        seo_score -= 20
        aeo_score -= 10
        metrics["meta_description"] = {"text": "", "length": 0, "status": "error", "message": "Meta description is missing."}
        recommendations.append("Add a meta description to summarize page content.")
    elif meta_desc_len < 110 or meta_desc_len > 160:
        seo_score -= 5
        msg = f"Meta description length is {meta_desc_len} chars (recommended: 110-160)."
        metrics["meta_description"] = {"text": meta_desc, "length": meta_desc_len, "status": "warning", "message": msg}
        recommendations.append(f"Optimize meta description length (currently {meta_desc_len} chars; recommend 110-160).")
    else:
        metrics["meta_description"] = {"text": meta_desc, "length": meta_desc_len, "status": "pass", "message": "Meta description is optimized."}

    # 3. Headings analysis
    h1s = [h for h in parser.headings if h["tag"] == "h1"]
    h1_count = len(h1s)
    if h1_count == 0:
        seo_score -= 15
        aeo_score -= 10
        metrics["h1"] = {"count": 0, "status": "error", "message": "No <h1> tag found."}
        recommendations.append("Add exactly one <h1> heading to represent the primary topic.")
    elif h1_count > 1:
        seo_score -= 10
        metrics["h1"] = {"count": h1_count, "status": "error", "message": f"Multiple <h1> tags found ({h1_count})."}
        recommendations.append("Consolidate headings so there is only one <h1> tag per page.")
    else:
        metrics["h1"] = {"count": 1, "text": h1s[0]["text"], "status": "pass", "message": "Single H1 heading found."}

    # Heading hierarchy check
    hierarchy_errors = []
    prev_level = None
    for h in parser.headings:
        level = int(h["tag"][1])
        if prev_level is not None:
            if level > prev_level + 1:
                hierarchy_errors.append(f"Skip from {prev_level} to H{level} ('{h['text']}')")
        prev_level = level
    
    if hierarchy_errors:
        seo_score -= 5
        metrics["heading_hierarchy"] = {"status": "warning", "errors": hierarchy_errors, "message": "Heading levels skip hierarchy."}
        recommendations.append("Fix heading structure hierarchy (e.g., do not skip from H2 directly to H4).")
    else:
        metrics["heading_hierarchy"] = {"status": "pass", "errors": [], "message": "Heading hierarchy is logical."}

    # 4. Canonical URL analysis
    canonical = parser.canonical_url
    if not canonical:
        seo_score -= 10
        metrics["canonical"] = {"text": "", "status": "error", "message": "Canonical link is missing."}
        recommendations.append("Add a self-referencing canonical URL link tag.")
    else:
        metrics["canonical"] = {"text": canonical, "status": "pass", "message": "Canonical URL tag present."}

    # 5. Robots tag
    robots = parser.meta_robots
    if not robots:
        metrics["robots"] = {"text": "None (default: index, follow)", "status": "pass"}
    else:
        metrics["robots"] = {"text": robots, "status": "pass"}

    # 6. Image Alt attributes
    total_imgs = len(parser.images)
    missing_alt_imgs = [img for img in parser.images if img["alt"] is None]
    empty_alt_imgs = [img for img in parser.images if img["alt"] == ""]
    missing_alt_count = len(missing_alt_imgs)
    
    if total_imgs > 0:
        if missing_alt_count > 0:
            penalty = min(missing_alt_count * 2, 10)
            seo_score -= penalty
            metrics["images"] = {
                "total": total_imgs,
                "missing_alt": missing_alt_count,
                "empty_alt": len(empty_alt_imgs),
                "status": "warning",
                "message": f"{missing_alt_count} out of {total_imgs} images are missing an alt attribute."
            }
            recommendations.append(f"Add descriptive alt attributes to the {missing_alt_count} images missing them.")
        else:
            metrics["images"] = {
                "total": total_imgs,
                "missing_alt": 0,
                "empty_alt": len(empty_alt_imgs),
                "status": "pass",
                "message": "All images contain alt attributes."
            }
    else:
        metrics["images"] = {"total": 0, "missing_alt": 0, "empty_alt": 0, "status": "pass", "message": "No images found."}

    # 7. Links & Anchor texts
    total_links = len(parser.links)
    generic_words = ['click here', 'read more', 'learn more', 'link', 'go', 'here', 'more', 'website']
    generic_anchors = []
    for l in parser.links:
        t = l["text"].lower().strip()
        if t in generic_words or any(g == t for g in generic_words):
            generic_anchors.append(l)
    
    if total_links > 0:
        if len(generic_anchors) > 0:
            seo_score -= 5
            metrics["links"] = {
                "total": total_links,
                "generic_count": len(generic_anchors),
                "status": "warning",
                "message": f"Found {len(generic_anchors)} links with generic anchor texts (e.g. 'read more')."
            }
            recommendations.append("Use descriptive anchor text for links rather than generic phrases like 'read more' or 'click here'.")
        else:
            metrics["links"] = {"total": total_links, "generic_count": 0, "status": "pass", "message": "All links use customized anchor text."}
    else:
        metrics["links"] = {"total": 0, "generic_count": 0, "status": "pass", "message": "No links found."}

    # 8. Schema & JSON-LD
    schema_types = []
    schema_errors = []
    for script_content in parser.json_ld_contents:
        try:
            data = json.loads(script_content)
            # Support list or single object
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "@type" in item:
                        schema_types.append(item["@type"])
            elif isinstance(data, dict):
                if "@type" in data:
                    schema_types.append(data["@type"])
                # check @graph
                if "@graph" in data and isinstance(data["@graph"], list):
                    for item in data["@graph"]:
                        if isinstance(item, dict) and "@type" in item:
                            schema_types.append(item["@type"])
        except Exception as e:
            schema_errors.append(f"JSON-LD syntax error: {str(e)}")

    if schema_errors:
        seo_score -= 10
        aeo_score -= 15
        metrics["schema"] = {"types": schema_types, "errors": schema_errors, "status": "error", "message": "Invalid JSON-LD markup found."}
        recommendations.append("Fix JSON-LD syntax errors so search engines can read structured data.")
    elif not schema_types:
        seo_score -= 10
        aeo_score -= 20
        metrics["schema"] = {"types": [], "errors": [], "status": "warning", "message": "No structured data (JSON-LD) found."}
        recommendations.append("Add structured data schema (e.g., FAQPage, Article, or Organization) to assist answer engines.")
    else:
        # Check for AEO friendly schemas
        aeo_schemas = {"FAQPage", "Article", "BlogPosting", "NewsArticle", "Person", "Organization", "Product"}
        found_aeo_schemas = set(schema_types).intersection(aeo_schemas)
        if not found_aeo_schemas:
            aeo_score -= 10
            metrics["schema"] = {
                "types": schema_types,
                "errors": [],
                "status": "warning",
                "message": f"Found schema types ({', '.join(schema_types)}) but none are specifically optimized for direct answer extraction."
            }
            recommendations.append("Add AEO-friendly schemas such as FAQPage, Person, or Article to aid AI entity-linking.")
        else:
            metrics["schema"] = {
                "types": schema_types,
                "errors": [],
                "status": "pass",
                "message": f"Structured data present: {', '.join(schema_types)}."
            }

    # 9. AEO Answer-First Paragraph Checklist
    # Check if any paragraph matches the 30-70 word concise answer-first pattern
    answer_first_p = None
    first_p = parser.paragraphs[0] if parser.paragraphs else None
    
    if first_p:
        words = len(first_p.split())
        # AEO Sweet spot is 35 to 65 words
        if 30 <= words <= 70:
            metrics["aeo_answer_first"] = {
                "word_count": words,
                "text_preview": first_p[:80] + "...",
                "status": "pass",
                "message": f"Initial paragraph is optimized for answer engine summaries ({words} words)."
            }
        else:
            aeo_score -= 15
            status = "warning"
            if words > 70:
                msg = f"First paragraph is too long ({words} words). AI crawlers prefer concise, stand-alone answers (40-60 words)."
                rec = "Shorten the introductory paragraph to 40-60 words to create a high-quality answer snippet."
            else:
                msg = f"First paragraph is too short ({words} words) to be an informative summary."
                rec = "Expand the introductory paragraph to a 40-60 word comprehensive summary of the page topic."
            metrics["aeo_answer_first"] = {
                "word_count": words,
                "text_preview": first_p[:80] + "...",
                "status": status,
                "message": msg
            }
            recommendations.append(rec)
    else:
        aeo_score -= 20
        metrics["aeo_answer_first"] = {"word_count": 0, "status": "error", "message": "No paragraph `<p>` content discovered."}
        recommendations.append("Write a descriptive introductory paragraph (40-60 words) to summarize the content.")

    # 10. AEO Scannability Checklist
    lists = parser.lists_count
    tables = parser.tables_count
    if lists == 0 and tables == 0:
        aeo_score -= 10
        metrics["aeo_scannability"] = {
            "lists": 0,
            "tables": 0,
            "status": "warning",
            "message": "No list elements (ul, ol) or tables detected."
        }
        recommendations.append("Break down complex details into bulleted lists or comparison tables to help AI models parse facts.")
    else:
        metrics["aeo_scannability"] = {
            "lists": lists,
            "tables": tables,
            "status": "pass",
            "message": f"Content uses structured formats ({lists} lists, {tables} tables)."
        }

    # Normalize scores to 0-100 range
    seo_score = max(0, min(100, seo_score))
    aeo_score = max(0, min(100, aeo_score))

    return {
        "source": source_name,
        "seo_score": seo_score,
        "aeo_score": aeo_score,
        "metrics": metrics,
        "recommendations": list(dict.fromkeys(recommendations)) # deduplicate
    }

def scan_local_dir(dir_path):
    results = []
    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid directory.", file=sys.stderr)
        sys.exit(1)
        
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.html', '.htm')):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                rel_path = os.path.relpath(full_path, dir_path)
                print(f"Auditing file: {rel_path}")
                results.append(analyze_asset(content, rel_path))
    return results

def crawl_url(url):
    print(f"Fetching URL: {url}")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (SEO-AEO Audit Agent)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
        parsed_url = urllib.parse.urlparse(url)
        name = parsed_url.netloc + parsed_url.path
        if name.endswith('/'):
            name += 'index.html'
        return analyze_asset(content, name)
    except Exception as e:
        return {
            "source": url,
            "error": f"Failed to fetch URL: {str(e)}",
            "seo_score": 0,
            "aeo_score": 0,
            "metrics": {},
            "recommendations": [f"Verify network connectivity and check if the URL '{url}' is accessible."]
        }

def main():
    parser = argparse.ArgumentParser(description="Auditor script for client SEO/AEO assets.")
    parser.add_argument("--src", help="Path to local directory or file to audit")
    parser.add_argument("--url", help="Live website URL to audit")
    parser.add_argument("--output", default="audit_report.json", help="Path to write JSON output findings")
    args = parser.parse_args()

    results = []

    if args.url:
        results.append(crawl_url(args.url))
    elif args.src:
        if os.path.isdir(args.src):
            results.extend(scan_local_dir(args.src))
        elif os.path.isfile(args.src):
            with open(args.src, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            basename = os.path.basename(args.src)
            print(f"Auditing single file: {basename}")
            results.append(analyze_asset(content, basename))
        else:
            print(f"Error: {args.src} is not a valid file or directory.", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Write out JSON results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Audit completed. Findings written to: {args.output}")

if __name__ == '__main__':
    main()
