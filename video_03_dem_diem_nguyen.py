from manim_series_common import *

class SangLesson(LessonBase):
    def intro(self):
        self.clear_stage()
        g=VGroup(
            txt("ĐẾM ĐIỂM NGUYÊN TRONG MIỀN NGHIỆM",46,INK,BOLD),
            mtx(r"(x,y)\in\mathbb Z^2",42,GOLD),
            txt("Từ hình học liên tục đến các phương án rời rạc",29,CYAN),
            txt(TEN_THAY,22,MUTED)
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(g),run_time=1.1)
        self.narrate("Chào các em! Trong nhiều bài toán thực tế, x và y không thể nhận mọi số thực. Số xe, số phòng, số sản phẩm hay số phương án thường phải là số nguyên. Khi đó, sau khi tìm miền nghiệm, ta còn phải đếm xem có bao nhiêu điểm lưới nguyên nằm trong miền ấy.",1.9)

        self.clear_stage(); self.add_header_footer("Điểm nguyên là gì?", "Những nút của lưới tọa độ", "Mở đầu")
        axes=Axes(x_range=[0,6,1],y_range=[0,6,1],x_length=5.8,y_length=4.8,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":22}).shift(LEFT*2.4+DOWN*0.25)
        dots=VGroup(*[Dot(axes.c2p(i,j),radius=0.045,color=CYAN) for i in range(0,6) for j in range(0,6)])
        side=VGroup(mtx(r"x\in\mathbb Z",36,GOLD),mtx(r"y\in\mathbb Z",36,GOLD),mtx(r"(x,y)\in\mathbb Z^2",38,BLUE)).arrange(DOWN,buff=0.35).to_edge(RIGHT,buff=0.7)
        self.play(Create(axes),FadeIn(dots),FadeIn(side),run_time=1.1)
        self.narrate("Mỗi chấm sáng trên hình là một điểm có hai tọa độ nguyên. Công việc của ta là giữ lại đúng những chấm vừa nằm trong miền nghiệm, vừa thỏa tất cả điều kiện biên. Khi miền lớn, đếm bằng mắt rất dễ sót, nên ta cần một quy trình có hệ thống.",1.7)

    def ex1(self):
        self.show_problem(
            "Ví dụ 1 – Tam giác cơ bản",
            [
                ("text","Đếm số nghiệm nguyên không âm của hệ:",28,INK,BOLD),
                ("math",r"\begin{cases}x\ge0\\y\ge0\\x+y\le4\end{cases}",42,GOLD),
                ("math",r"x,y\in\mathbb Z",34,CYAN),
            ],
            "Ví dụ đầu tiên: đếm các cặp số nguyên không âm x y thỏa x cộng y nhỏ hơn hoặc bằng bốn. Ta sẽ làm bằng cách quét từng hàng ngang. Đây là bài mẫu để các em thấy rõ mỗi hàng đóng góp bao nhiêu điểm.",
            "Ví dụ 1/5")
        self.clear_stage(); self.add_header_footer("Ví dụ 1", "Quét từng hàng ngang", "Ví dụ 1/5")
        axes=Axes(x_range=[0,6,1],y_range=[0,6,1],x_length=5.8,y_length=4.8,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":22}).shift(LEFT*2.5+DOWN*0.25)
        line=axes.plot(lambda x:4-x,x_range=[0,4],color=BLUE,stroke_width=4)
        tri=Polygon(axes.c2p(0,0),axes.c2p(4,0),axes.c2p(0,4),fill_color=BLUE,fill_opacity=0.14,stroke_color=BLUE)
        pts=[]
        for x in range(5):
            for y in range(5-x):
                pts.append(Dot(axes.c2p(x,y),radius=0.06,color=GREEN))
        self.play(Create(axes),Create(line),FadeIn(tri),run_time=0.9)
        self.play(LaggedStart(*[FadeIn(d) for d in pts],lag_ratio=0.03),run_time=1.3)
        self.narrate("Miền nghiệm là tam giác có các đỉnh không không, bốn không và không bốn. Vì dấu là nhỏ hơn hoặc bằng, các điểm nằm trên cạnh xiên cũng được tính. Bây giờ chỉ quan tâm các nút lưới nằm trong hoặc trên biên tam giác.",1.7)
        rows=VGroup(
            mtx(r"y=0:\quad x=0,1,2,3,4\quad\Rightarrow5",30,INK),
            mtx(r"y=1:\quad x=0,1,2,3\quad\Rightarrow4",30,INK),
            mtx(r"y=2:\quad x=0,1,2\quad\Rightarrow3",30,INK),
            mtx(r"y=3:\quad x=0,1\quad\Rightarrow2",30,INK),
            mtx(r"y=4:\quad x=0\quad\Rightarrow1",30,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.18).to_edge(RIGHT,buff=0.25).shift(UP*0.45)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate("Ở hàng y bằng không có năm điểm. Hàng y bằng một có bốn điểm. Tiếp theo là ba, hai và một. Cách quét này giúp ta không đếm trùng và cũng không bỏ sót điểm nào.",1.6)
        ans=mtx(r"N=5+4+3+2+1=15",40,GOLD).to_edge(RIGHT,buff=0.45).shift(DOWN*1.75)
        self.play(Write(ans),run_time=0.6)
        self.narrate("Tổng cộng hệ có mười lăm nghiệm nguyên không âm. Sau này, tổng một cộng hai đến n chính là dạng tam giác số xuất hiện rất thường xuyên.",1.3)

    def ex2(self):
        self.show_problem(
            "Ví dụ 2 – Dấu nghiêm ngặt và cận nguyên",
            [
                ("text","Đếm nghiệm nguyên của hệ:",28,INK,BOLD),
                ("math",r"\begin{cases}x\ge1\\y\ge0\\2x+y<8\end{cases}",42,GOLD),
                ("math",r"x,y\in\mathbb Z",34,CYAN),
            ],
            "Ví dụ hai có dấu nhỏ hơn nghiêm ngặt. Vì hai x cộng y là một số nguyên, điều kiện hai x cộng y nhỏ hơn tám tương đương hai x cộng y nhỏ hơn hoặc bằng bảy. Đây là mẹo rất quan trọng khi đếm điểm nguyên.",
            "Ví dụ 2/5")
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Đổi dấu nghiêm ngặt trên tập số nguyên", "Ví dụ 2/5")
        eq=VGroup(
            mtx(r"2x+y<8",42,ORANGE),
            mtx(r"2x+y\in\mathbb Z",34,CYAN),
            mtx(r"\Longleftrightarrow\ 2x+y\le7",42,GOLD)
        ).arrange(DOWN,buff=0.30).shift(UP*0.8)
        self.play(FadeIn(eq),run_time=0.8)
        self.narrate("Trên tập số nguyên, không có giá trị nào nằm giữa bảy và tám. Do đó nhỏ hơn tám chính là nhỏ hơn hoặc bằng bảy. Đây là bước chuyển từ bất phương trình thực sang bất phương trình nguyên.",1.5)
        table=VGroup(
            mtx(r"x=1:\ y\le5\Rightarrow6",32,INK),
            mtx(r"x=2:\ y\le3\Rightarrow4",32,INK),
            mtx(r"x=3:\ y\le1\Rightarrow2",32,INK),
            mtx(r"x\ge4:\ \varnothing",32,RED),
            mtx(r"N=6+4+2=12",40,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.25).shift(DOWN*0.7)
        self.play(FadeIn(table),run_time=0.9)
        self.narrate("Với x bằng một, y chạy từ không đến năm nên có sáu giá trị. x bằng hai cho bốn giá trị. x bằng ba cho hai giá trị. Từ x bằng bốn trở đi không còn nghiệm. Tổng cộng mười hai điểm nguyên.",1.8)
        note=VGroup(txt("Mẹo",26,GOLD,BOLD),mtx(r"A<k,\ A\in\mathbb Z\Rightarrow A\le k-1",34,GOLD)).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.45)
        self.play(FadeIn(note),run_time=0.5)
        self.narrate("Mẹo này dùng được rộng hơn: nếu A là số nguyên và k là số nguyên, A nhỏ hơn k tương đương A nhỏ hơn hoặc bằng k trừ một.",1.2)

    def ex3(self):
        self.show_problem(
            "Ví dụ 3 – Miền kẹp giữa hai đường",
            [
                ("text","Đếm số nghiệm nguyên không âm:",28,INK,BOLD),
                ("math",r"\begin{cases}x+y\ge3\\x+2y\le8\\x\ge0\\y\ge0\end{cases}",39,GOLD),
                ("math",r"x,y\in\mathbb Z",34,CYAN),
            ],
            "Ví dụ ba có miền nghiệm nằm giữa hai đường thẳng. Ta sẽ không đếm bằng mắt, mà viết cận dưới và cận trên của x theo từng y. Đây là kỹ thuật dùng rất tốt khi miền là một đa giác xiên.",
            "Ví dụ 3/5")
        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Viết cận theo từng hàng", "Ví dụ 3/5")
        axes=Axes(x_range=[0,10,1],y_range=[0,6,1],x_length=6.6,y_length=4.7,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":21}).shift(LEFT*2.5+DOWN*0.3)
        l1=axes.plot(lambda x:3-x,x_range=[0,3],color=ORANGE,stroke_width=4)
        l2=axes.plot(lambda x:(8-x)/2,x_range=[0,8],color=BLUE,stroke_width=4)
        feasible=[]
        for x in range(9):
            for y in range(5):
                if x+y>=3 and x+2*y<=8:
                    feasible.append(Dot(axes.c2p(x,y),radius=0.052,color=GREEN))
        self.play(Create(axes),Create(l1),Create(l2),run_time=1.0)
        self.play(LaggedStart(*[FadeIn(d) for d in feasible],lag_ratio=0.025),run_time=1.2)
        self.narrate("Các chấm xanh là những điểm nguyên thỏa cả hai điều kiện. Để đếm chắc chắn, ta cố định y rồi tìm khoảng giá trị nguyên của x. Khi có cả cận dưới và cận trên, cách này đặc biệt hiệu quả.",1.6)
        deriv=VGroup(
            mtx(r"x+y\ge3\ \Longrightarrow\ x\ge3-y",31,ORANGE),
            mtx(r"x+2y\le8\ \Longrightarrow\ x\le8-2y",31,BLUE),
            mtx(r"\max(0,3-y)\le x\le8-2y",34,GOLD),
        ).arrange(DOWN,buff=0.26).to_edge(RIGHT,buff=0.25).shift(UP*1.15)
        self.play(FadeIn(deriv),run_time=0.7)
        self.narrate("Điều kiện đầu cho x ít nhất bằng ba trừ y. Điều kiện sau cho x không vượt quá tám trừ hai y. Đồng thời x không âm, nên cận dưới là số lớn hơn giữa không và ba trừ y.",1.7)
        rows=VGroup(
            mtx(r"y=0:\ 3\le x\le8\Rightarrow6",28,INK),
            mtx(r"y=1:\ 2\le x\le6\Rightarrow5",28,INK),
            mtx(r"y=2:\ 1\le x\le4\Rightarrow4",28,INK),
            mtx(r"y=3:\ 0\le x\le2\Rightarrow3",28,INK),
            mtx(r"y=4:\ x=0\Rightarrow1",28,INK),
            mtx(r"N=6+5+4+3+1=19",34,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.14).to_edge(RIGHT,buff=0.30).shift(DOWN*1.25)
        self.play(FadeIn(rows),run_time=0.9)
        self.narrate("Ta lần lượt được sáu, năm, bốn, ba và một điểm. Tổng cộng mười chín nghiệm nguyên. Hàng y bằng bốn chỉ còn x bằng không; từ y bằng năm trở lên cận trên đã âm nên không còn điểm nào.",1.5)

    def ex4(self):
        self.show_problem(
            "Ví dụ 4 – Mô hình thực tế",
            [
                ("text","Một đội vận tải chọn x xe nhỏ và y xe lớn.",27,INK,BOLD),
                ("math",r"2x+3y\le12",38,GOLD),
                ("text","Tổng số xe phải ít nhất 3 chiếc.",26,INK),
                ("math",r"x+y\ge3,\qquad x,y\in\mathbb Z_{\ge0}",38,CYAN),
                ("text","Có bao nhiêu phương án điều xe?",27,GREEN,BOLD),
            ],
            "Ví dụ bốn gắn với một bài toán rời rạc thực tế. x là số xe nhỏ, y là số xe lớn. Ngân sách tạo điều kiện hai x cộng ba y không vượt quá mười hai, và đội cần ít nhất ba xe. Ta cần đếm số phương án nguyên không âm.",
            "Ví dụ 4/5")
        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Đếm phương án thực tế", "Ví dụ 4/5")
        table=VGroup(
            mtx(r"y=0:\ 3\le x\le6\Rightarrow4",31,INK),
            mtx(r"y=1:\ 2\le x\le4\Rightarrow3",31,INK),
            mtx(r"y=2:\ 1\le x\le3\Rightarrow3",31,INK),
            mtx(r"y=3:\ 0\le x\le1\Rightarrow2",31,INK),
            mtx(r"y=4:\ x=0\Rightarrow1",31,INK),
            mtx(r"N=4+3+3+2+1=13",42,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).shift(UP*0.1)
        self.play(FadeIn(table),run_time=0.8)
        self.narrate("Quét theo số xe lớn y. Khi y bằng không, x từ ba đến sáu có bốn phương án. Sau đó lần lượt có ba, ba, hai và một phương án. Tổng cộng mười ba cách điều xe.",1.7)
        note=VGroup(txt("Mỗi điểm nguyên",27,CYAN,BOLD),mtx(r"(x,y)",34,CYAN),txt("chính là một phương án thực tế khả thi.",27,INK)).arrange(RIGHT,buff=0.18).shift(DOWN*2.0)
        self.play(FadeIn(note),run_time=0.5)
        self.narrate("Đây là ý nghĩa rất quan trọng: mỗi điểm nguyên trong miền nghiệm tương ứng đúng một phương án thực tế có thể thực hiện. Khi đề hỏi số phương án, thực chất ta đang đếm điểm nguyên.",1.5)

    def ex5_floor(self):
        self.show_problem(
            "Ví dụ 5 – Khi cận không chia hết",
            [
                ("text","Đếm nghiệm nguyên không âm:",28,INK,BOLD),
                ("math",r"3x+2y\le10",42,GOLD),
                ("math",r"x,y\in\mathbb Z_{\ge0}",34,CYAN),
            ],
            "Ví dụ năm cho thấy vì sao phần nguyên dưới xuất hiện tự nhiên. Khi cố định y, cận trên của x là mười trừ hai y chia ba, thường không phải số nguyên. Ta phải lấy phần nguyên dưới để biết giá trị nguyên lớn nhất của x.",
            "Ví dụ 5/5")
        self.clear_stage(); self.add_header_footer("Ví dụ 5", "Dùng phần nguyên dưới", "Ví dụ 5/5")
        formula=VGroup(
            mtx(r"3x\le10-2y",36,INK),
            mtx(r"x\le\frac{10-2y}{3}",38,BLUE),
            mtx(r"0\le x\le\left\lfloor\frac{10-2y}{3}\right\rfloor",40,GOLD),
        ).arrange(DOWN,buff=0.30).shift(UP*0.85)
        self.play(FadeIn(formula),run_time=0.8)
        self.narrate("Từ ba x cộng hai y không vượt quá mười, ta suy ra x không vượt quá mười trừ hai y chia ba. Nhưng x là số nguyên, nên cận thật sự là phần nguyên dưới của phân số này.",1.5)
        rows=VGroup(
            mtx(r"y=0:\ 0\le x\le3\Rightarrow4",29,INK),
            mtx(r"y=1:\ 0\le x\le2\Rightarrow3",29,INK),
            mtx(r"y=2:\ 0\le x\le2\Rightarrow3",29,INK),
            mtx(r"y=3:\ 0\le x\le1\Rightarrow2",29,INK),
            mtx(r"y=4:\ 0\le x\le0\Rightarrow1",29,INK),
            mtx(r"y=5:\ 0\le x\le0\Rightarrow1",29,INK),
            mtx(r"\boxed{N=14}",40,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.14).shift(DOWN*0.75)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate("Các hàng y từ không đến năm lần lượt cho bốn, ba, ba, hai, một và một điểm. Tổng cộng mười bốn nghiệm nguyên. Nếu chỉ nhìn phân số mà không lấy phần nguyên dưới, ta rất dễ đếm sai ở những hàng cận không chia hết.",1.7)

        self.clear_stage(); self.add_header_footer("Một cách kiểm tra ngược", "Đếm theo cột để đối chiếu", "Ví dụ 5/5")
        alt=VGroup(
            mtx(r"x=0:\ 0\le y\le5\Rightarrow6",30,INK),
            mtx(r"x=1:\ 0\le y\le3\Rightarrow4",30,INK),
            mtx(r"x=2:\ 0\le y\le2\Rightarrow3",30,INK),
            mtx(r"x=3:\ y=0\Rightarrow1",30,INK),
            mtx(r"6+4+3+1=14",38,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.22)
        self.play(FadeIn(alt),run_time=0.8)
        self.narrate("Ta còn có thể kiểm tra ngược bằng cách quét theo cột x. Khi x bằng không có sáu điểm; x bằng một có bốn; x bằng hai có ba; x bằng ba có một. Kết quả vẫn là mười bốn. Với bài dài, đối chiếu hai cách là một phương pháp kiểm tra rất tốt.",1.7)

    def methods(self):
        self.clear_stage(); self.add_header_footer("Ba chiến lược đếm", "Chọn cách phù hợp với miền", "Tổng kết")
        g=VGroup(
            VGroup(mtx(r"1.",34,GOLD),txt("Vẽ miền rồi đếm trực tiếp nếu miền nhỏ.",27,INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"2.",34,GOLD),txt("Quét từng hàng y hoặc từng cột x.",27,INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"3.",34,GOLD),txt("Dùng cận nguyên với",27,INK),mtx(r"\lfloor\cdot\rfloor,\ \lceil\cdot\rceil",32,CYAN)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"a<b,\ a,b\in\mathbb Z",31,ORANGE),mtx(r"\Longleftrightarrow a\le b-1",31,GREEN)).arrange(RIGHT,buff=0.30),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.45).shift(DOWN*0.1)
        for r in g:self.play(FadeIn(r,shift=RIGHT*0.1),run_time=0.4)
        self.narrate("Có ba chiến lược chính. Miền nhỏ thì có thể đếm trực tiếp. Miền lớn hơn, hãy quét theo hàng hoặc cột. Khi cận không nguyên, dùng phần nguyên dưới và phần nguyên trên. Với đại lượng nguyên, dấu nhỏ hơn nghiêm ngặt cũng thường đổi được thành một cận nhỏ hơn hoặc bằng.",1.9)

        self.clear_stage(); self.add_header_footer("Bài tự luyện", "Đếm mà không bỏ sót biên", "Tự luyện")
        q=VGroup(
            txt("Đếm nghiệm nguyên không âm:",28,INK,BOLD),
            mtx(r"\begin{cases}x+2y\le10\\x+y\ge4\end{cases}",42,GOLD),
            mtx(r"x,y\in\mathbb Z_{\ge0}",35,CYAN)
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(q),run_time=0.7)
        self.narrate("Bài tự luyện: hãy đếm các cặp số nguyên không âm thỏa x cộng hai y không vượt quá mười và x cộng y ít nhất bằng bốn. Hãy thử quét theo y và nhớ kiểm tra cả những điểm nằm trên đường biên.",1.6)
        self.wait(1.0)
        sol=VGroup(
            mtx(r"y=0:\ 4\le x\le10\Rightarrow7",28,INK),
            mtx(r"y=1:\ 3\le x\le8\Rightarrow6",28,INK),
            mtx(r"y=2:\ 2\le x\le6\Rightarrow5",28,INK),
            mtx(r"y=3:\ 1\le x\le4\Rightarrow4",28,INK),
            mtx(r"y=4:\ 0\le x\le2\Rightarrow3",28,INK),
            mtx(r"y=5:\ x=0\Rightarrow1",28,INK),
            mtx(r"\boxed{N=26}",38,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.14).to_edge(RIGHT,buff=0.35)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate("Lời giải: với y từ không đến năm, số giá trị x lần lượt là bảy, sáu, năm, bốn, ba và một. Tổng bằng hai mươi sáu. Như vậy bài tự luyện cũng được giải trọn vẹn.",1.5)

    def outro(self):
        self.clear_stage()
        g=VGroup(txt("CHỐT LẠI",44,GOLD,BOLD),mtx(r"(x,y)\in S\cap\mathbb Z^2",40,BLUE),txt("Mỗi điểm nguyên là một phương án rời rạc khả thi.",29,CYAN),txt(TEN_THAY,22,MUTED)).arrange(DOWN,buff=0.30)
        self.play(FadeIn(g),run_time=0.9)
        self.narrate("Video tiếp theo sẽ kết hợp cả hai ý tưởng: tham số m và số điểm nguyên. Khi m thay đổi, số điểm nguyên không thay đổi liên tục mà nhảy theo từng ngưỡng. Đây là một lớp bài rất hay và có tính phân loại cao.",1.7)

    def construct(self):
        self.intro(); self.ex1(); self.ex2(); self.ex3(); self.ex4(); self.ex5_floor(); self.methods(); self.outro()

if __name__ == "__main__":
    render_scene(SangLesson, "he_bpt_dem_diem_nguyen_1080p")
