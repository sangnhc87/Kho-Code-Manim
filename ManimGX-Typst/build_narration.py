import asyncio
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

try:
    import edge_tts
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts

ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "vi-VN-NamMinhNeural"
RATE = "-5%"
PITCH = "+0Hz"

SCRIPTS = [
    (
        "seg_01_intro",
        "Chào các em. Hôm nay chúng ta cùng giải bài toán tối ưu sản xuất hai kiểu mũ, áp dụng hệ bất phương trình bậc nhất hai ẩn thuộc chương trình Toán 10.",
    ),
    (
        "seg_02_model",
        "Gọi x và y lần lượt là số mũ kiểu một và kiểu hai cần sản xuất trong một ngày, với x và y không âm. Do một giờ làm được sáu mươi mũ kiểu hai, nên mỗi chiếc mũ kiểu hai mất một phần sáu mươi giờ. Một mũ kiểu một mất thời gian gấp đôi, tức là hai phần sáu mươi giờ.",
    ),
    (
        "seg_03_time_prop_a",
        "Như vậy, tổng thời gian để làm x mũ kiểu một và y mũ kiểu hai là hai x cộng y, tất cả chia cho sáu mươi giờ. Do đó, phát biểu a ghi dấu trừ hai x trừ y chia sáu mươi là sai.",
    ),
    (
        "seg_04_system_prop_b",
        "Phân xưởng làm việc tám tiếng mỗi ngày, nên ta có bất phương trình hai x cộng y chia sáu mươi nhỏ hơn hoặc bằng tám, tương đương hai x cộng y nhỏ hơn hoặc bằng bốn trăm tám mươi. Kết hợp với nhu cầu tối đa của thị trường, ta có hệ bất phương trình mô tả các điều kiện. Vì vậy, phát biểu b là đúng.",
    ),
    (
        "seg_05_geometry",
        "Chuyển sang phần hai, ta biểu diễn hệ bất phương trình trên mặt phẳng tọa độ Oxy. Miền nghiệm của hệ là miền ngũ giác O A B C D, giới hạn bởi các đường thẳng x bằng hai trăm, y bằng hai trăm bốn mươi và hai x cộng y bằng bốn trăm tám mươi.",
    ),
    (
        "seg_06_profit_prop_cd",
        "Hàm tiền lãi thu được là F bằng hai mươi tư x cộng mười lăm y nghìn đồng. Tính giá trị F tại năm đỉnh của miền nghiệm, ta thấy tiền lãi đạt cực đại là sáu triệu bốn trăm tám mươi nghìn đồng tại đỉnh C, ứng với một trăm hai mươi mũ kiểu một và hai trăm bốn mươi mũ kiểu hai. Do đó, phát biểu c và phát biểu d đều đúng.",
    ),
    (
        "seg_07_summary",
        "Tổng kết lại, bài toán có đáp án chuẩn: a sai, b đúng, c đúng và d đúng. Chúc các em học tập thật tốt!",
    ),
]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


async def generate_clip(key: str, text: str) -> Path:
    out_file = AUDIO_DIR / f"{key}.mp3"
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(out_file))
    return out_file


def main():
    print("=== Đang sinh Audio bằng Edge TTS (Giọng Thầy Nguyễn Văn Sang - NamMinh) ===")
    timings = {}
    total_time = 0.0
    clips = []

    for key, text in SCRIPTS:
        print(f"-> Tạo audio: {key} ...")
        out_path = asyncio.run(generate_clip(key, text))
        dur = probe_duration(out_path)
        print(f"   Thời lượng: {dur:.2f}s")
        timings[key] = {
            "path": str(out_path),
            "duration": dur,
            "text": text,
        }
        clips.append((key, out_path, dur))

    timings_path = ROOT / "narration_timings.json"
    timings_path.write_text(json.dumps(timings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã lưu bảng timings vào: {timings_path}")


if __name__ == "__main__":
    main()
