---
id: 020
title: System Handover and Launch Guide
stage: general
date_iso: 2026-06-16
surface: agent
model: gemini-1.5-pro
feature: none
branch: 006-frontend-nextjs
user: HP
command: none
labels: ["handover", "commands", "integration", "verification"]
links:
  spec: "specs/005-integration-testing/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/src/lib/api.ts
  - frontend/src/app/page.tsx
tests_yaml: []
---

# PROMPT_TEXT
mjhe fronetnd oer backend ko run krne ki commands bat do or ye bhi btao k sahi se proepr ackend kam kr rha he na fronetdn me nazr a rha he na

# RESPONSE_TEXT
I have provided the final step-by-step commands to run both the backend and frontend. I also confirmed that the "Noir Elite" frontend is logically integrated with the FastAPI backend, using correct endpoints for health, metrics, and ticket submission. The system is ready for live data display once the infrastructure is launched via Docker.
