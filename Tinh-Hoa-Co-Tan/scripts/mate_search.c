#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define EMPTY '.'
#define NB 90

static int HORSE[NB][8][2]; static int HORSE_N[NB];
static int ELEPHANT[NB][4][2]; static int ELEPHANT_N[NB];
static int ADVISOR[NB][4]; static int ADVISOR_N[NB];
static int KING[NB][4]; static int KING_N[NB];
static int KNIGHT_ATTACK[NB][8][2]; static int KNIGHT_ATTACK_N[NB];

static inline int in_palace(int x, int y, int red){ return x>=3 && x<=5 && (red ? (y>=7 && y<=9) : (y>=0 && y<=2)); }
static inline int on_side(int y, int red){ return red ? y>=5 : y<=4; }

static void init_tables(void){
    for (int s=0;s<NB;s++){
        int x=s%9, y=s/9;
        static const int hd[8][2] = {{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};
        for (int i=0;i<8;i++){
            int nx=x+hd[i][0], ny=y+hd[i][1];
            if (nx<0||nx>=9||ny<0||ny>=10) continue;
            int legx = (hd[i][0]==2||hd[i][0]==-2) ? x + hd[i][0]/2 : x;
            int legy = (hd[i][1]==2||hd[i][1]==-2) ? y + hd[i][1]/2 : y;
            HORSE[s][HORSE_N[s]][0]=ny*9+nx;
            HORSE[s][HORSE_N[s]][1]=legy*9+legx;
            HORSE_N[s]++;
        }
        static const int ed[4][2] = {{2,2},{2,-2},{-2,2},{-2,-2}};
        for (int i=0;i<4;i++){
            int nx=x+ed[i][0], ny=y+ed[i][1];
            if (nx<0||nx>=9||ny<0||ny>=10) continue;
            ELEPHANT[s][ELEPHANT_N[s]][0]=ny*9+nx;
            ELEPHANT[s][ELEPHANT_N[s]][1]=(y+ed[i][1]/2)*9+(x+ed[i][0]/2);
            ELEPHANT_N[s]++;
        }
        static const int ad[4][2] = {{1,1},{1,-1},{-1,1},{-1,-1}};
        for (int i=0;i<4;i++){
            int nx=x+ad[i][0], ny=y+ad[i][1];
            if (nx<0||nx>=9||ny<0||ny>=10) continue;
            ADVISOR[s][ADVISOR_N[s]++]=ny*9+nx;
        }
        static const int kd[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        for (int i=0;i<4;i++){
            int nx=x+kd[i][0], ny=y+kd[i][1];
            if (nx<0||nx>=9||ny<0||ny>=10) continue;
            KING[s][KING_N[s]++]=ny*9+nx;
        }
    }
    for (int s=0;s<NB;s++){
        for (int i=0;i<HORSE_N[s];i++){
            int dest=HORSE[s][i][0], leg=HORSE[s][i][1];
            KNIGHT_ATTACK[dest][KNIGHT_ATTACK_N[dest]][0]=s;
            KNIGHT_ATTACK[dest][KNIGHT_ATTACK_N[dest]][1]=leg;
            KNIGHT_ATTACK_N[dest]++;
        }
    }
}

static int find_king(const char *b, int red){
    char t = red?'K':'k';
    for (int i=0;i<NB;i++) if (b[i]==t) return i;
    return -1;
}

static int facing(const char *b){
    int rk=find_king(b,1), bk=find_king(b,0);
    if (rk<0 || bk<0) return 0;
    if (rk%9 != bk%9) return 0;
    int x=rk%9;
    int lo=(rk/9<bk/9)?rk/9:bk/9, hi=(rk/9<bk/9)?bk/9:rk/9;
    for (int y=lo+1;y<hi;y++) if (b[y*9+x]!=EMPTY) return 0;
    return 1;
}

static int attacked(const char *b, int t, int by_red){
    int x=t%9, y=t/9;
    for (int i=0;i<KNIGHT_ATTACK_N[t];i++){
        int atk=KNIGHT_ATTACK[t][i][0], leg=KNIGHT_ATTACK[t][i][1];
        if (b[atk]==(by_red?'N':'n') && b[leg]==EMPTY) return 1;
    }
    for (int i=0;i<ELEPHANT_N[t];i++){
        int atk=ELEPHANT[t][i][0], eye=ELEPHANT[t][i][1];
        if (b[atk]==(by_red?'B':'b') && b[eye]==EMPTY && on_side(y,by_red)) return 1;
    }
    if (in_palace(x,y,by_red)){
        for (int i=0;i<ADVISOR_N[t];i++){
            if (b[ADVISOR[t][i]]==(by_red?'A':'a')) return 1;
        }
        for (int i=0;i<KING_N[t];i++){
            if (b[KING[t][i]]==(by_red?'K':'k')) return 1;
        }
    }
    char general = by_red?'K':'k';
    for (int step=-9; step<=9; step+=18){
        int s=t+step;
        while (s>=0 && s<NB && b[s]==EMPTY) s+=step;
        if (s>=0 && s<NB && b[s]==general) return 1;
    }
    char pawn = by_red?'P':'p';
    int behind = by_red ? y+1 : y-1;
    if (behind>=0 && behind<=9 && b[behind*9+x]==pawn) return 1;
    if (on_side(y, !by_red)){
        for (int dx=-1;dx<=1;dx+=2){
            int nx=x+dx;
            if (nx>=0 && nx<9 && b[y*9+nx]==pawn) return 1;
        }
    }
    return 0;
}

static void gen_legal(const char *b, int red, int (*moves)[2], int *mn){
    char w[NB]; memcpy(w,b,NB);
    *mn=0;
    for (int s=0;s<NB;s++){
        char c=w[s];
        if (c==EMPTY) continue;
        int isred = (c>='A' && c<='Z');
        if (isred != red) continue;
        int x=s%9, y=s/9;
        char t = (c>='a'&&c<='z') ? (char)(c-'a'+'A') : c;
        int dests[8]; int dn=0;
        switch(t){
            case 'K': for(int i=0;i<KING_N[s];i++) dests[dn++]=KING[s][i]; break;
            case 'A': for(int i=0;i<ADVISOR_N[s];i++) dests[dn++]=ADVISOR[s][i]; break;
            case 'B': for(int i=0;i<ELEPHANT_N[s];i++){ int d=ELEPHANT[s][i][0], eye=ELEPHANT[s][i][1]; if(w[eye]==EMPTY && on_side(d/9,red)) dests[dn++]=d; } break;
            case 'N': for(int i=0;i<HORSE_N[s];i++){ int d=HORSE[s][i][0], leg=HORSE[s][i][1]; if(w[leg]==EMPTY) dests[dn++]=d; } break;
            case 'P': {
                int fwd = red?-1:1;
                int ny=y+fwd;
                if (ny>=0 && ny<=9) dests[dn++]=ny*9+x;
                if (on_side(y, !red)) for(int dx=-1;dx<=1;dx+=2){ int nx=x+dx; if(nx>=0&&nx<9) dests[dn++]=y*9+nx; }
                break;
            }
            default: fprintf(stderr,"unsupported piece %c\n",c); exit(2);
        }
        for (int di=0;di<dn;di++){
            int d=dests[di];
            char dc=w[d];
            if (dc!=EMPTY){
                int disred = (dc>='A' && dc<='Z');
                if (disred==red) continue;
                char dt = (dc>='a'&&dc<='z') ? (char)(dc-'a'+'A') : dc;
                if (dt=='K') continue;
            }
            if ((t=='K'||t=='A') && !in_palace(d%9,d/9,red)) continue;
            char cap=w[d];
            w[d]=w[s]; w[s]=EMPTY;
            int ksq=find_king(w,red);
            int bad=0;
            if (ksq<0 || attacked(w,ksq,!red) || facing(w)) bad=1;
            w[s]=w[d]; w[d]=cap;
            if (bad) continue;
            moves[*mn][0]=s; moves[*mn][1]=d; (*mn)++;
        }
    }
}

#define HSIZE (1<<24)
typedef struct { uint64_t key; uint8_t win; uint8_t lose; uint8_t bf; uint8_t bt; } Entry;
static Entry *HT;
static uint64_t ZT[NB][10];

static int piece_index(char c){
    switch(c){
        case 'K': return 0; case 'A': return 1; case 'B': return 2; case 'N': return 3; case 'P': return 4;
        case 'k': return 5; case 'a': return 6; case 'b': return 7; case 'n': return 8; case 'p': return 9;
    }
    return -1;
}

static uint64_t zobrist(const char *b){
    uint64_t key=0;
    for (int i=0;i<NB;i++) if (b[i]!=EMPTY) key ^= ZT[i][piece_index(b[i])];
    if (key==0) key=0x9e3779b97f4a7c15ULL;
    return key;
}

static Entry *probe(uint64_t key){
    uint64_t h = key & (HSIZE-1);
    for(;;){
        Entry *e=&HT[h];
        if (e->key==key || e->key==0) return e;
        h=(h+1)&(HSIZE-1);
    }
}

static long long nodes=0, node_cap=0; static int aborted=0;
static inline void do_move(char *b,int s,int d){ b[d]=b[s]; b[s]=EMPTY; }

static int search(char *b, int k){
    if (k<=0) return 0;
    uint64_t key=zobrist(b);
    Entry *e=probe(key);
    if (e->key==key){
        if (e->win && k>=e->win) return 1;
        if (e->lose && k<=e->lose) return 0;
    }
    nodes++;
    if (node_cap && nodes>node_cap){ aborted=1; return 0; }

    int ms[256][2]; int mn=0; int score[256];
    gen_legal(b,1,ms,&mn);
    int bk=find_king(b,0);
    for (int i=0;i<mn;i++){
        int s=ms[i][0], d=ms[i][1];
        char cap=b[d];
        do_move(b,s,d);
        score[i] = attacked(b,bk,1)?0:(cap!=EMPTY?1:2);
        b[s]=b[d]; b[d]=cap;
    }
    for (int i=1;i<mn;i++){
        int ss=score[i], m0=ms[i][0], m1=ms[i][1];
        int j=i-1;
        while(j>=0 && score[j]>ss){ score[j+1]=score[j]; ms[j+1][0]=ms[j][0]; ms[j+1][1]=ms[j][1]; j--; }
        score[j+1]=ss; ms[j+1][0]=m0; ms[j+1][1]=m1;
    }

    for (int mi=0;mi<mn;mi++){
        int s=ms[mi][0], d=ms[mi][1];
        char cap=b[d];
        do_move(b,s,d);
        int bs[256][2]; int bn=0; int bscore[256];
        gen_legal(b,0,bs,&bn);
        if (bn==0){
            b[s]=b[d]; b[d]=cap;
            Entry *e2=probe(key); e2->key=key;
            if (!e2->win){ e2->win=1; e2->bf=s; e2->bt=d; }
            return 1;
        }
        if (k-1<=0){ b[s]=b[d]; b[d]=cap; continue; }
        for (int i=0;i<bn;i++){ bscore[i]=(b[bs[i][1]]!=EMPTY)?0:1; }
        for (int i=1;i<bn;i++){
            int ss=bscore[i], m0=bs[i][0], m1=bs[i][1];
            int j=i-1;
            while(j>=0 && bscore[j]>ss){ bscore[j+1]=bscore[j]; bs[j+1][0]=bs[j][0]; bs[j+1][1]=bs[j][1]; j--; }
            bscore[j+1]=ss; bs[j+1][0]=m0; bs[j+1][1]=m1;
        }
        int ok=1;
        for (int bi=0;bi<bn;bi++){
            int b0=bs[bi][0], b1=bs[bi][1];
            char bcap=b[b1];
            do_move(b,b0,b1);
            int r=search(b,k-1);
            b[b0]=b[b1]; b[b1]=bcap;
            if (!r){ ok=0; break; }
        }
        b[s]=b[d]; b[d]=cap;
        if (ok){
            Entry *e2=probe(key); e2->key=key;
            if (!e2->win || k<e2->win){ e2->win=k; e2->bf=s; e2->bt=d; }
            return 1;
        }
    }
    Entry *e2=probe(key); e2->key=key;
    if (!e2->lose || k>e2->lose) e2->lose=k;
    return 0;
}

static int dtm_red(char *b, int cap){
    for (int k=1;k<=cap;k++){
        if (search(b,k)) return k;
        if (aborted) return -1;
    }
    return 0;
}

static void name(int s, char out[3]){ out[0]='a'+s%9; out[1]='0'+s/9; out[2]=0; }

static void parse_fen(const char *fen, char *b){
    memset(b,EMPTY,NB);
    int x=0,y=0;
    for (const char *p=fen; *p && *p!=' '; p++){
        if (*p=='/'){ x=0; y++; continue; }
        if (*p>='1' && *p<='9'){ x += *p-'0'; continue; }
        if (x>=9){ fprintf(stderr,"rank overflow\n"); exit(2); }
        b[y*9+x]=*p; x++;
    }
}

int main(int argc, char **argv){
    init_tables();
    HT = calloc(HSIZE, sizeof(Entry));
    if (!HT){ fprintf(stderr,"alloc failed\n"); return 2; }
    uint64_t seed=0x243F6A8885A308D3ULL;
    for (int i=0;i<NB;i++) for (int j=0;j<10;j++){
        seed ^= seed<<13; seed ^= seed>>7; seed ^= seed<<17;
        ZT[i][j]=seed;
    }
    if (argc<3){ fprintf(stderr,"usage: %s moves <fen> <w|b> | dtm <fen> <cap> [nodecap]\n",argv[0]); return 2; }
    char b[NB];
    parse_fen(argv[2], b);

    if (strcmp(argv[1],"moves")==0){
        int red = (argv[3][0]=='w');
        int ms[256][2]; int mn=0;
        gen_legal(b,red,ms,&mn);
        for (int i=0;i<mn;i++){ char a[3],c[3]; name(ms[i][0],a); name(ms[i][1],c); printf("%s%s\n",a,c); }
        return 0;
    }

    if (strcmp(argv[1],"dtm")==0){
        int cap=atoi(argv[3]);
        node_cap = (argc>=5)? atoll(argv[4]) : 0;
        int d = dtm_red(b, cap);
        printf("DTM %d nodes %lld aborted %d\n", d, nodes, aborted);
        if (d>0 && !getenv("NOMAIN")){
            char cur[NB]; memcpy(cur,b,NB);
            int remaining=d; int ply=0;
            while (remaining>0 && ply<64){
                uint64_t key=zobrist(cur);
                Entry *e=probe(key);
                if (e->key!=key || !e->win){ printf("MAINLINE-FAIL\n"); break; }
                char f[3],t[3]; name(e->bf,f); name(e->bt,t);
                printf("RED %s%s (dtm %d)\n", f, t, e->win);
                do_move(cur, e->bf, e->bt);
                int bs[256][2]; int bn=0;
                gen_legal(cur,0,bs,&bn);
                if (bn==0){ printf("  -> MATE\n"); break; }
                int longest=-1, pick=-1;
                for (int i=0;i<bn;i++){
                    char cap=cur[bs[i][1]];
                    do_move(cur,bs[i][0],bs[i][1]);
                    int v = dtm_red(cur, cap);
                    cur[bs[i][0]]=cur[bs[i][1]]; cur[bs[i][1]]=cap;
                    char f2[3],t2[3]; name(bs[i][0],f2); name(bs[i][1],t2);
                    printf("  black %s%s (remaining %d)\n", f2,t2,v);
                    if (v>longest){ longest=v; pick=i; }
                }
                char f2[3],t2[3]; name(bs[pick][0],f2); name(bs[pick][1],t2);
                printf("BLACK %s%s\n", f2,t2);
                char cap=cur[bs[pick][1]];
                do_move(cur,bs[pick][0],bs[pick][1]);
                (void)cap;
                remaining=longest;
                ply++;
            }
        }
        return 0;
    }
    if (strcmp(argv[1],"root")==0){
        int cap=atoi(argv[3]);
        node_cap = (argc>=5)? atoll(argv[4]) : 0;
        int d = dtm_red(b, cap);
        printf("ROOT-DTM %d nodes %lld aborted %d\n", d, nodes, aborted);
        int ms[256][2]; int mn=0;
        gen_legal(b,1,ms,&mn);
        for (int i=0;i<mn;i++){
            char after[NB]; memcpy(after,b,NB);
            do_move(after,ms[i][0],ms[i][1]);
            int bs[256][2]; int bn=0;
            gen_legal(after,0,bs,&bn);
            int worst = (bn==0)?0:-1;
            int unknown=0;
            for (int j=0;j<bn;j++){
                char r[NB]; memcpy(r,after,NB);
                char cap=r[bs[j][1]];
                do_move(r,bs[j][0],bs[j][1]);
                int v=dtm_red(r,cap);
                if (v<=0){ unknown=1; worst=-1; break; }
                if (v>worst) worst=v;
            }
            char f[3],t[3]; name(ms[i][0],f); name(ms[i][1],t);
            if (unknown) printf("  %s%s -> UNKNOWN\n", f,t);
            else printf("  %s%s -> total %d\n", f,t, 1+worst);
        }
        return 0;
    }

    fprintf(stderr,"unknown cmd\n");
    return 2;
}
