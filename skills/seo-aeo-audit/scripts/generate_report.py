#!/usr/bin/env python3
import os
import sys
import json
import argparse

REPORT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO & AEO Audit Executive Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0c10;
            --surface-color: #12131a;
            --surface-hover: #1b1c24;
            --border-color: rgba(255, 255, 255, 0.07);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            
            --primary-glow: linear-gradient(135deg, hsl(265, 85%, 60%), hsl(230, 90%, 65%));
            --aeo-glow: linear-gradient(135deg, hsl(180, 85%, 45%), hsl(210, 90%, 55%));
            
            --seo-color: hsl(265, 85%, 65%);
            --aeo-color: hsl(180, 85%, 50%);
            --success-color: hsl(142, 70%, 50%);
            --warning-color: hsl(38, 92%, 55%);
            --danger-color: hsl(350, 89%, 60%);
            
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.3);
            --shadow-md: 0 8px 16px rgba(0,0,0,0.4);
            --shadow-lg: 0 16px 32px rgba(0,0,0,0.5);
            
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .light-mode {
            --bg-color: #f8fafc;
            --surface-color: #ffffff;
            --surface-hover: #f1f5f9;
            --border-color: rgba(0, 0, 0, 0.08);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            
            --seo-color: hsl(265, 80%, 50%);
            --aeo-color: hsl(190, 90%, 40%);
            
            --shadow-md: 0 8px 16px rgba(0,0,0,0.05);
            --shadow-lg: 0 16px 32px rgba(0,0,0,0.08);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            padding: 2.5rem;
            transition: var(--transition);
            line-height: 1.5;
        }

        /* Container Layout */
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
        }

        /* Premium Header Styling */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 2rem;
        }

        .header-title h1 {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.03em;
        }
        .light-mode .header-title h1 {
            background: linear-gradient(to right, #0f172a, #475569);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-title p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-top: 0.25rem;
            font-weight: 300;
        }

        .header-controls {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        button.btn {
            background-color: var(--surface-color);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            font-family: inherit;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
        }

        button.btn:hover {
            background-color: var(--surface-hover);
            transform: translateY(-2px);
            border-color: var(--text-secondary);
        }

        /* Overview Section: Ring Charts & Key KPIs */
        .overview-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr 1fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .overview-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
            transition: var(--transition);
        }

        .card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }

        .score-card {
            display: flex;
            align-items: center;
            justify-content: space-around;
            gap: 1.5rem;
        }

        .score-gauge {
            position: relative;
            width: 140px;
            height: 140px;
        }

        .score-gauge svg {
            width: 140px;
            height: 140px;
            transform: rotate(-90deg);
        }

        .score-gauge circle {
            fill: none;
            stroke-width: 12;
            stroke-linecap: round;
        }

        .score-gauge .bg-circle {
            stroke: rgba(255, 255, 255, 0.05);
        }
        .light-mode .score-gauge .bg-circle {
            stroke: rgba(0, 0, 0, 0.05);
        }

        .score-gauge .progress-circle {
            transition: stroke-dashoffset 1s ease-out;
        }

        .seo-gauge-color {
            stroke: var(--seo-color);
        }
        .aeo-gauge-color {
            stroke: var(--aeo-color);
        }

        .gauge-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-primary);
        }

        .score-info {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .score-label {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .score-val-title {
            font-size: 2rem;
            font-weight: 800;
        }

        /* KPI Quick Counters */
        .kpi-vertical-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        .kpi-mini-card {
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 110px;
        }
        .light-mode .kpi-mini-card {
            background-color: rgba(0, 0, 0, 0.02);
        }

        .kpi-val {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
        }

        .kpi-title {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        /* Color classes */
        .seo-text { color: var(--seo-color); }
        .aeo-text { color: var(--aeo-color); }
        .success-text { color: var(--success-color); }
        .warning-text { color: var(--warning-color); }
        .danger-text { color: var(--danger-color); }

        /* Asset Table / List Section */
        .assets-section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .search-filter-bar {
            display: flex;
            gap: 1rem;
            flex-grow: 1;
            max-width: 600px;
        }

        .search-input {
            width: 100%;
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            font-family: inherit;
            font-size: 0.95rem;
            outline: none;
            transition: var(--transition);
        }

        .search-input:focus {
            border-color: var(--text-secondary);
            box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.05);
        }

        .filter-buttons {
            display: flex;
            gap: 0.5rem;
        }

        .filter-btn {
            background-color: var(--surface-color);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
            padding: 0.6rem 1rem;
            border-radius: 10px;
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .filter-btn:hover {
            color: var(--text-primary);
            background-color: var(--surface-hover);
        }

        .filter-btn.active {
            color: #ffffff !important;
            background: var(--primary-glow);
            border-color: transparent;
        }

        /* Asset List (Accordions) */
        .asset-list {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .asset-row {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            overflow: hidden;
            transition: var(--transition);
        }

        .asset-summary {
            padding: 1.25rem 2rem;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr auto;
            align-items: center;
            cursor: pointer;
            user-select: none;
            gap: 1rem;
        }

        @media (max-width: 768px) {
            .asset-summary {
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }
        }

        .asset-summary:hover {
            background-color: var(--surface-hover);
        }

        .asset-name {
            font-weight: 600;
            font-size: 1.05rem;
            word-break: break-all;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .score-pill-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .score-pill {
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 50px;
        }

        .score-pill.seo-bg {
            background-color: rgba(139, 92, 246, 0.15);
            color: var(--seo-color);
        }

        .score-pill.aeo-bg {
            background-color: rgba(6, 182, 212, 0.15);
            color: var(--aeo-color);
        }

        .status-badge {
            padding: 0.35rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: inline-block;
            text-align: center;
            width: fit-content;
        }

        .status-badge.pass {
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--success-color);
        }

        .status-badge.warning {
            background-color: rgba(245, 158, 11, 0.15);
            color: var(--warning-color);
        }

        .status-badge.error {
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--danger-color);
        }

        .chevron-icon {
            color: var(--text-muted);
            transition: transform 0.3s;
            font-size: 1.25rem;
            font-weight: bold;
        }

        .asset-row.expanded .chevron-icon {
            transform: rotate(180deg);
        }

        /* Accordion Expanded Detail Body */
        .asset-details {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s cubic-bezier(0, 1, 0, 1);
            border-top: 0px solid var(--border-color);
            background-color: rgba(255, 255, 255, 0.01);
        }
        .light-mode .asset-details {
            background-color: rgba(0, 0, 0, 0.01);
        }

        .asset-row.expanded .asset-details {
            max-height: 2000px;
            transition: max-height 0.6s ease-in-out;
            border-top: 1px solid var(--border-color);
        }

        .details-wrapper {
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .details-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        @media (max-width: 900px) {
            .details-grid {
                grid-template-columns: 1fr;
            }
        }

        .details-column h3 {
            font-size: 1.1rem;
            margin-bottom: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .metric-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .metric-item {
            background-color: rgba(255,255,255,0.015);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .light-mode .metric-item {
            background-color: rgba(0,0,0,0.01);
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .metric-name {
            font-weight: 600;
            font-size: 0.95rem;
        }

        .metric-message {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .metric-data-dump {
            font-family: 'JetBrains Mono', monospace;
            background-color: rgba(0, 0, 0, 0.2);
            color: #10b981;
            padding: 0.5rem 0.75rem;
            border-radius: 8px;
            font-size: 0.8rem;
            word-break: break-all;
            white-space: pre-wrap;
            max-height: 120px;
            overflow-y: auto;
            margin-top: 0.25rem;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }
        .light-mode .metric-data-dump {
            background-color: #f1f5f9;
            color: #0f766e;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        .recommendation-list {
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }

        .recommendation-item {
            display: flex;
            gap: 0.75rem;
            background-color: rgba(245, 158, 11, 0.03);
            border: 1px solid rgba(245, 158, 11, 0.15);
            border-left: 4px solid var(--warning-color);
            padding: 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
        }

        .recommendation-item .rec-bullet {
            color: var(--warning-color);
            font-weight: bold;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 3rem 0;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.85rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    </style>
</head>
<body>

<div class="dashboard-container">
    
    <header>
        <div class="header-title">
            <h1 id="brand-title">SEO & AEO Audit Executive Summary</h1>
            <p>Interactive analysis of client digital assets for AI Answer Engines & Traditional Search</p>
        </div>
        <div class="header-controls">
            <button class="btn" onclick="toggleTheme()">
                <span id="theme-icon">🔆</span> Theme
            </button>
            <button class="btn" onclick="exportData()">
                📥 Export JSON
            </button>
        </div>
    </header>

    <main style="display: flex; flex-direction: column; gap: 2.5rem;">
        
        <!-- Score and KPI Panel -->
        <section class="overview-grid">
            
            <div class="card score-card">
                <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                    <div class="score-gauge">
                        <svg>
                            <circle class="bg-circle" cx="70" cy="70" r="58"></circle>
                            <circle class="progress-circle seo-gauge-color" id="overall-seo-circle" cx="70" cy="70" r="58" stroke-dasharray="364.4" stroke-dashoffset="364.4"></circle>
                        </svg>
                        <div class="gauge-text" id="overall-seo-text">0</div>
                    </div>
                    <div class="score-info" style="margin-top: 1rem;">
                        <span class="score-label">Overall SEO</span>
                        <span class="score-val-title seo-text">Traditional</span>
                    </div>
                </div>

                <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                    <div class="score-gauge">
                        <svg>
                            <circle class="bg-circle" cx="70" cy="70" r="58"></circle>
                            <circle class="progress-circle aeo-gauge-color" id="overall-aeo-circle" cx="70" cy="70" r="58" stroke-dasharray="364.4" stroke-dashoffset="364.4"></circle>
                        </svg>
                        <div class="gauge-text" id="overall-aeo-text">0</div>
                    </div>
                    <div class="score-info" style="margin-top: 1rem;">
                        <span class="score-label">Overall AEO</span>
                        <span class="score-val-title aeo-text">AI Search</span>
                    </div>
                </div>
            </div>

            <div class="card kpi-vertical-grid" style="grid-column: span 2;">
                <div class="kpi-mini-card">
                    <span class="kpi-title">Audited Assets</span>
                    <span class="kpi-val" id="kpi-assets">0</span>
                </div>
                <div class="kpi-mini-card">
                    <span class="kpi-title">Critical Errors</span>
                    <span class="kpi-val danger-text" id="kpi-errors">0</span>
                </div>
                <div class="kpi-mini-card">
                    <span class="kpi-title">Optimization Warnings</span>
                    <span class="kpi-val warning-text" id="kpi-warnings">0</span>
                </div>
                <div class="kpi-mini-card">
                    <span class="kpi-title">Clean & Fully Optimized</span>
                    <span class="kpi-val success-text" id="kpi-clean">0</span>
                </div>
            </div>

        </section>

        <!-- Asset Search and Filter Panel -->
        <section class="assets-section">
            
            <div class="assets-section-header">
                <div class="search-filter-bar">
                    <input type="text" class="search-input" id="search-box" placeholder="Search audited assets by file path or URL..." oninput="renderAssets()">
                </div>
                
                <div class="filter-buttons">
                    <button class="filter-btn active" id="filter-all" onclick="setFilter('all')">All</button>
                    <button class="filter-btn" id="filter-errors" onclick="setFilter('errors')">Errors</button>
                    <button class="filter-btn" id="filter-warnings" onclick="setFilter('warnings')">Warnings</button>
                    <button class="filter-btn" id="filter-optimized" onclick="setFilter('optimized')">Optimized</button>
                </div>
            </div>

            <!-- List of Audited Items -->
            <div class="asset-list" id="asset-list-container">
                <!-- Rows injected dynamically by JS -->
            </div>

        </section>

    </main>

    <footer>
        <div>SEO/AEO Audit Agent Skill — Automated Report Dashboard</div>
        <div>Generated by Antigravity AI</div>
    </footer>

</div>

<script>
    // Injected Data
    const auditData = __AUDIT_DATA_PLACEHOLDER__;

    let activeFilter = 'all';

    function toggleTheme() {
        document.body.classList.toggle('light-mode');
        const icon = document.body.classList.contains('light-mode') ? '🌙' : '🔆';
        document.getElementById('theme-icon').textContent = icon;
    }

    function exportData() {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(jsonStringify(auditData));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", "seo_aeo_audit_report.json");
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    }

    function jsonStringify(obj) {
        return JSON.stringify(obj, null, 2);
    }

    function calculateOverallScores() {
        if (auditData.length === 0) return { seo: 0, aeo: 0 };
        let totalSeo = 0;
        let totalAeo = 0;
        auditData.forEach(item => {
            totalSeo += item.seo_score || 0;
            totalAeo += item.aeo_score || 0;
        });
        return {
            seo: Math.round(totalSeo / auditData.length),
            aeo: Math.round(totalAeo / auditData.length)
        };
    }

    function updateGauges() {
        const scores = calculateOverallScores();
        
        // Update texts
        document.getElementById('overall-seo-text').innerText = scores.seo;
        document.getElementById('overall-aeo-text').innerText = scores.aeo;
        
        // Update SVG circle strokes
        // Radius of circle is 58. Circumference is 2 * PI * r = 364.42
        const circumference = 364.4;
        
        const seoOffset = circumference - (scores.seo / 100) * circumference;
        const aeoOffset = circumference - (scores.aeo / 100) * circumference;
        
        document.getElementById('overall-seo-circle').style.strokeDashoffset = seoOffset;
        document.getElementById('overall-aeo-circle').style.strokeDashoffset = aeoOffset;
    }

    function updateKPIs() {
        document.getElementById('kpi-assets').innerText = auditData.length;
        
        let errors = 0;
        let warnings = 0;
        let clean = 0;
        
        auditData.forEach(item => {
            const worstStatus = getWorstStatus(item);
            if (worstStatus === 'error') errors++;
            else if (worstStatus === 'warning') warnings++;
            else clean++;
        });
        
        document.getElementById('kpi-errors').innerText = errors;
        document.getElementById('kpi-warnings').innerText = warnings;
        document.getElementById('kpi-clean').innerText = clean;
    }

    function getWorstStatus(item) {
        if (item.error) return 'error';
        let status = 'pass';
        if (item.metrics) {
            for (const key in item.metrics) {
                const metricStatus = item.metrics[key].status;
                if (metricStatus === 'error') return 'error';
                if (metricStatus === 'warning') status = 'warning';
            }
        }
        return status;
    }

    function setFilter(filterType) {
        activeFilter = filterType;
        
        // Toggle active button
        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById('filter-' + filterType).classList.add('active');
        
        renderAssets();
    }

    function toggleRow(rowId) {
        const row = document.getElementById(rowId);
        row.classList.toggle('expanded');
    }

    function renderAssets() {
        const container = document.getElementById('asset-list-container');
        container.innerHTML = '';
        
        const searchVal = document.getElementById('search-box').value.toLowerCase().strip ? document.getElementById('search-box').value.toLowerCase().trim() : document.getElementById('search-box').value.toLowerCase();
        
        let filtered = auditData.filter(item => {
            // Search filter
            const pathMatch = item.source.toLowerCase().includes(searchVal);
            if (!pathMatch) return false;
            
            // Status filter
            const status = getWorstStatus(item);
            if (activeFilter === 'errors' && status !== 'error') return false;
            if (activeFilter === 'warnings' && status !== 'warning') return false;
            if (activeFilter === 'optimized' && status !== 'pass') return false;
            
            return true;
        });

        if (filtered.length === 0) {
            container.innerHTML = `<div class="card" style="text-align: center; padding: 3rem; color: var(--text-secondary);">No assets match your search or filter filters.</div>`;
            return;
        }

        filtered.forEach((item, index) => {
            const worstStatus = getWorstStatus(item);
            const rowId = 'asset-row-' + index;
            
            // Create status badge
            let statusText = 'Optimized';
            if (worstStatus === 'error') statusText = 'Error';
            if (worstStatus === 'warning') statusText = 'Warning';
            
            const badgeClass = worstStatus;
            
            let metricsHtml = '';
            if (item.error) {
                metricsHtml = `<div class="recommendation-item" style="border-left-color: var(--danger-color); background-color: rgba(239, 68, 68, 0.03);">
                    <span class="danger-text" style="font-weight:bold;">CRAWL ERROR:</span> ${item.error}
                </div>`;
            } else {
                metricsHtml = renderDetailedMetrics(item);
            }

            const recsHtml = (item.recommendations && item.recommendations.length > 0) 
                ? item.recommendations.map(r => `
                    <div class="recommendation-item">
                        <span class="rec-bullet">⚠</span>
                        <div>${r}</div>
                    </div>
                `).join('') 
                : '<div class="success-text" style="font-weight: 600; padding: 1rem; border: 1px solid rgba(16,185,129,0.2); background-color: rgba(16,185,129,0.03); border-radius: 8px;">✓ This asset is fully optimized for search and AI engine queries!</div>';

            const html = `
                <div class="asset-row" id="${rowId}">
                    <div class="asset-summary" onclick="toggleRow('${rowId}')">
                        <div class="asset-name">
                            📄 ${item.source}
                        </div>
                        <div class="score-pill-container">
                            <span class="score-label" style="font-size:0.75rem;">SEO</span>
                            <span class="score-pill seo-bg">${item.error ? 0 : item.seo_score}</span>
                        </div>
                        <div class="score-pill-container">
                            <span class="score-label" style="font-size:0.75rem;">AEO</span>
                            <span class="score-pill aeo-bg">${item.error ? 0 : item.aeo_score}</span>
                        </div>
                        <div>
                            <span class="status-badge ${badgeClass}">${statusText}</span>
                        </div>
                        <div class="chevron-icon">▼</div>
                    </div>
                    <div class="asset-details">
                        <div class="details-wrapper">
                            <div class="details-grid">
                                <div class="details-column">
                                    <h3>🔍 Asset Audit Insights</h3>
                                    <div class="metric-list">
                                        ${metricsHtml}
                                    </div>
                                </div>
                                <div class="details-column">
                                    <h3>⚡ Targeted Recommendations</h3>
                                    <div class="recommendation-list">
                                        ${recsHtml}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += html;
        });
    }

    function renderDetailedMetrics(item) {
        if (!item.metrics) return '';
        let html = '';
        for (const [key, m] of Object.entries(item.metrics)) {
            const statusColor = m.status === 'pass' ? 'success-text' : (m.status === 'warning' ? 'warning-text' : 'danger-text');
            const statusSymbol = m.status === 'pass' ? '✓' : '⚠';
            
            let dataValue = '';
            if (m.text) {
                dataValue = `<div class="metric-data-dump">${escapeHtml(m.text)}</div>`;
            } else if (m.types) {
                dataValue = `<div class="metric-data-dump">Detected Schema: ${escapeHtml(m.types.join(', ') || 'None')}</div>`;
            } else if (m.errors && m.errors.length > 0) {
                dataValue = `<div class="metric-data-dump danger-text">Schema Errors:\\n${escapeHtml(m.errors.join('\\n'))}</div>`;
            } else if (m.errors) {
                dataValue = `<div class="metric-data-dump">None</div>`;
            }

            html += `
                <div class="metric-item">
                    <div class="metric-header">
                        <span class="metric-name" style="text-transform: capitalize;">${key.replace(/_/g, ' ')}</span>
                        <span class="${statusColor}" style="font-weight: 700;">${statusSymbol} ${m.status.toUpperCase()}</span>
                    </div>
                    <span class="metric-message">${m.message || ''}</span>
                    ${dataValue}
                </div>
            `;
        }
        return html;
    }

    function escapeHtml(text) {
        if (!text) return '';
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Init
    window.onload = function() {
        updateGauges();
        updateKPIs();
        renderAssets();
    }
</script>
</body>
</html>
"""

def generate_report(json_path, output_path):
    print(f"Reading audit data from: {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Inject JSON string into HTML
    json_str = json.dumps(data, indent=2)
    html_content = REPORT_HTML_TEMPLATE.replace("__AUDIT_DATA_PLACEHOLDER__", json_str)

    print(f"Writing executive dashboard report to: {output_path}")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Executive report generated successfully.")
    except Exception as e:
        print(f"Error writing HTML report: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Report builder dashboard compiler for SEO/AEO audits.")
    parser.add_argument("--input", default="audit_report.json", help="Path to input JSON findings file")
    parser.add_argument("--output", default="seo_aeo_audit_dashboard.html", help="Path to output HTML report dashboard")
    args = parser.parse_args()

    generate_report(args.input, args.output)

if __name__ == '__main__':
    main()
