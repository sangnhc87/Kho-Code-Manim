#!/usr/bin/env bash
set -Eeuo pipefail
MANIM_PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$MANIM_PROJECT_DIR"
if [[ "${CODESPACES:-}" != "true" ]]; then
  printf '%s\n' 'Chạy bộ cài này trong Terminal của GitHub Codespaces.' >&2
  exit 1
fi
MANIM_STATE_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/manim-teaching-019"
MANIM_VENV="$MANIM_STATE_DIR/venv"
MANIM_MARKER="$MANIM_STATE_DIR/setup_ready"
mkdir -p "$MANIM_STATE_DIR/logs"
MANIM_SETUP_LOG="$MANIM_STATE_DIR/logs/setup.log"
MANIM_SETUP_KEY="$(sha256sum requirements.txt | cut -d ' ' -f 1)-$(python3 -V)"
if [[ -x "$MANIM_VENV/bin/python" && -f "$MANIM_MARKER" ]] && [[ "$(cat "$MANIM_MARKER")" == "$MANIM_SETUP_KEY" ]]; then
  if "$MANIM_VENV/bin/python" check_environment.py > "$MANIM_SETUP_LOG" 2>&1; then
    printf '%s\n' 'Đã cài đủ; dùng lại môi trường. Render bằng bash render.sh oxyz hoặc bash render.sh nuoc.'
    exit 0
  fi
fi
printf 'Đang cài môi trường một lần, ngoài repo. Log: %s\n' "$MANIM_SETUP_LOG"
exec 3>&1
exec > "$MANIM_SETUP_LOG" 2>&1
trap 'printf "Cài đặt chưa xong tại dòng %s. Xem log: %s\n" "$LINENO" "$MANIM_SETUP_LOG" >&3' ERR
if [[ "$EUID" -eq 0 ]]; then
  MANIM_SUDO=()
else
  MANIM_SUDO=(sudo -n)
fi
"${MANIM_SUDO[@]}" env DEBIAN_FRONTEND=noninteractive apt-get update -qq
"${MANIM_SUDO[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  ffmpeg util-linux pkg-config build-essential python3-dev python3-venv libcairo2-dev libpango1.0-dev \
  fonts-dejavu-core fonts-noto-core fontconfig texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-fonts-recommended texlive-science dvisvgm
rm -rf "$MANIM_VENV"
python3 -m venv "$MANIM_VENV"
"$MANIM_VENV/bin/python" -m pip install --disable-pip-version-check --progress-bar off -q -r requirements.txt
"$MANIM_VENV/bin/python" check_environment.py --smoke
printf '%s\n' "$MANIM_SETUP_KEY" > "$MANIM_MARKER"
printf '%s\n' 'Cài đặt và render thử ngắn đã đạt. Lần sau chỉ chạy bash render.sh oxyz hoặc bash render.sh nuoc.' >&3
