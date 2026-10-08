# CACH DUA COMB01 LEN GITHUB ACTIONS

## Da co code cho bao nhieu tap?

- Co ma Manim co the render: COMB01 (Quy tac cong).
- COMB02-COMB08: moi co de cuong; KHONG CO code Manim trong goi nay.
- Scene duoc render: `COMB01` trong `episodes/comb01_rule_of_sum.py`.
- Workflow can chay: `.github/workflows/render-comb01.yml`.

## Cach don gian voi GitHub Desktop (khuyen dung)

1. Giai nen ZIP 'SangMath_COMB01_GitHub_Ready.zip'.
2. Mo GitHub Desktop. Chon File > Add Local Repository, chon thu muc da giai nen. Neu ung dung thong bao thu muc chua la git repository, bam Create a Repository Here.
3. Commit to main (neu co thay doi chua commit), sau do bam Publish repository.
4. Mo repository tren GitHub, chon Actions.
5. Chon 'Render COMB01 - Manim + Typst' (ten hien thi co the co dau cham giua), bam Run workflow.
6. Chon `quality: preview` va `notation: user`, sau do bam Run workflow.
7. Khi hoan thanh, bam lan chay -> Artifacts -> tai goi `COMB01-preview-user` de lay MP4.
8. Neu ban preview dat yeu cau, chay lai workflow va chon `quality: fullhd`.

## Cach dung terminal khi da tao repository trong GitHub

Mo Terminal tai thu muc goc da giai nen (thu muc co `README.md` va `.github`):

```
git init
git add -A
git commit -m "Add COMB01 Manim Typst"
git branch -M main
git remote add origin https://github.com/TEN_TAI_KHOAN/TEN_REPOSITORY.git
git push -u origin main
```

Thay TEN_TAI_KHOAN va TEN_REPOSITORY bang thong tin that. Repository tren GitHub nen rong, chua co README/commit ban dau, de tranh loi push.

## Luu y quan trong

- KHONG tai len nguyen file ZIP: GitHub khong tu giai nen thanh source code.
- KHONG dat cac file trong them mot thu muc cha ben trong repository. `README.md`, `requirements.txt`, `.github`, `episodes`, `scripts` phai o GOC repository.
- Tren macOS, `.github` co the bi an trong Finder; dung GitHub Desktop hoac `git add -A` se giu duoc thu muc nay.
- Workflow se cai Manim va Typst trong Ubuntu runner, khong can cai Manim tren Mac.
- `COMB_NOTATION=user` su dung `C^(n)_(k)`, `A^(n)_(k)` nhu da yeu cau (n o tren k o duoi). `sgk` chuyen ve `C_(n)^(k)`.
- MP4 hien tai la animation CHUA co am thanh/giong doc va CHUA can duoc nhac theo kich ban 11 phut. Can duyet ket qua run dau tien, roi moi hoan thien thoi luong.
- Workflow chua duoc thu render Manim thuc su; lan chay dau tien la buoc kiem chung.
