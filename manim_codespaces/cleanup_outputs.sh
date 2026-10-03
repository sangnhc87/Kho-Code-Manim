#!/usr/bin/env bash
# Chỉ chạy sau khi đã tải MP4 về máy và kiểm tra file tải thành công.
set -Eeuo pipefail
if [[ "${CODESPACES:-}" != 'true' ]]; then
  printf '%s\n' 'Chạy trong Terminal của Codespaces.' >&2; exit 1
fi
MANIM_OUTPUT_DIR="${MANIM_OUTPUT_DIR:-/tmp/manim-video-output}"
if [[ ! -f "$MANIM_OUTPUT_DIR/.manim-output" ]] || [[ "$(cat "$MANIM_OUTPUT_DIR/.manim-output")" != 'manim-teaching-output-v1' ]]; then
  printf '%s\n' 'Không thấy thư mục kết quả của bộ này. Không xóa gì.'; exit 0
fi
exec 9> "$MANIM_OUTPUT_DIR/.render.lock"
if ! flock -n 9; then
  printf '%s\n' 'Đang render; không dọn dữ liệu. Chờ render xong và tải MP4 trước.' >&2; exit 1
fi
# Chỉ xóa hai thư mục kết quả được biết; giữ nguyên mã, thư viện và file khác.
rm -rf -- "$MANIM_OUTPUT_DIR/Oxyz_Tam_Ti_Cu" "$MANIM_OUTPUT_DIR/Nuoc_Dang_3D_Mat_Thoang"
printf '%s\n' 'Đã dọn video, audio, cache và log render của hai bài. Môi trường cài đặt vẫn còn.'
