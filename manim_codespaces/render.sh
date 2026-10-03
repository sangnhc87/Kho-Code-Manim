#!/usr/bin/env bash
set -Eeuo pipefail
MANIM_PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$MANIM_PROJECT_DIR"
case "${1:-}" in
  oxyz) MANIM_LESSON_FILE='oxyz_tam_ti_cu_hay_la_kho.py' ;;
  nuoc) MANIM_LESSON_FILE='toc_do_nuoc_dang_3d_dien_tich_mat_thoang.py' ;;
  *) printf '%s\n' 'Cách dùng: bash render.sh oxyz|nuoc [final|standard|preview] [B01,B02,...]'; exit 2 ;;
esac
export MANIM_QUALITY="${2:-final}"
case "$MANIM_QUALITY" in final|standard|preview) ;; *) printf '%s\n' 'Chất lượng phải là final, standard hoặc preview.'; exit 2 ;; esac
if [[ $# -ge 3 ]]; then export MANIM_LESSONS="$3"; fi
if [[ "${CODESPACES:-}" != 'true' ]]; then
  printf '%s\n' 'Chạy lệnh này trong Terminal của GitHub Codespaces.' >&2; exit 1
fi
MANIM_STATE_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/manim-teaching-019"
MANIM_PYTHON="$MANIM_STATE_DIR/venv/bin/python"
export MANIM_OUTPUT_DIR="${MANIM_OUTPUT_DIR:-/tmp/manim-video-output}"
if [[ ! -x "$MANIM_PYTHON" ]]; then
  printf '%s\n' 'Lần đầu: chạy bash setup_codespaces.sh trước.' >&2; exit 1
fi
# Một tiến trình mỗi bộ: tránh ghi chồng MP4 hoặc tạo nhiều render vô ý.
mkdir -p "$MANIM_OUTPUT_DIR"
printf '%s\n' 'manim-teaching-output-v1' > "$MANIM_OUTPUT_DIR/.manim-output"
exec 9> "$MANIM_OUTPUT_DIR/.render.lock"
if ! flock -n 9; then
  printf '%s\n' 'Bộ này đang có một video được render. Chờ xong rồi chạy video tiếp theo.' >&2; exit 1
fi
"$MANIM_PYTHON" check_environment.py
printf 'Đang dựng %s (%s). Chỉ in trạng thái theo chương.\n' "$1" "$MANIM_QUALITY"
export PYTHONUNBUFFERED=1
"$MANIM_PYTHON" "$MANIM_LESSON_FILE"
