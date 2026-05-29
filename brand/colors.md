# CareEZ Color Palette

> Derived from `careez.org/index.html` CSS custom properties. Version 1.0.0 · 2026-05-25

---

## Brand Colors

| Token | Name | Hex | RGB | HSL | Role |
|---|---|---|---|---|---|
| `--navy` | Navy Deep | `#0A1428` | 10, 20, 40 | 220° 60% 10% | Primary background |
| `--navy2` | Navy Mid | `#0E1C3A` | 14, 28, 58 | 222° 61% 14% | Cards / secondary bg |
| `--navy3` | Navy Elevated | `#132046` | 19, 32, 70 | 226° 57% 17% | Elevated surfaces |
| `--cyan` | Cyan Primary | `#00E5FF` | 0, 229, 255 | 187° 100% 50% | Accent / CTA / links |
| `--cyan2` | Cyan Secondary | `#29B6F6` | 41, 182, 246 | 199° 91% 56% | Soft highlights |

## Neutrals

| Token | Name | Hex | RGB | HSL | Role |
|---|---|---|---|---|---|
| `--white` | White | `#FFFFFF` | 255, 255, 255 | 0° 0% 100% | Primary text on dark |
| `--gray` | Gray Light | `#B0BEC5` | 176, 190, 197 | 200° 13% 73% | Body text on dark |
| `--gray2` | Gray Mid | `#78909C` | 120, 144, 156 | 200° 13% 54% | Muted / secondary |
| `--gray3` | Gray Dark | `#455A64` | 69, 90, 100 | 199° 18% 33% | Borders / dividers |

## State Colors

| Token | Name | Hex | RGB | HSL |
|---|---|---|---|---|
| `--green` | Success | `#4CAF50` | 76, 175, 80 | 122° 39% 49% |
| `--yellow` | Warning | `#FFD43B` | 255, 212, 59 | 47° 100% 62% |
| `--orange` | Warning Alt | `#FFA726` | 255, 167, 38 | 36° 100% 57% |
| `--red` | Danger | `#EF5350` | 239, 83, 80 | 1° 83% 63% |

---

## Contrast Ratios (WCAG 2.1)

| Combo | Ratio | Level |
|---|---|---|
| White on Navy (`#FFFFFF` / `#0A1428`) | 18.1:1 | AAA |
| Gray on Navy (`#B0BEC5` / `#0A1428`) | 7.2:1 | AAA |
| Cyan on Navy (`#00E5FF` / `#0A1428`) | 12.4:1 | AAA (large text) |
| Gray2 on Navy (`#78909C` / `#0A1428`) | 4.1:1 | AA |

> **Warning:** Cyan (`#00E5FF`) on white yields only 1.3:1 — **never use as text on light backgrounds.** Use `#0097A7` (dark cyan) for text on white.

---

## Usage Rules

1. **Dark-first**: CareEZ is a dark-theme product. Default backgrounds are `#0A1428`.
2. **Cyan = action**: Cyan is reserved for interactive elements, highlights, and the EZ monogram. Don't use it decoratively everywhere.
3. **No gradient logos**: The cyan→cyan2 gradient is for accent bars and icons only. Wordmark text is flat.
4. **Yellow = clinical alert**: `#FFD43B` signals AI confidence warnings or clinical cautions. Don't use as decorative color.
