# CareEZ Typography Specification

> Version 1.0.0 · 2026-05-25

---

## Font Stack

### Primary (System Sans-serif)
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
             Helvetica, Arial, sans-serif;
```
**Rationale:** Matches careez.org. Renders as SF Pro on Apple, Segoe UI on Windows, Roboto on Android/Chrome OS. Zero web-font latency — important for clinical workflow tools.

### Monospace / Code
```css
font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Consolas,
             'Liberation Mono', monospace;
```
Used for: API responses, JSON payloads, clinical identifiers, model output metadata.

### Web Font Option (future)
**Plus Jakarta Sans** (open license, Google Fonts) — closest geometric match to the system stack if a web font is ever adopted. Weights: 400, 600, 800, 900.

---

## Type Scale

### Display / Hero
| Class | Size | Weight | Line-height | Letter-spacing | Use |
|---|---|---|---|---|---|
| `.display-xl` | `clamp(52px, 8vw, 88px)` | 900 | 1.05 | -2px | Hero headline |
| `.display-lg` | `clamp(36px, 5vw, 56px)` | 900 | 1.1 | -1.5px | Section hero |

### Headings
| Class | Size | Weight | Line-height | Use |
|---|---|---|---|---|
| `h1` | `clamp(26px, 3.5vw, 36px)` | 800 | 1.2 | Section title |
| `h2` | `28px` | 800 | 1.25 | Subsection / card title |
| `h3` | `20px` | 700 | 1.3 | Card subheading |
| `h4` | `16px` | 700 | 1.4 | Label / grouped items |

### Body
| Class | Size | Weight | Line-height | Use |
|---|---|---|---|---|
| `.body-lg` | `16px` | 400 | 1.6 | Primary body copy |
| `.body-md` | `15px` | 400 | 1.6 | Card body, descriptions |
| `.body-sm` | `13px` | 400–500 | 1.5 | Captions, meta |
| `.body-xs` | `11px` | 500–700 | 1.4 | Tags, badges, labels |

### Navigation
| Element | Size | Weight |
|---|---|---|
| Nav brand | `20px` | 800 |
| Nav links | `13px` | 500 |

---

## Color Pairings for Type

| Context | Color | Hex |
|---|---|---|
| Primary text on dark | White | `#FFFFFF` |
| Body / secondary text on dark | Gray Light | `#B0BEC5` |
| Muted / meta text on dark | Gray Mid | `#78909C` |
| Interactive / accent text on dark | Cyan Primary | `#00E5FF` |
| Headings on light | Navy Deep | `#0A1428` |
| Links on light | Dark Cyan | `#0097A7` |
| Warning / alert text | Yellow | `#FFD43B` |

---

## Usage Rules

1. **Weight anchors**: Use 900 for hero, 800 for section heads, 700 for card heads, 400–500 for body. Don't use 300 (too light on dark backgrounds) or mix more than 3 weight levels per page.
2. **No italic in clinical data**: Reserve italics for blockquotes and UI hints, never in clinical text tables.
3. **Minimum body size**: 13px for any on-screen text. Never below 11px even for labels.
4. **Line-height**: Always ≥1.5 for paragraphs. ≥1.4 for labels. Never 1.0 for multi-word content.
5. **Letter-spacing**: Negative only for display-weight headings. Keep 0 for body. +0.05em for ALL-CAPS micro-labels.
