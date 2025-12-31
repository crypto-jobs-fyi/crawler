# AI Jobs Viewer Specification

This document describes the features and technical requirements for the `jobs_viewer.html` frontend. It is designed to be used as a reference for regenerating or extending the viewer.

## Overview
The AI Jobs Viewer is a single-page application (SPA) that aggregates job listings from multiple JSON sources (Greenhouse, Ashby, and Lever) and provides a searchable, responsive interface for exploring opportunities.

## Core Features

### 1. Data Aggregation
- **Parallel Loading**: Fetches multiple JSON files simultaneously using `Promise.all`.
- **Sources**:
  - `ai_jobs_greenhouse_descriptions.json`
  - `ai_jobs_ashby_descriptions.json`
  - `ai_jobs_lever_descriptions.json`
- **Company Extraction**: Automatically parses the `link` field to extract company names:
  - Greenhouse: `greenhouse.io/{company}/...`
  - Ashby: `ashbyhq.com/{company}/...`
  - Lever: `lever.co/{company}/...`
- **Source Tagging**: Tracks the origin of each job (greenhouse, ashby, or lever).

### 2. User Interface
- **Responsive Grid**: 
  - Desktop: 3 columns.
  - Tablet: 2 columns.
  - Mobile: 1 column.
- **Job Cards**:
  - Displays Job Title, Location (with 📍 emoji), Salary (with 💰 emoji, if available), and a truncated Description (max 6 lines).
  - Features a prominent Company Badge with distinct styling.
  - Includes a "View Details & Apply" call-to-action.
- **Statistics Bar**: Displays real-time counts for:
  - Total Jobs
  - Unique Companies
  - Breakdown by Source (Greenhouse, Ashby, Lever)

### 3. Search & Filtering
- **Multi-Term Filtering**: Supports comma-separated queries for both Title and Description.
- **OR Logic**: If multiple terms are provided (e.g., "Engineer, Scientist"), the viewer shows jobs matching *any* of the terms.
- **Real-time Updates**: Filtering happens instantly as the user types.

### 4. Job Detail Modal
- **Centered Overlay**: Clicking a card opens a large, centered modal.
- **Full Description**: Displays the complete, un-truncated job description with preserved line breaks (`white-space: pre-wrap`).
- **Salary Info**: Displays extracted salary information prominently at the top of the description.
- **Backdrop**: Dims the background with a semi-transparent overlay to focus on the content.
- **Scrollable**: The modal content scrolls independently if the text exceeds the screen height.
- **Apply Button**: A direct link to the original job posting.

## Technical Implementation Details

### CSS Requirements
- **Layout**: Uses CSS Grid (`grid-template-columns: repeat(auto-fill, minmax(30%, 1fr))`).
- **Truncation**: Uses `-webkit-line-clamp: 6` for card descriptions.
- **Modal**: 
  - `position: fixed` for the overlay.
  - `max-height: 90vh` for the content box.
  - `overflow-y: auto` for scrolling.
- **Interactions**: `cursor: pointer` and `transform: translateY(-5px)` on card hover.

### JavaScript Requirements
- **State Management**: Maintains an `allJobs` array as the single source of truth.
- **Filtering Logic**:
  ```javascript
  const filtered = allJobs.filter(job => {
      const titleMatch = titleTerms.some(term => job.title.toLowerCase().includes(term));
      const descMatch = descTerms.some(term => job.description.toLowerCase().includes(term));
      return titleMatch && descMatch;
  });
  ```
- **DOM Manipulation**: Uses `document.createElement` and `innerHTML` for dynamic rendering.
- **Event Handling**: `input` listeners for filters and `onclick` for modal management.

## Regeneration Prompt for AI Agents
"Create a single-file HTML/JS/CSS job viewer that loads three JSON files (`ai_jobs_greenhouse_descriptions.json`, `ai_jobs_ashby_descriptions.json`, `ai_jobs_lever_descriptions.json`). The viewer should extract company names from the job links, display a responsive grid of cards with truncated descriptions, and feature a centered modal for full job details. Include a comma-separated filter for titles and descriptions, and a stats bar showing total jobs and unique companies."
