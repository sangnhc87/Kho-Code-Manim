# Episode 0001 review — 2026-10-09

Reference: https://youtu.be/sj2f_z0g7YM. Reviewed the matching original 1080p artifact from GitHub Actions run 37935423325 (duration 361.533 seconds).

Confirmed display problem: the narration and captions identify squares with coordinates such as d2–f1, but the original board has no file/rank labels. This prevents a beginner from locating the named squares. Added external file labels a–i and rank labels 0–9, and an explicit top-left origin caption. Expanded the spoken introduction to explain the notation.

The sampled original frames and a Manim scene regression through all 18 beats and all 63 moves did not reproduce missing board artwork, ghost pieces, or pieces disappearing except when captured. The regression now checks actual scene membership, visible piece counts and centers after each reset and move. Do not describe an unobserved disappearance as a fixed defect.

Clarified the teaching objective: 13/21 are total plies to force capture of the advisor in the four-piece ordinary-move retrograde model. These numbers are not mate distances. Official repetition adjudication is outside that model. The scope now appears in the spoken introduction, visible board stamp and episode subtitle.

Fixed the engine integration's coordinate ambiguity. Display rank 0 is the black/top edge; Pikafish UCI rank 0 is the red/bottom edge. The conversion is y_UCI = 9 - y_display, so display d2f1 is UCI d7f8. `check_pikafish.py` now checks every illustrated move with perft depth 1, sets an explicit matching NNUE path, rejects engine errors and saves a reproducible report. Initial depth-22 search selects d7f8/d2f1. All 63 moves passed engine legality checks; this is not a proof of the entire retrograde objective or tournament-rule result.

Production uses the existing `render-xiangqi.yml`: preview first, then a single full dispatch with Edge Vietnamese narration and automatic public YouTube upload. The old published video is preserved.
