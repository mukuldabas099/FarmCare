"""
download_hindi_fonts.py  (v2 — restructured paths)
===================================================
Run this ONCE inside your FarmCare_2 project folder:

    python3 download_hindi_fonts.py

What it does:
  1. Downloads NotoSans-Regular/Bold.ttf           (English/Latin/numbers)
  2. Downloads NotoSansDevanagari-Regular/Bold.ttf  (Hindi/Devanagari)
  3. Merges each pair → NotoMerged-Regular.ttf + NotoMerged-Bold.ttf
     These merged fonts contain BOTH English AND Hindi glyphs.
  4. Saves everything into the  fonts/  subfolder.

Requirements:
    pip3 install fonttools --break-system-packages
"""

import os, sys, urllib.request

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")   # ← save into fonts/ subfolder

# Create fonts/ if it doesn't exist
os.makedirs(FONTS_DIR, exist_ok=True)

FONT_URLS = {
    "NotoSans-Regular.ttf":
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
    "NotoSans-Bold.ttf":
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf",
    "NotoSansDevanagari-Regular.ttf":
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf",
    "NotoSansDevanagari-Bold.ttf":
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf",
}


def download(fname, url):
    dest = os.path.join(FONTS_DIR, fname)
    if os.path.exists(dest):
        print(f"  [skip] {fname} already exists in fonts/")
        return dest
    print(f"  [down] {fname} ...", end="", flush=True)
    try:
        urllib.request.urlretrieve(url, dest)
        print(f" done ({os.path.getsize(dest) // 1024} KB)")
        return dest
    except Exception as e:
        print(f"\n  FAILED: {e}")
        return None


def merge_fonts(latin, devanagari, out_name):
    out = os.path.join(FONTS_DIR, out_name)
    try:
        from fontTools.merge import Merger
        merged = Merger().merge([latin, devanagari])
        merged.save(out)
        print(f"  [merge] {out_name} → fonts/{out_name}  ({os.path.getsize(out) // 1024} KB)  OK")
        return True
    except ImportError:
        print("  fonttools not installed.")
        print("  Run:  pip3 install fonttools --break-system-packages")
        return False
    except Exception as e:
        print(f"  Merge error: {e}")
        return False


print("=" * 55)
print("  FarmCare Hindi Font Setup  (v2 — saves to fonts/)")
print("=" * 55)
print(f"  Target folder: {FONTS_DIR}")

print("\n[1] Downloading individual fonts into fonts/...")
paths = {}
for fname, url in FONT_URLS.items():
    p = download(fname, url)
    if not p:
        print("\nDownload failed. Check internet connection and retry.")
        sys.exit(1)
    paths[fname] = p

print("\n[2] Merging Latin + Devanagari into single font files...")
ok1 = merge_fonts(
    paths["NotoSans-Regular.ttf"],
    paths["NotoSansDevanagari-Regular.ttf"],
    "NotoMerged-Regular.ttf"
)
ok2 = merge_fonts(
    paths["NotoSans-Bold.ttf"],
    paths["NotoSansDevanagari-Bold.ttf"],
    "NotoMerged-Bold.ttf"
)

print()
if ok1 and ok2:
    print("✅  Done!  Both merged fonts saved to  fonts/")
    print()
    print("   fonts/NotoMerged-Regular.ttf")
    print("   fonts/NotoMerged-Bold.ttf")
    print()
    print("   Restart Flask (python3 app.py) and generate a Hindi PDF to verify.")
else:
    print("❌  Merge failed. Install fonttools and retry:")
    print("    pip3 install fonttools --break-system-packages")
    sys.exit(1)


# ── Also check if old fonts exist in root and remind user ────────
old_files = ["NotoMerged-Regular.ttf", "NotoMerged-Bold.ttf",
             "NotoSans-Regular.ttf", "NotoSans-Bold.ttf",
             "NotoSansDevanagari-Regular.ttf", "NotoSansDevanagari-Bold.ttf"]
found_old = [f for f in old_files if os.path.exists(os.path.join(BASE_DIR, f))]
if found_old:
    print()
    print("ℹ️   Old font files found in project root (no longer needed there):")
    for f in found_old:
        print(f"    {f}")
    print("    You can delete them or leave them — the app now uses fonts/ subfolder.")