#!/usr/bin/env python3
"""Generate chapter 001 using an exhaustive four-piece ordinary-legal-move solver.
No proof of official Xiangqi long-check/long-chase repetition restrictions.
"""
import json
from pathlib import Path
from src.core import Board
from scripts.solve_masi import solve, fen_of, legal_moves

ROOT=Path(__file__).resolve().parents[1]
INITIAL='3k1a3/9/3N5/9/9/9/9/4K4/9/9 w'


def fen_board(b):
    rows=[]
    for y in range(10):
        line=''; blank=0
        for x in range(9):
            piece=b.cells.get((x,y))
            if piece:
                if blank:line+=str(blank);blank=0
                line+=piece
            else:blank+=1
        if blank:line+=str(blank)
        rows.append(line)
    return '/'.join(rows)+' '+('w' if b.turn=='red' else 'b')


def position_after(moves):
    b=Board.fen(INITIAL)
    for mv in moves:b.play(mv[:2],mv[2:])
    return fen_board(b)


def beaten(mvs, label, headline, narration, insight, pause=1.4, **extra):
    prefix,following=mvs
    beat={'label':label,'headline':headline,'narration':narration,'insight':insight,
          'fen':position_after(prefix),'moves':following,'pause':pause}
    beat.update(extra)
    return beat


def best_line(state,idx,res,dist,max_moves=35):
    steps=[]
    for _ in range(max_moves):
        choices=[]
        for move,next_state in legal_moves(state):
            if next_state=='CAPTURE_A':choices.append((move,-1,0,next_state))
            elif next_state=='CAPTURE_N':choices.append((move,0,0,next_state))
            elif next_state in idx:choices.append((move,res[idx[next_state]],dist[idx[next_state]],next_state))
        target=-1 if res[idx[state]]==1 else 1
        possible=[z for z in choices if z[1]==target]
        if not possible:break
        move,_,_,next_state=(min(possible,key=lambda z:z[2]) if target==-1 else max(possible,key=lambda z:z[2]))
        steps.append(move)
        if next_state=='CAPTURE_A':break
        state=next_state
    return steps


