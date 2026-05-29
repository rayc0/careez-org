# CareEZ API — Multilingual cURL Examples

> **Base URL:** `https://www.seniordeli.com`  
> **Auth:** None required  
> **CORS:** `Access-Control-Allow-Origin: *`  
> **Disclaimer:** Prototype classifiers — outputs are decision-support tools only. Clinical decisions require a qualified Speech-Language Pathologist (SLP).

---

## Table of Contents

1. [POST /api/iddsi-classify — Text IDDSI Classification (9 languages)](#1-post-apiiddsi-classify)
2. [POST /api/voice-aspiration-screen — Aspiration Risk Screening (4 languages)](#2-post-apivoice-aspiration-screen)
3. [POST /api/iddsi-classify-image — Image IDDSI Classification (multipart + base64)](#3-post-apiiddsi-classify-image)
4. [POST /api/iddsi-batch — Batch Meal Validation](#4-post-apiiddsi-batch)
5. [POST /api/clinical-qa — Clinical Q&A RAG](#5-post-apiclinical-qa)
6. [Expected Output Snippets](#6-expected-output-snippets)

---

## 1. POST /api/iddsi-classify

Classify a food or liquid from a plain-text description. Returns IDDSI Level 0–7, confidence score, and multilingual explanation.

### English (en)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "thick congee, soft, no lumps",
    "language": "en"
  }'
```

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.87,
  "explanation_en": "This food item matches IDDSI Level 4 (Extremely Thick / Puréed). It can be eaten with a spoon and does not require chewing.",
  "explanation_zh_hant": "此食物符合IDDSI第4級（極稠/糊狀）。可用匙羹進食，無需咀嚼。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Traditional Chinese / Cantonese (zh-HK)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "免治豬肉，質地柔軟，有少量小粒，加醬汁保濕",
    "language": "zh-HK"
  }'
```

**Expected output:**
```json
{
  "iddsi_level": 5,
  "label": "Minced & Moist",
  "confidence": 0.91,
  "explanation_en": "Minced pork with sauce matches IDDSI Level 5 (Minced & Moist). Particles are small enough to be manageable without chewing.",
  "explanation_zh_hant": "免治豬肉符合IDDSI第5級（免治及濕潤）。顆粒細小，毋須咀嚼亦可吞嚥。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Simplified Chinese (zh-CN)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "嫩豆腐，极软，无颗粒，入口即化，蒸熟后切小块",
    "language": "zh-CN"
  }'
```

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.85,
  "explanation_en": "Silken tofu that melts in the mouth matches IDDSI Level 4 (Puréed). Smooth with no lumps.",
  "explanation_zh_hant": "嫩豆腐入口即化，符合IDDSI第4級（糊狀）。質地均勻，無顆粒。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Japanese (ja)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "やわらかく煮た豆腐、なめらか、固まりなし、スプーンでつぶせる",
    "language": "en"
  }'
```

> **Note:** The `language` field controls the response language, not the input language. Japanese text input is supported regardless of the `language` field value.

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.83,
  "explanation_en": "Soft cooked tofu that can be mashed with a spoon matches IDDSI Level 4 (Puréed).",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Filipino / Tagalog (tl)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "malambot na kanin, walang butil na matigas, makatas at malapot, kinain ng kutsara",
    "language": "tl"
  }'
```

> Translation: "Soft rice, no hard grains, moist and thick, eaten with a spoon"

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.82,
  "explanation_en": "Soft, moist rice without hard grains matches IDDSI Level 4 (Extremely Thick / Puréed).",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Bahasa Indonesia (id)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "bubur nasi yang kental, lembut, tidak ada gumpalan, dimakan dengan sendok",
    "language": "id"
  }'
```

> Translation: "Thick rice porridge, soft, no lumps, eaten with a spoon"

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.86,
  "explanation_en": "Thick rice porridge with no lumps matches IDDSI Level 4 (Extremely Thick / Puréed).",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Vietnamese (vi)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "cháo đặc, mềm, không có cục, ăn bằng thìa",
    "language": "vi"
  }'
```

> Translation: "Thick congee, soft, no lumps, eaten with a spoon"

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.84,
  "explanation_en": "Thick congee with no lumps matches IDDSI Level 4 (Extremely Thick / Puréed).",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Thai (th)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "โจ๊กข้าวข้น นุ่มมาก ไม่มีก้อน รับประทานด้วยช้อน",
    "language": "th"
  }'
```

> Translation: "Thick rice congee, very soft, no lumps, eaten with a spoon"

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.85,
  "explanation_en": "Thick rice congee with no lumps matches IDDSI Level 4 (Extremely Thick / Puréed).",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Spanish (es)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "text": "puré de patata espeso, suave, sin grumos, se come con cuchara",
    "language": "es"
  }'
```

> Translation: "Thick mashed potato, smooth, no lumps, eaten with a spoon"

**Expected output:**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.88,
  "explanation_en": "Thick smooth mashed potato with no lumps matches IDDSI Level 4 (Extremely Thick / Puréed).",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

## 2. POST /api/voice-aspiration-screen

Screen for aspiration risk from reported swallowing symptoms. Returns risk level (low/moderate/high), score 0–100, and clinical recommendation.

### English (en)

```bash
curl -s -X POST "https://www.seniordeli.com/api/voice-aspiration-screen" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "symptoms": "Patient coughs frequently during meals, has a wet/gurgly voice after swallowing, and has lost 3kg in the past month.",
    "age": 82,
    "diagnosis": "stroke",
    "language": "en"
  }'
```

**Expected output:**
```json
{
  "risk_level": "high",
  "risk_score": 78,
  "flags": ["wet/gurgly voice", "coughing during meals", "significant weight loss"],
  "recommendation_en": "High aspiration risk detected. Refer to a Speech-Language Pathologist for formal swallowing assessment immediately. Consider NPO (nil per os) pending evaluation.",
  "recommendation_zh_hant": "發現高度誤嚥風險。請立即轉介言語治療師進行正式吞嚥評估。評估前考慮禁食（NPO）。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Traditional Chinese / Cantonese (zh-HK)

```bash
curl -s -X POST "https://www.seniordeli.com/api/voice-aspiration-screen" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "symptoms": "病人進食時經常咳嗽，吞嚥後聲音濕潤沙啞，最近一個月體重減少2公斤，有時進食後出現發燒情況。",
    "age": 78,
    "diagnosis": "柏金遜症",
    "language": "zh-HK"
  }'
```

> Translation: "Patient coughs frequently during meals, wet/hoarse voice after swallowing, lost 2kg in past month, sometimes develops fever after eating."

**Expected output:**
```json
{
  "risk_level": "high",
  "risk_score": 74,
  "flags": ["wet voice post-swallow", "coughing during meals", "weight loss", "post-prandial fever"],
  "recommendation_en": "High aspiration risk. Immediate SLP referral recommended.",
  "recommendation_zh_hant": "高度誤嚥風險。建議立即轉介言語治療師進行正式評估。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Filipino / Tagalog (tl)

```bash
curl -s -X POST "https://www.seniordeli.com/api/voice-aspiration-screen" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "symptoms": "Ang pasyente ay umuubo habang kumakain, may basa at paos na boses pagkatapos lumunok, at gumagaan ng 2kg sa nakaraang buwan.",
    "age": 75,
    "language": "tl"
  }'
```

> Translation: "The patient coughs while eating, has a wet/hoarse voice after swallowing, and has lost 2kg in the past month."

**Expected output:**
```json
{
  "risk_level": "high",
  "risk_score": 71,
  "flags": ["coughing during meals", "wet voice post-swallow", "weight loss"],
  "recommendation_en": "High aspiration risk. Refer to a Speech-Language Pathologist immediately.",
  "recommendation_zh_hant": "高度誤嚥風險。請立即轉介言語治療師。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

### Bahasa Indonesia (id)

```bash
curl -s -X POST "https://www.seniordeli.com/api/voice-aspiration-screen" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "symptoms": "Pasien sering batuk saat makan, suara basah setelah menelan, berat badan turun 3kg dalam sebulan terakhir, dan sesekali tersedak.",
    "age": 80,
    "diagnosis": "stroke",
    "language": "id"
  }'
```

> Translation: "Patient often coughs while eating, wet voice after swallowing, lost 3kg in past month, and occasionally chokes."

**Expected output:**
```json
{
  "risk_level": "high",
  "risk_score": 80,
  "flags": ["wet voice post-swallow", "coughing during meals", "choking episodes", "significant weight loss"],
  "recommendation_en": "High aspiration risk. Immediate SLP referral and consider NPO pending evaluation.",
  "recommendation_zh_hant": "高度誤嚥風險。建議即時轉介言語治療師，並考慮在評估期間禁食。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

## 3. POST /api/iddsi-classify-image

Upload a photo for visual IDDSI classification. Accepts `multipart/form-data` with JPEG, PNG, or WebP (max 10 MB).

### Method A: Multipart File Upload (recommended)

```bash
# Replace /path/to/food_photo.jpg with your actual file path
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -F "image=@/path/to/food_photo.jpg;type=image/jpeg" \
  -F "language=en"
```

For PNG:
```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -F "image=@/path/to/pureed_soup.png;type=image/png" \
  -F "language=zh-HK"
```

For WebP:
```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -F "image=@/path/to/thickened_drink.webp;type=image/webp" \
  -F "language=tl"
```

---

### Method B: Base64-encoded Image (alternative)

Some clients prefer sending images as base64 within a JSON body. Use this pattern if multipart is not supported by your HTTP client:

```bash
# Step 1: Encode your image to base64
IMAGE_B64=$(base64 -i /path/to/food_photo.jpg)

# Step 2: Send as JSON with base64 field
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d "{
    \"image_base64\": \"${IMAGE_B64}\",
    \"image_type\": \"image/jpeg\",
    \"language\": \"en\"
  }"
```

> **Note:** The base64 method may not be supported in all API versions. Check the current OpenAPI spec at `https://careez.org/api-docs/openapi.yaml`. The multipart method (Method A) is the canonical approach.

---

### 4-Language Explanation Requests

The `language` field controls the language of the explanation returned. Examples for all four primary RCHE languages:

**English (en):**
```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Origin: https://careez.org" \
  -F "image=@food.jpg;type=image/jpeg" \
  -F "language=en"
```

**Traditional Chinese / Cantonese (zh-HK):**
```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Origin: https://careez.org" \
  -F "image=@food.jpg;type=image/jpeg" \
  -F "language=zh-HK"
# → explanation_zh_hant will be the primary explanation
```

**Filipino / Tagalog (tl):**
```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Origin: https://careez.org" \
  -F "image=@food.jpg;type=image/jpeg" \
  -F "language=tl"
```

**Bahasa Indonesia (id):**
```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-classify-image" \
  -H "Origin: https://careez.org" \
  -F "image=@food.jpg;type=image/jpeg" \
  -F "language=id"
```

**Image classification expected output (pureed soup):**
```json
{
  "iddsi_level": 4,
  "label": "Extremely Thick / Puréed",
  "confidence": 0.79,
  "explanation_en": "Visual analysis indicates a smooth, homogeneous purée consistent with IDDSI Level 4. No visible lumps or particulates detected.",
  "explanation_zh_hant": "視覺分析顯示質地均勻，符合IDDSI第4級（糊狀）。未見可見顆粒。",
  "warning": "Prototype rule-based classifier — clinical decisions require qualified SLP"
}
```

---

## 4. POST /api/iddsi-batch

Validate a full RCHE meal plan (up to 20 items) against a resident's prescribed IDDSI level. Uses Claude Haiku for AI-powered per-item classification.

### English (en)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-batch" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "meal": [
      { "item": "steamed fish", "portion": "100g" },
      { "item": "rice porridge (congee)", "portion": "200ml" },
      { "item": "minced pork with sauce", "portion": "80g" },
      { "item": "plain water", "portion": "150ml" }
    ],
    "resident_iddsi_level": 5,
    "language": "en"
  }'
