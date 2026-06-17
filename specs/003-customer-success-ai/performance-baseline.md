# Performance Baseline — Phase 1 Prototype

**Date:** 2026-05-07
**Tickets tested:** 60

## Summary Metrics

| Metric | Achieved | Target | Pass? |
|--------|----------|--------|-------|
| Overall accuracy | 95.0% | >85% | ✅ |
| Avg response time | 1ms | <3000ms | ✅ |
| Correct escalation decisions | 100.0% | >90% | ✅ |

## Detailed Results

| ID | Channel | Expected | Actual | Latency | Pass |
|----|---------|----------|--------|---------|------|
| ticket_001 | email | answer | escalate | 2ms | ❌ |
| ticket_002 | email | answer | answer | 6ms | ✅ |
| ticket_003 | email | escalate | escalate | 0ms | ✅ |
| ticket_004 | whatsapp | answer | answer | 1ms | ✅ |
| ticket_005 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_006 | web_form | answer | escalate | 0ms | ❌ |
| ticket_007 | email | escalate | escalate | 0ms | ✅ |
| ticket_008 | email | escalate | escalate | 0ms | ✅ |
| ticket_009 | whatsapp | answer | answer | 0ms | ✅ |
| ticket_010 | web_form | answer | answer | 1ms | ✅ |
| ticket_011 | email | answer | answer | 0ms | ✅ |
| ticket_012 | email | escalate | escalate | 0ms | ✅ |
| ticket_013 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_014 | email | answer | answer | 1ms | ✅ |
| ticket_015 | email | answer | answer | 1ms | ✅ |
| ticket_016 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_017 | web_form | escalate | escalate | 0ms | ✅ |
| ticket_018 | email | answer | answer | 0ms | ✅ |
| ticket_019 | email | answer | answer | 1ms | ✅ |
| ticket_020 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_021 | email | answer | answer | 1ms | ✅ |
| ticket_022 | whatsapp | answer | answer | 1ms | ✅ |
| ticket_023 | web_form | escalate | escalate | 0ms | ✅ |
| ticket_024 | email | answer | answer | 1ms | ✅ |
| ticket_025 | email | answer | answer | 1ms | ✅ |
| ticket_026 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_027 | web_form | answer | answer | 1ms | ✅ |
| ticket_028 | email | answer | answer | 1ms | ✅ |
| ticket_029 | email | answer | answer | 1ms | ✅ |
| ticket_030 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_031 | web_form | answer | answer | 2ms | ✅ |
| ticket_032 | email | escalate | escalate | 0ms | ✅ |
| ticket_033 | email | answer | answer | 1ms | ✅ |
| ticket_034 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_035 | web_form | answer | answer | 1ms | ✅ |
| ticket_036 | email | escalate | escalate | 0ms | ✅ |
| ticket_037 | email | answer | answer | 1ms | ✅ |
| ticket_038 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_039 | web_form | answer | answer | 1ms | ✅ |
| ticket_040 | email | escalate | escalate | 0ms | ✅ |
| ticket_041 | email | escalate | escalate | 0ms | ✅ |
| ticket_042 | whatsapp | answer | answer | 0ms | ✅ |
| ticket_043 | web_form | escalate | escalate | 0ms | ✅ |
| ticket_044 | email | escalate | escalate | 0ms | ✅ |
| ticket_045 | email | answer | escalate | 0ms | ❌ |
| ticket_046 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_047 | web_form | answer | answer | 1ms | ✅ |
| ticket_048 | email | answer | answer | 1ms | ✅ |
| ticket_049 | email | answer | answer | 1ms | ✅ |
| ticket_050 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_051 | web_form | answer | answer | 2ms | ✅ |
| ticket_052 | email | escalate | escalate | 0ms | ✅ |
| ticket_053 | email | answer | answer | 1ms | ✅ |
| ticket_054 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_055 | web_form | answer | answer | 1ms | ✅ |
| ticket_056 | email | escalate | escalate | 0ms | ✅ |
| ticket_057 | email | answer | answer | 1ms | ✅ |
| ticket_058 | whatsapp | escalate | escalate | 0ms | ✅ |
| ticket_059 | web_form | escalate | escalate | 0ms | ✅ |
| ticket_060 | email | answer | answer | 0ms | ✅ |