def main():
    states, idx, res, depth=solve()
    start=next(s for s in states if fen_of(*s)==INITIAL)
    assert res[idx[start]]==1 and depth[idx[start]]==13
    openings={m:n for m,n in legal_moves(start)}
    mainline=best_line(start,idx,res,depth)
    slow=['d2e0']+best_line(openings['d2e0'],idx,res,depth)
    alt=['d2c4']+best_line(openings['d2c4'],idx,res,depth)
    after_best=openings['d2f1']
    defend={m:n for m,n in legal_moves(after_best)}
    quick=['d2f1','d0d1']+best_line(defend['d0d1'],idx,res,depth)
    after_three=start
    for uci in mainline[:3]:
        after_three=next(n for mv,n in legal_moves(after_three) if mv==uci)
    black_choices={m:n for m,n in legal_moves(after_three)}
    short_a=mainline[:3]+['e1f0']+best_line(black_choices['e1f0'],idx,res,depth)
    short_b=mainline[:3]+['e1d2']+best_line(black_choices['e1d2'],idx,res,depth)
    assert len(mainline)==13 and len(slow)==21 and len(alt)==13 and len(quick)==9
    assert len(short_a)==7 and len(short_b)==9
    assert mainline[-1]=='g0f2' and quick[-1]=='c2e1'
    assert res[idx[openings['e7d7']]]==0
    beats=[
      beaten(([],[]),'THẾ CỜ','Đỏ đi trước — Mã bắt Sĩ?',
       'Đỏ còn Tướng và Mã. Đen còn Tướng và một Sĩ. Đỏ đi trước. Chữ cái a đến i là các cột từ trái sang phải; hàng không đến chín tính từ trên xuống. Mục tiêu của bài là buộc bắt Sĩ trong mô hình bốn quân theo luật đi thông thường. Mười ba và hai mươi mốt là tổng số lượt đi của cả hai bên đến khi bắt Sĩ, không phải khoảng cách chiếu bí. Bài này chưa xét luật lặp nước. Ta xét lần lượt từng biến.',
       'ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: BẮT SĨ',2.0,spotlight='d2'),
      beaten(([],mainline[:1]),'NƯỚC ĐẦU','1. Mã d2–f1',
       'Đỏ đi Mã từ d2 đến f1. Đây là một trong hai nước ngắn nhất để buộc bắt Sĩ ở thế này. Đen còn hai cách đi hợp lệ: đẩy Sĩ về trung tâm, hoặc đưa Tướng tiến một bước. Ta thử cách chống đỡ lâu hơn trước.',
       'ĐEN CÓ 2 CÁCH ĐÁP',1.3,horse_leg=['d2','f1']),
      beaten((mainline[:1],mainline[1:4]),'ĐEN CHỐNG ĐỠ','Sĩ về trung tâm',
       'Đen đi Sĩ f0 lên e1. Đỏ đưa Mã f1 đến e3. Sĩ tiếp tục sang f2. Nếu chưa nhìn ra nước tiếp theo, hãy dừng hình: Đỏ nên điều Tướng hay đi Mã? Ở đây, điều Tướng mới giữ được sức ép.',
       '1... Sĩ f0–e1  •  2... Sĩ e1–f2',1.7),
      beaten((mainline[:4],mainline[4:9]),'BIẾN CHÍNH','Đỏ dùng Tướng khóa đường',
       'Đỏ đi Tướng e7 sang f7, buộc Tướng Đen thay vị trí. Mã lần lượt đi e3 đến c2, rồi c2 đến e1. Lưu ý quân Mã không đuổi theo Sĩ một cách máy móc. Từng nước đều giữ những ô cần thiết để tiếp tục ép phòng thủ.',
       'TƯỚNG PHỐI HỢP MÃ',1.1),
      beaten((mainline[:9],mainline[9:]),'BIẾN CHÍNH','Bắt Sĩ sau 13 lượt quân',
       'Tướng Đen trở lại e0. Đỏ nhảy Mã e1 đến g0, dọa Sĩ ở f2. Nếu Đen lùi Tướng về d0, Mã g0 bắt ngay Sĩ f2. Toàn bộ biến này dài mười ba lượt đi, tính cả hai bên, khi Đen chống đỡ lâu nhất trong mô hình.',
       '13 LƯỢT ĐI  •  BẮT ĐƯỢC SĨ',1.8,spotlight='f2'),
      beaten((mainline[:11],['e0f0','g0f2']),'CHỐNG ĐỠ KHÁC','Tướng sang f0 — vẫn mất Sĩ',
       'Trước nước bắt Sĩ cuối, Đen còn một đường dùng Tướng từ e0 sang f0. Nhưng quân Sĩ vẫn nằm ở f2. Đỏ đi Mã g0 bắt f2. Cũng chỉ một nước là mất Sĩ. Đen đã hết cách phòng thủ.',
       'TƯỚNG e0–f0  •  MÃ g0×f2',1.2),
      beaten((mainline[:11],['f2e1','g0e1']),'CHỐNG ĐỠ KHÁC','Sĩ lui e1 — cũng bị bắt',
       'Nếu thay vì đi Tướng, Đen đưa Sĩ từ f2 trở về e1 thì sao? Đỏ đi Mã g0 bắt ngay Sĩ e1. Đây là nhánh thứ ba. Dù Đen chọn Tướng sang trái, sang phải, hay rút Sĩ, kết quả đều như nhau: mất Sĩ ngay.',
       'SĨ f2–e1  •  MÃ g0×e1',1.2),
      beaten((mainline[:3],short_a[3:]),'SĨ ĐI SAI','Sĩ về f0 — mất sau 7 lượt',
       'Quay lại khi Đỏ vừa đưa Mã lên e3, Đen không sang f2 mà rút Sĩ từ e1 về f0. Đỏ nhảy Mã đến g2, Đen đưa Tướng xuống d1, Đỏ bắt Sĩ ở f0. Tính từ đầu chỉ bảy lượt. Đen chống đỡ sai nên mất Sĩ rất nhanh.',
       'SĨ e1–f0  •  MẤT SAU 7 LƯỢT',1.3),
      beaten((mainline[:3],short_b[3:]),'SĨ ĐI SAI','Sĩ sang d2 — mất sau 9 lượt',
       'Cũng vị trí ấy, nếu Đen đi Sĩ e1 sang d2 thì Đỏ đưa Mã đến c2. Đen tiến Tướng d1, Đỏ điều Tướng lên e8. Sĩ phải về e1, Đỏ dùng Mã c2 bắt Sĩ. Tổng cộng chín lượt. Vẫn không kéo dài được như Sĩ sang f2.',
       'SĨ e1–d2  •  MẤT SAU 9 LƯỢT',1.3),
      beaten((mainline[:1],quick[1:5]),'ĐEN ĐI YẾU','Tướng lên — mất Sĩ sớm',
       'Quay lại sau Mã d2 đến f1. Nếu Đen không chuyển Sĩ mà đi Tướng d0 đến d1, Đỏ lập tức Mã f1 đến e3. Đen tiến Tướng e1. Đỏ điều Tướng e7 sang d7. Cách chống đỡ này không giữ được Sĩ lâu bằng phương án trước.',
       'ĐEN: d0–d1  •  THUA NHANH HƠN',1.2),
      beaten((quick[:5],quick[5:]),'ĐEN ĐI YẾU','Mã bắt Sĩ ở lượt thứ 9',
       'Đen lui Tướng về e0. Đỏ đưa Mã từ e3 tới c2. Sĩ buộc về e1. Mã c2 bắt Sĩ e1. Chỉ chín lượt đi, thay vì mười ba. Đó là khác biệt giữa chống đỡ tốt và chống đỡ yếu trong cùng một thế cờ.',
       '9 LƯỢT ĐI  •  BẮT ĐƯỢC SĨ',1.8),
      beaten(([],slow[:1]),'ĐỎ ĐI CHẬM','Mã d2–e0: bắt Sĩ chậm',
       'Nếu nước đầu Đỏ đi Mã d2 đến e0, Đỏ vẫn có thể buộc bắt Sĩ. Nhưng chống đỡ tốt nhất sẽ kéo dài hơn. Ta không nói nước này thua, mà nói nó thắng chậm hơn. Cùng xem Đen kéo dài cuộc chống đỡ như thế nào.',
       'THẮNG CHẬM: 21 LƯỢT',1.2),
      beaten((slow[:1],slow[1:7]),'THẮNG CHẬM','Sĩ cơ động, Mã phải vòng',
       'Đen chuyển Sĩ về e1, Đỏ phải đưa Mã từ e0 đến g1, rồi đến f3. Tướng Đen chen lên d1, Sĩ lui về f0. Đỏ lại đưa Mã tiến e5. So với nhánh trước, Mã phải vòng nhiều hơn mới tạo được thế khóa cung.',
       'MÃ PHẢI ĐI ĐƯỜNG VÒNG',1.0),
      beaten((slow[:7],slow[7:13]),'THẮNG CHẬM','Đỏ tiếp tục siết cung',
       'Đen đưa Tướng về d0. Mã đi e5 đến c4 rồi e3. Sĩ từ f0 đi e1 rồi f2. Cuối cùng Đỏ điều Tướng e7 sang f7. Tới đây thế cờ nhập lại dạng khống chế quen thuộc, nhưng Đỏ đã tốn thêm nhiều nước.',
       'KHÔNG SAI, NHƯNG TỐN NƯỚC',1.0),
      beaten((slow[:13],slow[13:]),'THẮNG CHẬM','Đến lượt 21 mới bắt Sĩ',
       'Từ đây, Đỏ đi Mã đến c2, rồi e1 và g0. Đen chống đỡ bằng cách chuyển Tướng qua lại. Cuối cùng Mã g0 bắt Sĩ f2. Đủ hai mươi mốt lượt đi. So sánh: chọn Mã d2 đến f1, chỉ cần mười ba lượt trong phương án chống đỡ lâu nhất.',
       '21 LƯỢT  SO VỚI  13 LƯỢT',1.7),
      beaten(([],alt[:5]),'CÁCH THẮNG KHÁC','Mã d2–c4 cũng hiệu quả',
       'Còn một nước thắng nhanh tương đương: Mã d2 đến c4. Đen đưa Sĩ về e1; Đỏ Mã c4 đến e3. Sĩ về f2 và Đỏ chuyển Tướng e7 sang f7. Sau đó thế cờ nhập lại nhánh chính. Vậy Đỏ không chỉ có một nước thắng.',
       'CÁCH KHÁC: CŨNG 13 LƯỢT',1.2),
      beaten(([],['e7d7','d0d1']),'NƯỚC SAI','Tướng e7–d7: không ép bắt Sĩ',
       'Nước sai ở thế đầu là đưa Tướng từ e7 sang d7. Đen chỉ cần đưa Tướng d0 xuống d1. Trong bảng tính bốn quân theo luật đi thông thường, Đỏ không còn đường buộc bắt Sĩ. Đây là khác biệt giữa nước không phạm luật và nước giữ được thế tất thắng.',
       'ĐỎ MẤT THẾ BUỘC BẮT SĨ',1.8),
      beaten(([],[]),'CHỐT BIẾN','13 — 21 — không ép bắt Sĩ',
       'Tóm lại, ở thế xuất phát này: Mã d2 đến f1 hoặc c4 bắt được Sĩ sau tối đa mười ba lượt đi trong mô hình. Mã d2 đến e0 cần đến hai mươi mốt lượt. Còn Tướng e7 đến d7 làm mất khả năng buộc bắt Sĩ. Hết tập một.',
       'f1 hoặc c4: 13  •  e0: 21  •  Kd7: không ép bắt Sĩ',2.1)
    ]
    obj={
      'id':'tap-0001',
      'title':'MÃ PHÁ ĐƠN SĨ — PHÂN TÍCH CÁC BIẾN',
      'subtitle':'Đỏ đi trước • Ép bắt Sĩ trong mô hình 4 quân; chưa xét luật lặp nước.',
      'fen':INITIAL,
      'analysis_status':'four_piece_retrograde_ordinary_moves',
      'verification_note':'Exhaustive 4-piece win/draw/loss retrograde to capturing black advisor under ordinary legal moves, checks and stalemate. Long-check and long-chase repetition adjudication NOT covered; 13/21 are plies to capture advisor against a delaying defender, not mate distances.',
      'beats':beats,
    }
    dst=ROOT/'episodes'/'tap-0001.json'
    dst.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Episode:',dst,'beats:',len(beats),'main/quick/slow:',len(mainline),len(quick),len(slow))

if __name__=='__main__':main()
