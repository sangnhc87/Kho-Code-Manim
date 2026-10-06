from manim_series_common import *

class SangLesson(LessonBase):
    def intro(self):
        self.clear_stage()
        main = fit_width(txt("HỆ BẤT PHƯƠNG TRÌNH CÓ THAM SỐ", 48, INK, BOLD), 12.1)
        sub = mtx(r"m\in\mathbb R", 42, GOLD)
        desc = txt("Khi đường biên chuyển động, miền nghiệm thay đổi thế nào?", 29, CYAN)
        brand = txt(TEN_THAY, 23, MUTED)
        g = VGroup(main, sub, desc, brand).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(main, shift=UP*0.2), Write(sub), run_time=1.2)
        self.play(FadeIn(desc), FadeIn(brand), run_time=0.7)
        self.narrate(
            "Chào các em! Ở video trước, chúng ta đã biết mỗi bất phương trình bậc nhất hai ẩn biểu diễn một nửa mặt phẳng, và miền nghiệm của hệ là phần giao. Hôm nay ta thêm một tham số m. Khi m thay đổi, một đường biên sẽ dịch chuyển. Nhiệm của bài toán không còn chỉ là tô miền, mà còn phải tìm đúng ngưỡng để miền nghiệm xuất hiện, co lại thành một đoạn hay một điểm, hoặc biến mất hoàn toàn.", 2.0)

        self.clear_stage(); self.add_header_footer("Tư duy cốt lõi", "Tham số làm đường biên chuyển động", "Mở đầu")
        rows = VGroup(
            VGroup(mtx(r"x+y=m", 38, BLUE), txt("→ đường thẳng dịch chuyển song song", 27, INK)).arrange(RIGHT,buff=0.35),
            VGroup(mtx(r"m<m_0", 36, RED), txt("→ có thể vô nghiệm", 27, RED)).arrange(RIGHT,buff=0.35),
            VGroup(mtx(r"m=m_0", 36, GOLD), txt("→ trạng thái tiếp xúc / suy biến", 27, GOLD)).arrange(RIGHT,buff=0.35),
            VGroup(mtx(r"m>m_0", 36, GREEN), txt("→ có thể xuất hiện miền nghiệm", 27, GREEN)).arrange(RIGHT,buff=0.35),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN*0.1)
        for r in rows: self.play(FadeIn(r, shift=RIGHT*0.15), run_time=0.4)
        self.narrate("Ta sẽ luôn tìm một giá trị ngưỡng m không, nơi trạng thái của miền nghiệm thay đổi. Điều quan trọng là nhìn hình trước, rồi mới biến đổi đại số để chứng minh.", 1.5)

    def ex1(self):
        self.show_problem(
            "Ví dụ 1 – Ngưỡng xuất hiện miền nghiệm",
            [
                ("text", "Tìm m để hệ có nghiệm:", 28, INK, BOLD),
                ("math", r"\begin{cases}x\ge1\\y\ge1\\x+y\le m\end{cases}", 40, GOLD),
                ("text", "Phân biệt trường hợp có đúng một nghiệm và có vô số nghiệm.", 26, CYAN),
            ],
            "Ví dụ một là mô hình đơn giản nhưng rất quan trọng. Ta cần tìm m để hệ x lớn hơn hoặc bằng một, y lớn hơn hoặc bằng một, và x cộng y nhỏ hơn hoặc bằng m có nghiệm. Ta cũng phân biệt khi miền nghiệm chỉ còn một điểm và khi nó có diện tích.",
            "Ví dụ 1/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 1", "Nhìn hình để thấy ngưỡng", "Ví dụ 1/4")
        axes = Axes(x_range=[0,6,1], y_range=[0,6,1], x_length=6.2, y_length=5.2,
                    axis_config={"color":MUTED,"include_numbers":True,"font_size":22}).shift(LEFT*2.4+DOWN*0.2)
        x1 = DashedLine(axes.c2p(1,0), axes.c2p(1,6), color=GREEN, dash_length=0.12)
        y1 = DashedLine(axes.c2p(0,1), axes.c2p(6,1), color=GREEN, dash_length=0.12)
        p = label_point(axes,1,1,"A(1,1)",GOLD,UR)
        side = VGroup(
            mtx(r"x\ge1",32,GREEN), mtx(r"y\ge1",32,GREEN),
            mtx(r"x+y\le m",34,BLUE)
        ).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.55).shift(UP*1.25)
        self.play(Create(axes), Create(x1), Create(y1), FadeIn(side), FadeIn(p), run_time=1.2)
        self.narrate("Hai điều kiện đầu ép điểm nghiệm nằm về phía trên bên phải điểm A một một. Vì vậy trong toàn bộ miền này, giá trị nhỏ nhất có thể của x cộng y chính là hai, đạt tại A.",1.8)

        lines = VGroup()
        for mm, col in [(1,RED),(2,GOLD),(4,BLUE)]:
            ln = axes.plot(lambda x, mm=mm: mm-x, x_range=[0,min(mm,6)], color=col, stroke_width=4)
            lines.add(ln)
        self.play(Create(lines[0]), run_time=0.5)
        self.narrate("Nếu m bằng một, đường x cộng y bằng một nằm hoàn toàn bên dưới điểm A. Không thể có điểm vừa có x và y ít nhất bằng một, vừa có tổng không vượt quá một. Hệ vô nghiệm.",1.7)
        self.play(ReplacementTransform(lines[0], lines[1]), run_time=0.7)
        self.narrate("Khi m bằng hai, đường biên đi đúng qua A. Phần giao co lại thành duy nhất điểm A một một. Hệ có đúng một nghiệm.",1.5)
        self.play(ReplacementTransform(lines[1], lines[2]), run_time=0.7)
        tri = Polygon(axes.c2p(1,1),axes.c2p(3,1),axes.c2p(1,3),fill_color=GREEN,fill_opacity=0.28,stroke_color=GREEN)
        self.play(FadeIn(tri),run_time=0.6)
        self.narrate("Nếu m lớn hơn hai, đường biên dịch ra xa và ta có cả một tam giác nghiệm. Như vậy điều kiện để hệ có nghiệm là m lớn hơn hoặc bằng hai; có đúng một nghiệm khi m bằng hai; và có vô số nghiệm khi m lớn hơn hai.",2.1)
        box=make_panel(4.6,2.2).to_edge(RIGHT,buff=0.35).shift(DOWN*1.35)
        ans = VGroup(mtx(r"m\ge2",40,GOLD), mtx(r"m=2",32,GREEN), mtx(r"m>2",32,CYAN)).arrange(DOWN,buff=0.22).move_to(box)
        self.play(FadeIn(box),FadeIn(ans),run_time=0.5)

    def ex2(self):
        self.show_problem(
            "Ví dụ 2 – Một dải miền nghiệm",
            [
                ("text", "Tìm m để hệ có nghiệm:", 28, INK, BOLD),
                ("math", r"\begin{cases}x\ge0\\y\ge0\\m\le x+y\le4\end{cases}", 40, GOLD),
                ("text", "Khi nào miền nghiệm có diện tích dương?", 26, CYAN),
            ],
            "Ví dụ hai có hai đường thẳng song song: x cộng y bằng m và x cộng y bằng bốn. Ta cần tìm khi nào giữa hai đường này còn phần nằm trong góc phần tư thứ nhất.",
            "Ví dụ 2/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Hai đường song song tạo một dải", "Ví dụ 2/4")
        axes=Axes(x_range=[0,6,1],y_range=[0,6,1],x_length=6.2,y_length=5.2,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":22}).shift(LEFT*2.4+DOWN*0.2)
        l4=axes.plot(lambda x:4-x,x_range=[0,4],color=BLUE,stroke_width=4)
        lm=axes.plot(lambda x:2-x,x_range=[0,2],color=ORANGE,stroke_width=4)
        self.play(Create(axes),Create(l4),Create(lm),run_time=1.0)
        self.narrate("Đường x cộng y bằng bốn là biên trên cố định. Đường x cộng y bằng m là biên dưới và sẽ trượt song song khi m thay đổi.",1.5)
        reg=Polygon(axes.c2p(0,2),axes.c2p(0,4),axes.c2p(4,0),axes.c2p(2,0),fill_color=GREEN,fill_opacity=0.25,stroke_color=GREEN)
        self.play(FadeIn(reg),run_time=0.6)
        self.narrate("Với m bằng hai, ta thấy một dải nghiệm rõ ràng. Nếu tăng m, dải này mỏng dần. Khi m bằng bốn, hai biên trùng nhau và miền nghiệm chỉ còn đoạn thẳng nối không bốn với bốn không.",1.8)
        self.play(Transform(lm,l4.copy().set_color(GOLD)),FadeOut(reg),run_time=0.8)
        self.narrate("Nếu m lớn hơn bốn, yêu cầu x cộng y vừa lớn hơn hoặc bằng m vừa nhỏ hơn hoặc bằng bốn là không thể. Do đó hệ có nghiệm khi và chỉ khi m nhỏ hơn hoặc bằng bốn. Nếu muốn miền nghiệm có diện tích dương thì phải có m nhỏ hơn bốn.",2.0)
        result = VGroup(
            VGroup(txt("Có nghiệm khi và chỉ khi",25,INK),mtx(r"m\le4",36,GOLD)).arrange(RIGHT,buff=0.22),
            VGroup(txt("Miền có diện tích dương khi",25,INK),mtx(r"m<4",36,GREEN)).arrange(RIGHT,buff=0.22)
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.35).shift(DOWN*1.25)
        self.play(FadeIn(result),run_time=0.5)

    def ex3(self):
        self.show_problem(
            "Ví dụ 3 – Ngưỡng bằng giá trị lớn nhất",
            [
                ("text", "Tìm m để hệ có nghiệm:", 28, INK, BOLD),
                ("math", r"\begin{cases}x\ge0\\y\ge0\\x+y\le4\\2x+y\ge m\end{cases}", 39, GOLD),
            ],
            "Ví dụ ba sâu hơn. Ba điều kiện đầu tạo một tam giác cố định. Điều kiện cuối yêu cầu hai x cộng y ít nhất bằng m. Muốn tồn tại nghiệm, m không được vượt quá giá trị lớn nhất mà biểu thức hai x cộng y đạt được trên tam giác cố định.",
            "Ví dụ 3/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Tìm ngưỡng từ các đỉnh", "Ví dụ 3/4")
        axes=Axes(x_range=[0,6,1],y_range=[0,6,1],x_length=6.1,y_length=5.1,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":22}).shift(LEFT*2.5+DOWN*0.15)
        tri=Polygon(axes.c2p(0,0),axes.c2p(4,0),axes.c2p(0,4),fill_color=BLUE,fill_opacity=0.18,stroke_color=BLUE,stroke_width=3)
        labs=VGroup(label_point(axes,0,0,"O",CYAN,DL),label_point(axes,4,0,"A(4,0)",CYAN,DR),label_point(axes,0,4,"B(0,4)",CYAN,UL))
        self.play(Create(axes),FadeIn(tri),FadeIn(labs),run_time=1.0)
        self.narrate("Ba điều kiện x không âm, y không âm và x cộng y không vượt quá bốn tạo tam giác O A B. Ta chỉ cần tìm giá trị lớn nhất của biểu thức hai x cộng y trên tam giác này.",1.7)
        table=VGroup(
            VGroup(mtx(r"O(0,0)",30,CYAN),mtx(r"2x+y=0",30,INK)).arrange(RIGHT,buff=0.35),
            VGroup(mtx(r"A(4,0)",30,CYAN),mtx(r"2x+y=8",30,GOLD)).arrange(RIGHT,buff=0.35),
            VGroup(mtx(r"B(0,4)",30,CYAN),mtx(r"2x+y=4",30,INK)).arrange(RIGHT,buff=0.35),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.32).to_edge(RIGHT,buff=0.35).shift(UP*0.55)
        self.play(FadeIn(table),run_time=0.7)
        self.narrate("Tại O, giá trị là không. Tại A bốn không, giá trị là tám. Tại B không bốn, giá trị là bốn. Lớn nhất là tám tại A.",1.5)
        moving=axes.plot(lambda x:8-2*x,x_range=[1,4],color=GOLD,stroke_width=4)
        self.play(Create(moving),run_time=0.7)
        self.narrate("Đường hai x cộng y bằng m chỉ còn cắt tam giác khi m không vượt quá tám. Với m bằng tám, nó chỉ chạm tam giác tại A. Nếu m lớn hơn tám, đường này đi ra ngoài và hệ vô nghiệm.",1.9)
        ans=VGroup(txt("Kết luận",26,GOLD,BOLD),mtx(r"m\le8",42,GOLD)).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.7).shift(DOWN*1.55)
        self.play(FadeIn(ans),run_time=0.5)

    def ex4(self):
        self.show_problem(
            "Ví dụ 4 – Dấu nghiêm ngặt làm đổi ngưỡng",
            [
                ("text", "Tìm m để hệ có nghiệm:", 28, INK, BOLD),
                ("math", r"\begin{cases}x>1\\y>1\\x+y<m\end{cases}", 42, GOLD),
            ],
            "Ví dụ bốn nhìn gần giống ví dụ một, nhưng tất cả các dấu đều nghiêm ngặt. Điểm một một không còn được phép lấy. Đây là lúc các em phải rất cẩn thận với dấu bằng.",
            "Ví dụ 4/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Biên không được lấy", "Ví dụ 4/4")
        axes=Axes(x_range=[0,5,1],y_range=[0,5,1],x_length=5.8,y_length=5.0,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":22}).shift(LEFT*2.35+DOWN*0.2)
        x1=DashedLine(axes.c2p(1,0),axes.c2p(1,5),color=GREEN,dash_length=0.14)
        y1=DashedLine(axes.c2p(0,1),axes.c2p(5,1),color=GREEN,dash_length=0.14)
        l2=DashedLine(axes.c2p(0,2),axes.c2p(2,0),color=GOLD,dash_length=0.14)
        self.play(Create(axes),Create(x1),Create(y1),Create(l2),run_time=1.0)
        self.narrate("Khi m bằng hai, ba đường biên gặp nhau về mặt hình học tại điểm một một, nhưng điểm này không thuộc miền nghiệm vì x phải lớn hơn một và y cũng phải lớn hơn một. Do đó m bằng hai vẫn vô nghiệm.",1.8)
        l3=DashedLine(axes.c2p(0,3),axes.c2p(3,0),color=BLUE,dash_length=0.14)
        self.play(ReplacementTransform(l2,l3),run_time=0.7)
        tiny=Polygon(axes.c2p(1.02,1.02),axes.c2p(1.95,1.02),axes.c2p(1.02,1.95),fill_color=GREEN,fill_opacity=0.25,stroke_opacity=0)
        self.play(FadeIn(tiny),run_time=0.5)
        self.narrate("Chỉ khi m lớn hơn hai, giữa ba biên mới xuất hiện những điểm thật sự thỏa tất cả dấu nghiêm ngặt. Vì vậy điều kiện là m lớn hơn hai, không phải lớn hơn hoặc bằng hai.",1.7)
        ans=mtx(r"\boxed{m>2}",44,GOLD).to_edge(RIGHT,buff=0.8)
        self.play(Write(ans),run_time=0.5)


    def deepening(self):
        self.clear_stage(); self.add_header_footer("Ba kiểu ngưỡng thường gặp", "Nhìn trạng thái biên để phân loại", "Mở rộng")
        cards=VGroup(
            VGroup(mtx(r"m<m_0",34,RED),txt("Hai miền chưa chạm nhau",25,RED)).arrange(DOWN,buff=0.16),
            VGroup(mtx(r"m=m_0",34,GOLD),txt("Vừa tiếp xúc: điểm hoặc đoạn",25,GOLD)).arrange(DOWN,buff=0.16),
            VGroup(mtx(r"m>m_0",34,GREEN),txt("Xuất hiện miền có diện tích",25,GREEN)).arrange(DOWN,buff=0.16),
        ).arrange(RIGHT,buff=0.55).shift(UP*0.65)
        for c in cards:
            box=RoundedRectangle(width=3.8,height=1.75,corner_radius=0.15,fill_color=PANEL,fill_opacity=0.9,stroke_color=MUTED,stroke_opacity=0.25)
            box.move_to(c)
            self.play(FadeIn(box),FadeIn(c),run_time=0.45)
        self.narrate("Các em nên ghi nhớ ba trạng thái hình học. Trước ngưỡng, hai yêu cầu còn mâu thuẫn nên không có phần giao. Đúng tại ngưỡng, miền thường suy biến thành một điểm hoặc một đoạn thẳng. Sau ngưỡng, miền có thể mở ra thành một vùng có diện tích. Tuy nhiên chiều bất đẳng thức có thể làm thứ tự đảo lại, vì vậy không học thuộc m lớn hay m nhỏ mà phải nhìn hướng chuyển động của đường biên.",2.2)

        self.clear_stage(); self.add_header_footer("Một mẹo rất mạnh", "Ngưỡng m thường là min hoặc max của một biểu thức tuyến tính", "Mở rộng")
        g=VGroup(
            txt("Nếu miền cố định là",26,INK),mtx(r"S",38,BLUE),
            txt("và điều kiện mới có dạng",26,INK),mtx(r"ax+by\ge m",38,ORANGE),
            VGroup(txt("thì cần so sánh m với",26,INK),mtx(r"\max_{(x,y)\in S}(ax+by)",38,GOLD)).arrange(RIGHT,buff=0.20),
            VGroup(txt("Tương tự với",26,INK),mtx(r"ax+by\le m",38,ORANGE),txt("ta thường xét giá trị nhỏ nhất.",26,INK)).arrange(RIGHT,buff=0.20),
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(g),run_time=0.8)
        self.narrate("Một mẹo mạnh hơn là biến bài tham số thành bài tìm cực trị tuyến tính trên miền cố định. Nếu điều kiện mới là a x cộng b y lớn hơn hoặc bằng m, m không thể vượt quá giá trị lớn nhất của a x cộng b y trên miền cũ. Ngược lại, nếu điều kiện là a x cộng b y nhỏ hơn hoặc bằng m, ngưỡng thường liên quan đến giá trị nhỏ nhất. Với miền đa giác, các giá trị cực trị tuyến tính đạt tại đỉnh, nên ta chỉ cần kiểm tra một số hữu hạn điểm.",2.3)

        self.clear_stage(); self.add_header_footer("Đừng quên trường hợp suy biến", "Có nghiệm không đồng nghĩa với có diện tích", "Mở rộng")
        items=VGroup(
            VGroup(mtx(r"m=m_0",36,GOLD),txt("có thể chỉ còn 1 điểm",26,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"m=m_0",36,GOLD),txt("cũng có thể còn cả 1 đoạn",26,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"m>m_0",36,GREEN),txt("mới có miền hai chiều",26,INK)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN,buff=0.38)
        self.play(FadeIn(items),run_time=0.7)
        self.narrate("Khi đề hỏi hệ có nghiệm, một điểm duy nhất cũng đã là nghiệm. Nhưng nếu đề hỏi miền nghiệm có diện tích dương, hay có điểm nằm trong miền trong, ta phải loại trường hợp suy biến. Đây chính là lý do ở ví dụ hai, m bằng bốn vẫn có nghiệm nhưng diện tích bằng không.",1.8)

    def summary(self):
        self.clear_stage(); self.add_header_footer("Chiến lược giải bài có tham số", "Không đoán m bằng biến đổi máy móc", "Tổng kết")
        steps=VGroup(
            bullet("Bước 1. Vẽ hoặc nhận diện miền cố định trước.",INK,27,BLUE),
            bullet("Bước 2. Xem đường chứa m dịch chuyển theo hướng nào.",INK,27,CYAN),
            bullet("Bước 3. Tìm trạng thái biên: chạm điểm, trùng đường hoặc vừa xuất hiện miền.",INK,27,GOLD),
            bullet("Bước 4. Kiểm tra dấu nghiêm ngặt hay có dấu bằng.",INK,27,ORANGE),
            bullet("Bước 5. Viết điều kiện m và kiểm tra lại bằng một giá trị thử.",INK,27,GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.33).shift(DOWN*0.1)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.35)
        self.narrate("Với bài có tham số, các em đừng vội biến đổi m. Hãy nhìn miền cố định, xem đường chứa m đang dịch chuyển thế nào, tìm đúng trạng thái biên rồi mới kết luận. Và nhớ rằng dấu nghiêm ngặt có thể làm mất nghiệm đúng tại ngưỡng.",1.9)

        self.clear_stage(); self.add_header_footer("Bài tự luyện", "Tự dừng video và thử trước", "Tự luyện")
        q=VGroup(
            txt("Tìm m để hệ có nghiệm:",29,INK,BOLD),
            mtx(r"\begin{cases}x\ge0\\y\ge0\\x+y\le5\\x+2y\ge m\end{cases}",42,GOLD),
            txt("Gợi ý: tìm giá trị lớn nhất của biểu thức",26,MUTED),
            mtx(r"x+2y",38,CYAN)
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(q),run_time=0.7)
        self.narrate("Bài tự luyện cuối video: với tam giác x không âm, y không âm, x cộng y không vượt quá năm, hãy tìm giá trị lớn nhất của x cộng hai y. Đó chính là ngưỡng của m. Các em hãy dừng video và thử làm trước.",1.8)
        self.wait(1.0)
        sol=VGroup(mtx(r"(0,0):0",30,INK),mtx(r"(5,0):5",30,INK),mtx(r"(0,5):10",30,GOLD),mtx(r"\boxed{m\le10}",40,GOLD)).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(sol),run_time=0.7)
        self.narrate("Ba đỉnh cho các giá trị không, năm và mười. Lớn nhất là mười tại không năm. Vì vậy điều kiện là m nhỏ hơn hoặc bằng mười.",1.5)

    def outro(self):
        self.clear_stage()
        g=VGroup(txt("CHỐT LẠI",44,GOLD,BOLD),VGroup(mtx(r"m",40,BLUE),Arrow(LEFT*0.5,RIGHT*0.5,color=CYAN,stroke_width=3),txt("đường biên chuyển động",28,BLUE,BOLD)).arrange(RIGHT,buff=0.20),txt("Ngưỡng của m xuất hiện khi hình dạng miền nghiệm đổi trạng thái.",28,INK),txt(TEN_THAY,22,MUTED)).arrange(DOWN,buff=0.30)
        self.play(FadeIn(g),run_time=1.0)
        self.narrate("Nếu em nhìn được đường biên nào đang chuyển động khi m thay đổi, bài tham số sẽ trở nên trực quan hơn rất nhiều. Video tiếp theo, chúng ta sẽ chuyển sang một kỹ năng rất hay: đếm các điểm có tọa độ nguyên nằm trong miền nghiệm.",1.8)

    def construct(self):
        self.intro(); self.ex1(); self.ex2(); self.ex3(); self.ex4(); self.deepening(); self.summary(); self.outro()

if __name__ == "__main__":
    render_scene(SangLesson, "he_bpt_tham_so_m_1080p")
