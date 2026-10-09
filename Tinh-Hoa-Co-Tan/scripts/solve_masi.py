"""Small exact retrograde calculation for K+N vs k+a capture-Si objective.
This is NOT a certified Xiangqi endgame tablebase: repetition/chase rules not modeled.
Only states with four pieces and ordinary legal moves are enumerated.
"""
from collections import deque
from src.core import Board, sq

ADVISOR=((3,0),(5,0),(4,1),(3,2),(5,2))
R_KING=tuple((x,y) for x in range(3,6) for y in range(7,10))
B_KING=tuple((x,y) for x in range(3,6) for y in range(0,3))
SQUARES=tuple((x,y) for y in range(10) for x in range(9))

def fen_of(k,K,n,a,side):
    cells={k:'k', K:'K', n:'N', a:'a'}
    ranks=[]
    for y in range(10):
        run=0; rank=''
        for x in range(9):
            piece=cells.get((x,y))
            if piece:
                if run: rank+=str(run);run=0
                rank+=piece
            else:run+=1
        if run: rank+=str(run)
        ranks.append(rank)
    return '/'.join(ranks)+' '+('w' if side==0 else 'b')

def legal_moves(state):
    k,K,n,a,turn=state
    b=Board({k:'k',K:'K',n:'N',a:'a'}, 'red' if turn==0 else 'black')
    for start,p in tuple(b.cells.items()):
        if (p.isupper()) != (turn==0): continue
        for dst in SQUARES:
            if dst in b.cells and b.cells[dst].isupper()==p.isupper(): continue
            if not b.attacks(start,dst): continue
            prev=b.cells.pop(start)
            captured=b.cells.get(dst)
            if captured and captured.upper()=='K':
                b.cells[start]=prev; continue
            b.cells[dst]=prev
            invalid=b.in_check(b.turn)
            b.cells.pop(dst)
            b.cells[start]=prev
            if captured: b.cells[dst]=captured
            if invalid:continue
            move=sq(*start)+sq(*dst)
            if captured:
                # Horse captures advisor -> goal; black captures horse -> only kings -> draw.
                yield move, ('CAPTURE_A' if captured=='a' else 'CAPTURE_N')
            else:
                updated={'k':k,'K':K,'N':n,'a':a}
                updated[p]=dst
                yield move,(updated['k'],updated['K'],updated['N'],updated['a'],1-turn)

def solve():
    states=[]
    for k in B_KING:
      for K in R_KING:
       for a in ADVISOR:
        for n in SQUARES:
         if n in (k,K,a): continue
         b=Board({k:'k',K:'K',n:'N',a:'a'})
         if b.facing_generals():continue
         for turn in (0,1):
          # Previous mover cannot leave its own general under attack.
          if b.in_check('black' if turn==0 else 'red'):continue
          states.append((k,K,n,a,turn))
    index={s:i for i,s in enumerate(states)}
    parents=[[] for _ in states]
    degree=[0]*len(states)
    # status 1: winning current mover; -1: losing current mover; 0: unresolved draw.
    result=[0]*len(states)
    # Win in minimum plies, Loss in maximum plies; terminal goal and stalemate.
    depth=[0]*len(states)
    q=deque()
    for i,s in enumerate(states):
      for mv, nxt in legal_moves(s):
       if nxt=='CAPTURE_A':
        result[i]=1;depth[i]=1
       elif nxt=='CAPTURE_N':
        degree[i]+=1 # draw child
       elif nxt in index:
        j=index[nxt];parents[j].append(i);degree[i]+=1
      if result[i]==1:q.append(i)
      elif degree[i]==0:
        result[i]=-1;q.append(i)
    # Note: immediate win states are in queue and may be losing too if degree==0 but handled.
    while q:
      i=q.popleft()
      for p in parents[i]:
       if result[p]:continue
       if result[i]==-1:
        result[p]=1;depth[p]=depth[i]+1;q.append(p)
       else:
        degree[p]-=1
        depth[p]=max(depth[p],depth[i]+1)
        if degree[p]==0:
         result[p]=-1;q.append(p)
    return states,index,result,depth

if __name__=='__main__':
 import json,collections
 ss,idx,res,d=solve()
 print('STATES',len(ss),'WDL',dict(collections.Counter(res)), 'maxdist',max(d))
 starts=[]
 for s in ss:
  if s[-1]!=0:continue
  i=idx[s]
  if res[i]!=1 or not (6<=d[i]<=28):continue
  opts=[]
  for move,n in legal_moves(s):
   if n in idx:opts.append((move,res[idx[n]],d[idx[n]]))
   elif n=='CAPTURE_A':opts.append((move,-1,0))
   else:opts.append((move,0,0))
  wins=[o for o in opts if o[1]==-1]
  bad=[o for o in opts if o[1]==0]
  if wins and bad:
   starts.append((s,d[i],min(wins,key=lambda x:x[2]),bad[0],len(wins)))
 print('CANDIDATES',len(starts))
 for x in starts[:16]:
  print(fen_of(*x[0]),'dtm',x[1],'best',x[2], 'draw',x[3],'win-moves',x[4])
