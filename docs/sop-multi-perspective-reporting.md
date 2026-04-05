# SOP-IV-MPR-001: Multi-Perspective Reporting

**Version:** 1.0
**Date:** 2026-04-05
**Scope:** Commerce domain (applicable to client engagements across organs)
**Lifecycle Stage:** ABSORB (proven on Sovereign Systems engagement, 2026-03-20 to 2026-04-04)
**Provenance:** Extracted from `organvm-iii-ergon/sovereign-systems--elevate-align/docs/process-extraction/2026-04-04-reusable-processes.md`

> Analyzing the same data from multiple viewpoints and presenting each to its intended audience as a standalone document.

---

## 1. When This Protocol Applies

Four invariant conditions, all of which must hold:

| # | Condition | Negative Test (does NOT apply) |
|---|-----------|-------------------------------|
| 1 | A dataset exists that serves multiple audiences | Data serves a single audience with a single perspective |
| 2 | Audiences have different vocabulary, detail needs, and decision surfaces | All stakeholders share the same context and technical depth |
| 3 | Each audience should receive a standalone document (not a filtered view of one master doc) | A single comprehensive report with audience-tagged sections suffices |
| 4 | The underlying data is stable enough to generate consistent reports | Data is in active flux and reports would be immediately stale |

If conditions 1-2 hold but 3 does not, produce a single report with clearly marked audience sections.
If condition 4 fails, defer reporting until the data stabilizes (e.g., until Xenograft Phase 6 coverage is proved).

---

## 2. Protocol Phases

```
SHARED DATA SOURCE (atom registry, metrics, analysis)
    |
    +-- Phase 1: SELECT          Choose applicable report types and audiences
    +-- Phase 2: LENS            Define the inclusion/exclusion lens per report
    +-- Phase 3: GENERATE        Produce each report from shared data through its lens
    +-- Phase 4: REVIEW          Internal cross-check for audience appropriateness
    +-- Phase 5: DELIVER         Send to audiences, track delivery
```

### Phase 1: SELECT

**Purpose:** Determine which report types are needed for this engagement and identify the audience for each.

**Invariant steps:**
1. Evaluate the 4-report template against the engagement:

   | # | Report Type | Audience | When Applicable |
   |---|-------------|----------|-----------------|
   | 1 | Executive Summary | Stakeholders, board, partners | Engagement has decision-makers beyond the primary client |
   | 2 | Client Report | The client | Always — the client should see their own content analyzed |
   | 3 | Technical Audit | Build team, developers | Engagement includes technical implementation |
   | 4 | System Health | Operations, maintenance | Engagement produces an ongoing system requiring monitoring |

2. For each selected report, identify:
   - Primary audience (who receives it)
   - Secondary audience (who might also read it)
   - Decision surface (what decisions this report enables)
   - Vocabulary level (executive, practitioner, technical, operational)
3. Not all 4 reports are required for every engagement. Select only those that serve a real audience.
4. Record selections in the reporting plan

**Outputs:** Reporting plan with selected types, audiences, and decision surfaces

**Ledger emission:** `reports_selected` with `{report_types, audience_count}`

### Phase 2: LENS

**Purpose:** For each report type, define precisely what data to include, exclude, and how to frame it. The SAME underlying data feeds all reports; the lens determines what each audience sees.

**Invariant steps:**
1. For each selected report, define the lens:

   **Executive Summary lens:**
   - Include: top-line metrics, strategic findings, decision points, timeline
   - Exclude: technical details, individual atoms, implementation specifics
   - Vocabulary: business language, strategic framing, outcome-oriented
   - Detail level: summary only — one page if possible, never more than three
   - Decision surface: approve/defer/redirect

   **Client Report lens:**
   - Include: their content analyzed and organized, IP inventory highlights, editorial items, what was found and what it means for them
   - Exclude: system architecture, internal process details, technical debt
   - Vocabulary: the client's own language reflected back, accessible, warm-professional
   - Detail level: comprehensive but readable — this is their mirror
   - Decision surface: content decisions, priority choices, direction confirmation

   **Technical Audit lens:**
   - Include: architecture assessment, dependency analysis, implementation complexity, technology stack evaluation, risk items
   - Exclude: client content details, editorial decisions, strategic framing
   - Vocabulary: technical, precise, implementation-oriented
   - Detail level: detailed — the build team needs specifics
   - Decision surface: technical approach, resource allocation, risk mitigation

   **System Health lens:**
   - Include: operational metrics, coverage statistics, process health, pipeline status, atom counts and distributions
   - Exclude: content meaning, strategic interpretation, client-facing framing
   - Vocabulary: operational, metric-driven, status-oriented
   - Detail level: dashboard-style — metrics, counts, percentages, trends
   - Decision surface: resource allocation, maintenance scheduling, process improvement