```

### Traditional Chinese (zh-HK)

```bash
curl -s -X POST "https://www.seniordeli.com/api/iddsi-batch" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "meal": [
      { "item": "蒸魚", "portion": "100克" },
      { "item": "白粥", "portion": "200毫升" },
      { "item": "免治豬肉加醬汁", "portion": "80克" },
      { "item": "清水", "portion": "150毫升" }
    ],
    "resident_iddsi_level": 5,
    "language": "zh-HK"
  }'
```

**Expected output (excerpt):**
```json
{
  "meal_safety_verdict": "unsafe",
  "non_matching_items": [
    { "item": "steamed fish", "iddsi_level": 6, "label": "Soft & Bite-Sized" }
  ],
  "recommendations": "steamed fish (Level 6): Mince finely and moisten with sauce or gravy to meet Level 5 (Minced & Moist).",
  "resident_iddsi_level": 5,
  "resident_iddsi_label": "Minced & Moist",
  "model": "claude-haiku-4-5-20251001"
}
```

---

## 5. POST /api/clinical-qa

RAG endpoint for dysphagia/IDDSI clinical questions. Searches 120 softmeal.org articles.

### English

```bash
curl -s -X POST "https://www.seniordeli.com/api/clinical-qa" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "question": "What is IDDSI Level 4 and what foods are appropriate for it?",
    "language": "en",
    "top_k": 5
  }'
