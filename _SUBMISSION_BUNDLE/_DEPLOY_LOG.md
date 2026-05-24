# careez-org Deploy Log

## 2026-05-25 HKT — Cloudflare Web Analytics + RUM enabled

**Task:** Enable CF Web Analytics + Real User Monitoring on careez.org, demo.careez.org, softmeal.org.

**Method:** Two-layer approach:
1. CF Pages project `build_config.web_analytics_tag` set to `"auto"` via API (account `2c4fde...`) — CF edge-injects beacon on every response.
2. Beacon script tag also injected manually into `<head>` of each site's HTML as belt-and-suspenders fallback.

**CF Pages project IDs:**
- `careez-org` → `2b7b4567-5101-4809-8bb0-367e320740e8` (careez.org, www.careez.org)
- `careez-demo` → `74f6e270-1640-4726-8955-f93c511d6252` (demo.careez.org)
- `softmeal-org` → `bb43ec2f-66ef-4af2-91fd-3f8d2f5223e9` (softmeal.org)

**Site tags:** Using `"auto"` token (CF Pages auto-provisioned). To get explicit RUM site_tag UUIDs: CF dashboard → each Pages project → Web Analytics → copy token. Replace `"auto"` in HTML `<head>` with the real UUID.

**Token permission note:** The token at `~/.raymond/cloudflare.env` has CF Pages scope only. CF RUM API (`/rum/site_info`) requires `Account Analytics:Edit` permission. Current token cannot create explicit RUM sites via API. CF Pages `"auto"` mode handles this at the edge.

**Files changed:**
- `careez-org/index.html` — beacon added to `<head>` (line ~791)
- `careez-demo/index.html` — beacon added to `<head>` (line 8)
- `softmeal-org/src/layouts/BaseLayout.astro` — beacon added to `<head>` (line ~217)

**Verification post-deploy:**
- careez.org: `curl https://careez.org/ | grep cloudflareinsights` → 1+ match ✅ (CF edge injection live)
- demo.careez.org: pending fresh deploy
- softmeal.org: pending fresh deploy (Astro build required)

## 2026-05-25 01:05 HKT — seniordeli.com/[locale]/careez full landing page

**Task:** Replace rename-banner stub at seniordeli.com/en/careez with a full CareEZ landing page for judges.

**Repo:** `rayc0/seniordeli-website` (Next.js + next-intl, CF Pages)

**Files changed:**
- `src/app/[locale]/careez/page.tsx` — full replacement (rename-banner gone)
- `messages/en.json` / `zh-HK.json` / `zh-CN.json` — CareEZPage namespace updated

**Sections added:**
1. Hero: "Multimodal clinical AI for dysphagia / 照護食 standard adoption. Built on HKCSS 護食標準 + IDDSI." + dual CTAs (Try Live → /api docs, Visit careez.org)
2. Live demo widget (inline): text classifier + image upload + voice aspiration screen — calls /api/iddsi-classify, /api/iddsi-classify-image, /api/voice-aspiration-screen
3. Why CareEZ — 3 pillars: Multilingual (Cantonese/English/Tagalog/Bahasa), Clinical Safety Bias (over-refer), Governance Inversion (HKU + s.88 Full Linkage)
4. Live endpoints panel: 3 API URLs with curl examples + JSON-LD SoftwareApplication schema
5. Linked resources footer: careez.org, demo.careez.org, softmeal.org, dysphagia.cn

**Commits:**
- `41765bc` feat(careez): replace rename-banner stub with full CareEZ landing page
- `7b6e1a7` i18n(ja): add CareEZPage translations to unblock build (concurrent session)
- `af3101c` fix(careez): replace JSX event handlers with vanilla-JS DOMContentLoaded wiring (concurrent session — Server Component constraint fix)

**GH Actions run:** https://github.com/rayc0/seniordeli-website/actions/runs/26367336086
**Status:** ✅ Cloudflare Pages Deploy success (4m20s)

**Verification (2026-05-25 01:05 HKT):**
```
curl -s https://seniordeli.com/en/careez | grep -c "Multimodal clinical AI" → 5 ✅
HKCSS 護食標準: ✅
IDDSI: ✅
iddsi-classify endpoint in page: ✅
voice-aspiration-screen in page: ✅
careez.org external link: ✅
softmeal.org / dysphagia.cn: ✅
Clinical Safety Bias pillar: ✅
```

## 2026-05-25 01:01 HKT — /status/ page deployed

**Task:** Public status page at careez.org/status/ showing live ping status of all 4 CareEZ API endpoints.

