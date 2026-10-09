#!/usr/bin/env python3
"""
Script hỗ trợ lấy YouTube OAuth Refresh Token trên macOS / Linux.
Tự động tìm kiếm file client_secret*.json trên Desktop hoặc Downloads.
"""

import glob
import json
import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def find_client_secrets_file():
    # 1. Kiểm tra tham số dòng lệnh
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        return sys.argv[1]

    # 2. Tìm kiếm trong các thư mục phổ biến
    search_patterns = [
        os.path.expanduser("~/Desktop/client_secret*.json"),
        os.path.expanduser("~/Downloads/client_secret*.json"),
        os.path.expanduser("~/Desktop/youtube_client*.json"),
        "./client_secret*.json",
        "./youtube_client*.json",
    ]

    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

    return None


def main():
    client_file = find_client_secrets_file()
    if not client_file:
        print("❌ Không tìm thấy file client_secret JSON nào.")
        print("Vui lòng truyền đường dẫn file: python3 scripts/get_youtube_token.py /path/to/client_secret.json")
        sys.exit(1)

    print(f"🔍 Đang dùng file credentials: {client_file}")

    with open(client_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        key = "installed" if "installed" in data else "web"
        if key not in data:
            print("❌ File JSON không hợp lệ (không chứa block 'installed' hoặc 'web').")
            sys.exit(1)
        client_id = data[key].get("client_id", "")
        client_secret = data[key].get("client_secret", "")

    print("\n🌐 Đang mở trình duyệt để xác thực tài khoản Google...")
    print("👉 Hãy chọn đúng tài khoản Google sở hữu kênh YouTube.")
    print("👉 Nếu có thông báo 'Google chưa xác minh ứng dụng này' -> Chọn 'Nâng cao' (Advanced) -> Chọn 'Đi tới... (không an toàn)'.")
    print("👉 Tích chọn cho phép quyền 'Quản lý video YouTube của bạn'.\n")

    flow = InstalledAppFlow.from_client_secrets_file(client_file, scopes=SCOPES)
    credentials = flow.run_local_server(
        host="localhost",
        port=0,
        access_type="offline",
        prompt="consent",
    )

    if not credentials.refresh_token:
        print("❌ Không nhận được refresh_token từ Google.")
        print("Gợi ý: Thử chạy lại và chắc chắn tài khoản Google đồng ý cấp quyền truy cập offline.")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("🎉 LẤY TOKEN THÀNH CÔNG! HÃY LƯU VÀO GITHUB REPOSITORY SECRETS:")
    print("=" * 65)
    print(f"\n1. Tên Secret: YOUTUBE_CLIENT_ID")
    print(f"   Giá trị:\n{client_id}")
    print(f"\n2. Tên Secret: YOUTUBE_CLIENT_SECRET")
    print(f"   Giá trị:\n{client_secret}")
    print(f"\n3. Tên Secret: YOUTUBE_REFRESH_TOKEN")
    print(f"   Giá trị:\n{credentials.refresh_token}")
    print("\n" + "=" * 65)
    print("⚠️ BẢO MẬT: Tuyệt đối KHÔNG gửi các giá trị trên vào nhóm chat/AI và KHÔNG commit lên Git!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
