# CareEZ Brand Kit

> Version 1.0.0 · 2026-05-25
> License: Free for any use referencing CareEZ / careez.org

---

## Contents

```
brand/
├── logo.svg                      Wordmark — white + cyan on transparent
├── logo-white.svg                Wordmark — white + cyan on navy background
├── logo-dark.svg                 Wordmark — navy + dark-cyan on white background
├── logo-icon.svg                 Monogram "Cz" icon, 200x200, for favicons / app icons
│
├── logo-512.png                  Logo raster, 512px wide, transparent bg
├── logo-1024.png                 Logo raster, 1024px wide, transparent bg
├── logo-white-1024.png           Logo raster, 1024px wide, white text, transparent bg
│
├── og-image-1200x630.png         OpenGraph / default social share image
├── social-twitter-1600x900.png   Twitter / X card
├── social-linkedin-1200x627.png  LinkedIn share image
├── social-wechat-1080x1080.png   WeChat Moments (square)
├── social-whatsapp-1080x1920.png WhatsApp Status (portrait)
│
├── templates/
│   ├── twitter-1600x900.html     Editable HTML source for Twitter card
│   ├── linkedin-1200x627.html    Editable HTML source for LinkedIn card
│   ├── wechat-1080x1080.html     Editable HTML source for WeChat card
│   └── whatsapp-1080x1920.html   Editable HTML source for WhatsApp card
│
├── colors.json                   Full color palette with hex/RGB/HSL/contrast
├── colors.md                     Human-readable color reference + usage rules
├── typography.md                 Type scale, font stack, pairing guide
└── export_pngs.py                Re-export all PNGs (Python + Chrome headless)
```

---

## Colors (Quick Reference)

| Token | Hex | Use |
|---|---|---|
| Navy Deep | `#0A1428` | Primary background |
| Navy Mid | `#0E1C3A` | Cards / secondary bg |
| Navy Elevated | `#132046` | Hover / elevated |
| Cyan | `#00E5FF` | Accent / "EZ" / CTAs |
| Cyan 2 | `#29B6F6` | Gradient endpoint |
| White | `#FFFFFF` | Primary text on dark |
| Gray | `#B0BEC5` | Body text on dark |
| Gray 2 | `#78909C` | Muted / meta |
| Success | `#4CAF50` | Positive states |
| Warning | `#FFD43B` | Clinical alerts |
| Danger | `#EF5350` | Error states |

See `colors.md` for contrast ratios and usage rules.

---

## Typography

- **Primary font stack:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`
- **Logo weight:** 900 (black) — "Care" in white, "EZ" in cyan
- **Headings:** weight 800–900
- **Body:** weight 400, size 15–16px, line-height 1.6

See `typography.md` for full scale.

---

## Generating / Updating PNGs

```bash
# From the brand/ directory:
python3 export_pngs.py
```

Requires: Python 3.9+ with Pillow, plus Google Chrome installed at
`/Applications/Google Chrome.app/` (for social card rendering).

---

## Customizing Social Cards

1. Open the relevant HTML file in `templates/`
2. Edit the text between `<!-- EDIT BELOW -->` and `<!-- EDIT ABOVE -->`
3. Render to PNG:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox \
  --window-size=1600,900 \
  --screenshot=social-twitter-custom.png \
  "file://$(pwd)/templates/twitter-1600x900.html"
```
Adjust `--window-size` to match the card dimensions.

---

## Usage Rules

1. **Dark-first**: CareEZ is a dark-theme product. Prefer navy backgrounds.
2. **Cyan = brand accent**: Use `#00E5FF` for the "EZ" wordmark, CTAs, and icon highlights only. Not for decorative fills.
3. **Don't recolor the logo**: The Care/EZ color split is fixed. Never use a single color for the full wordmark.
4. **Clear space**: Maintain at least 1× logo-height of clear space around the logo on all sides.
5. **Minimum size**: Do not render the wordmark below 120px wide. Use `logo-icon.svg` for smaller applications.
6. **Yellow = clinical alert**: `#FFD43B` signals AI confidence warnings or clinical cautions. Don't use decoratively.

---

## License

Free for any use referencing CareEZ — commercial, non-commercial, derivative works — provided the reference to CareEZ or careez.org is preserved. No attribution beyond the product name is required.

CareEZ is a trademark of CareEZ Ltd. The brand assets in this kit may not be used to impersonate or misrepresent CareEZ.
