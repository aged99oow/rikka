#
# 六華（リッカ）1.2
# pict.py 2024/6/22
#
import pyxel
import rkfont
# HandName：六華(7),三連(3～5),一色(1～3),無双(9),輝光(5),三対(5,7,9,11),三色(3),立直,直撃
HN_NONE,HN_RIKKA,HN_SANREN,HN_ISSHIKI,HN_MUSOU,HN_KIKOU,HN_SANTSUI,HN_SANSHIKI = 0,101,102,103,104,105,106,107
RL_REACH,RL_RON,RL_10PT = 111,112,113  # Rule：立直,直撃,10点終了
AM_DRAW,AM_DISCARD,AM_WINNING = 301,302,303  # ActionMessage：ツモる,捨てる,勝つ

def textbox(x, y, txt, col=7, only_cnt=False):  # col：*0～*F, pip：$11～$66
    init_x = x
    init_col = col
    pips, pip1, pip2 = 0, 0, 0
    strs, lines = 1, 1
    for ch in txt:
        if col==-1:
            if ch=='*':
                col = init_col
            else:
                col = int(ch, 16)
            continue
        elif ch=='*':
            col = -1
            continue
        if pips==1:
            if ch=='$':
                pips = 0
            else:
                pip1 = int(ch)
                pips = 2
                continue
        elif pips==2:
            if not only_cnt:
                pip2 = int(ch)
                small_tile(x-4, y-1, pip1, pip2, thk=False)
            x += 8
            pips = 0
            continue
        elif ch=='$':
            pips = 1
            continue
        if ch=='\n':
            strs = max(strs, (x-init_x)//4)
            lines += 1
            x = init_x
            y += 12
        else:
            font_data = rkfont.FONT_DIC.get(ch)
            if font_data == None:
                x += 8
            else:
                if not only_cnt:
                    for dx, dy in zip(*[iter(font_data)]*2):
                        pyxel.pset(x+dx, y+dy, col)
                if ord(ch)<=0xff:
                    x += 4
                else:
                    x += 8
    if only_cnt:
        strs = max(strs, (x-init_x)//4)
        return strs, lines

def large_tile(x, y, n1, n2, vert=True, thk=1):  # Number1, Number2, Vertical, Thickness(-1,0,1)
    dy = 0
    if vert:  # 縦
        if 1<=n1<=6 and 1<=n2<=6:  # 表
            if thk<0:  # 厚み上
                pyxel.blt(x, y, 0, 128, 16, 15, 5, 1)
                dy = 4
            elif thk>0:  # 厚み下
                pyxel.blt(x, y+31, 0, 128, 24, 15, 5, 1)
            pyxel.blt(x, y+dy, 0, 16*n1, 0, 15, 16, 1)
            pyxel.blt(x, y+dy+16, 0, 16*n2, 16, 15, 16, 1)
            if n1==n2:
                pyxel.blt(x+6, y+dy+14, 0, 112, 0, 3, 3, 1)
        else:  # 裏
            if thk<0:  # 厚み上
                pyxel.blt(x, y, 0, 112, 16, 15, 5, 1)
                dy = 4
            elif thk>0:  # 厚み下
                pyxel.blt(x, y+31, 0, 112, 24, 15, 5, 1)
            pyxel.blt(x, y+dy, 0, 0, 0, 15, 32, 1)
    else:  # 横
        if 1<=n1<=6 and 1<=n2<=6:  # 表
            if thk<0:  # 厚み上
                pyxel.blt(x, y, 0, 176, 16, 31, 5, 1)
                dy = 4
            elif thk>0:  # 厚み下
                pyxel.blt(x, y+15, 0, 176, 24, 31, 5, 1)
            pyxel.blt(x, y+dy, 0, 32*n1, 32, 16, 16, 1)
            pyxel.blt(x+16, y+dy, 0, 32*n2+16, 48, 15, 16, 1)
            if n1==n2:
                pyxel.blt(x+14, y+dy+6, 0, 112, 0, 3, 3, 1)
        else:  # 裏
            if thk<0:  # 厚み上
                pyxel.blt(x, y, 0, 144, 16, 31, 5, 1)
                dy = 4
            elif thk>0:  # 厚み下
                pyxel.blt(x, y+dy+15, 0, 144, 26, 31, 5, 1)
            pyxel.blt(x, y+dy, 0, 0, 32, 31, 16, 1)

def mid_tile(x, y, n1, n2, vert=True, thk=1):  # Number1, Number2, Vertical, Thickness(-1,0,1)
    if vert:
        if 1<=n1<=6 and 1<=n2<=6:
            if thk<0:
                pyxel.blt(x, y-3, 0, 112, 64, 11, 4, 1)  # 厚み上
            elif thk>0:
                pyxel.blt(x, y+23, 0, 112, 68, 11, 3, 1)  # 厚み下
            pyxel.blt(x, y, 0, 16*n1, 48, 11, 12, 1)
            pyxel.blt(x, y+12, 0, 16*n2, 60, 11, 12, 1)
            if n1==n2:
                pyxel.blt(x+4, y+10, 0, 112, 48, 3, 3, 1)
        else:  # 裏
            if thk<0:
                pyxel.blt(x, y-3, 0, 112, 56, 11, 4, 1)  # 厚み上
            elif thk>0:
                pyxel.blt(x, y+23, 0, 112, 60, 11, 3, 1)  # 厚み下
            pyxel.blt(x, y, 0, 0, 48, 11, 24, 1)
    else:
        if 1<=n1<=6 and 1<=n2<=6:
            if thk<0:
                pyxel.blt(x, y-3, 0, 168, 80, 23, 4, 1)  # 厚み上
            elif thk>0:
                pyxel.blt(x, y+11, 0, 168, 84, 23, 3, 1)  # 厚み下
            pyxel.blt(x, y, 0, 24*n1, 72, 12, 12, 1)
            pyxel.blt(x+12, y, 0, 24*n2+12, 72, 11, 12, 1)
            if n1==n2:
                pyxel.blt(x+10, y+4, 0, 112, 192-144, 3, 3, 1)
        else:  # 裏
            if thk<0:
                pyxel.blt(x, y-3, 0, 168, 72, 23, 4, 1)  # 厚み上
            elif thk>0:
                pyxel.blt(x, y+11, 0, 168, 76, 23, 3, 1)  # 厚み下
            pyxel.blt(x, y, 0, 0, 72, 23, 12, 1)

def mid_stand(x, y, dlc, thk=False):  #  Direction(1,2,3), Thickness
    if dlc==1:
        if thk:
            pyxel.blt(x, y+11, 0, 128, 60, 6, 2, 1)
        pyxel.blt(x, y, 0, 128, 48, 6, 12, 1)
    elif dlc==2:
        if thk:
            pyxel.blt(x, y+6, 0, 128, 62, 11, 2, 1)
        pyxel.blt(x, y, 0, 128, 64, 11, 7, 1)
    elif dlc==3:
        if thk:
            pyxel.blt(x, y+11, 0, 136, 60, 6, 2, 1)
        pyxel.blt(x, y, 0, 136, 48, 6, 12, 1)

TM_STILE_V = {  # Vertical
    (1,1):( 8,88,0), (1,2):(16,88,0), (1,3):( 24,88,0), (1,4):( 32,88,0), (1,5):( 40,88,0), (1,6):( 48,88,0),
    (2,1):(16,88,1), (2,2):(56,88,0), (2,3):( 64,88,0), (2,4):( 72,88,0), (2,5):( 80,88,0), (2,6):( 88,88,0),
    (3,1):(24,88,1), (3,2):(64,88,1), (3,3):( 96,88,0), (3,4):(104,88,0), (3,5):(112,88,0), (3,6):(120,88,0),
    (4,1):(32,88,1), (4,2):(72,88,1), (4,3):(104,88,1), (4,4):(128,88,0), (4,5):(136,88,0), (4,6):(144,88,0),
    (5,1):(40,88,1), (5,2):(80,88,1), (5,3):(112,88,1), (5,4):(136,88,1), (5,5):(152,88,0), (5,6):(160,88,0),
    (6,1):(48,88,1), (6,2):(88,88,1), (6,3):(120,88,1), (6,4):(144,88,1), (6,5):(160,88,1), (6,6):(168,88,0),
}
TM_STILE_H = {  # Horizontal
    (1,1):(16,104,0), (1,2):( 32,104,0), (1,3):( 48,104,0), (1,4):( 64,104,0), (1,5):( 80,104,0), (1,6):( 96,104,0),
    (2,1):(32,104,1), (2,2):(112,104,0), (2,3):(128,104,0), (2,4):(144,104,0), (2,5):(160,104,0), (2,6):(176,104,0),
    (3,1):(48,104,1), (3,2):(128,104,1), (3,3):(  0,112,0), (3,4):( 16,112,0), (3,5):( 32,112,0), (3,6):( 48,112,0),
    (4,1):(64,104,1), (4,2):(144,104,1), (4,3):( 16,112,1), (4,4):( 64,112,0), (4,5):( 80,112,0), (4,6):( 96,112,0),
    (5,1):(80,104,1), (5,2):(160,104,1), (5,3):( 32,112,1), (5,4):( 80,112,1), (5,5):(112,112,0), (5,6):(128,112,0),
    (6,1):(96,104,1), (6,2):(176,104,1), (6,3):( 48,112,1), (6,4):( 96,112,1), (6,5):(128,112,1), (6,6):(144,112,0),
}
TM_STILE_D = {  # DIAGONAL
    (1,1):(16,120,0), (1,2):( 32,120,0), (1,3):( 48,120,0), (1,4):( 64,120,0), (1,5):( 80,120,0), (1,6):( 96,120,0),
    (2,1):(32,120,1), (2,2):(112,120,0), (2,3):(128,120,0), (2,4):(144,120,0), (2,5):(160,120,0), (2,6):(176,120,0),
    (3,1):(48,120,1), (3,2):(128,120,1), (3,3):(  0,136,0), (3,4):( 16,136,0), (3,5):( 32,136,0), (3,6):( 48,136,0),
    (4,1):(64,120,1), (4,2):(144,120,1), (4,3):( 16,136,1), (4,4):( 64,136,0), (4,5):( 80,136,0), (4,6):( 96,136,0),
    (5,1):(80,120,1), (5,2):(160,120,1), (5,3):( 32,136,1), (5,4):( 80,136,1), (5,5):(112,136,0), (5,6):(128,136,0),
    (6,1):(96,120,1), (6,2):(176,120,1), (6,3):( 48,136,1), (6,4):( 96,136,1), (6,5):(128,136,1), (6,6):(144,136,0),
}
def small_tile(x, y, n1, n2, dr=2, d=3, thk=True):  # Number1, Number2, Vertical/Horizontal/Diagonal0～3,ずれ0~5
    if dr==2:  # Vertical
        if 1<=n1<=6 and 1<=n2<=6:
            pos = TM_STILE_V[(n1, n2)]
            if thk:
                pyxel.blt(x+d+1, y+12, 0, 176, 92, 7, 3, 1)  # 厚み
            pyxel.blt(x+d+1, y, 0, pos[0], pos[1], 7, -13 if pos[2] else 13, 1)
        else:
            if thk:
                pyxel.blt(x+d+1, y+12, 0, 176, 88, 7, 3, 1)  # 厚み
            pyxel.blt(x+d+1, y, 0, 8-8, 88, 7, 13, 1)  # 裏面
    elif dr==0:  # Horizontal
        if 1<=n1<=6 and 1<=n2<=6:
            pos = TM_STILE_H[(n1, n2)]
            if thk:
                pyxel.blt(x, y+d+6, 0, 160, 116, 13, 3, 1)  # 厚み
            pyxel.blt(x, y+d, 0, pos[0], pos[1], -13 if pos[2] else 13, 7, 1)
        else:
            if thk:
                pyxel.blt(x, y+d+6, 0, 160, 112, 13, 3, 1)  # 厚み
            pyxel.blt(x, y+d, 0, 0, 104, 13, 7, 1)
    elif dr in (1,3):  # Diagonal
        if 1<=n1<=6 and 1<=n2<=6:
            pos = TM_STILE_D[(n1, n2)]
            if thk:
                pyxel.blt(x+d%3, y+d//3+7, 0, 160, 144, 12 if dr==3 else -12, 8, 1)  # 厚み
            pyxel.blt(x+d%3, y+d//3, 0, pos[0], pos[1], 12 if (dr==3)^pos[2] else -12, -13 if pos[2] else 13, 1)
        else:
            if thk:
                pyxel.blt(x+d%3, y+d//3+7, 0, 160, 136, 12 if dr==3 else -12, 8, 1)  # 厚み
            pyxel.blt(x+d%3, y+d//3, 0, 0, 120, 12 if dr==3 else -12, 13, 1)

def rotate(x, y):
    pyxel.blt(x, y, 0, 144, 0, 8, 8, 1)
def swap(x, y):
    pyxel.blt(x, y, 0, 152, 0, 8, 8, 1)
def discard(x, y):
    pyxel.blt(x, y, 0, 168, 0, 8, 4, 1)
def sort(x, y):
    pyxel.blt(x, y, 0, 176, 0, 16, 8, 1)

def actionmessage(x, y, msg, col=False):  # Message, colorful
    if msg==AM_DRAW:  # ツモる
        pyxel.blt(x, y, 0, 0, 184-8 if col else 168-8, 16, 12, 1)
    elif msg==AM_DISCARD:  # ステる
        pyxel.blt(x, y, 0, 16, 184-8 if col else 168-8, 16, 12, 1)
    elif msg==AM_WINNING:  # アガる
        pyxel.blt(x, y, 0, 32, 184-8 if col else 168-8, 16, 12, 1)

def handname(x, y, hn, col):  # handname, colorful
    if hn==HN_ISSHIKI:
        pyxel.blt(x, y, 0, 64, 184-8 if col else 168-8, 16, 12, 1)
    elif hn==HN_SANREN:
        pyxel.blt(x, y, 0, 80, 184-8 if col else 168-8, 16, 12, 1)
    elif hn==HN_RIKKA:
        pyxel.blt(x, y, 0, 96, 184-8 if col else 168-8, 16, 12, 1)
    elif hn==HN_SANSHIKI:
        pyxel.blt(x, y, 0, 112, 184-8 if col else 168-8, 16, 12, 1)
    elif hn==HN_MUSOU:
        pyxel.blt(x, y, 0, 128, 184-8 if col else 168-8, 16, 12, 1)
    elif hn==HN_SANTSUI:
        pyxel.blt(x, y, 0, 144, 184-8 if col else 168-8, 16, 12, 1)
    elif hn==HN_KIKOU:
        pyxel.blt(x, y, 0, 160, 184-8 if col else 168-8, 16, 12, 1)

def message(x, y, player, txt, col=7):
    n, row = textbox(0, 0, txt, only_cnt=True)
    if player==0:
        if row==1:
            pyxel.blt(x, y-16, 0, 192, 48, 8, 16, 1)
            for i in range(n):
                pyxel.blt(x+8+4*i, y-16, 0, 200, 48, 4, 16, 1)
            pyxel.blt(x+8+4*n, y-16, 0, 204, 48, 2, 16, 1)
        else:
            pyxel.blt(x, y-16, 0, 192, 96, 8, 16, 1)
            for r in range(row-2):
                pyxel.blt(x, y-16-12-12*r, 0, 192, 80, 8, 12, 1)
            pyxel.blt(x, y-16-12-12*(row-2), 0, 192, 64, 8, 12, 1)
            for i in range(n):
                pyxel.blt(x+8+4*i, y-16, 0, 200, 96, 4, 16, 1)
                for r in range(row-2): 
                    pyxel.blt(x+8+4*i, y-16-12-12*r, 0, 200, 80, 4, 12, 1)
                pyxel.blt(x+8+4*i, y-16-12-12*(row-2), 0, 200, 64, 4, 12, 1)
            pyxel.blt(x+8+4*n, y-16, 0, 204, 96, 2, 16, 1)
            for r in range(row-2): 
                pyxel.blt(x+8+4*n, y-16-12-12*r, 0, 204, 80, 2, 12, 1)
            pyxel.blt(x+8+4*n, y-16-12-12*(row-2), 0, 204, 64, 2, 12, 1)
        textbox(x+8, y-1-12*row, txt, col)
    elif player==1:
        if row==1:
            pyxel.blt(x, y, 0, 208, 48, 8, 16, 1)
            for i in range(n):
                pyxel.blt(x+8+4*i, y, 0, 216, 48, 4, 16, 1)
            pyxel.blt(x+8+4*n, y, 0, 220, 48, 2, 16, 1)
        else:
            pyxel.blt(x, y, 0, 208, 64, 8, 16, 1)
            for r in range(row-2):
                pyxel.blt(x, y+16+12*r, 0, 208, 80, 8, 12, 1)
            pyxel.blt(x, y+16+12*(row-2), 0, 208, 96, 8, 12, 1)
            for i in range(n):
                pyxel.blt(x+8+4*i, y, 0, 216, 64, 4, 16, 1)
                for r in range(row-2): 
                    pyxel.blt(x+8+4*i, y+16+12*r, 0, 216, 80, 4, 12, 1)
                pyxel.blt(x+8+4*i, y+16+12*(row-2), 0, 216, 96, 4, 12, 1)
            pyxel.blt(x+8+4*n, y, 0, 220, 64, 2, 16, 1)
            for r in range(row-2): 
                pyxel.blt(x+8+4*n, y+16+12*r, 0, 220, 80, 2, 12, 1)
            pyxel.blt(x+8+4*n, y+16+12*(row-2), 0, 220, 96, 2, 12, 1)
        textbox(x+8, y+3, txt, col)
    elif player==2:
        if row==1:
            pyxel.blt(x-8, y, 0, 232, 48, 8, 16, 1)
            for i in range(n):
                pyxel.blt(x-8-4-4*i, y, 0, 228, 48, 4, 16, 1)
            pyxel.blt(x-8-2-4*n, y, 0, 226, 48, 2, 16, 1)
        else:
            pyxel.blt(x-8, y, 0, 232, 64, 8, 16, 1)
            for r in range(row-2):
                pyxel.blt(x-8, y+16+12*r, 0, 232, 80, 8, 12, 1)
            pyxel.blt(x-8, y+16+12*(row-2), 0, 232, 96, 8, 12, 1)
            for i in range(n):
                pyxel.blt(x-8-4-4*i, y, 0, 228, 64, 4, 16, 1)
                for r in range(row-2): 
                    pyxel.blt(x-8-4-4*i, y+16+12*r, 0, 228, 80, 4, 12, 1)
                pyxel.blt(x-8-4-4*i, y+16+12*(row-2), 0, 228, 96, 4, 12, 1)
            pyxel.blt(x-8-2-4*n, y, 0, 226, 64, 2, 16, 1)
            for r in range(row-2): 
                pyxel.blt(x-8-2-4*n, y+16+12*r, 0, 226, 80, 2, 12, 1)
            pyxel.blt(x-8-2-4*n, y+16+12*(row-2), 0, 226, 96, 2, 12, 1)
        textbox(x-7-4*n, y+3, txt, col)
    elif player==3:
        if row==1:
            pyxel.blt(x-8, y-16, 0, 248, 48, 8, 16, 1)
            for i in range(n):
                pyxel.blt(x-8-4-4*i, y-16, 0, 244, 48, 4, 16, 1)
            pyxel.blt(x-8-2-4*n, y-16, 0, 242, 48, 2, 16, 1)
        else:
            pyxel.blt(x-8, y-16, 0, 248, 96, 8, 16, 1)
            for r in range(row-2):
                pyxel.blt(x-8, y-16-12-12*r, 0, 248, 80, 8, 12, 1)
            pyxel.blt(x-8, y-16-12-12*(row-2), 0, 248, 64, 8, 12, 1)
            for i in range(n):
                pyxel.blt(x-8-4-4*i, y-16, 0, 244, 96, 4, 16, 1)
                for r in range(row-2): 
                    pyxel.blt(x-8-4-4*i, y-16-12-12*r, 0, 244, 80, 4, 12, 1)
                pyxel.blt(x-8-4-4*i, y-16-12-12*(row-2), 0, 244, 64, 4, 12, 1)
            pyxel.blt(x-8-2-4*n, y-16, 0, 242, 96, 2, 16, 1)
            for r in range(row-2): 
                pyxel.blt(x-8-2-4*n, y-16-12-12*r, 0, 242, 80, 2, 12, 1)
            pyxel.blt(x-8-2-4*n, y-16-12-12*(row-2), 0, 242, 64, 2, 12, 1)
        textbox(x-7-4*n, y-1-12*row, txt, col)

def chara(x, y, n, colorful=False, left=True):
    pyxel.blt(x, y, 0, n*16, 224 if colorful else 240, 16 if left else -16, 16, 1)

def addrule(x, y):
    pyxel.blt(x, y, 0, 112, 192, 40, 12, 1)  # 追加ルール

def rule(x, y, rl, col=True):
    if rl==RL_REACH:  # 立直
        pyxel.blt(x, y, 0, 176, 176 if col else 160, 16, 12, 1)
    elif rl==RL_RON:  # 直撃
        pyxel.blt(x, y, 0, 192, 176 if col else 160, 16, 12, 1)
    elif rl==RL_10PT:  # 終了
        if col:
            pyxel.blt(x, y, 0, 32, 208, 32, 12, 1)
            pyxel.blt(x+4, y+13, 0, 64, 208, 24, 12, 1)
        else:
            pyxel.blt(x+9, y, 0, 32, 192, 14, 12, 1)
            pyxel.blt(x+4, y+13, 0, 64, 192, 24, 12, 1)

def start(x, y):
    pyxel.blt(x, y, 0, 112, 208, 24, 12, 1)

def startplayer(x, y, col=True):
    pyxel.blt(x, y, 0, 208, 16 if col else 24, 6, 6, 1)

def crown(x, y):
    pyxel.blt(x, y, 0, 240, 224, 16, 16, 1)