```

### Traditional Chinese (zh-HK)

```bash
curl -s -X POST "https://www.seniordeli.com/api/clinical-qa" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org" \
  -d '{
    "question": "IDDSI 第4級食物有什麼特點？適合什麼類型嘅病人？",
    "language": "zh-HK",
    "top_k": 3
  }'
```

### Health check (GET)

```bash
curl -s "https://www.seniordeli.com/api/clinical-qa" \
  -H "Accept: application/json" \
  -H "Origin: https://careez.org"
```

**Health check expected output:**
```json
{
  "status": "ok",
  "index_size": 120,
  "embedding_model": "text-embedding-3-small",
  "answer_model": "claude-haiku-4-5"
}
```

---

## 6. Expected Output Snippets

### IDDSI Level Reference

| Level | Label | Type | Color |
|-------|-------|------|-------|
| 0 | Thin | Drink | `#0077B6` |
| 1 | Slightly Thick | Drink | `#00B4D8` |
| 2 | Mildly Thick | Drink | `#90E0EF` |
| 3 | Moderately Thick / Liquidised | Drink / Food | `#CAF0F8` |
| 4 | Extremely Thick / Puréed | Drink / Food | `#E06027` |
| 5 | Minced & Moist | Food | `#F4A261` |
| 6 | Soft & Bite-Sized | Food | `#64B4E1` |
| 7 | Regular | Food | `#2EC4B6` |

