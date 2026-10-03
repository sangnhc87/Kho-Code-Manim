import re

with open("toc_do_nuoc_dang.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace prep loop
prep_old = """total_items = sum(1 + sum(len(p["rows"]) for p in les["pages"]) for les in selected)
done = 0

for les in selected:
    intro = les["intro"]
    wav = get_audio(intro["voice"])
    intro["audio"] = str(wav); intro["duration"] = probe_dur(wav)
    done += 1
    for pi, page in enumerate(les["pages"]):
        for ri, row in enumerate(page["rows"]):
            wav = get_audio(row["voice"])
            row["audio"] = str(wav); row["duration"] = probe_dur(wav)
            done += 1
        if done % 15 == 0 or done == total_items:
            print(f"  Đã chuẩn bị {done} / {total_items} đoạn lời đọc.")
print(f"  Đã chuẩn bị đủ {total_items} đoạn lời đọc.")"""

prep_new = """total_items = sum(1 + len(les["pages"]) for les in selected)
done = 0

for les in selected:
    intro = les["intro"]
    wav = get_audio(intro["voice"])
    intro["audio"] = str(wav); intro["duration"] = probe_dur(wav)
    done += 1
    for pi, page in enumerate(les["pages"]):
        full_text = " ".join(r["voice"] for r in page["rows"])
        wav = get_audio(full_text)
        page["audio"] = str(wav)
        dur = probe_dur(wav)
        total_len = max(1, sum(len(r["voice"]) for r in page["rows"]))
        for ri, row in enumerate(page["rows"]):
            row["duration"] = dur * (len(row["voice"]) / total_len)
        done += 1
        if done % 15 == 0 or done == total_items:
            print(f"  Đã chuẩn bị {done} / {total_items} đoạn lời đọc.")
print(f"  Đã chuẩn bị đủ {total_items} đoạn lời đọc.")"""

text = text.replace(prep_old, prep_new)

# Replace speak method
speak_old = """    def speak(self, item, anim=None):
        start = float(self.time)
        dur   = float(item["duration"])
        self.add_sound(item["audio"])
        self.events.append({"start": start, "end": start+dur, "text": item["voice"]})
        reveal = 0.0
        if anim is not None:
            reveal = min(0.6, max(0.25, dur*0.25))
            self.play(anim, run_time=reveal)
        self.wait(max(0.1, dur - reveal) + 0.45)"""

speak_new = """    def speak(self, item, anim=None):
        start = float(self.time)
        dur   = float(item["duration"])
        if "audio" in item:
            self.add_sound(item["audio"])
        self.events.append({"start": start, "end": start+dur, "text": item["voice"]})
        reveal = 0.0
        if anim is not None:
            reveal = min(0.6, max(0.25, dur*0.25))
            self.play(anim, run_time=reveal)
        self.wait(max(0.1, dur - reveal))"""

text = text.replace(speak_old, speak_new)

# Modify the play loop in construct
loop_old = """            for data, mob in zip(page["rows"], rows):
                self.speak(data, FadeIn(mob, shift=UP*0.04))
                current.add(mob)
            self.wait(0.55)"""

loop_new = """            self.add_sound(page["audio"])
            for data, mob in zip(page["rows"], rows):
                self.speak(data, FadeIn(mob, shift=UP*0.04))
                current.add(mob)
            self.wait(0.55)"""

text = text.replace(loop_old, loop_new)

with open("toc_do_nuoc_dang.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Done replacing.")
