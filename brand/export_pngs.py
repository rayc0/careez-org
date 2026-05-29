#!/usr/bin/env python3
"""
CareEZ Brand Kit — PNG Export Script
Uses Pillow for logo PNGs and Chrome headless for social cards.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BRAND_DIR = Path(__file__).parent.resolve()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Colors
NAVY    = (10, 20, 40, 255)
CYAN    = (0, 229, 255, 255)
CYAN2   = (41, 182, 246, 255)
WHITE   = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

def chrome_capture(html_path: str, out_path: str, width: int, height: int):
    """Render an HTML file to PNG via Chrome headless."""
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={out_path}",
        f"file://{html_path}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"  Chrome stderr: {result.stderr[:300]}")
    return result.returncode == 0


def export_logo_pngs():
    """Export logo PNGs using Pillow (draw directly — no SVG renderer needed)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not available — skipping logo PNGs")
        return

    def draw_logo(width, height, bg_color, text_color, accent_color, bg_opaque=False):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        if bg_opaque:
            img.paste(Image.new("RGBA", (width, height), bg_color), (0, 0))
        draw = ImageDraw.Draw(img)

        # Scale factor
        sf = width / 512

        # Draw "C" bracket (simplified as thick arc-ish lines)
        # Left bracket: 3 lines forming C shape
        lx, ly = int(20 * sf), int(15 * sf)
        bw = int(80 * sf)
        bh = int(70 * sf)
        thick = max(3, int(8 * sf))
        cy_center = ly + bh // 2

        # Draw bracket arms
        draw.line([(lx + bw//3, ly), (lx + bw//2, ly)], fill=accent_color, width=thick)
        draw.line([(lx, ly), (lx, ly + bh)], fill=accent_color, width=thick)
        draw.line([(lx + bw//3, ly + bh), (lx + bw//2, ly + bh)], fill=accent_color, width=thick)

        # Checkmark inside
        ck_x = lx + int(15 * sf)
        ck_y = cy_center - int(5 * sf)
        ck_size = int(20 * sf)
        draw.line([(ck_x, ck_y), (ck_x + ck_size//2, ck_y + ck_size//2)], fill=accent_color, width=max(2, thick//2))
        draw.line([(ck_x + ck_size//2, ck_y + ck_size//2), (ck_x + ck_size + int(10*sf), ck_y - ck_size//3)], fill=accent_color, width=max(2, thick//2))

        # Wordmark text
        tx = int(110 * sf)
        ty = int(10 * sf)
        fs = int(60 * sf)

        # Try to get a font, fall back to default
        try:
            font_care = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", fs)
            font_ez   = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", fs)
        except Exception:
            try:
                font_care = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", fs)
                font_ez   = font_care
            except Exception:
                font_care = ImageFont.load_default()
                font_ez   = font_care

        draw.text((tx, ty), "Care", fill=text_color, font=font_care)
        # Measure "Care" width
        try:
            care_w = int(draw.textlength("Care", font=font_care))
        except Exception:
            care_w = int(fs * 2.8)

        draw.text((tx + care_w, ty), "EZ", fill=accent_color, font=font_ez)

        # Accent underline
        ul_y = ty + int(fs * 1.15)
        ul_h = max(2, int(4 * sf))
        ul_w = int((width - tx) * 0.85)
        draw.rectangle([tx, ul_y, tx + ul_w, ul_y + ul_h], fill=accent_color + (153,) if len(accent_color) == 3 else accent_color)

        return img

    # logo-512.png — transparent background
    print("Exporting logo-512.png...")
    img = draw_logo(512, 128, NAVY, WHITE, CYAN)
    img.save(str(BRAND_DIR / "logo-512.png"))

    # logo-1024.png — transparent background
    print("Exporting logo-1024.png...")
    img = draw_logo(1024, 256, NAVY, WHITE, CYAN)
    img.save(str(BRAND_DIR / "logo-1024.png"))

    # logo-white-1024.png — white text on transparent
    print("Exporting logo-white-1024.png...")
    img = draw_logo(1024, 256, NAVY, WHITE, CYAN)
    img.save(str(BRAND_DIR / "logo-white-1024.png"))

    print("  Logo PNGs done.")


def render_social_card(html_content: str, out_path: str, width: int, height: int, label: str):
    """Write HTML to temp file, render with Chrome, save PNG."""
    print(f"Rendering {label} ({width}x{height})...")
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as f:
        f.write(html_content)
        tmp = f.name
    try:
        ok = chrome_capture(tmp, out_path, width, height)
        if ok and Path(out_path).exists():
            print(f"  Saved: {out_path}")
        else:
            print(f"  Failed: {out_path}")
    finally:
        os.unlink(tmp)


CARD_BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background: #0A1428;
  color: #FFFFFF;
  overflow: hidden;
}
.logo-text { font-weight: 900; }
.care { color: #FFFFFF; }
.ez   { color: #00E5FF; }
.tagline { color: #B0BEC5; font-weight: 400; }
.accent-bar { background: linear-gradient(90deg, #00E5FF, #29B6F6); border-radius: 2px; }
.domain { color: #00E5FF; font-weight: 600; letter-spacing: 0.02em; }
.badge {
  display: inline-block;
  background: rgba(0,229,255,0.12);
  border: 1px solid rgba(0,229,255,0.3);
  color: #00E5FF;
  border-radius: 20px;
  font-size: inherit;
  font-weight: 600;
  padding: 0.25em 0.75em;
}
"""

def make_twitter_card():
    # 1600x900
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{CARD_BASE_CSS}
body {{ width: 1600px; height: 900px; }}
.card {{
  width: 1600px; height: 900px;
  display: flex; flex-direction: column;
  justify-content: center; align-items: flex-start;
  padding: 100px 120px;
  background: linear-gradient(135deg, #0A1428 0%, #0E1C3A 60%, #132046 100%);
  position: relative;
}}
.card::before {{
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(0,229,255,0.06) 0%, transparent 70%);
  border-radius: 50%;
}}
.logo-wrap {{ display: flex; align-items: center; gap: 28px; margin-bottom: 40px; }}
.logo-icon {{
  width: 90px; height: 90px;
  border: 5px solid #00E5FF;
  border-right: none;
  border-radius: 8px 0 0 8px;
  display: flex; align-items: center; justify-content: center;
  position: relative;
}}
.logo-text {{ font-size: 80px; line-height: 1; }}
.accent-bar {{ width: 180px; height: 5px; margin-bottom: 48px; }}
.tagline {{ font-size: 44px; line-height: 1.35; max-width: 900px; margin-bottom: 60px; }}
.meta {{ display: flex; gap: 28px; align-items: center; }}
.domain {{ font-size: 28px; }}
.badge {{ font-size: 24px; }}
</style></head>
<body>
<div class="card">
  <div class="logo-wrap">
    <div class="logo-text"><span class="care">Care</span><span class="ez">EZ</span></div>
  </div>
  <div class="accent-bar"></div>
  <div class="tagline">Multimodal Clinical AI<br>for <strong style="color:#fff">Dysphagia</strong></div>
  <div class="meta">
    <span class="domain">careez.org</span>
    <span class="badge">Beta · Free Access</span>
    <span class="badge">CE/FDA Pathway</span>
  </div>
</div>
</body></html>"""
    render_social_card(html, str(BRAND_DIR / "social-twitter-1600x900.png"), 1600, 900, "Twitter card")


def make_linkedin_card():
    # 1200x627
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{CARD_BASE_CSS}
body {{ width: 1200px; height: 627px; }}
.card {{
  width: 1200px; height: 627px;
  display: flex; flex-direction: column;
  justify-content: center; align-items: flex-start;
  padding: 70px 90px;
  background: linear-gradient(135deg, #0A1428 0%, #0E1C3A 70%, #132046 100%);
  position: relative;
}}
.card::after {{
  content: '';
  position: absolute;
  bottom: 0; right: 0;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(0,229,255,0.05) 0%, transparent 70%);
}}
.logo-text {{ font-size: 64px; line-height: 1; margin-bottom: 24px; }}
.accent-bar {{ width: 140px; height: 4px; margin-bottom: 36px; }}
.tagline {{ font-size: 32px; line-height: 1.4; max-width: 700px; margin-bottom: 40px; }}
.meta {{ display: flex; gap: 20px; align-items: center; flex-wrap: wrap; }}
.domain {{ font-size: 22px; }}
.badge {{ font-size: 18px; }}
</style></head>
<body>
<div class="card">
  <div class="logo-text"><span class="care">Care</span><span class="ez">EZ</span></div>
  <div class="accent-bar"></div>
  <div class="tagline">Multimodal Clinical AI for <strong style="color:#fff">Dysphagia</strong></div>
  <div class="meta">
    <span class="domain">careez.org</span>
    <span class="badge">AI · VFSS · FEES · Clinical NLP</span>
  </div>
</div>
</body></html>"""
    render_social_card(html, str(BRAND_DIR / "social-linkedin-1200x627.png"), 1200, 627, "LinkedIn card")


def make_wechat_card():
    # 1080x1080
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{CARD_BASE_CSS}
body {{ width: 1080px; height: 1080px; }}
.card {{
  width: 1080px; height: 1080px;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  text-align: center;
  padding: 80px;
  background: radial-gradient(ellipse at center, #0E1C3A 0%, #0A1428 70%);
  position: relative;
}}
.card::before {{
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(0,229,255,0.04) 0%, transparent 70%);
  border-radius: 50%;
}}
.logo-icon-big {{
  width: 160px; height: 160px;
  border: 8px solid #00E5FF;
  border-right: none;
  border-radius: 16px 0 0 16px;
  margin: 0 auto 40px;
  display: flex; align-items: center; justify-content: center;
}}
.check {{ color: #00E5FF; font-size: 64px; font-weight: 900; }}
.logo-text {{ font-size: 96px; line-height: 1; margin-bottom: 24px; }}
.accent-bar {{ width: 200px; height: 5px; margin: 0 auto 48px; }}
.tagline {{ font-size: 38px; line-height: 1.5; margin-bottom: 60px; max-width: 800px; }}
.domain {{ font-size: 32px; margin-bottom: 20px; }}
.badge {{ font-size: 26px; }}
</style></head>
<body>
<div class="card">
  <div class="logo-icon-big"><span class="check">✓</span></div>
  <div class="logo-text"><span class="care">Care</span><span class="ez">EZ</span></div>
  <div class="accent-bar"></div>
  <div class="tagline">Multimodal Clinical AI<br>for <strong style="color:#fff">Dysphagia</strong></div>
  <div class="domain">careez.org</div>
  <div class="badge">AI-Powered · Free Beta Access</div>
</div>
</body></html>"""
    render_social_card(html, str(BRAND_DIR / "social-wechat-1080x1080.png"), 1080, 1080, "WeChat card")


def make_whatsapp_card():
    # 1080x1920
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{CARD_BASE_CSS}
body {{ width: 1080px; height: 1920px; }}
.card {{
  width: 1080px; height: 1920px;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  text-align: center;
  padding: 100px 80px;
  background: linear-gradient(180deg, #0A1428 0%, #0E1C3A 50%, #0A1428 100%);
  position: relative;
}}
.card::before {{
  content: '';
  position: absolute;
  top: 30%; left: 50%;
  transform: translate(-50%, -50%);
  width: 900px; height: 900px;
  background: radial-gradient(circle, rgba(0,229,255,0.05) 0%, transparent 70%);
  border-radius: 50%;
}}
.spacer {{ flex: 1; }}
.logo-icon-big {{
  width: 200px; height: 200px;
  border: 10px solid #00E5FF;
  border-right: none;
  border-radius: 20px 0 0 20px;
  margin: 0 auto 60px;
  display: flex; align-items: center; justify-content: center;
}}
.check {{ color: #00E5FF; font-size: 80px; font-weight: 900; }}
.logo-text {{ font-size: 130px; line-height: 1; margin-bottom: 36px; }}
.accent-bar {{ width: 280px; height: 7px; margin: 0 auto 70px; }}
.tagline {{ font-size: 52px; line-height: 1.5; margin-bottom: 80px; max-width: 900px; }}
.features {{
  display: flex; flex-direction: column; gap: 28px;
  margin-bottom: 80px;
}}
.feature-row {{ display: flex; gap: 24px; justify-content: center; flex-wrap: wrap; }}
.badge {{ font-size: 34px; }}
.domain {{ font-size: 44px; margin-top: 20px; }}
</style></head>
<body>
<div class="card">
  <div class="spacer"></div>
  <div class="logo-icon-big"><span class="check">✓</span></div>
  <div class="logo-text"><span class="care">Care</span><span class="ez">EZ</span></div>
  <div class="accent-bar"></div>
  <div class="tagline">Multimodal Clinical AI<br>for <strong style="color:#fff">Dysphagia</strong></div>
  <div class="features">
    <div class="feature-row">
      <span class="badge">VFSS Analysis</span>
      <span class="badge">FEES Review</span>
    </div>
    <div class="feature-row">
      <span class="badge">Clinical NLP</span>
      <span class="badge">Free Beta</span>
    </div>
  </div>
  <div class="domain">careez.org</div>
  <div class="spacer"></div>
</div>
</body></html>"""
    render_social_card(html, str(BRAND_DIR / "social-whatsapp-1080x1920.png"), 1080, 1920, "WhatsApp card")


def make_og_image():
    # 1200x630 OG image
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{CARD_BASE_CSS}
body {{ width: 1200px; height: 630px; }}
.card {{
  width: 1200px; height: 630px;
  display: flex; flex-direction: column;
  justify-content: center; align-items: flex-start;
  padding: 70px 90px;
  background: linear-gradient(135deg, #0A1428 0%, #0E1C3A 65%, #132046 100%);
  position: relative;
}}
.card::before {{
  content: '';
  position: absolute;
  top: -100px; right: -100px;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(0,229,255,0.07) 0%, transparent 70%);
  border-radius: 50%;
}}
.logo-text {{ font-size: 72px; line-height: 1; margin-bottom: 20px; }}
.accent-bar {{ width: 150px; height: 4px; margin-bottom: 36px; }}
.tagline {{ font-size: 34px; line-height: 1.45; max-width: 750px; margin-bottom: 44px; }}
.meta {{ display: flex; gap: 20px; align-items: center; }}
.domain {{ font-size: 24px; }}
.badge {{ font-size: 20px; }}
</style></head>
<body>
<div class="card">
  <div class="logo-text"><span class="care">Care</span><span class="ez">EZ</span></div>
  <div class="accent-bar"></div>
  <div class="tagline">Multimodal Clinical AI for <strong style="color:#fff">Dysphagia</strong></div>
  <div class="meta">
    <span class="domain">careez.org</span>
    <span class="badge">Free Beta · AI · VFSS · FEES</span>
  </div>
</div>
</body></html>"""
    render_social_card(html, str(BRAND_DIR / "og-image-1200x630.png"), 1200, 630, "OG image (1200x630)")


if __name__ == "__main__":
    print(f"CareEZ Brand Kit — PNG Export")
    print(f"Output dir: {BRAND_DIR}")
    print()

    export_logo_pngs()
    print()

    make_og_image()
    make_twitter_card()
    make_linkedin_card()
    make_wechat_card()
    make_whatsapp_card()

    print()
    print("Done. Files in brand/:")
    for f in sorted(BRAND_DIR.glob("*.png")):
        size = f.stat().st_size
        print(f"  {f.name:45s}  {size:>8,} bytes")
