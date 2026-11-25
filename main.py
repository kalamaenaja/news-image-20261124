"""make.fun entry for news-image-20261124 — second submission.

The picture this program delivers is the rebuilt 27-story version of
the 24 November 2026 world-news image. The first submission carried
42 stories in a dense grid and the judging showed the cost of that
density: round 1 placed it 1,428th of 7,302, and round 2 dropped it
to 4,719th of 9,063 — the same slide the 23 November entry suffered
when it tried the same dense layout, and the same fix that entry got.
So this version goes back to the readable shape that scored best on
23 November: one hero, three medium cards, sixteen grid cards and
seven ticker items, twenty-seven stories in total, each one verified
against search results dated 24 November 2026.

What is on the picture (entry.png, 1024 by 1024, 132,735 bytes):
  - Hero: Huang is back at Nvidia and the market roars — then gives
    some back. Monday's board reinstatement sent the shares up 31.48
    percent, the biggest daily gain in 23 years; Tuesday the stock
    pulled back 5.86 percent to $155.38 as the Nasdaq slipped 1.48
    percent. Both legs of the move are in the hero text, because a
    one-day snapshot that only shows the surge would be stale by
    judging time.
  - Medium (3): Iran hits three ships in the Strait of Hormuz;
    Russian strikes black out Odesa; Russian jets breach South
    Korea's air defence zone.
  - Grid (16): one verified story per card, from the Megaspeed
    blacklist to the Indonesia factory fire toll of 24.
  - Ticker (7): EU tariff retaliation, Brent, gold, the Fed, Trump's
    warning on Iran, COP31, Panama's Cobre talks.

The picture itself was drawn once, by a Pillow generator, from the
verified story list, with a self-check that warns on any clipped
headline; the final render had zero warnings and was read visually.
This program does not redraw anything: it only carries the finished
picture to the grader's output directory, checking it on the way.

Checks this program performs before it copies:
  - The source must start with the eight-byte PNG signature, so a
    truncated download or a JPEG with the wrong name fails here with
    exit code 1 instead of reaching the grader.
  - The source must fit the 1 MiB ceiling; at 132,735 bytes it uses
    about an eighth of the budget.
  - After copying, the program reads both files back in full and
    compares every byte, so a short write caused by a full disk is
    caught here rather than submitted as a corrupt entry.

Size note: 132,735 bytes is about an eighth of the 1,048,576-byte
ceiling, and the rebuilt layout is lighter than the 151,553-byte
42-story original because sixteen fewer cards means less text to
draw — the smaller file is a side effect of the readability fix,
not a goal in itself.

Running the program twice writes identical bytes both times, which is
what the grader requires. MAKEFUN_OUTPUT_DIR lets the same program
be exercised locally against a scratch directory; in grading it
defaults to /output and nothing else changes. Exit code 0 means the
copy landed and verified; 1 means a check failed. On success the
only output is one line naming the file and its byte count.
"""
import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAGIC = b"\x89PNG\r\n\x1a\n"


def _read_prefix(path, count):
    with open(path, "rb") as handle:
        return handle.read(count)


def _abort(message):
    print(message, file=sys.stderr)
    return 1


def run():
    origin = Path(__file__).resolve().parent / "entry.png"
    outdir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "entry.png"
    if origin.stat().st_size > MAX_BYTES:
        return _abort("entry.png exceeds the 1 MiB limit")
    if _read_prefix(origin, len(MAGIC)) != MAGIC:
        return _abort("entry.png is not a PNG file")
    shutil.copyfile(origin, outfile)
    source_bytes = origin.read_bytes()
    written_bytes = outfile.read_bytes()
    if source_bytes != written_bytes:
        return _abort("copy mismatch between entry.png and output")
    print(f"wrote {outfile} ({len(written_bytes)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
