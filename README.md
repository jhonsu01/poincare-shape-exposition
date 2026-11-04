# The Shape of a World You Cannot Leave

A plain-language exposition of the Poincaré conjecture, Perelman's proof, and what a computer check can and cannot tell us.

**This is exposition only. It claims no new mathematical result.** All the mathematics is due to the cited authors. The essay and video were prepared with AI assistance (Claude, Anthropic).

- **Problem:** Poincaré conjecture, JSP-000007, [MathDB #316224](https://mathdb.com/p/316224/poincare-conjecture)
- **Category:** Exposition
- **Author:** @jhonsu777
- **Contact:** 2xrqx82e2@mozmail.com
- **Version:** v1.0, 4 November 2026 (UTC). Not independently reviewed.
- **Video:** <https://youtu.be/kgnliLkoP-0>

## Contents

| Path | What it is |
| --- | --- |
| `essay/essay_en.pdf` | The essay |
| `essay/essay_en.md` | Essay source |
| `video/poincare_en.mp4` | Narrated video, about 4:16, 1080p (attached to the release, not stored in git) |
| `video/poincare_en.srt` | Subtitles (timing is approximate) |
| `video/video_script.md` | Narration script |
| `checks/poincare_checks.py` | Symbolic checks used in the essay |
| `production/` | Scripts that generate the animation, audio and sound effects |
| `NOTICE.md` | Licenses and credits |
| `SHA256SUMS.txt` | File checksums |

## What we checked

- With `checks/poincare_checks.py`: the round three-sphere under Ricci flow, and the arithmetic of the width argument.
- We confirmed the form of the Colding–Minicozzi inequality in their paper.

## What we did not check

- We did not compile the Lean formalization by Qin, Liao, Khaitan and Chow, which has 14,234 helper modules in its MathDB submission. We report what its authors state and what MathDB displays.
- We did not audit whether the Lean statement faithfully matches Poincaré's question.
- We did not read the classical papers line by line.
- This exposition has not been independently reviewed.

## Reproducing

```bash
python checks/poincare_checks.py
```

The scripts in `production/` contain absolute Windows paths from the original machine and need editing to run elsewhere.
