#!/usr/bin/env bash
# Make Edge TTS narration on this machine and publish it for CI (release "xss-voice", one xssNNN.tar.gz per Short).
# CI unpacks it before prepare_voice.py, which reuses every clip whose text hash still matches.
# usage: [FORCE=1] scripts/pack_voice.sh FIRST LAST [python]
set -u
cd "$(dirname "$0")/.."
FIRST=$1; LAST=$2; PY=${3:-python3}
OUT=$(mktemp -d)
gh release view xss-voice >/dev/null 2>&1 || \
  gh release create xss-voice --prerelease --title "XSS narration cache" --notes "Edge TTS audio made off-CI; see scripts/pack_voice.sh"
HAVE=$(gh release view xss-voice --json assets -q '.assets[].name')
for n in $(seq "$FIRST" "$LAST"); do
  sh=$(printf 'xss%03d' "$n")
  [ -f "xss/$sh.py" ] || continue
  # already published: skip unless FORCE=1 (needed after editing a Short's narration)
  [ "${FORCE:-0}" = 1 ] || ! grep -qx "$sh.tar.gz" <<<"$HAVE" || continue
  # a stalled Edge connection never returns: give each Short at most 10 minutes (macOS has no `timeout`)
  if perl -e 'alarm shift; exec @ARGV' 600 "$PY" scripts/prepare_voice.py --short "$sh" --voice on >"$OUT/$sh.log" 2>&1; then
    tar -czf "$OUT/$sh.tar.gz" "plans/$sh.json" "voice/$sh"
    gh release upload xss-voice "$OUT/$sh.tar.gz" --clobber >/dev/null && echo "$sh packed" || echo "$sh UPLOAD FAILED"
  else
    echo "$sh VOICE FAILED: $(tail -1 "$OUT/$sh.log")"
  fi
done