**Approach chosen:** Client-side pings + GitHub Actions server-side cron (hybrid). Skipped CF Worker/KV — token `cfut_b6f8i...` has Pages scope only (no Workers/KV API access). Achieved equivalent functionality via:

1. **status/index.html** — 4-card dashboard, pure static. JS pings all endpoints every 30s from browser (CORS-aware), stores 24h history in localStorage, renders green/yellow/red badges with latency, uptime %, 48-check sparkbar, per-card "Test now" button.
2. **status/data.json** — Overwritten every 5min by GitHub Actions cron (`status-check.yml`). Server-side curl pings each endpoint, writes structured JSON. Page also fetches this on load and merges into history, so historical data survives browser refreshes.
3. **index.html** — "Status" nav link added.

**Commit:** `f4d97a8`  
**GH Actions run:** https://github.com/rayc0/careez-org/actions/runs/26367342383  
**Status:** ✅ Success (deploy ~25s)

**Verification (2026-05-25 01:01 HKT):**
```
curl -sI https://careez.org/status/ → HTTP/2 200 ✅
curl -s https://careez.org/status/data.json | python3 -m json.tool → 4-endpoint object ✅
```

**Note on CF Worker:** Token lacks Workers/KV scope. If a CF cron Worker is preferred later, it needs token `cfut_XHyDl...` (stored on MBA M1/M5, not Mac Mini M4). The GH Actions cron achieves the same 5-min ping cadence and is live now.

## 2026-05-25 01:00 HKT — Email Routing setup attempt (BLOCKED — token scope)

**Task:** Configure Cloudflare Email Routing: hello@careez.org → rayc00210@gmail.com

**Blocker:** The token in `~/.raymond/cloudflare.env` on Mac Mini M4 (`cfut_b6f8i...`, token ID `0cd6b84b...`) is valid but has ZERO zone access — no zones returned, authentication error on all careez.org zone endpoints including Email Routing. This token was the OLD PQSafe token, not the CAREEZ token.

**The CAREEZ token** (`cfut_XHyDl...`) is stored in `~/.zshrc.local` on MBA M1/M5 (user `tun`), not synced to Mac Mini M4. MBA was unreachable via LAN SSH during this session.

**Current DNS state (verified):**
- careez.org: No MX records, No TXT/SPF records → Email Routing NOT enabled
- Zone: active (CF nameservers marek + zelda confirmed)
- Pages: careez-org.pages.dev live, https://careez.org serving ✅

**To complete email routing — Raymond must do ONE of:**

Option A (recommended — 5 min via dashboard):
1. Go to dash.cloudflare.com → careez.org → Email → Email Routing → Get Started
2. Add destination: rayc00210@gmail.com (click verification email from CF)
3. Add rule: hello@careez.org → Forward to → rayc00210@gmail.com
4. Add catch-all: *@careez.org → Forward to → rayc00210@gmail.com (priority 100)

Option B (API — 10 min, requires token with Email Routing scope):
1. Go to dash.cloudflare.com → My Profile → API Tokens
2. Edit token `d58fc1b94a462fe250f00cee04661267` (CAREEZ token) OR create new token
3. Add scope: Zone → Email Routing → Edit (for careez.org zone)
4. Save token to `~/.raymond/cloudflare.env` on Mac Mini M4
5. Then re-run this task

**IMPORTANT:** After enabling Email Routing, Raymond must click the verification email Cloudflare sends to rayc00210@gmail.com to activate the destination address. Agent cannot click verification links.

## 2026-05-25 00:37 HKT — GitHub Actions deploy (workflow_dispatch)

**Commits deployed:**
- `baebe30` ci: switch to pages-action@v1
- `89e5dd2` feat: add Try CareEZ Live interactive widget
- `36bbd0e` fix(cloudflare): remove catch-all redirect (SEO)
- `a16f84f` (HKCSS polish — already in main)

**Run:** https://github.com/rayc0/careez-org/actions/runs/26366795756  
**Status:** ✅ Success (25s)

**Fix applied:** Added missing `CLOUDFLARE_API_TOKEN` secret to rayc0/careez-org repo (token `cfut_XHyDl...` — Pages + Workers Edit scope, still active).

**Verification (curl at 2026-05-25 00:37 HKT):**
```
HTTP/2 200
date: Sun, 24 May 2026 16:37:31 GMT
content-type: text/html; charset=utf-8

grep "Try CareEZ Live": 3 matches ✅
grep "iddsi-classify": 4 matches ✅
grep "護食標準": 16 matches ✅
/llms.txt: serving correctly ✅
```
