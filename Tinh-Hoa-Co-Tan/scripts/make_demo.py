"""Build the pilot. Narration covers principles only; not a verified PV."""
import json
from pathlib import Path

beats=[
('MỞ ĐẦU', 'Một con Mã có đủ sức?',
'''Trên bàn cờ chỉ còn đúng bốn quân: hai Tướng, một Mã Đỏ và một Sĩ Đen. Nghe thì có vẻ Đỏ rất dễ thắng. Nhưng tôi muốn hỏi bạn một câu: vì sao có người đưa Mã đi tới đi lui hàng chục nước vẫn chưa bắt được Sĩ? Phải chăng Mã không đủ mạnh? Hay người chơi đang thiếu một ý tưởng quan trọng? Trong tập đầu tiên của Tinh Hoa Cờ Tàn, chúng ta không học thuộc một chuỗi nước cờ. Chúng ta học cách nhìn thế trận. Khi xem xong, bạn sẽ biết mình phải quan sát điều gì trước khi điều Mã, và vì sao quân Tướng cũng tham gia tấn công.''',
'Đừng vội đuổi theo Sĩ. Hãy nhìn cả Tướng Đen.',[],None,None,1.2),
('NHÌN THẾ CỜ', 'Đếm quân, nhưng phải nhìn vị trí',
'''Bên Đỏ có Tướng và Mã. Bên Đen có Tướng và Sĩ. Sĩ tuy yếu khi ra ngoài cung, nhưng ở trong cung lại có nhiệm vụ rất rõ ràng: che chắn và giữ các điểm quan trọng cho Tướng. Nếu chỉ đếm quân, ta dễ nghĩ Đỏ có ưu thế là xong. Cờ tàn không đơn giản thế. Càng ít quân, mỗi ô trên bàn cờ càng có giá trị. Một ô bị khống chế có thể khiến Tướng không thể lùi; một ô trống lại có thể trở thành lối thoát. Vì thế, trước khi tìm nước hay, hãy tập thói quen nhìn toàn bộ cung Tướng.''',
'Sức mạnh nằm ở điểm khống chế, không chỉ ở số quân.',[],None,'d1',.8),
('HIỂU CON MÃ', 'Mã đi chữ nhật, nhưng có chân',
'''Bây giờ hãy quan sát Mã Đỏ. Mã có thể đi hai ô theo một hướng và một ô theo hướng vuông góc, nhưng đường đi của Mã trong cờ tướng khác quân mã cờ vua ở một chỗ rất quan trọng: chân Mã có thể bị cản. Nếu ô ngay cạnh theo hướng đi dài bị quân khác chiếm, Mã không thể nhảy qua. Ta sẽ vẽ rõ ô chân Mã bằng một chấm vàng và đường đi bằng hai nét nối. Khi phân tích cờ tàn, đừng chỉ nhìn ô Mã sắp đến; hãy kiểm tra cả ô chân Mã. Sai một chi tiết nhỏ ở đây, cả lời giải có thể bị đảo lộn.''',
'Nhớ kiểm tra chân Mã trước mỗi nước đi.',[],['g4','e3'],None,.9),
('ĐI MÃ', 'Đi Mã phải có mục tiêu',
'''Trên bàn cờ, Mã Đỏ di chuyển để mở ra một góc tấn công mới. Sĩ Đen đáp lại bằng cách đổi vị trí trong cung. Đây chỉ là một chuỗi minh họa nước đi hợp lệ, chưa phải lời giải tối ưu của thế cờ. Hãy chú ý điều đang thay đổi: mỗi lần Mã đến một ô khác, tập hợp các ô nó khống chế cũng thay đổi theo. Nếu không đọc được sự thay đổi đó, người chơi sẽ chỉ thấy Mã đang chạy vòng quanh. Một kỳ thủ có mục đích rõ ràng sẽ hỏi: Mã từ đây đang đe dọa ô nào, và Tướng Đen còn những đường thoát nào?''',
'Đổi vị trí Mã là đổi cả bản đồ khống chế.',['g4e3','d1e2'],None,None,.7),
('ĐỌC PHÒNG THỦ', 'Sĩ không đi lung tung',
'''Sĩ chỉ đi chéo từng bước trong cung ba nhân ba. Vì số điểm đứng ít, trông Sĩ có vẻ dễ bị bắt; nhưng chính những đường chéo cố định ấy lại giúp nó giữ những ô rất quan trọng. Bạn hãy nhìn vị trí Sĩ lúc này, rồi quan sát Mã chuyển sang bên trái. Nếu Đen đưa Sĩ trở về một đường chéo khác, thế phòng thủ sẽ đổi ngay. Phần khó của cờ tàn không chỉ là tìm nước tấn công mạnh. Phần khó hơn là dự đoán đối phương sẽ chống đỡ ra sao, kể cả khi họ không đi theo nước chúng ta mong muốn.''',
'Luôn hỏi: nếu Sĩ đổi đường chéo thì sao?',['e3c2','e2d1'],None,None,.8),
('HỎI ĐÚNG', 'Đừng biến Mã thành quân đuổi bắt',
'''Bây giờ là câu hỏi tôi muốn bạn nhớ nhất. Nếu chỉ dùng Mã đuổi theo Sĩ, liệu Sĩ có thể đổi góc trong cung để tránh mãi không? Để giải một thế thắng, ta thường cần thêm sự khống chế từ quân Tướng. Tướng của ta không phải nhân vật đứng ngoài cuộc. Khi được đặt vào vị trí đúng và không vi phạm luật đối mặt hai Tướng, nó có thể hạn chế những đường mà Tướng đối phương muốn dùng. Còn Mã đảm nhận việc khóa các điểm thoát hoặc ép quân phòng thủ phải đổi vị trí. Đây là tư duy phối hợp, không phải mẹo đi một quân.''',
'Tướng và Mã phối hợp mới tạo được sức ép thực sự.',['c2e1','d1e2'],None,None,.8),
('THỬ THÁCH', 'Tạm dừng: bạn nhìn thấy gì?',
'''Hãy tạm dừng video vài giây và nhìn vào bàn cờ. Đừng cố đoán ngay một nước chiếu. Bạn chỉ cần trả lời hai câu. Một là: quân Mã đang khống chế những ô nào quanh cung Đen? Hai là: nếu Đen chuyển Sĩ về một đường chéo khác, Mã có thể đứng ở đâu để tiếp tục gây sức ép? Hãy nghĩ trong năm giây. Năm, bốn, ba, hai, một. Bây giờ xem Mã dịch sang một cánh khác. Không phải để khoe một nước cờ thần kỳ, mà để thấy thay đổi vị trí giúp chúng ta nhìn ra những ô khống chế mới.''',
'Tự gọi tên ô khống chế trước khi xem đáp án.',['e1g2','e2d1'],None,None,1.2),
('PHÂN TÍCH', 'Đường đẹp chưa chắc là đường thắng',
'''Chúng ta tiếp tục một nhịp Mã và Sĩ đổi vị trí. Bạn sẽ thấy quân Mã trở về vùng cũ. Chuỗi nước đi này không được đưa ra như một biến cưỡng bức bắt Sĩ; nó là phòng thí nghiệm trực quan để bạn rèn khả năng đọc thế. Nếu một video cờ tàn chỉ cho bạn những nước đi đẹp mà không kiểm chứng đáp trả của đối phương, bạn có thể học nhầm cả định thức. Khi đến các tập phân tích thực chiến, chúng ta sẽ dùng Pikafish và tài liệu cờ tàn để rà soát từng nhánh, nhất là những nước phòng thủ khó tìm.''',
'Một nước hay phải đứng vững trước cách chống đỡ tốt nhất.',['g2e3','d1e2'],None,None,.6),
('BA ĐIỂM NHỚ', 'Công thức tư duy ba bước',
'''Tôi xin tóm lại bài hôm nay bằng ba câu ngắn. Thứ nhất, xác định các ô Tướng Đen có thể đi đến; đó là bản đồ phòng thủ cần phá. Thứ hai, xem Tướng Đỏ có thể khống chế thêm những đường nào mà vẫn đảm bảo hai Tướng không nhìn thẳng nhau. Thứ ba, điều Mã đến ô phù hợp để ép đối phương rời thế an toàn, và luôn kiểm tra chân Mã. Bạn đừng cố thuộc hình ảnh của đúng một bàn cờ. Hãy ghi nhớ ba câu hỏi này. Khi gặp một vị trí khác, chúng sẽ giúp bạn bắt đầu phân tích một cách có phương pháp.''',
'Quan sát cung → phối hợp Tướng → chọn điểm đặt Mã.',['e3g4','e2d1'],None,None,.7),
('KẾT THÚC', 'Tập tiếp theo: tìm nước bắt Sĩ',
'''Trong tập này, chúng ta đã làm quen với cách nghĩ khi Mã đấu với đơn Sĩ. Ta biết sự khác biệt giữa một nước đi hợp lệ và một nước thắng thực sự. Ta cũng thấy vai trò của chân Mã, vùng khống chế và sự phối hợp với Tướng. Ở bài tiếp theo, chúng ta sẽ lấy một vị trí được kiểm chứng, nhìn các cách chống đỡ cụ thể của Đen và từng bước xây dựng phương án giành thắng lợi. Nếu thấy cách giảng này dễ hiểu, hãy để lại bình luận: đoạn nào bạn muốn tôi chiếu chậm hơn? Cảm ơn bạn đã xem Tinh Hoa Cờ Tàn. Tôi là Nguyễn Văn Sang, hẹn gặp lại ở tập sau.''',
'Đúng luật chưa đủ: còn phải đúng phương án thắng.',[],None,None,1.4),
]
obj={'id':'tap-0001','title':'ĐƠN MÃ ĐẤU ĐƠN SĨ — BÍ QUYẾT CỜ TÀN',
     'subtitle':'Bài 01  ·  Nhìn thế cờ để hiểu cách thắng',
     'fen':'4k4/3a5/9/9/6N2/9/9/9/9/3K5 w',
     'analysis_status':'illustrative_not_engine_verified',
     'verification_note':'Các nước chỉ minh họa nguyên lý và luật; không được công bố là PV hay biến thắng cưỡng bức.',
     'beats':[dict(label=label,headline=head,narration=narr,insight=insight,moves=moves,
                   **({'horse_leg':leg} if leg else {}),**({'spotlight':spot} if spot else {}),pause=pause)
              for label,head,narr,insight,moves,leg,spot,pause in beats]}
folder=Path(__file__).resolve().parents[1]/'episodes'
folder.mkdir(exist_ok=True)
(folder/'tap-0001.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
print('Wrote pilot with',len(beats),'segments;',sum(len(b['narration'].split()) for b in obj['beats']),'words')
