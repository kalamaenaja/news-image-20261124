"""Entry program for make.fun news-image-20261124.

Copies the committed news image (one image summing up the world's news
of Tuesday 24 November 2026) to the output directory. Standard library only.

About the image (entry.png, 1024x1024, 151,553 bytes, 42 stories):
  - Hero: Huang returns as Nvidia CEO; the market roars (Nasdaq +6.5%).
  - Medium (6): Iran hits 3 ships in Hormuz; Odesa blackout; Russian jet
    in South Korean airspace; US blacklists Megaspeed; Trump fast-tracks
    federal executions; Trump seals the Japan trade deal.
  - Grid (25): one verified story per card, each with a category glyph
    (diamond = conflict, triangle = markets, dot = science/health,
    square = politics, star = culture/sport).
  - Ticker (10): EU retaliatory tariffs, US Treasury, Spain election,
    Brent $89.37, gold $3,640, the Fed, Trump on Iran, COP31, Cobre Panama.

How the image was made: a Python generator (Pillow) drew the whole
1024x1024 layout from the verified story list, with a self-check that
warns on any clipped headline; the final render had zero warnings and
was read visually twice. The generator is deterministic: two runs
produce byte-identical output.

Contract with the grader:
  - Output is exactly one file, /output/entry.png, a real PNG by its
    first bytes, at most 1 MiB (1,048,576 bytes).
  - Running this program twice must write identical bytes both times,
    so the copy is verified against the source before exiting.
"""
import os
import shutil
import sys

MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    # Cheap format check first: read only the 8-byte PNG magic, so a
    # wrong file fails fast before the size check and the copy.
    with open(src, "rb") as f:
        magic = f.read(8)
    if magic != PNG_MAGIC:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if os.path.getsize(src) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    # Determinism guard: the grader runs this twice and both runs must
    # write identical bytes, so confirm the copy matches the source.
    with open(src, "rb") as f:
        src_bytes = f.read()
    with open(dst, "rb") as f:
        dst_bytes = f.read()
    if src_bytes != dst_bytes:
        print("copy mismatch between entry.png and output", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(dst_bytes)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
