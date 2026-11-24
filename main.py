"""Entry program for make.fun news-image-20261124.

Copies the committed news image (one image summing up the world's news
of Tuesday 24 November 2026) to the output directory. Standard library only.
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