### Aspiration Risk Levels

| Risk Level | Score Range | Recommended Action |
|------------|-------------|-------------------|
| `low` | 0–30 | Monitor; maintain current diet |
| `moderate` | 31–59 | Review diet texture; consider SLP referral |
| `high` | 60–100 | Immediate SLP referral; consider NPO pending evaluation |

### Common Error Responses

**400 — Missing required field:**
```json
{
  "error": "invalid_request",
  "message": "The 'text' field is required and must be at least 3 characters."
}
```

**413 — Image too large (image endpoint only):**
```json
{
  "error": "payload_too_large",
  "message": "Image exceeds 10 MB size limit. Please compress or resize the image."
}
```

**501 — Research-staged endpoint (audio only):**
```json
{
  "error": "not_implemented",
  "message": "Audio classification endpoint is research-staged and not yet live."
}
```

**503 — Anthropic API not configured (batch endpoint only):**
```json
{
  "error": "service_unavailable",
  "message": "Anthropic API key not configured on this server."
}
```

---

## Tips for Developers

1. **Always include `Origin` header** — confirms CORS is working and helps server-side analytics.
2. **Use `jq` for pretty-printing**: append `| jq '.'` to any curl command.
3. **Test connectivity first** with the health check: `curl -s "https://www.seniordeli.com/api/clinical-qa" | jq '.'`
4. **Image uploads**: For liquids, photograph in a transparent container from the side for better classification accuracy.
5. **Batch endpoint timeout**: Allow up to 30 seconds for `/api/iddsi-batch` — it makes a live LLM call.
6. **No API key needed** for any endpoint — open access for demo and research use.

---

*Generated by CareEZ AI | Carewells Limited (Hong Kong SED-registered) | hello@careez.org | https://careez.org*
