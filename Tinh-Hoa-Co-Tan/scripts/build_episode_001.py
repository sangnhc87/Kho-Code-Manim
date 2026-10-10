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
       'Đỏ còn Tướng và Mã, Đen còn Tướng và một Sĩ khuyết. Đỏ đi trước. Mục tiêu của bài là khéo léo dùng Tướng và Mã phối hợp ép bắt Sĩ Đen. Chúng ta cùng phân tích các biến đi: nước nào bắt Sĩ nhanh nhất, nước nào thắng chậm, và nước đi sai lầm làm mất thế thắng.',
       'ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: BẮT SĨ',2.0,spotlight='d2'),
      beaten(([],mainline[:1]),'NƯỚC ĐẦU','1. Mã 6 tiến 4',
       'Nước đầu tiên, Đỏ đi Mã 6 tiến 4. Đây là một trong hai nước đi tối ưu nhất để ép bắt Sĩ ở thế này. Đứng trước nước này, Đen có hai cách đối phó: hoặc đưa Sĩ vào trung tâm, hoặc đưa Tướng tiến một bước. Ta cùng xét phương án Đen chống đỡ dẻo dai nhất trước.',
       'ĐEN CÓ 2 CÁCH ĐÁP',1.3,horse_leg=['d2','f1']),
      beaten((mainline[:1],mainline[1:4]),'ĐEN CHỐNG ĐỠ','Sĩ về trung tâm',
       'Đen đi Sĩ 6 tiến 5 vào tâm. Đỏ lập tức Mã 4 thoái 5 kiềm chế. Đen tiếp tục đưa Sĩ 5 tiến 6 ra góc. Lúc này, Đỏ nên điều Tướng hay đi Mã? Điểm mấu chốt ở đây: phải điều Tướng mới duy trì được sức ép khống chế.',
       '1... Sĩ 6 tiến 5  •  2... Sĩ 5 tiến 6',1.7),
      beaten((mainline[:4],mainline[4:9]),'BIẾN CHÍNH','Đỏ dùng Tướng khóa đường',
       'Đỏ đi Tướng 5 bình 4 khóa lộ, buộc Tướng Đen phải bình 5. Kế đó, Đỏ nhảy Mã 5 tiến 7. Đen lại phải chạy Tướng 5 bình 6. Đỏ tiếp tục Mã 7 tiến 5 chiếm trung lộ. Chú ý rằng quân Mã không đuổi theo Sĩ một cách vội vàng, mà từng bước chiếm giữ những điểm huyết mạch để ép cung.',
       'TƯỚNG PHỐI HỢP MÃ',1.1),
      beaten((mainline[:9],mainline[9:]),'BIẾN CHÍNH','Bắt Sĩ sau 13 hiệp',
       'Tướng Đen buộc phải bình 5. Đỏ tung đòn quyết định: Mã 5 tiến 3, đe dọa trực tiếp Sĩ Đen. Nếu Tướng Đen bình 4 tránh nước, Mã 3 lập tức thoái 4 bắt gọn Sĩ Đen. Toàn bộ biến chính này dài mười ba hiệp, khi Đen kiên cường chống đỡ lâu nhất.',
       '13 HIỆP ĐẤU  •  BẮT ĐƯỢC SĨ',1.8,spotlight='f2'),
      beaten((mainline[:11],['e0f0','g0f2']),'CHỐNG ĐỠ KHÁC','Tướng bình 6 — vẫn mất Sĩ',
       'Trước nước bắt Sĩ cuối, nếu Đen không bình Tướng sang 4 mà bình sang 6, thì Sĩ vẫn nằm trơ trọi. Đỏ chỉ việc thoái Mã 3 thoái 4 bắt Sĩ. Chỉ một nước là mất Sĩ, Đen đã hết cách phòng thủ.',
       'TƯỚNG 5 BÌNH 6  •  MÃ 3 THOÁI 4',1.2),
      beaten((mainline[:11],['f2e1','g0e1']),'CHỐNG ĐỠ KHÁC','Sĩ thoái 5 — cũng bị bắt',
       'Còn nếu thay vì đi Tướng, Đen đưa Sĩ 6 thoái 5 về tâm thì sao? Đỏ lập tức thoái Mã 3 thoái 5 bắt thẳng Sĩ. Dù Đen chạy Tướng hay thoái Sĩ, kết cục đều bị bắt Sĩ không lối thoát.',
       'SĨ 6 THOÁI 5  •  MÃ 3 THOÁI 5',1.2),
      beaten((mainline[:3],short_a[3:]),'SĨ ĐI SAI','Sĩ thoái 6 — mất sau 7 hiệp',
       'Quay lại thời điểm Đỏ vừa thoái Mã 4 thoái 5. Nếu Đen không tiến Sĩ mà lại thoái Sĩ 5 thoái 6, Đỏ lập tức nhảy Mã 5 tiến 3. Đen đưa Tướng 4 tiến 1, Đỏ liền đi Mã 3 tiến 4 bắt gọn Sĩ. Tính từ đầu chỉ bảy hiệp. Đen chống đỡ sai nên mất Sĩ rất nhanh.',
       'SĨ 5 THOÁI 6  •  MẤT SAU 7 HIỆP',1.3),
      beaten((mainline[:3],short_b[3:]),'SĨ ĐI SAI','Sĩ tiến 4 — mất sau 9 hiệp',
       'Cũng vị trí ấy, nếu Đen đi Sĩ 5 tiến 4 thì Đỏ đưa Mã 5 tiến 7. Đen tiến Tướng 4 tiến 1, Đỏ thoái Tướng 5 thoái 1. Sĩ phải thoái 4 thoái 5 về tâm, Đỏ dùng Mã 7 tiến 5 bắt Sĩ ngay. Tổng cộng chín hiệp, thua nhanh hơn biến chính.',
       'SĨ 5 TIẾN 4  •  MẤT SAU 9 HIỆP',1.3),
      beaten((mainline[:1],quick[1:5]),'ĐEN ĐI YẾU','Tướng lên — mất Sĩ sớm',
       'Quay lại sau nước đầu Mã 6 tiến 4. Nếu Đen không chuyển Sĩ mà đi Tướng 4 tiến 1, Đỏ lập tức thoái Mã 4 thoái 5. Đen bình Tướng 4 bình 5, Đỏ điều Tướng 5 bình 6 khóa cung. Cách chống đỡ này không giữ được Sĩ lâu bằng phương án trước.',
       'ĐEN: TƯỚNG 4 TIẾN 1  •  THUA NHANH HƠN',1.2),
      beaten((quick[:5],quick[5:]),'ĐEN ĐI YẾU','Mã bắt Sĩ ở hiệp thứ 9',
       'Đen thoái Tướng 5 thoái 1. Đỏ đưa Mã 5 tiến 7. Sĩ buộc phải tiến 6 tiến 5. Mã 7 tiến 5 bắt gọn Sĩ. Chỉ chín hiệp đấu, thay vì mười ba. Đó là khác biệt giữa chống đỡ tốt và chống đỡ yếu trong cùng một thế cờ.',
       '9 HIỆP ĐẤU  •  BẮT ĐƯỢC SĨ',1.8),
      beaten(([],slow[:1]),'ĐỎ ĐI CHẬM','Mã 6 tiến 5: bắt Sĩ chậm',
       'Nếu nước đầu Đỏ đi Mã 6 tiến 5 vào tâm, Đỏ vẫn có thể buộc bắt Sĩ. Nhưng đối phương chống đỡ tốt sẽ kéo dài hơn. Ta không nói nước này sai, mà nói nó thắng chậm hơn. Cùng xem Đen kéo dài cuộc chống đỡ như thế nào.',
       'THẮNG CHẬM: 21 HIỆP',1.2),
      beaten((slow[:1],slow[1:7]),'THẮNG CHẬM','Sĩ cơ động, Mã phải vòng',
       'Đen chuyển Sĩ 6 tiến 5, Đỏ phải thoái Mã 5 thoái 3, rồi thoái tiếp Mã 3 thoái 4. Tướng Đen tiến 4 tiến 1, Sĩ thoái 5 thoái 6. Đỏ lại đưa Mã 4 thoái 5. So với nhánh trước, Mã phải vòng nhiều hơn mới tạo được thế khóa cung.',
       'MÃ PHẢI ĐI ĐƯỜNG VÒNG',1.0),
      beaten((slow[:7],slow[7:13]),'THẮNG CHẬM','Đỏ tiếp tục siết cung',
       'Đen thoái Tướng 4 thoái 1. Mã nhảy Mã 5 tiến 7 rồi Mã 7 tiến 5. Sĩ từ 6 tiến 5 rồi tiến 6. Cuối cùng Đỏ điều Tướng 5 bình 4. Tới đây thế cờ nhập lại dạng khống chế quen thuộc, nhưng Đỏ đã tốn thêm nhiều hiệp.',
       'KHÔNG SAI, NHƯNG TỐN HIỆP',1.0),
      beaten((slow[:13],slow[13:]),'THẮNG CHẬM','Đến hiệp 21 mới bắt Sĩ',
       'Từ đây, Đỏ đi Mã tiến 7, tiến 5 rồi tiến 3. Đen chống đỡ bằng cách chuyển Tướng qua lại. Cuối cùng Mã 3 thoái 4 bắt gọn Sĩ. Đủ hai mươi mốt hiệp đấu. So sánh: chọn Mã 6 tiến 4, chỉ cần mười ba hiệp trong phương án chống đỡ lâu nhất.',
       '21 HIỆP  SO VỚI  13 HIỆP',1.7),
      beaten(([],alt[:5]),'CÁCH THẮNG KHÁC','Mã 6 thoái 7 cũng hiệu quả',
       'Còn một nước thắng nhanh tương đương: Mã 6 thoái 7. Đen đưa Sĩ 6 tiến 5; Đỏ nhảy Mã 7 tiến 5. Sĩ tiến 6 và Đỏ chuyển Tướng 5 bình 4. Sau đó thế cờ nhập lại nhánh chính. Như vậy Đỏ có tới hai cách đi tối ưu.',
       'CÁCH KHÁC: CŨNG 13 HIỆP',1.2),
      beaten(([],['e7d7','d0d1']),'NƯỚC SAI','Tướng 5 bình 6: không ép bắt Sĩ',
       'Nước sai ở thế đầu là vội đưa Tướng 5 bình 6. Đen chỉ cần đưa Tướng 4 tiến 1 chiếm cao điểm. Trong bảng tính bốn quân theo luật đi thông thường, Đỏ không còn đường buộc bắt Sĩ. Đây là khác biệt giữa nước không phạm luật và nước giữ được thế tất thắng.',
       'ĐỎ MẤT THẾ BUỘC BẮT SĨ',1.8),
      beaten(([],[]),'CHỐT BIẾN','13 — 21 — không ép bắt Sĩ',
       'Tóm lại, ở thế xuất phát này: Mã 6 tiến 4 hoặc Mã 6 thoái 7 bắt được Sĩ sau tối đa mười ba hiệp. Mã 6 tiến 5 cần đến hai mươi mốt hiệp. Còn vội đi Tướng 5 bình 6 làm mất khả năng buộc bắt Sĩ. Hết tập một.',
       'Mã 6.4 hoặc 6/7: 13  •  Mã 6.5: 21  •  Tướng bình 6: mất thế',2.1)
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