2. For each lens, explicitly state what must NOT appear:
   - Client Report must not contain internal process critique
   - Executive Summary must not contain technical jargon
   - Technical Audit must not contain client personal content
   - System Health must not contain strategic opinions
3. Document the lens definitions in the reporting plan

**Lens invariant:** The same fact may appear in multiple reports but framed differently for each audience. A 91% agreement rate is a "strong validation" in the Executive Summary, a "91% inter-model agreement across 1,821 atoms" in the Technical Audit, and a "verification: PASS" in System Health.

**Outputs:** Lens definitions per report type

**Ledger emission:** `lenses_defined` with `{report_count, exclusion_rules_count}`

### Phase 3: GENERATE

**Purpose:** Produce each report from the shared data using its specific lens. Each report must stand alone.

**Invariant steps:**
1. For each selected report type, generate the document:
   - Draw only from the shared data source (atom registry, metrics, analysis results)
   - Apply the lens: include only what the lens specifies, exclude what it prohibits
   - Use the vocabulary level defined for this audience
   - Frame findings for the audience's decision surface
2. Each report must be self-contained:
   - A reader should understand the report without having read any other report
   - No references like "as detailed in the Technical Audit" — if it matters, include it
   - Context that the audience needs must be provided within the report
3. Structure each report with:
   - Summary/TL;DR at the top (2-3 sentences)
   - Key findings (bulleted, scannable)
   - Detailed sections (organized by the audience's mental model)
   - Recommendations or next steps (audience-appropriate actions)
   - Appendix (supporting data, only if the audience would use it)
4. Apply the engagement-specific data:
   - Atom counts, SIGNAL/CONTEXT/NOISE distribution
   - IP inventory highlights (Client Report)
   - Editorial flag summary (Client Report)
   - Architecture assessment (Technical Audit)
   - Process metrics (System Health)

**Generation invariant:** No report is a subset of another report. Each is written for its audience from scratch, drawing from the same well.

**Outputs:** Complete report set (2-4 documents)

**Ledger emission:** `reports_generated` with `{report_count, total_words, total_pages}`

### Phase 4: REVIEW

**Purpose:** Internal cross-check to ensure each report serves its audience and no inappropriate content leaks between reports.

**Invariant steps:**
1. For each report, verify against its lens:
   - Does the report include everything the lens specifies?
   - Does the report exclude everything the lens prohibits?
   - Is the vocabulary appropriate for the audience?
   - Does the report stand alone without requiring other reports?
2. Cross-report leak check:
   - Scan each report for content that belongs in a different report
   - Technical jargon in the Executive Summary = leak
   - Internal process critique in the Client Report = leak
   - Client personal content in the Technical Audit = leak
   - Strategic opinions in the System Health report = leak
3. Consistency check:
   - Do the reports agree on facts? (Same atom count, same coverage percentage)
   - Do the framings conflict? (One report cannot say "strong results" while another says "concerning gaps" about the same data)
4. If leaks or inconsistencies are found, revise the affected report(s)

**Outputs:** Reviewed and approved report set

**Ledger emission:** `reports_reviewed` with `{leaks_found, leaks_fixed, consistency_issues}`

### Phase 5: DELIVER

**Purpose:** Send each report to its intended audience and track delivery.

**Invariant steps:**
1. For each report, deliver to the primary audience:
   - Record: report type, recipient, delivery method, delivery date
   - Format: Markdown by default; PDF if the audience requires it
2. For secondary audiences, deliver if appropriate:
   - The client may also receive the Executive Summary
   - The build team may receive the Client Report for context (if the client approves)
3. Track delivery in the engagement log:
   ```yaml
   deliveries:
     - report: executive_summary
       recipient: "Stakeholder group"
       method: email
       date: 2026-04-03
       acknowledged: true
     - report: client_report
       recipient: "Maddie"
       method: shared_drive
       date: 2026-04-03
       acknowledged: true
       reaction: "#3 & #5 made me actually lol lmao that's crazyyyyy"
   ```
4. If a recipient requests changes to their report, loop back to Phase 3 for that report only

**Outputs:** Delivery log

**Ledger emission:** `reports_delivered` with `{delivered_count, acknowledged_count, revision_requests}`

---

## 3. Outputs

| Phase | Primary Output | Format | Audience |
|-------|---------------|--------|----------|
| SELECT | Reporting plan | YAML | Internal |
| LENS | Lens definitions per report | Markdown | Internal |
| GENERATE | Complete report set (2-4 documents) | Markdown | Audience-specific |
| REVIEW | Reviewed and approved reports | Markdown | Internal |
| DELIVER | Delivery log | YAML | Internal |

---

## 4. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Reports contradict each other on facts | Phase 4 consistency check | Trace to shared data source; one report has a stale or incorrect reference. Fix at the source. |
| Client report contains technical jargon | Phase 4 leak check | Rewrite affected sections using client vocabulary. The client's own language is the gold standard. |
| Executive summary exceeds 3 pages | Phase 3 length check | Compress. If it cannot be compressed, the engagement may need two executive documents (overview + details). |
| Audience does not acknowledge receipt | Phase 5 tracking | Follow up once. If no response, log as "delivered, unacknowledged" and proceed. |
| Client requests a report type not in the template | Phase 1 selection | Add a custom lens definition for the requested audience. The 4-report template is a starting point, not a ceiling. |
| Same data interpreted differently across reports | Phase 4 review | This is expected and correct — different audiences need different framings. Only flag if the interpretations are contradictory, not merely different. |

---

## 5. Relationship to Existing SOPs

| SOP | Relationship | Integration Point |
|-----|-------------|-------------------|
| SOP-IV-CPP-001 (Content-to-Product Pipeline) | Parent pipeline | Reporting is invoked during CPP Phase 5 |
| SOP-IV-XGR-001 (Xenograft Protocol) | Upstream producer | Atom registry and coverage data are the shared data source |
| SOP-IV-ETP-001 (Editorial Triage Protocol) | Data contributor | Editorial flag summary appears in the Client Report |
| SOP-IV-CIP-001 (Client IP Identification) | Data contributor | IP inventory highlights appear in the Client Report |
| `essay-publishing-and-distribution` | Related pattern | Essay publication uses a single-audience model; this SOP is multi-audience |
| `system-dashboard-telemetry` | Related pattern | System Health report mirrors dashboard telemetry but as a snapshot document |
| `dynamic-lens-assembly` | Conceptual prior | The lens metaphor originates in dynamic lens assembly; this SOP applies it to reports |

---

## 6. Protocol Governance

- **Owner:** ORGAN-IV (Taxis)
- **Primary domain:** ORGAN-III (Ergon) client engagements; extensible to any multi-audience reporting need
- **Invocable by:** Any organ producing analysis that serves multiple audiences
- **Versioning:** SemVer. New report types increment minor. Changes to the lens model or review process increment major.
- **Review cadence:** After every 3rd engagement, review whether the 4-report template still covers all recurring audience types. Add new templates only when a pattern recurs.
- **Sovereign Systems instance:** 4 reports generated (Executive Summary, Client Report, Technical Audit, System Health). Client reaction to receiving these: "#3 & #5 made me actually lol lmao that's crazyyyyy this is amazing I knew I had a lot of info but had no idea." This validates the multi-perspective approach — the same data, seen through different lenses, creates different forms of value.
