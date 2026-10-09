#!/usr/bin/env python3
"""
Sửa lỗi cú pháp Typst trong tất cả 31 file công thức của Series-Dai-So-To-Hop:
- ne -> !=
- cdot -> dot
- prod -> product
- Biến nhiều chữ cái/tiếng Việt trong math mode -> đặt trong dấu ngoặc kép hoặc tách dấu cách
- boxed(...) -> #rect(...)
"""

from pathlib import Path
import subprocess

BASE = Path("Series-Dai-So-To-Hop/assets")

FIXES = {
    "comb16v2/unequal_3.typ": [
        ("ne", "!="),
    ],
    "comb17v2/binary_2.typ": [
        ("ab + ba = 2 a b", "a b + b a = 2 a b"),
    ],
    "comb18v2/proof_5.typ": [
        ("N_(co A)+N_(khong A)", 'N_("có A")+N_("không A")'),
    ],
    "comb19v2/special_0.typ": [
        ("N_(no A)", 'N_("không A")'),
    ],
    "comb19v2/special_2.typ": [
        ("N_(no A)", 'N_("không A")'),
    ],
    "comb19v2/special_3.typ": [
        ("N_(A, no B)", 'N_(A, "không B")'),
    ],
    "comb20v2/challenge_5.typ": [
        ("$ boxed(S=112500) $", '#rect(stroke: 1.5pt + rgb("#22D3EE"), inset: 6pt)[$ S=112500 $]'),
    ],
    "comb20v2/evenodd_3.typ": [
        ("N_(chan)=N_(le)", 'N_("chẵn")=N_("lẻ")'),
    ],
    "comb22v2/capstone_2.typ": [
        ("dp[i+1,k,q_0]", '"dp"[i+1,k,q_0]'),
    ],
    "comb22v2/capstone_3.typ": [
        ("dp[i+1,k+1,q_1]", '"dp"[i+1,k+1,q_1]'),
    ],
    "comb23v2/fixed_ban_2.typ": [
        ("cdot", "dot"),
    ],
    "comb24v2/narayana_0.typ": [
        ("peaks(w)=#(UD)", '"peaks"(w)="UD"'),
    ],
    "comb25v2/bracelet_5.typ": [
        ("N_(quay)=14,quad N_(guong)=13", 'N_("quay")=14, quad N_("gương")=13'),
    ],
    "comb25v2/cube_1.typ": [
        ("cdot", "dot"),
    ],
    "comb25v2/cube_2.typ": [
        ("cdot", "dot"),
    ],
    "comb25v2/cube_3.typ": [
        ("cdot", "dot"),
    ],
    "comb25v2/cube_5.typ": [
        ("N_(orbit)=57", 'N_("orbit")=57'),
    ],
    "comb25v2/fixedweight_1.typ": [
        ("|Fix(e)|=20", '|"Fix"(e)|=20'),
    ],
    "comb25v2/fixedweight_2.typ": [
        ("|Fix(r^2)|=|Fix(r^4)|=2", '|"Fix"(r^2)|=|"Fix"(r^4)|=2'),
    ],
    "comb25v2/fixedweight_3.typ": [
        ("|Fix(r)|=|Fix(r^3)|=|Fix(r^5)|=0", '|"Fix"(r)|=|"Fix"(r^3)|=|"Fix"(r^5)|=0'),
    ],
    "comb25v2/fixedweight_5.typ": [
        ("prod_(j)", "product_(j)"),
    ],
    "comb25v2/polya_1.typ": [
        ("cdot", "dot"),
    ],
    "comb25v2/polya_2.typ": [
        ("cdot", "dot"),
    ],
    "comb25v2/roots_5.typ": [
        ("zeta^(-jr)", "zeta^(-j r)"),
    ],
    "comb25v2/synthesis_0.typ": [
        ("N_(orbits)=frac(1,|G|)sum_(g in G)|Fix(g)|", 'N_("orbits")=frac(1,|G|)sum_(g in G)|"Fix"(g)|'),
    ],
    "comb25v2/synthesis_1.typ": [
        ("|Orb(x)|=frac(|G|,|Stab(x)|)", '|"Orb"(x)|=frac(|G|,|"Stab"(x)|)'),
    ],
    "comb25v2/synthesis_3.typ": [
        ("zeta^(-jr)", "zeta^(-j r)"),
    ],
    "comb25v2/synthesis_4.typ": [
        ("|G_(cube)|=24", '|G_("cube")|=24'),
    ],
    "comb25v2/weighted_1.typ": [
        ("prod_(j)", "product_(j)"),
    ],
    "formulas/geo_boundary.typ": [
        ("D_(AB)", "D_(A B)"),
        ("D_(BC)", "D_(B C)"),
        ("D_(CA)", "D_(C A)"),
    ],
    "formulas/geo_general.typ": [
        ("D_(AB)", "D_(A B)"),
        ("D_(BC)", "D_(B C)"),
        ("D_(CA)", "D_(C A)"),
    ],
}

def apply_fixes():
    for rel_path, replacements in FIXES.items():
        p = BASE / rel_path
        if not p.exists():
            print(f"⚠️ Không tìm thấy: {rel_path}")
            continue
        content = p.read_text(encoding="utf-8")
        for old, new in replacements:
            content = content.replace(old, new)
        p.write_text(content, encoding="utf-8")
        print(f"✅ Đã sửa: {rel_path}")

def verify_all():
    print("\n🔍 Đang kiểm tra biên dịch lại tất cả file vừa sửa...")
    failed = 0
    for rel_path in FIXES:
        p = BASE / rel_path
        if not p.exists():
            continue
        res = subprocess.run(["typst", "compile", str(p), "/tmp/test.pdf"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ LỖI VẪN CÒN: {rel_path}")
            print("  ", res.stderr.strip())
            failed += 1
        else:
            print(f"✓ Biên dịch OK: {rel_path}")
    if failed == 0:
        print("\n🎉 HOÀN TẤT! 100% CÁC FILE ĐỀU ĐÃ BIÊN DỊCH THÀNH CÔNG VỚI TYPST!")
    else:
        print(f"\n⚠️ Còn {failed} file lỗi.")

if __name__ == "__main__":
    apply_fixes()
    verify_all()
