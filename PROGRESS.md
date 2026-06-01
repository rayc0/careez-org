# careez-org — Progress

<!-- This file is the AI-facing progress ledger. Claude updates it at the END of
     every dev session in this repo. The portfolio dashboard reads the fields below.
     Keep it short. Git activity (last commit) is detected automatically. -->

Updated: 2026-05-31
Health: 🟢
Percent: 65            <!-- M1 DONE (HKEX IFS submission 2026-05-26); M2 ~30-40% done -->
One-liner: CareEZ AI swallowing-safety platform for RCHE carers — 16+ pages live, HKEX IFS 2026 submitted 2026-05-26, M2 post-submission hardening in progress

## Next action
- Fix ARIA live region on safety banner "AI-Assisted Screening — Not Diagnostic" (~30 min, patient-safety priority, not cosmetic) — Raymond greenlight required before code change

## This week
- [x] M1 complete: 16+ HTML pages, CI/CD (GitHub Actions → Cloudflare Pages), SEO/AIO pass (llms.txt, agent.json, ai-plugin.json, hreflang, JSON-LD), PWA (sw.js, webmanifest, offline.html), HKEX IFS submission bundle assembled
- [x] SEO/AIO fixes: hreflang x-default/zh-Hans-HK, Twitter card, meta desc ≤160, JSON-LD WebPage schema on trial page
- [ ] ARIA live region fix (safety banner) — pending Raymond greenlight
- [ ] SLP cohort validation kick-off (n≥30 SLPs, HKD 20-40K, 60-90d) — κ=0.89 currently mock-set
- [ ] Redirect careforge.softmeal.org → careez.org + update seniordeli.com/careforge

## Blockers (needs Raymond)
- ARIA safety banner fix: greenlight to proceed (tagged 🔴 ASK in workbench)
- LOI templates for NGO RCHEs: careez-lane LOI distinct from kinaite commercial LOI? Decision pending
- Carewells Ltd SE bank account: confirm opened (target 2026-06-15)

<!-- COMMIT COUNT NOTE: git log shows 99 total commits but the majority (~76) are automated
     "chore: status check" entries from .github/workflows/status-check.yml (CI heartbeat).
     Meaningful feature commits (F-series SEO/AIO fixes, chore/sync pulls, merge) = ~10-12.
     The ROADMAP note that "only 1 commit showed" was likely from a shallow clone before the
     2026-05-30 sync that pulled all live CF Pages state into git. Working tree is fully built. -->
