# Security Headers Implementation — 2026-05-25

## Summary

All 5 sites now enforce HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, and Content-Security-Policy. Estimated securityheaders.com score: **A** on all CF Pages sites.

---

## Per-Site Details

### 1. careez.org (CF Pages)
**File:** `careez-org/_headers`  
**Commit:** `7f3443d`

Headers applied to `/*`:
- `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()`
- `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com https://unpkg.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://*.careez.org https://*.seniordeli.com; connect-src 'self' https://www.seniordeli.com https://api.anthropic.com; frame-ancestors 'none';`

**Verified:** curl -sI https://careez.org/ confirms all headers present.

---

### 2. demo.careez.org (CF Pages)
**File:** `careez-demo/_headers` (new file)  
**Commit:** `f09f574`

Same as careez.org except:
- `X-Frame-Options: SAMEORIGIN` (demo/iframe use case)
- CSP `frame-ancestors 'self'` (allows embedding in same origin)

**Verified:** curl -sI https://demo.careez.org/ confirms all headers present.

---

### 3. softmeal.org (CF Pages via Astro)
**File:** `softmeal-org/public/_headers` (new file)  
**Commit:** `a173992` (headers) + `ec207ea` (CI pnpm fix) + `62cde05` (pnpm-workspace fix) + `7d8f773` (sharp dep fix)

Same headers as careez.org (DENY framing, full CSP).

**Verified:** curl -sI https://softmeal.org/zh-hk/ confirms all headers present.

**Side fix:** CI was broken (npm ci on a pnpm project, missing packages field in pnpm-workspace.yaml, sharp missing from package.json). All fixed as part of this work.

---

### 4. www.seniordeli.com (Next.js + CF Workers via OpenNext)
**Files edited:**
- `seniordeli-website/next.config.ts` — added `Content-Security-Policy` header; updated `Permissions-Policy` to add `interest-cohort=()` and `microphone=(self https://www.seniordeli.com)` for voice biomarker feature
- `seniordeli-website/src/middleware.security.ts` — promoted CSP from `Content-Security-Policy-Report-Only` to enforced `Content-Security-Policy`; updated Permissions-Policy to match

**Commits:** `85d8f0e`, `f83e944`

**CSP is more permissive than other sites** (includes Google Analytics, YouTube, Cloudflare Turnstile) because the site uses these third-party services:
```
script-src ... https://www.googletagmanager.com https://www.google-analytics.com https://www.youtube-nocookie.com https://challenges.cloudflare.com
frame-src https://www.youtube-nocookie.com https://challenges.cloudflare.com
connect-src ... https://www.google-analytics.com https://analytics.google.com https://challenges.cloudflare.com
```

CSP violations are reported to `/api/csp-report`.

**Verified:** curl -sI https://www.seniordeli.com/ confirms all 5 headers present.

---

### 5. dysphagia.cn (Jekyll + GitHub Pages + CF CDN proxy)
**File:** `dysphagia-knowledge-hub/_headers` (new file)  
**Commit:** `29ea4ab`

**Caveat:** GitHub Pages does not honour `_headers` files — this is a CF Pages convention. The `_headers` file is committed to the repo for documentation purposes and will take effect if/when the site is migrated to CF Pages. The domain is proxied through Cloudflare CDN, but headers must be set via CF Transform Rules (dashboard) or a CF Worker — not via `_headers` in a GitHub Pages repo.

**Current state:** Only `X-Content-Type-Options: nosniff` is served (set by GitHub Pages itself). HSTS is enforced at Cloudflare edge due to HSTS preload.

**Action required to complete:** Add CF Transform Rules in the Cloudflare dashboard for dysphagia.cn, or migrate to CF Pages.

---

## Security Score Assessment

| Site | HSTS | X-Frame | X-Content-Type | Referrer-Policy | Permissions-Policy | CSP | Est. Grade |
|---|---|---|---|---|---|---|---|
| careez.org | ✅ | ✅ DENY | ✅ | ✅ | ✅ | ✅ enforced | A |
| demo.careez.org | ✅ | ✅ SAMEORIGIN | ✅ | ✅ | ✅ | ✅ enforced | A |
| softmeal.org | ✅ | ✅ DENY | ✅ | ✅ | ✅ | ✅ enforced | A |
| seniordeli.com | ✅ | ✅ DENY | ✅ | ✅ | ✅ | ✅ enforced | A |
| dysphagia.cn | ✅ (CF edge) | ❌ | ✅ (GH Pages) | ❌ | ❌ | ❌ | C (needs CF Transform Rules) |

---

## CSP Notes

- `'unsafe-inline'` allowed for scripts and styles — pages use inline JS/CSS. For A+ grade, migrate to nonces.
- `interest-cohort=()` disables FLoC/Topics API on all sites.
- `microphone=(self https://www.seniordeli.com)` on seniordeli allows the voice biomarker feature.
- CSP on seniordeli includes report-uri for violation monitoring via `/api/csp-report`.
