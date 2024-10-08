#
# 六華（リッカ）1.3
# Rikka.py 2024/8/13
#
DRAW_GRID,GRID_LINE = False,10  # DEBUGグリッド
CONSOLEOUT = False  # DEBUGコンソール表示
P1_OPEN,P2_OPEN,P3_OPEN,RIVER_OPEN = False,False,False,False  # DEBUG手配表示
import pyxel
import json
import pict
# HandName：六華(7),三連(3～5),一色(1～3),無双(9),輝光(5),三対(5,7,9,11),三色(3),立直,直撃
HN_NONE,HN_RIKKA,HN_SANREN,HN_ISSHIKI,HN_MUSOU,HN_KIKOU,HN_SANTSUI,HN_SANSHIKI = 0,101,102,103,104,105,106,107
RL_REACH,RL_RON,RL_10PT = 111,112,113  # Rule：立直,直撃,10点終了
AM_DRAW,AM_DISCARD,AM_WINNING = 301,302,303  # ActionMessage：取る,捨てる,勝つ
# GAMING
WIDTH,HEIGHT = 16*9,16*10
OWN,P1,P2,P3 = 0,1,2,3
NEXT = {OWN:P1, P1:P2, P2:P3, P3:OWN}
DISABLE = -1
SZ_SMALL,SZ_MID,SZ_LARGE = 1,2,3  # Size
MAX_TILE = 42  # (6+5+4+3+2+1)*2
RIVER_LINE = 5
RIVER_NUM = RIVER_LINE*RIVER_LINE  # 25
CHARA_XY = {OWN:(2,16*7-2), P1:(4,4), P2:(16*7-3,2), P3:(16*8-6,16*6+6)}
MSG_XY = {OWN:(2+20,16*7-4), P1:(4+20,4+24), P2:(16*7-3,2+24), P3:(16*8-8,16*6+6)}
TILE_XY = {OWN:(16+8,16*7,24,112,16,0), P1:(8,28,1,28,0,12), P2:(96,8,96,1,-12,0), P3:(130,86,120,86,0,-12)}  # 立ち位置X,Y,倒し位置X,Y,dx,dy
RIVER_X,RIVER_Y = 16*2,16*2-4
ROT_BTN_DY,HN_BTN_X,HN_BTN_Y = 38,16*7+10,16*7+13
OP_HIDDEN,OP_STAND,OP_FACE,OP_BACK = -1,0,1,2  # Open：非表示-1,立ち0,表1,裏2
TA_COMMON,TA_RIKKA,TA_SANREN,TA_ISSHIKI,TA_MUSOU,TA_KIKOU,TA_SANTSUI = HN_NONE,HN_RIKKA,HN_SANREN,HN_ISSHIKI,HN_MUSOU,HN_KIKOU,HN_SANTSUI  # Tactic
CHARA_NAME = ('プレイヤー','プレイヤー','三対ピノキオ','三連ピーターパン','輝光人魚','無双桃太郎','輝光金太郎','六華の王様',
              'シャー六華ホームズ','無双赤ちゃん','一色悟空','三連法師','一色エイリアン','三対忍者')
CAHAR_TACTIC = (TA_COMMON,TA_COMMON,TA_SANTSUI,TA_SANREN,TA_KIKOU,TA_MUSOU,TA_KIKOU,TA_RIKKA,
                TA_RIKKA,TA_MUSOU,TA_ISSHIKI,TA_SANREN,TA_ISSHIKI,TA_SANTSUI)
# TITLE
RIKKA_BTN_X,RIKKA_BTN_Y = 16*6+6,16*2-4
RULE_BTN_XY = {HN_MUSOU:(16*5+4,16*5-4),HN_KIKOU:(16*5+4,16*6-4),HN_SANTSUI:(16*5+4,16*7-4),HN_SANSHIKI:(16*5+4,16*8-4),
               RL_REACH:(16*7+4,16*5-4),RL_RON:(16*7+4,16*6-4),RL_10PT:(16*7-4,16*7-2)}
START_BTN_X,START_BTN_Y = 16*6+2,16*9
# GAMEEND
CROWN_XY = {OWN:(16*4,16*6+6), P1:(16+2,16*3+6), P2:(16*4,16+4), P3:(16*7-1,16*3+4)}
# rev=[0];for i in range(6):;rev=rev+[i]+rev
SQ_REV = (0,0,1,0,2,0,1,0,3,0,1,0,2,0,1,0,4,0,1,0,2,0,1,0,3,0,1,0,2,0,1,0,5,0,1,0,2,0,1,0,3,0,1,0,2,0,1,0,4,0,1,0,2,0,1,0,3,0,1,0,2,0,1,0)  # Sequence
# [(x,y,z) for x in range(1,5) for y in range(x+1,6) for z in range(y+1,7)]
SQ_SANSHIKI = [(1,2,3),(1,2,4),(1,2,5),(1,2,6),(1,3,4),(1,3,5),(1,3,6),(1,4,5),(1,4,6),(1,5,6),
               (2,3,4),(2,3,5),(2,3,6),(2,4,5),(2,4,6),(2,5,6),(3,4,5),(3,4,6),(3,5,6),(4,5,6)]  # Squence Sanshiki
SQ_SANREN = ((0,1,2,3,4,5),(0,1,3,2,4,5),(0,2,3,1,4,5),(0,2,4,1,3,5))  # Sequence Sanren
ST_TITLE,ST_DEAL,ST_NEXT,ST_COM_PICK,ST_COM_PICK_MOVE,ST_COM_DISCARD,ST_COM_DISCARD_MOVE = 901,902,903,904,905,906,907  # Status
ST_PICK,ST_PICK_MOVE,ST_DISCARD,ST_DISCARD_MOVE,ST_JUDGE,ST_JUDGE_OPEN,ST_JUDGE_MOVE,ST_ROUNDEND,ST_GAMEEND = 908,909,910,911,912,913,914,915,916  # Status
# Message
MSG_HANDNAME = {HN_NONE:'なし',HN_RIKKA:'六華',HN_SANREN:'三連',HN_ISSHIKI:'一色',HN_MUSOU:'無双',HN_KIKOU:'輝光',HN_SANTSUI:'三対',HN_SANSHIKI:'三色'}
MSG_OWN_PICK = ('どれを取ろうか','どれを取りましょうか','どれにしますか','取りましょう')  # 順番が来た時（自動）
MSG_OWN_DISCARD = ('どれを捨てようか','どれを捨てましょうか','どれにしますか','捨てましょう')  # 取った後（自動）
MSG_OWN_WINORNOT = ('アガりましょう','やりましたね','完成です','完成ですね','完成しました','完成しましたね')  # 取った後（自動）
MSG_OWN_WINORDISCARD = ('アガりますか','完成ですがアガりますか','続けますか','続けましょう','完成ですが続けますか','高得点を狙いますか')  # 取った後（自動）
MSG_OWN_WIN = ('アガり','完成ですね','勝ち','アガりです','完成です','勝ちです')  # 完成（自動）
MSG_OWN_TSUIDE = ('ついでに完成','ついでにアガり','ついでに完成です','ついでにアガりです')  # ついでに完成（自動）
MSG_OWN_PICKONE = ('を取ろうか','を取りますか','を取りましょう','を取ろう','は必要ですね','は必要だね','これはいるね')  # 取る時（キャラクタークリック）
MSG_OWN_DISCARDONE = ('を捨てようか','を捨てますか','を捨てましょう','を捨てよう','これはいらないね')  # 捨てる時（キャラクタークリック）
MSG_OWN_WINONE = ('やったね','うまいですね','アガりましょう','アガろう','完成しましたね','完成です','完成ですね')  # 捨てる時（キャラクタークリック）
MSG_OWN_ROUNDWIN = ('おめでとう','やりましたね','うまくいきましたね','この調子でいきましょう','次も勝ちましょう','上手ですね')  # ラウンド終了勝ち（キャラクタークリック）
MSG_OWN_ROUNDLOSE = ('残念ですね','おしいですね','もう少しでしたね','次は勝ちますよ','勝負はこれからですよ')  #  ラウンド終了負け（キャラクタークリック）
MSG_OWN_GAMEWIN = ('おめでとう','おめでとうございます','お見事です','あなたの勝ちです','素晴らしいです','１位ですね')  #  ゲーム終了勝ち（キャラクタークリック）
MSG_OWN_GAMELOSE = ('残念でしたね','もう一回しましょう','次は勝ちますよ','いい勝負でした')  #  ゲーム終了負け（キャラクタークリック）

MSG_OPP_PICK_FACE = ('欲しいのはこれ','これが欲しかった','これこれ','まさにこれ','これがあれば','ほぼ完成')  # 取る表牌（自動）
MSG_OPP_PICK = ('さて','さてと','えーっと','よし','いいね','いいぞ','う～ん','これから','まだまだ','まあまあ','うんうん','そうそう','どうしよう','そうねぇ','えいっ')  # 取る（自動）
MSG_OPP_TSUMOGIRI = ('ツモ切りで','ツモ牌いらない','いらない牌だった','引きが悪い','ツモが悪い')  # ツモ切り（自動）
MSG_OPP_DISCARD = ('これだ','いいね','いらない','もう少し','いい感じ','まだまだ','これから','どうしよう')  # 捨てる（自動）
MSG_OPP_DISCARDBUTWIN = ('完成したけど','そろったけど','もう少し続けよう','様子をみよう','続けてみようかな','ついでに完成も狙って','アガれるけど','高得点を目指そう')  # 完成でも捨てる（自動）
MSG_OPP_WIN = ('アガり','勝ち','よし','やった','狙いどおり','完成','ラッキー','できあがり')  # アガり/ついでに完成（自動）
MSG_OPP_TSUIDE = ('ついでに完成','ついでにアガり','こちらも完成','こちらもアガり')  # ついでに完成（自動）
MSG_OPP_CHARA = ('楽しいですね','本気でいきますよ','負けませんよ','今回は勝ちます','手加減しません','これからです','調子いいです','真剣勝負で')  # （キャラクタークリック）
MSG_OPP_OPENING = ('序盤は様子見で','よろしくお願いします','よろしく','お願いします','始めが大事','いい牌がそろってます')  # 序盤（キャラクタークリック）
MSG_OPP_CLOSING = ('終盤ですね','そろそろ終わりですね','あきらめません','そろそろアガりかな','誰がアガりそう')  # 終盤（キャラクタークリック）
MSG_OPP_HAND_PRE = ('得意な役は','好きな役は','狙いは','目指すは','ゴールは','今回の狙いは')  # 得意役（キャラクタークリック）「～です」
MSG_OPP_HAND_POST = ('が得意です','を狙います','狙いで','狙いです','でアガりたい')  # 得意役（キャラクタークリック）
MSG_OPP_ROUNDWIN = ('次もアガります','やりました','うまくいきました','うれしいです','調子いいです','調子がよかった')  # ラウンド終了勝ち（キャラクタークリック）
MSG_OPP_ROUNDWIN_PRE = ('得意の','狙いどおり','狙いどおりの','狙いの','いつもの','今回も')  # ラウンド終了得意役勝ち（キャラクタークリック）「～です」
MSG_OPP_ROUNDLOSE = ('くやしいです','あと一歩でした','もう少しだったのに','次は勝ちます','ミスしました','うまくいきません','次にいきましょう')  #  ラウンド終了負け（キャラクタークリック）
MSG_OPP_GAMEWIN = ('１位です','次も勝ちます','うまくいきました','うれしいです','楽しいですね','楽しかったです','運がよかったです','運も実力のうちです','もう一回しましょう')  #  ゲーム終了勝ち（キャラクタークリック）
MSG_OPP_GAMELOSE = ('負けました','残念です','次は勝ちます','失敗でした','もう一回しましょう','出直します','運八技二ですから','もっと強くなりたい','いい勝負でした')  #  ゲーム終了負け（キャラクタークリック）

class Shooting:
    def __init__(self, x, y, width, height, rate=200):
        self.sx, self.sy, self.width, self.height = x, y, width, height
        self.x1, self.y1, self.x2, self.y2, self.c = 0, 0, 0, 0, 0
        self.rate, self.state = rate, 0
    def update(self):
        if self.state==0:
            if pyxel.rndi(1, self.rate)==1:
                if pyxel.rndi(0, 1)==0:
                    self.x1 = pyxel.rndi(self.sx, self.sx+self.width//3*2)
                    self.x2 = self.x1+10+pyxel.rndi(0, 20)
                else:
                    self.x1 = pyxel.rndi(self.sx+self.width//3, self.sx+self.width)
                    self.x2 = self.x1-10-pyxel.rndi(0, 20)
                self.y1, self.y2 = 0, 10+pyxel.rndi(0, 10)
                self.c = pyxel.rndi(13, 15)
                self.state = 1
        else:
            self.x1, self.x2 = self.x1+(self.x2-self.x1)//2, self.x2+(self.x2-self.x1)//2
            self.y1, self.y2 = self.y1+(self.y2-self.y1)//2, self.y2+(self.y2-self.y1)//2
            if self.y1>self.sy+self.height:
                self.state = 0
    def draw(self):
        if self.state==1:
            pyxel.line(self.x1, self.y1, self.x2, self.y2, self.c)

class Blinking:
    def __init__(self, x, y, width, height, rate=200):
        self.sx, self.sy, self.width, self.height = x, y, width, height
        self.tx, self.ty, self.tc = 0, 0, 0
        self.rate, self.state = rate, 0
    def update(self):
        if self.state==0:
            if pyxel.rndi(1, self.rate)==1:
                self.tx = pyxel.rndi(self.sx+3, self.sx+self.width-7)
                self.ty = pyxel.rndi(self.sy+3, self.sy+self.height-7)
                self.tc = pyxel.rndi(13, 15)
                self.state = 1
        else:
            self.state += 1
            if self.state>18:
                self.state = 0
    def draw(self):
        if self.state in (1,2,3,4,17,18):
            pyxel.line(self.tx-1, self.ty, self.tx+1, self.ty, self.tc)
            pyxel.line(self.tx, self.ty-1, self.tx, self.ty+1, self.tc)
        elif self.state in (5,6,14,15,16):
            pyxel.line(self.tx-2, self.ty, self.tx+2, self.ty, self.tc)
            pyxel.line(self.tx, self.ty-2, self.tx, self.ty+2, self.tc)
        elif self.state in (7,8,9,10,11,12,13):
            pyxel.line(self.tx-3, self.ty, self.tx+3, self.ty, self.tc)
            pyxel.line(self.tx, self.ty-3, self.tx, self.ty+3, self.tc)

class Star:
    def __init__(self, x, y, width, height, rate=200):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.rate = rate
        self.next = pyxel.rndi(rate-rate//10, rate+rate//10)
        self.stars = [[pyxel.rndi(self.x+3, self.x+self.width-7),pyxel.rndi(self.y+3, self.y+self.height-7),pyxel.rndi(1, 4),pyxel.rndi(1000,2000)] for _ in range(10)]
    def update(self):
        self.next -= 1
        if self.next<=0:
            nx = pyxel.rndi(self.x+3, self.x+self.width-7)
            ny = pyxel.rndi(self.y+3, self.y+self.height-7)
            nc = pyxel.rndi(1, 4)
            tm = pyxel.rndi(1000,2000)
            self.stars.append([nx, ny, nc, tm])
            self.next = pyxel.rndi(self.rate-self.rate//10, self.rate+self.rate//10)
    def draw(self):
        for i in reversed(range(len(self.stars))):
            self.stars[i][3] -= 1
            if self.stars[i][3]<=0:
                del self.stars[i]
            else:
                pyxel.line(self.stars[i][0]-1, self.stars[i][1],self.stars[i][0]+1,self.stars[i][1], self.stars[i][2])
                pyxel.line(self.stars[i][0], self.stars[i][1]-1,self.stars[i][0],self.stars[i][1]+1, self.stars[i][2])

class Confetti:  # 紙吹雪
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.conft = []
    def update(self):
        if pyxel.rndi(0,7)==0:
            self.conft.append([pyxel.rndi(self.x, self.x+self.width-2), self.y, pyxel.rndi(6, 15)])  # x,y,color
        for i in reversed(range(len(self.conft))):
            self.conft[i][0] += pyxel.rndi(-1, 1)
            self.conft[i][1] += 1
            if self.conft[i][1]>=self.y+self.height:
                del self.conft[i]
    def draw(self):
        for i in reversed(range(len(self.conft))):
            pyxel.rect(self.conft[i][0], self.conft[i][1], 2, 2, self.conft[i][2])

class Balloon:  # 吹き出し
    def __init__(self, x, y, player, txt, tm=30, col=7):
        self.x, self.y, self.player, self.txt, self.tm, self.col = x, y, player, txt, tm, col
    def update(self):
        self.tm -= 1
        return True if self.tm<0 else False
    def draw(self):
        pict.message(self.x, self.y, self.player, self.txt, self.col)

class River2hand:
    def __init__(self, x1, y1, x2, y2, pip, vert=True):  # FromX, FromY, ToX, ToY, Pip, Vertical
        self.x1, self.y1, self.x2, self.y2, self.pip, self.vert = x1+2, y1-4, x2+2, y2+4, pip, vert
        self.x, self.y = self.x1, self.y1
        self.cnt = 0
        self.intv = [0,1,2,9,15,20,24,27,29,30]
    def update(self):
        self.x = self.x1+((self.x2-self.x1)*self.intv[self.cnt])//30
        self.y = self.y1+((self.y2-self.y1)*self.intv[self.cnt])//30
        self.cnt += 1
        return True if self.cnt>=len(self.intv) else False
    def draw(self):
        pict.mid_tile(self.x, self.y, *self.pip, self.vert)

class River2hand_opp(River2hand):
    def __init__(self, x1, y1, x2, y2, pip, vert=True):  # FromX, FromY, ToX, ToY, Pip, Vertical
        self.x1, self.y1, self.x2, self.y2, self.pip, self.vert = x1+2, y1-4, x2, y2, pip, vert
        self.x, self.y = self.x1, self.y1
        self.cnt = 0
        self.intv = [0,1,2,9,15,20,24,27,29,30]

class Hand2river(River2hand):
    def __init__(self, x1, y1, x2, y2, pip, vert=True):  # FromX, FromY, ToX, ToY, Pip, Vertical
        self.x1, self.y1, self.x2, self.y2, self.pip, self.vert = x1+2, y1+4, x2+2, y2-4, pip, vert
        self.x, self.y = self.x1, self.y1
        self.cnt = 0
        self.intv = [0,1,2,9,15,20,24,27,29,30]

class App:
    def holddown(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, hold=70, repeat=1):
            if self.rept==0:
                self.rept = 1
            elif self.rept==1:
                self.rept = 2
                self.reveal = not self.reveal
                pyxel.play(3, 0 if self.reveal else 1)  # オープンモード切替え音
        else:
            self.rept = 0

    def dotset(self):  # 背景ドットセット
        self.dot = [[pyxel.rndi(0,WIDTH),pyxel.rndi(0,HEIGHT//2+10),pyxel.rndi(12,13)] for _ in range(30)]
        self.dot.extend([[pyxel.rndi(0,WIDTH),pyxel.rndi(HEIGHT//2-10,HEIGHT),pyxel.rndi(1,2)] for _ in range(30)])

    def ruleset(self):  # ルールセット
        self.rule_musou = True
        self.rule_kikou = True
        self.rule_santsui = True
        self.rule_sanshiki = True
        self.rule_reach = False
        self.rule_ron = False
        self.rule_10pt = True

    def tileset(self):  # 牌セット
        self.tile = [[0 for i in range(2)] for j in range(MAX_TILE)]
        n = 0
        for i in range(1,7):
            for j in range(i,7):
                self.tile[n][0] = i
                self.tile[n][1] = j
                n += 1
                self.tile[n][0] = i
                self.tile[n][1] = j
                n += 1

    def p_choice(self, s):  # pyxel_choice
        r = pyxel.rndi(0,len(s)-1)
        return s[r]

    def p_shuffle(self, s):  # pyxel_shuffle
        for i in reversed(range(len(s))):
            j = pyxel.rndi(0,i-1)
            s[i],s[j] = s[j],s[i]

    def random_rotate(self, s):  # ランダム牌回転
        for _ in range(len(s)*3):
            a = pyxel.rndi(0,len(s)-1)
            self.tile_rotate(s[a])  # 牌回転

    def roundstart(self):
        self.p_shuffle(self.tile)  # 牌シャッフル
        self.random_rotate(self.tile)  # ランダム牌回転
        self.round_n += 1
        self.turn = self.startplayer
        self.startplayer = NEXT[self.startplayer]
        self.win_handname = {OWN:HN_NONE, P1:HN_NONE, P2:HN_NONE, P3:HN_NONE}  # 確定役名
        self.handname_own, self.handscore_own = HN_NONE, 0
        self.handopen = {OWN:[OP_STAND]*6, P1:[OP_STAND]*6, P2:[OP_STAND]*6, P3:[OP_STAND]*6}  # 立ち
        self.addscore = {OWN:0, P1:0, P2:0, P3:0}
        self.hand = {OWN:[], P1:[], P2:[], P3:[]}
        self.obvi_hand = {OWN:[], P1:[], P2:[], P3:[]}  # 明らかな手牌
        self.dsp_river = [[DISABLE] for _ in range(RIVER_NUM)]  # len()=25
        self.river = []  # 全河牌 [目1,目2]×22, 表示河牌:dsp_river=[河牌番号0～21,回転0～3,ずれ0～5,オープン1]or[ENABLE]×RIVER_NUM(25)
        self.bgm_n = pyxel.rndi(1,len(self.bgm)-1)

    def gamestart(self):
        self.st = ST_TITLE
        self.dotset()  # 背景ドットセット
        self.tileset()  # 牌セット
        self.round_n = 0 # ラウンド数
        self.startplayer = self.p_choice([OWN,P1,P2,P3])
        self.dsp_river_n = DISABLE
        self.own_n = DISABLE
        self.winning_n = DISABLE
        chara_order = [i for i in range(2,14)]
        self.p_shuffle(chara_order)
        self.chara = {OWN:pyxel.rndi(0,1), P1:chara_order[0], P2:chara_order[1], P3:chara_order[2]}
        #self.chara[P1], self.chara[P3] = 10, 12  # __DEBUG__ プレイヤー
        self.tactic = {P1:CAHAR_TACTIC[self.chara[P1]], P2:CAHAR_TACTIC[self.chara[P2]], P3:CAHAR_TACTIC[self.chara[P3]]}
        self.win_list = []
        self.score = {OWN:0, P1:0, P2:0, P3:0}
        self.roundstart()

    def message_pick(self, p):  # 取るメッセージ, Player, self.pickedtileface
        pyxel.play(3, 5)  # メッセージ音
        if p==OWN:
            msg = self.p_choice(MSG_OWN_PICK)
        elif self.pickedtileface and pyxel.rndi(0,1)==0:  # 表牌ツモ
            msg = self.p_choice(MSG_OPP_PICK_FACE)
        else:
            msg = self.p_choice(MSG_OPP_PICK)
        self.balloon.append(Balloon(*MSG_XY[p], p, msg, tm=40 if p==OWN else 30))

    def message_discard(self, p, add_sc):  # 捨てるメッセージ, Player, Score 
        if p==OWN or pyxel.rndi(0,1)==0:
            pyxel.play(3, 5)  # メッセージ音
            if p==OWN:
                msg = self.p_choice(MSG_OWN_DISCARD if add_sc==0 else MSG_OWN_WINORDISCARD if add_sc<5 else MSG_OWN_WINORNOT)
            else:
                if self.discard_n==5 and pyxel.rndi(0,1)==0:
                    msg = self.p_choice(MSG_OPP_TSUMOGIRI)
                else:
                    msg = self.p_choice(MSG_OPP_DISCARD if add_sc==0 else MSG_OPP_DISCARDBUTWIN)
            self.balloon.append(Balloon(*MSG_XY[p], p, msg, tm=40 if p==OWN else 20))
            return True
        return False

    def message_win(self, p, cfm_hn, add_sc):  # アガるメッセージ, Player, HandName, Score
        pyxel.play(3, 5)  # メッセージ音
        msg = self.p_choice(MSG_OWN_WIN if p==OWN else MSG_OPP_WIN)+f'\n*A{MSG_HANDNAME[cfm_hn]}{add_sc}点'
        self.balloon.append(Balloon(*MSG_XY[p], p, msg, tm=50))

    def message_tsuide(self, p, cfm_hn, add_sc):  # ついでに完成メッセージ, Player, HandName, Score
        pyxel.play(3, 5)  # メッセージ音
        msg = self.p_choice(MSG_OWN_WIN+MSG_OWN_TSUIDE if p==OWN else MSG_OPP_WIN+MSG_OPP_TSUIDE)+f'\n*9{MSG_HANDNAME[cfm_hn]}{add_sc}点'
        self.balloon.append(Balloon(*MSG_XY[p], p, msg, tm=50))

    def tile_rotate(self, tl):  # 牌回転
        tl[0],tl[1] = tl[1],tl[0]

    def tile_swap(self, pl, t1, t2):  # 牌交換
        self.hand[pl][t1],self.hand[pl][t2] = self.hand[pl][t2],self.hand[pl][t1]

    def hand_sort(self, tl, row=1):  # 牌ソート
        if row==0:
            tl.sort(key=lambda x:(x[0],x[1]))
        elif row==1:
            tl.sort(key=lambda x:(x[1],x[0]))

    def hand_norm(self, hand):  # 回転正規化
        for tile in hand:
            if tile[0]<tile[1]:
                self.tile_rotate(tile)

    def chk_bonus(self, hand):  # 手配のボーナス牌の数
        bonus = 0
        for tl in hand:
            if tl[0]==tl[1]:
                bonus += 1
        return bonus

    def chk_hand(self, hand, tsuide=False):  # 役と得点
        hn, sc = HN_NONE, 0
        h1 = [x[:] for x in hand]
        bonus = self.chk_bonus(h1)  # 手配ボーナス牌
        self.hand_norm(h1)  # 回転正規化
        h2 = [x[:] for x in h1]
        self.hand_sort(h2)
        self.win_sequence = [x[:] for x in h2]
        if bonus==6:
            if self.rule_santsui and h2[0][1]==h2[1][1] and h2[2][1]==h2[3][1] and h2[4][1]==h2[5][1]:
                return HN_SANTSUI, 11  # 三対(5+6)
            if self.rule_musou and h2[0][1]==1 and h2[1][1]==2 and h2[2][1]==3 and h2[3][1]==4 and h2[4][1]==5 and h2[5][1]==6:
                return HN_MUSOU, 9  # 無双(9)
            if self.rule_kikou:
                return HN_KIKOU, 5  # 輝光(5)
        if self.rule_santsui and h2[0][0]==h2[1][0] and h2[0][1]==h2[1][1] and h2[2][0]==h2[3][0] and h2[2][1]==h2[3][1] and h2[4][0]==h2[5][0] and h2[4][1]==h2[5][1]:
            return HN_SANTSUI, 5+bonus  # 三対(5+bonus)
        if self.rule_sanshiki and tsuide and len({x for row in h2 for x in row})==3: # セット平坦化個数
            return HN_SANSHIKI, 5  # 三色(5)
        for i in SQ_REV:  # 順に回転
            h1[i][0],h1[i][1] = h1[i][1],h1[i][0]
            h2 = [x[:] for x in h1]
            self.hand_sort(h2)
            self.win_sequence = [x[:] for x in h2]
            if h2[0][1]==h2[1][1]==h2[2][1]==h2[3][1]==h2[4][1]==h2[5][1]:  # 下段同じ
                if h2[0][0]==1 and h2[1][0]==2 and h2[2][0]==3 and h2[3][0]==4 and h2[4][0]==5 and h2[5][0]==6:
                    return HN_RIKKA, 7  # 六華(7)
                else:
                    for sq in SQ_SANREN:
                        if h2[sq[0]][0]+2==h2[sq[1]][0]+1==h2[sq[2]][0] and h2[sq[3]][0]+2==h2[sq[4]][0]+1==h2[sq[5]][0]:
                            self.win_sequence = [h2[i] for i in sq]
                            return HN_SANREN, 3+bonus  # 三連(3～5)
                    return HN_ISSHIKI, 1+bonus  # 一色(1～3)
            if h2[0][1]==h2[1][1]==h2[2][1] and h2[3][1]==h2[4][1]==h2[5][1] and h2[0][0]+2==h2[1][0]+1==h2[2][0] and h2[3][0]+2==h2[4][0]+1==h2[5][0]:
                return HN_SANREN, 3+bonus  # 三連(3～5)
        return HN_NONE, 0

    def list_add(self, lst1, lst2, mul=1):  # リスト加算
        for i in range(len(lst1)):
            lst1[i] += lst2[i]*mul

    def thkg_musou(self, hand):  # 無双(9)アガり-1,聴牌2,一向聴1
        discard_cndi = [1]*len(hand)
        for i in range(1,7):
            for j,tile in enumerate(hand):
                if tile[0]==tile[1]==i:
                    discard_cndi[j] = 0
                    break
        if discard_cndi.count(0)==len(hand):  # アガり-1
            return [-1]*len(hand)
        if discard_cndi.count(0)==len(hand)-1:  # 聴牌2
            return [x*2 for x in discard_cndi]
        if discard_cndi.count(0)==len(hand)-2:  # 一向聴1
            return discard_cndi
        return [0]*len(hand) 

    def thkg_rikka(self, hand):  # 六華(7)アガり-1,聴牌2,一向聴1
        h = [x[:] for x in hand]
        self.hand_norm(h)  # 回転正規化
        for i in range(1,7):
            discard_cndi = [1]*len(h)
            for j in range(1,7):
                p1,p2 = (i,j) if i>j else (j,i)
                if [p1,p2] in h:
                    discard_cndi[h.index([p1,p2])] = 0
            if discard_cndi.count(0)==len(h):  # アガり-1
                return [-1]*len(h)
            if discard_cndi.count(0)==len(h)-1:  # 聴牌2
                return [x*2 for x in discard_cndi]
            if discard_cndi.count(0)==len(h)-2:  # 一向聴1
                return discard_cndi
        return [0]*len(h)

    def thkg_kikou(self, hand):  # 輝光(5)アガり-1,聴牌2,一向聴1／ボーナス1
        discard_cndi = [1]*len(hand)
        for i,tile in enumerate(hand):
            if tile[0]==tile[1]:
                discard_cndi[i]=0
        if discard_cndi.count(0)==len(hand):  # アガり-1
            return [-1]*len(hand),[0]*len(hand)
        if discard_cndi.count(0)==len(hand)-1:  # 聴牌2
            return [x*2 for x in discard_cndi],discard_cndi
        if discard_cndi.count(0)==len(hand)-2:  # 一向聴1
            return discard_cndi,discard_cndi
        return [0]*len(hand),discard_cndi

    def thkg_santsui(self, hand):  # 三対(5,7,9,11)高み-2,アガり-1,聴牌2,一向聴1
        discard_cndi = [1]*len(hand)
        h = [x[:] for x in hand]
        self.hand_norm(h)  # 回転正規化
        for i in range(len(h)-1):
            for j in range(i+1,len(h)):
                if h[i]==h[j]:
                    discard_cndi[i],discard_cndi[j] = 0,0
                    break
        if discard_cndi.count(0)==len(h):  # アガり-1
            return [-1 if h[0]==h[1] else -2 for h in hand]
        if discard_cndi.count(0)==len(h)-2:  # 聴牌2
            return [x*2 for x in discard_cndi]
        if discard_cndi.count(0)==len(h)-4:  # 一向聴1
            return discard_cndi
        return [0]*len(h)

    def thkg_sanren(self, hand):  # 三連(3～5)アガり-1,聴牌2,一向聴1／二連1
        chain = []
        chain3 = False
        for i,h1 in enumerate(hand):
            for j,h2 in enumerate(hand):
                if i==j:
                    continue
                if (h1[0]==h2[0] and h1[1]+2==h2[1]) or (h1[0]==h2[1] and h1[1]+2==h2[0]) or (h1[1]==h2[0] and h1[0]+2==h2[1]) or (h1[1]==h2[1] and h1[0]+2==h2[0]):  # 1つ跳び
                    chain.append({i,j})
                if (h1[0]==h2[0] and h1[1]+1==h2[1]) or (h1[0]==h2[1] and h1[1]+1==h2[0]):  # 2連続
                    chain.append({i,j})
                    for k,h3 in enumerate(hand):
                        if i==k or j==k:
                            continue
                        if (h1[0]==h3[0] and h1[1]+2==h3[1]) or (h1[0]==h3[1] and h1[1]+2==h3[0]):  # 3連続
                            chain3 = True
                            chain.append({i,j,k})
                            break
                    if h1[0]==h1[1]:
                        continue
                if (h1[1]==h2[0] and h1[0]+1==h2[1]) or (h1[1]==h2[1] and h1[0]+1==h2[0]):  # 2連続
                    chain.append({i,j})
                    for k,h3 in enumerate(hand):
                        if i==k or j==k:
                            continue
                        if (h1[1]==h3[0] and h1[0]+2==h3[1]) or (h1[1]==h3[1] and h1[0]+2==h3[0]):  # 3連続
                            chain3 = True
                            chain.append({i,j,k})
                            break
        if chain3:
            discard_cndi = [1]*len(hand)
            for i in range(len(chain)):
                if len(chain[i])==3:
                    for c in chain[i]:
                        if discard_cndi[c]==1:
                            discard_cndi[c] = 0
                    for j in range(len(chain)):
                        if i==j:
                            continue
                        cndi = list({0,1,2,3,4,5}-chain[i]-chain[j])
                        if len(cndi)==0:  # アガり-1
                            return [-1]*len(hand), [0]*len(hand)
                        elif len(cndi)==1:  # 聴牌2
                            discard_cndi[cndi[0]] = 2
        else:
            discard_cndi = [0]*len(hand)
        niren_cndi = [1]*len(hand)
        for c1 in chain:
            for c2 in c1:
                niren_cndi[c2] = 0
        return discard_cndi, niren_cndi

    def thkg_sanshiki(self, hand):  # 三色(5)聴牌2,一向聴1
        discard_cndi = [0]*len(hand)
        for c in SQ_SANSHIKI:
            sq_match = [1]*len(hand)
            for i,tile in enumerate(hand):
                if tile[0] in c and tile[1] in c:
                    sq_match[i] = 0
            if sq_match.count(0)==len(hand)-1:  # 聴牌2
                for i in range(len(hand)):
                    if sq_match[i]:
                        discard_cndi[i] = 2
            elif sq_match.count(0)==len(hand)-2:  # 一向聴1
                for i in range(len(hand)):
                    if sq_match[i] and discard_cndi[i]==0:
                        discard_cndi[i] = 1
        return discard_cndi

    def thkg_isshiki(self, hand):  # 一色(5)高み-2,アガり-1,聴牌2,一向聴1
        discard_cndi = [0]*len(hand)
        for c in range(1,7):
            sq_match = [1]*len(hand)
            for i,tile in enumerate(hand):
                if tile[0]==c or tile[1]==c:
                    sq_match[i] = 0
            if sq_match.count(0)==len(hand):  # アガり-1
                return [-1 if h[0]==h[1] else -2 for h in hand]
            if sq_match.count(0)==len(hand)-1:  # 聴牌2
                for i in range(len(hand)):
                    if sq_match[i]:
                        discard_cndi[i] = 2
            elif sq_match.count(0)==len(hand)-2:  # 一向聴1
                for i in range(len(hand)):
                    if sq_match[i] and discard_cndi[i]==0:
                        discard_cndi[i] = 1
        return discard_cndi

    def consoleout_text(self, txt):  # __DEBUG__
        if not CONSOLEOUT:
            return
        print(txt)

    def consoleout_discard(self, tac, sum_cndi, mul_musou=1, mul_rikka=1, mul_kikou=1, mul_santsui=1, mul_sanren=1, mul_sanshiki=1, mul_isshiki=1, mul_bonus=1, mul_niren=1):  # __DEBUG__
        if not CONSOLEOUT:
            return
        print(f'P{self.turn} ===== 捨てる（'+tac+'） =====')
        if self.rule_musou:
            if self.musou_cndi[0]>=0:
                print(f'無双9 {self.musou_cndi}×{mul_musou}')
            else:
                print(f'無双9 [      完成      ]×{mul_musou}')
        if self.rikka_cndi[0]>=0:
            print(f'六華7 {self.rikka_cndi}×{mul_rikka}')
        else:
            print('六華7 [      完成      ]')
        if self.rule_kikou:
            if self.kikou_cndi[0]>=0:
                print(f'輝光5 {self.kikou_cndi}×{mul_kikou}')
            else:
                print('輝光5 [      完成      ]')
        if self.rule_santsui:
            if self.santsui_cndi[0]>=0:
                print(f'三対5+{self.santsui_cndi}×{mul_santsui}')
            else:
                print('三対5+[      完成      ]')
        if self.sanren_cndi[0]>=0:
            print(f'三連3+{self.sanren_cndi}×{mul_sanren}')
        else:
            print('三連3+[      完成      ]')
        if self.rule_sanshiki:
            if self.sanshiki_cndi[0]>=0:
                print(f'三色3 {self.sanshiki_cndi}×{mul_sanshiki}')
            else:
                print('三色3 [      完成      ]')
        if self.isshiki_cndi[0]>=0:
            print(f'一色1+{self.isshiki_cndi}×{mul_isshiki}')
        else:
            print('一色1+[      完成      ]')
        print(f'輝き  {self.bonus_cndi}×{mul_bonus}')
        print(f'二連  {self.niren_cndi}×{mul_niren}')
        print('-----------------------------')
        print(f'合計  {sum_cndi}')

    def select_discard(self, cndi):
        discard = [i for i,m in enumerate(cndi) if m==max(cndi)]  # 捨てる牌番号
        return self.p_choice(discard) if discard else pyxel.rndi(0,5)

    def pickup_common(self, win_river_n):  # 取る戦略：基本
        if self.win_sc>=5:  # 無双(9)アガり,六華(7)アガり,輝光(5)アガり,三連(5)アガり,三対(5,7,9,11)アガり
            self.win_cfm = True
            return win_river_n
        pickup_cndi = list(set(self.pickup_musou1_cndi) | set(self.pickup_rikka1_cndi) | set(self.pickup_kikou1_cndi) | set(self.pickup_santsui1_cndi))
        if pickup_cndi:  # 無双(9)聴牌,六華(7)聴牌,輝光(5)聴牌,三対(5,7,9,11)聴牌
            if win_river_n!=DISABLE:
                pickup_cndi.append(win_river_n)
            return self.p_choice(pickup_cndi)
        if self.win_sc>=3:  # 三連(3,4)アガり,一色(3)アガり
            self.win_cfm = True
            return win_river_n
        pickup_cndi = list(set(self.pickup_sanren1_cndi) | set(self.pickup_isshiki1_cndi))
        if pickup_cndi:  # 三連(3～5)聴牌,一色(1～3)聴牌
            if win_river_n!=DISABLE:
                pickup_cndi.append(win_river_n)
            return self.p_choice(pickup_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # 一色(1)アガり
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  # 全て表

    def win_or_discard_common(self, hand):  # アガる／捨てる戦略：基本
        if self.win_sc>=5:  # 無双(9)アガり,六華(7)アガり,輝光(5)アガり,三連(5)アガり,三対(5,7,9,11)アガり
            return -1  # アガり
        if 2 in self.musou_cndi or 2 in self.rikka_cndi or 2 in self.kikou_cndi or 2 in self.santsui_cndi:  # 無双(9)聴牌,六華(7)聴牌,輝光(5)聴牌,三対(5,7,9,11)聴牌
            cndi = [1 if x==2 or y==2 or z==2 or w==2 else 0 for x,y,z,w in zip(self.musou_cndi,self.rikka_cndi,self.kikou_cndi,self.santsui_cndi)]
            self.consoleout_text(f'P{self.turn} 無双(9)聴牌,六華(7)聴牌,輝光(5)聴牌,三対(5,7,9,11)聴牌 {cndi}')  # __DEBUG__
            return self.select_discard(cndi)
        if self.win_sc>=3:  # 三連(3,4)アガり,一色(3)アガり
            return -1  # アガり
        if 2 in self.sanren_cndi or 2 in self.isshiki_cndi:  # 三連(3～5)聴牌,一色(1～3)聴牌
            cndi = [1 if x==2 or y==2 else 0 for x,y in zip(self.sanren_cndi,self.isshiki_cndi)]
            self.consoleout_text(f'P{self.turn} 三連(3～5)聴牌,一色(1～3)聴牌 {cndi}')  # __DEBUG__
            return self.select_discard(cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 4)
        if self.rikka_cndi[0]>=0:
            self.list_add(sum_cndi, self.rikka_cndi, 4)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi, 3)
        if self.rule_santsui and self.santsui_cndi[0]>=0:
            self.list_add(sum_cndi, self.santsui_cndi, 3)
        if self.sanren_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanren_cndi, 3)
        if self.rule_sanshiki and self.sanshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanshiki_cndi, 2)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi, 2)
        self.list_add(sum_cndi, self.bonus_cndi)
        self.list_add(sum_cndi, self.niren_cndi)
        self.consoleout_discard('基本', sum_cndi, 4, 4, 3, 3, 3, 2, 2, 1, 1)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def pickup_rikka(self, win_river_n):  # 取る戦略：六華(7)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_musou1_cndi:  # 無双(9)聴牌
            return self.p_choice(self.pickup_musou1_cndi)
        if self.pickup_rikka1_cndi:  # 六華(7)聴牌
            return self.p_choice(self.pickup_rikka1_cndi)
        if self.pickup_rikka2_cndi:  # 六華(7)一向聴
            return self.p_choice(self.pickup_rikka2_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_kikou1_cndi:  # 輝光(5)聴牌
            return self.p_choice(self.pickup_kikou1_cndi)
        pickup_cndi = list(set(self.pickup_sanren1_cndi) | set(self.pickup_isshiki1_cndi))
        if pickup_cndi:  # 三連(3～5)聴牌,一色(1～3)聴牌
            return self.p_choice(pickup_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # 三連(3)アガり,一色(1～3)アガり
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  # 全て表

    def win_or_dicard_rikka(self, hand):  # アガる／捨てる戦略：六華(7)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            return -1  # アガり
        if 2 in self.musou_cndi:  # 無双(9)聴牌
            return self.select_discard(self.musou_cndi)
        if 2 in self.rikka_cndi:  # 六華(7)聴牌
            return self.select_discard(self.rikka_cndi)
        if 1 in self.rikka_cndi:  # 六華(7)一向聴
            return self.select_discard(self.rikka_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            return -1  # アガり
        if 2 in self.kikou_cndi:  # 輝光(5)聴牌
            return self.select_discard(self.kikou_cndi)
        if 2 in self.sanren_cndi or 2 in self.isshiki_cndi:  # 三連(3～5)聴牌,一色(1～3)聴牌
            cndi = [1 if x==2 or y==2 else 0 for x,y in zip(self.sanren_cndi,self.isshiki_cndi)]
            self.consoleout_text(f'P{self.turn} 三連(3～5)聴牌,一色(1～3)聴牌 {cndi}')  # __DEBUG__
            return self.select_discard(cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 4)
        if self.rikka_cndi[0]>=0:
            self.list_add(sum_cndi, self.rikka_cndi, 5)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi, 3)
        if self.rule_santsui and self.santsui_cndi[0]>=0:
            self.list_add(sum_cndi, self.santsui_cndi, 3)
        if self.sanren_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanren_cndi, 4)
        if self.rule_sanshiki and self.sanshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanshiki_cndi, 2)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi, 3)
        self.list_add(sum_cndi, self.bonus_cndi)
        self.list_add(sum_cndi, self.niren_cndi, 2)
        self.consoleout_discard('六華', sum_cndi, 4, 5, 3, 3, 4, 2, 3, 1, 2)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def pickup_sanren(self, win_river_n):  # 取る戦略：三連(3～5)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_musou1_cndi:  # 無双(9)聴牌
            return self.p_choice(self.pickup_musou1_cndi)
        if self.pickup_rikka1_cndi:  # 六華(7)聴牌
            return self.p_choice(self.pickup_rikka1_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            self.win_cfm = True
            return win_river_n
        pickup_cndi = list(set(self.pickup_kikou1_cndi) | set(self.pickup_santsui1_cndi))
        if pickup_cndi:  # 輝光(5)聴牌+三対(5)聴牌
            return self.p_choice(pickup_cndi)
        if self.win_sc>=3:  # 三連(3)アガり,一色(3)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_sanren1_cndi:  # 三連(3～5)聴牌
            return self.p_choice(self.pickup_sanren1_cndi)
        if self.pickup_sanren2_cndi:  # 三連(3～5)一向聴
            return self.p_choice(self.pickup_sanren2_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # アガり一色(1,2)
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  #   # 全て表

    def win_or_discard_sanren(self, hand):  # アガる／捨てる戦略：三連(3～5)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            return -1  # アガり
        if 2 in self.musou_cndi:  # 無双(9)聴牌
            return self.select_discard(self.musou_cndi)
        if 2 in self.rikka_cndi:  # 六華(7)聴牌
            return self.select_discard(self.rikka_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            return -1  # アガり
        if 2 in self.kikou_cndi or 2 in self.santsui_cndi:  # 輝光(5)聴牌,三対(5)聴牌
            cndi = [1 if x==2 or y==2 else 0 for x,y in zip(self.kikou_cndi,self.santsui_cndi)]
            self.consoleout_text(f'P{self.turn} 輝光(5)聴牌,三対(5)聴牌 {cndi}')  # __DEBUG__
            return self.select_discard(cndi)
        if self.win_sc>=3:  # 三連(3)アガり,一色(3)アガり
            return -1  # アガり
        if 2 in self.sanren_cndi:  # 三連(3～5)聴牌
            return self.select_discard(self.sanren_cndi)
        if 1 in self.sanren_cndi:  # 三連(3～5)一向聴
            return self.select_discard(self.sanren_cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 4)
        if self.rikka_cndi[0]>=0:
            self.list_add(sum_cndi, self.rikka_cndi, 4)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi, 3)
        if self.rule_santsui and self.santsui_cndi[0]>=0:
            self.list_add(sum_cndi, self.santsui_cndi, 3)
        if self.sanren_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanren_cndi, 4)
        if self.rule_sanshiki and self.sanshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanshiki_cndi, 2)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi, 2)
        self.list_add(sum_cndi, self.bonus_cndi)
        self.list_add(sum_cndi, self.niren_cndi, 2)
        self.consoleout_discard('三連', sum_cndi, 4, 4, 3, 3, 4, 2, 2, 1, 2)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def pickup_isshiki(self, win_river_n):  # 取る戦略：一色(1～3)
        if self.win_sc>=7 or (self.win_hn==HN_ISSHIKI and self.win_sc>=2):  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり,一色(2,3)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_musou1_cndi:  # 無双(9)聴牌
            return self.p_choice(self.pickup_musou1_cndi)
        if self.pickup_rikka1_cndi:  # 六華(7)聴牌
            return self.p_choice(self.pickup_rikka1_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            self.win_cfm = True
            return win_river_n
        pickup_cndi = list(set(self.pickup_kikou1_cndi) | set(self.pickup_santsui1_cndi))
        if pickup_cndi:  # 輝光(5)聴牌+三対(5)聴牌
            return self.p_choice(pickup_cndi)
        if self.win_sc>=3:  # 三連(3)アガり,一色(3)アガり
            self.win_cfm = True
            return win_river_n
        pickup_cndi = list(set(self.pickup_sanren1_cndi) | set(self.pickup_isshiki1_cndi))
        if pickup_cndi:  # 三連(3～5)聴牌+一色(1～3)聴牌
            return self.p_choice(pickup_cndi)
        if self.pickup_isshiki2_cndi:  # 一色(1～3)一向聴
            return self.p_choice(self.pickup_isshiki2_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # アガり一色(1)
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  #   # 全て表

    def win_or_discard_isshiki(self, hand):  # アガる／捨てる戦略：一色(1～3)
        if self.win_sc>=7 or (self.win_hn==HN_ISSHIKI and self.win_sc>=2):  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり,一色(2,3)アガり
            return -1  # アガり
        if 2 in self.musou_cndi:  # 無双(9)聴牌
            return self.select_discard(self.musou_cndi)
        if 2 in self.rikka_cndi:  # 六華(7)聴牌
            return self.select_discard(self.rikka_cndi)
        if 1 in self.rikka_cndi:  # 六華(7)一向聴
            return self.select_discard(self.rikka_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            return -1  # アガり
        if 2 in self.kikou_cndi or 2 in self.santsui_cndi:  # 輝光(5)聴牌,三対(5)聴牌
            cndi = [1 if x==2 or y==2 else 0 for x,y in zip(self.kikou_cndi,self.santsui_cndi)]
            self.consoleout_text(f'P{self.turn} 輝光(5)聴牌,三対(5)聴牌 {cndi}')  # __DEBUG__
            return self.select_discard(cndi)
        if self.win_sc>=3:  # 三連(3)アガり,一色(3)アガり
            return -1  # アガり
        if 2 in self.sanren_cndi or 2 in self.isshiki_cndi:  # 三連(3～5)聴牌,一色(1～3)聴牌
            cndi = [1 if x==2 or y==2 else 0 for x,y in zip(self.sanren_cndi,self.isshiki_cndi)]
            self.consoleout_text(f'P{self.turn} 三連(3～5)聴牌,一色(1～3)聴牌 {cndi}')  # __DEBUG__
            return self.select_discard(cndi)
        if 1 in self.isshiki_cndi:  # 一色(1～3)一向聴
            return self.select_discard(self.isshiki_cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 4)
        if self.rikka_cndi[0]>=0:
            self.list_add(sum_cndi, self.rikka_cndi, 4)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi, 3)
        if self.rule_santsui and self.santsui_cndi[0]>=0:
            self.list_add(sum_cndi, self.santsui_cndi, 3)
        if self.sanren_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanren_cndi, 3)
        if self.rule_sanshiki and self.sanshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanshiki_cndi, 2)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi, 4)
        self.list_add(sum_cndi, self.bonus_cndi)
        self.list_add(sum_cndi, self.niren_cndi, 2)
        self.consoleout_discard('一色', sum_cndi, 4, 4, 3, 3, 3, 2, 4, 1, 2)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def pickup_musou(self, hand_bonus, win_river_n):  # 取る戦略：無双(9)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_musou1_cndi:  # 無双(9)聴牌
            return self.p_choice(self.pickup_musou1_cndi)
        if self.pickup_rikka1_cndi:  # 六華(7)聴牌
            return self.p_choice(self.pickup_rikka1_cndi)
        if self.pickup_musou2_cndi:  # 無双(9)一向聴
            return self.p_choice(self.pickup_musou2_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_kikou1_cndi:  # 輝光(5)聴牌
            return self.p_choice(self.pickup_kikou1_cndi)
        bonus_num = hand_bonus+len(self.pickup_bonus_cndi)
        if self.pickup_bonus_cndi and bonus_num>=4:
            return self.p_choice(self.pickup_bonus_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # 三連(3)アガり,一色(1～3)アガり
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  # 全て表

    def win_or_discard_musou(self, hand):  # アガる／捨てる戦略：無双(9)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            return -1  # アガり
        if 2 in self.musou_cndi:  # 無双(9)聴牌
            return self.select_discard(self.musou_cndi)
        if 2 in self.rikka_cndi:  # 六華(7)聴牌
            return self.select_discard(self.rikka_cndi)
        if 1 in self.musou_cndi:  # 無双(9)一向聴
            return self.select_discard(self.musou_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            return -1  # アガり
        if 2 in self.kikou_cndi:  # 輝光(5)聴牌
            return self.select_discard(self.kikou_cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 2)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi)
        self.list_add(sum_cndi, self.bonus_cndi, 3)
        self.list_add(sum_cndi, self.niren_cndi)
        self.consoleout_discard('無双', sum_cndi, 2, 1, 1, 1, 1, 1, 1, 2, 1)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def pickup_kikou(self, hand_bonus, win_river_n):  # 取る戦略：輝光(5)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_musou1_cndi:  # 無双(9)聴牌
            return self.p_choice(self.pickup_musou1_cndi)
        if self.pickup_rikka1_cndi:  # 六華(7)聴牌
            return self.p_choice(self.pickup_rikka1_cndi)
        if self.pickup_musou2_cndi:  # 無双(9)一向聴
            return self.p_choice(self.pickup_musou2_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_kikou1_cndi:  # 輝光(5)聴牌
            return self.p_choice(self.pickup_kikou1_cndi)
        if self.pickup_kikou2_cndi:  # 輝光(5)一向聴
            return self.p_choice(self.pickup_kikou2_cndi)
        bonus_num = hand_bonus+len(self.pickup_bonus_cndi)
        if self.pickup_bonus_cndi and bonus_num>=4:
            return self.p_choice(self.pickup_bonus_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # 三連(3)アガり,一色(1～3)アガり
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  # 全て表

    def win_or_discard_kikou(self, hand):  # アガる／捨てる戦略：輝光(5)／基本
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            return -1  # アガり
        if 2 in self.musou_cndi:  # 無双(9)聴牌
            return self.select_discard(self.musou_cndi)
        if 2 in self.rikka_cndi:  # 六華(7)聴牌
            return self.select_discard(self.rikka_cndi)
        if 1 in self.musou_cndi:  # 無双(9)一向聴
            return self.select_discard(self.musou_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            return -1  # アガり
        if 2 in self.kikou_cndi:  # 輝光(5)聴牌
            return self.select_discard(self.kikou_cndi)
        if 1 in self.kikou_cndi:  # 輝光(5)一向聴
            return self.select_discard(self.kikou_cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 4)
        if self.rikka_cndi[0]>=0:
            self.list_add(sum_cndi, self.rikka_cndi, 4)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi, 3)
        if self.rule_santsui and self.santsui_cndi[0]>=0:
            self.list_add(sum_cndi, self.santsui_cndi, 3)
        if self.sanren_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanren_cndi, 3)
        if self.rule_sanshiki and self.sanshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanshiki_cndi, 2)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi, 2)
        self.list_add(sum_cndi, self.bonus_cndi)
        self.list_add(sum_cndi, self.niren_cndi)
        self.consoleout_discard('基本', sum_cndi, 4, 4, 3, 3, 3, 2, 2, 1, 1)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def pickup_santsui(self, win_river_n):  # 取る戦略：三対(5,7,9,11)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_musou1_cndi:  # 無双(9)聴牌
            return self.p_choice(self.pickup_musou1_cndi)
        if self.pickup_rikka1_cndi:  # 六華(7)聴牌
            return self.p_choice(self.pickup_rikka1_cndi)
        if self.pickup_musou2_cndi:  # 無双(9)一向聴
            return self.p_choice(self.pickup_musou2_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            self.win_cfm = True
            return win_river_n
        if self.pickup_kikou1_cndi:  # 輝光(5)聴牌
            return self.p_choice(self.pickup_kikou1_cndi)
        if self.pickup_santsui1_cndi:  # 三対(5,7,9,11)聴牌
            return self.p_choice(self.pickup_santsui1_cndi)
        if self.pickup_santsui2_cndi:  # 三対(5,7,9,11)一向聴
            return self.p_choice(self.pickup_santsui2_cndi)
        if self.river_back:  # 裏
            return self.p_choice(self.river_back)
        if self.win_sc:  # 三連(3)アガり,一色(1～3)アガり
            self.win_cfm = True
            return win_river_n
        return pyxel.rndi(0,len(self.river)-1)  # 全て表

    def win_or_discard_santsui(self, hand):  # アガる／捨てる戦略：三対(5,7,9,11)
        if self.win_sc>=7:  # 無双(9)アガり,六華(7)アガり,三対(7,9,11)アガり
            return -1  # アガり
        if 2 in self.musou_cndi:  # 無双(9)聴牌
            return self.select_discard(self.musou_cndi)
        if 2 in self.rikka_cndi:  # 六華(7)聴牌
            return self.select_discard(self.rikka_cndi)
        if 1 in self.musou_cndi:  # 無双(9)一向聴
            return self.select_discard(self.musou_cndi)
        if self.win_sc>=4:  # 輝光(5)アガり,三対(5)アガり,三連(4,5)アガり
            return -1  # アガり
        if 2 in self.kikou_cndi:  # 輝光(5)聴牌
            return self.select_discard(self.kikou_cndi)
        if 2 in self.santsui_cndi:  # 三対(5,7,9,11)聴牌
            return self.select_discard(self.santsui_cndi)
        if 1 in self.santsui_cndi:  # 三対(5,7,9,11)一向聴
            return self.select_discard(self.santsui_cndi)
        sum_cndi = [0]*len(self.musou_cndi)
        if self.rule_musou and self.musou_cndi[0]>=0:
            self.list_add(sum_cndi, self.musou_cndi, 4)
        if self.rikka_cndi[0]>=0:
            self.list_add(sum_cndi, self.rikka_cndi, 4)
        if self.rule_kikou and self.kikou_cndi[0]>=0:
            self.list_add(sum_cndi, self.kikou_cndi, 3)
        if self.rule_santsui and self.santsui_cndi[0]>=0:
            self.list_add(sum_cndi, self.santsui_cndi, 5)
        if self.sanren_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanren_cndi, 3)
        if self.rule_sanshiki and self.sanshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.sanshiki_cndi, 2)
        if self.isshiki_cndi[0]>=0:
            self.list_add(sum_cndi, self.isshiki_cndi, 2)
        self.list_add(sum_cndi, self.bonus_cndi, 2)
        self.list_add(sum_cndi, self.niren_cndi)
        self.consoleout_discard('三対', sum_cndi, 4, 4, 3, 5, 3, 2, 2, 2, 1)  # __DEBUG__
        return self.select_discard(sum_cndi)

    def generate_pickup_cndi(self, hand):
        self.pickup_rikka1_cndi, self.pickup_rikka2_cndi, self.pickup_sanren1_cndi, self.pickup_sanren2_cndi, = [], [], [], [] 
        self.pickup_isshiki1_cndi, self.pickup_isshiki2_cndi, self.pickup_musou1_cndi, self.pickup_musou2_cndi = [], [], [], []
        self.pickup_kikou1_cndi, self.pickup_kikou2_cndi, self.pickup_bonus_cndi = [], [], []
        self.pickup_santsui1_cndi, self.pickup_santsui2_cndi, self.pickup_sanshiki_cndi, self.river_back = [], [], [], []
        self.win_hn, self.win_sc = HN_NONE, 0
        win_river_n = DISABLE
        hand_bonus = self.chk_bonus(hand)  # 手牌ボーナス牌
        for i,tile in enumerate(self.dsp_river):
            river_n = tile[0]
            if river_n!=DISABLE:  # 存在
                if tile[3]:  # 表
                    h = [x[:] for x in hand]
                    h.append([self.river[tile[0]][0],self.river[tile[0]][1]])
                    hn, sc = self.chk_hand(h)
                    if sc>self.win_sc:
                        self.win_hn = hn
                        self.win_sc = sc
                        win_river_n = tile[0]
                    rikka_cndi = self.thkg_rikka(h)
                    if 2 in rikka_cndi and rikka_cndi[-1]!=2:  # 六華(7)聴牌
                        self.pickup_rikka1_cndi.append(river_n)
                    if 1 in rikka_cndi and rikka_cndi[-1]!=1:  # 六華(7)一向聴
                        self.pickup_rikka2_cndi.append(river_n)
                    sanren_cndi, _niren_cndi = self.thkg_sanren(h)
                    if 2 in sanren_cndi and sanren_cndi[-1]!=2:  # 三連(3～5)聴牌
                        self.pickup_sanren1_cndi.append(river_n)
                    if 1 in sanren_cndi and sanren_cndi[-1]!=2:  # 三連(3～5)一向聴
                        self.pickup_sanren2_cndi.append(river_n)
                    isshiki_cndi = self.thkg_isshiki(h)
                    if 2 in isshiki_cndi and isshiki_cndi[-1]!=2:  # 一色(1～3)聴牌
                        self.pickup_isshiki1_cndi.append(river_n)
                    if 1 in isshiki_cndi and isshiki_cndi[-1]!=1:  # 一色(1～3)一向聴
                        self.pickup_isshiki2_cndi.append(river_n)
                    if self.rule_musou:  # 無双ルールあり
                        musou_cndi = self.thkg_musou(h)
                        if 2 in musou_cndi and musou_cndi[-1]!=2:  # 無双(9)聴牌
                            self.pickup_musou1_cndi.append(river_n)
                        if 1 in musou_cndi and musou_cndi[-1]!=1:  # 無双(9)一向聴
                            self.pickup_musou2_cndi.append(river_n)
                    if self.rule_kikou:  # 輝光ルールあり
                        kikou_cndi, bonus_cndi = self.thkg_kikou(h)
                        if 2 in kikou_cndi and kikou_cndi[-1]!=2:  # 輝光(5)聴牌
                            self.pickup_kikou1_cndi.append(river_n)
                        if 1 in kikou_cndi and kikou_cndi[-1]!=1:  # 輝光(5)一向聴
                            self.pickup_kikou2_cndi.append(river_n)
                        if 1 in bonus_cndi and bonus_cndi[-1]!=1:  # ボーナス
                            self.pickup_bonus_cndi.append(river_n)
                    if self.rule_santsui:  # 三対ルールあり
                        santsui_cndi = self.thkg_santsui(h)
                        if 2 in santsui_cndi and santsui_cndi[-1]!=2:  # 三対(5,7,9,11)聴牌
                            self.pickup_santsui1_cndi.append(river_n)
                        if 1 in santsui_cndi and santsui_cndi[-1]!=1:  # 三対(5,7,9,11)一向聴
                            self.pickup_santsui2_cndi.append(river_n)
                    if self.rule_sanshiki:  # 三色ルールあり
                        sanshiki_cndi = self.thkg_sanshiki(h)
                        if 2 in sanshiki_cndi and sanshiki_cndi[-1]!=2:  # 三色(3)聴牌
                            self.pickup_sanshiki_cndi.append(river_n)
                else:  # 裏
                    self.river_back.append(river_n)
        return win_river_n

    def com_pickup(self, hand):  # 【戦略】どれを取る
        win_river_n = self.generate_pickup_cndi(hand)
        hand_bonus = self.chk_bonus(hand)  # 手牌ボーナス牌
        self.win_cfm = False
        if self.tactic[self.turn]==TA_RIKKA:  # 取る戦略：六華(7)
            return self.pickup_rikka(win_river_n)
        elif self.tactic[self.turn]==TA_SANREN:  # 取る戦略：三連(3～5)
            return self.pickup_sanren(win_river_n)
        elif self.tactic[self.turn]==TA_ISSHIKI:  # 取る戦略：一色(1～3)
            return self.pickup_isshiki(win_river_n)
        elif self.tactic[self.turn]==TA_MUSOU:  # 取る戦略：無双(9)
            if self.rule_musou:
                return self.pickup_musou(hand_bonus, win_river_n)
        elif self.tactic[self.turn]==TA_KIKOU:  # 取る戦略：輝光(5)
            if self.rule_kikou:
                return self.pickup_kikou(hand_bonus, win_river_n)
        elif self.tactic[self.turn]==TA_SANTSUI:  # 取る戦略：三対(5,7,9,11)
            if self.rule_santsui:
                return self.pickup_santsui(win_river_n)
        return self.pickup_common(win_river_n)  # 取る戦略：基本

    def generate_discard_cndi(self, hand):
        self.musou_cndi = self.thkg_musou(hand)
        self.rikka_cndi = self.thkg_rikka(hand)
        self.kikou_cndi, self.bonus_cndi = self.thkg_kikou(hand)
        self.santsui_cndi = self.thkg_santsui(hand)
        self.sanren_cndi, self.niren_cndi = self.thkg_sanren(hand)
        self.sanshiki_cndi = self.thkg_sanshiki(hand)
        self.isshiki_cndi = self.thkg_isshiki(hand)
        if self.pickedtileface:  # 表牌ツモならその牌は捨てない
            self.musou_cndi[-1], self.rikka_cndi[-1], self.kikou_cndi[-1], self.bonus_cndi[-1], self.santsui_cndi[-1] = 0, 0, 0, 0, 0 
            self.sanren_cndi[-1], self.niren_cndi[-1], self.sanshiki_cndi[-1], self.isshiki_cndi[-1] = 0, 0, 0, 0

    def chk_1by1(self, hand, tsuide=False):  # 河牌１つずつ役確認
        cfm_hn, max_sc, river_n = HN_NONE, 0, DISABLE
        for i,tile in enumerate(self.dsp_river):
            if tile[0]!=DISABLE and tile[3]:  # 存在+表
                h1 = [x[:] for x in hand]
                h1.append([self.river[tile[0]][0],self.river[tile[0]][1]])
                hn, sc = self.chk_hand(h1, tsuide)
                if sc>max_sc:
                    cfm_hn = hn
                    max_sc = sc
                    river_n = tile[0]
        return cfm_hn, max_sc, river_n

    def del_dspriver(self, dsp_river_n): # 河牌表示番号(0～24)から河牌を削除
        river_n = self.dsp_river[dsp_river_n][0]  # 河表示番号(0～24)から河牌番号(0～21)
        self.dsp_river[dsp_river_n] = [DISABLE]
        del self.river[river_n]
        for i in range(len(self.dsp_river)):
            if self.dsp_river[i][0]>river_n:
                self.dsp_river[i][0] -= 1

    def river_n2dsp_river_n(self, n):  # 河牌番号(0～21)から河表示番号(0～24)
        for i in range(len(self.dsp_river)):
            if self.dsp_river[i][0]==n:
                return i
        return DISABLE

    def chara_own_pickup_msg(self, tile): #  自分選択時の取るメッセージ
        pyxel.play(3, 3)  # 選択音
        if tile[0]<1:  # 裏
            msg = self.p_choice(MSG_OWN_PICK)
        else:  # 表
            msg = f'${tile[0]}{tile[1]}'+self.p_choice(MSG_OWN_PICKONE)
        self.balloon.clear()
        self.balloon.append(Balloon(*MSG_XY[OWN], OWN, msg, tm=50))

    def chara_own_win_msg(self):  # 自分選択時のアガるメッセージ
        pyxel.play(3, 3)  # 選択音
        msg = self.p_choice(MSG_OWN_WINONE)
        self.balloon.clear()
        self.balloon.append(Balloon(*MSG_XY[OWN], OWN, msg, tm=50))

    def chara_own_discard_msg(self, tile):  # 自分選択時の捨てるメッセージ
        pyxel.play(3, 3)  # 選択音
        msg = f'${tile[0]}{tile[1]}'+self.p_choice(MSG_OWN_DISCARDONE)
        self.balloon.clear()
        self.balloon.append(Balloon(*MSG_XY[OWN], OWN, msg, tm=50))

    def rule_msg(self):  # ルールボタン押下メッセージ
        pyxel.play(3, 3)  # 選択音
        msg = '*A六華\n*B三連\n*C一色'
        msg += '\n*E無双 あり' if self.rule_musou else '\n*D無双 なし'
        msg += '\n*E輝光 あり' if self.rule_kikou else '\n*D輝光 なし'
        msg += '\n*E三対 あり' if self.rule_santsui else '\n*D三対 なし'
        msg += '\n*E三色 あり' if self.rule_sanshiki else '\n*D三色 なし'
        msg += '\n*E立直 あり' if self.rule_reach else '\n*D立直 なし'
        msg += '\n*E直撃 あり' if self.rule_ron else '\n*D直撃 なし'
        msg += '\n*A10点 終了' if self.rule_10pt else '\n*B２周 終了'
        self.balloon.append(Balloon(19, HEIGHT-8, OWN, msg, tm=200))

    def score_msg(self):  # スコアボタン押下メッセージ
        pyxel.play(3, 3)  # 選択音
        msg = f'*7連チャン\n現在 *A{self.consecutive_round}*7 回 *A{self.consecutive_score}*7点'
        self.balloon.append(Balloon(CHARA_XY[OWN][0]+20, CHARA_XY[OWN][1]-8, OWN, msg, tm=100))

    def chara_opp_msg(self, chara_n):  # 相手選択時のメッセージ
        pyxel.play(3, 3)  # 選択音
        msg = '*5'+CHARA_NAME[self.chara[chara_n]]
        if self.obvi_hand[chara_n]:
            #msg += '\n'
            for tile in self.obvi_hand[chara_n]:
                msg += f'${tile[0]}{tile[1]}'
        if len(self.river_back)>18 and pyxel.rndi(0,3)==0:  # 序盤
            msg += '\n*7'+self.p_choice(MSG_OPP_OPENING)
        elif len(self.river_back)<9 and pyxel.rndi(0,3)==0:  # 終盤
            msg += '\n*7'+self.p_choice(MSG_OPP_CLOSING)
        else:
            if pyxel.rndi(0,3)==0 and \
                    (CAHAR_TACTIC[self.chara[chara_n]] in (TA_RIKKA,TA_SANREN,TA_ISSHIKI) or \
                    (CAHAR_TACTIC[self.chara[chara_n]]==TA_MUSOU and self.rule_musou) or \
                    (CAHAR_TACTIC[self.chara[chara_n]]==TA_KIKOU and self.rule_kikou) or \
                    (CAHAR_TACTIC[self.chara[chara_n]]==TA_SANTSUI and self.rule_santsui)):
                if pyxel.rndi(0,1)==0:
                    msg += '\n*7'+self.p_choice(MSG_OPP_HAND_PRE)+'*A'+MSG_HANDNAME[CAHAR_TACTIC[self.chara[chara_n]]]+'*7です'
                else:
                    msg += '\n*A'+MSG_HANDNAME[CAHAR_TACTIC[self.chara[chara_n]]]+'*7'+self.p_choice(MSG_OPP_HAND_POST)
            else:
                msg += '\n*7'+self.p_choice(MSG_OPP_CHARA)
        self.balloon.append(Balloon(*MSG_XY[chara_n], chara_n, msg, tm=50))

    def chara_roundend_msg(self, chara_n):  # 自分選択時のラウンド終了メッセージ
        pyxel.play(3, 3)  # 選択音
        if chara_n==OWN:
            msg = self.p_choice(MSG_OWN_ROUNDWIN if self.addscore[OWN] else MSG_OWN_ROUNDLOSE)
        else:
            msg = '*5'+CHARA_NAME[self.chara[chara_n]]+'*7\n'
            if self.addscore[chara_n]:  # 勝ち
                #if pyxel.rndi(0,1)==0:
                if self.win_handname[chara_n]==CAHAR_TACTIC[self.chara[chara_n]]:
                    msg += self.p_choice(MSG_OPP_ROUNDWIN_PRE)+'*A'+MSG_HANDNAME[self.win_handname[chara_n]]+'*7です'
                else:
                    msg += self.p_choice(MSG_OPP_ROUNDWIN)
            else:  # 負け
                msg += self.p_choice(MSG_OPP_ROUNDLOSE)
        self.balloon.clear()
        self.balloon.append(Balloon(*MSG_XY[chara_n], chara_n, msg, tm=50))

    def chara_gameend_msg(self, chara_n):  # キャラクター選択時のゲーム終了メッセージ
        pyxel.play(3, 3)  # 選択音
        if chara_n==OWN:
            msg = self.p_choice(MSG_OWN_GAMEWIN if OWN in self.win_list else MSG_OWN_GAMELOSE)
        else:
            msg = '*5'+CHARA_NAME[self.chara[chara_n]]+'*7\n'+self.p_choice(MSG_OPP_GAMEWIN if chara_n in self.win_list else MSG_OPP_GAMELOSE)
        self.balloon.clear()
        self.balloon.append(Balloon(*MSG_XY[chara_n], chara_n, msg, tm=50))

    def click_title_rikka(self):
        pyxel.play(3, 3)  # 選択音
        txt = '*A六華 $14$24$34$44$54$64\n 7点 ボーナス込み\n*B三連 $36$46$56$13$23$33\n 3点 ＋ボーナス\n*C一色 $16$16$26$46$46$56\n 1点 ＋ボーナス'
        self.balloon.clear()
        self.balloon.append(Balloon(RIKKA_BTN_X-5,RIKKA_BTN_Y+7,P2,txt,tm=240))

    def click_title_musou(self):
        pyxel.play(3, 3)  # 選択音
        self.rule_musou = not self.rule_musou
        y = RULE_BTN_XY[HN_MUSOU][1]
        txt1 = '\n無双 $11$22$33$44$55$66\n 9点 ボーナス込み'
        if self.rule_musou:
            txt2 = '*Aあり'+txt1
        else:
            y += 1
            txt2 = '*Dなし'+txt1
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[HN_MUSOU][0]-1,y,P3,txt2,tm=120))

    def click_title_kikou(self):
        pyxel.play(3, 3)  # 選択音
        self.rule_kikou = not self.rule_kikou
        y = RULE_BTN_XY[HN_KIKOU][1]
        txt1 = '\n輝光 $11$11$33$44$44$66\n 5点 ボーナスなし'
        if self.rule_kikou:
            txt2 = '*Bあり'+txt1
        else:
            y += 1
            txt2 = '*Dなし'+txt1
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[HN_KIKOU][0]-1,y,P3,txt2,tm=120))

    def click_title_santsui(self):
        pyxel.play(3, 3)  # 選択音
        self.rule_santsui = not self.rule_santsui
        y = RULE_BTN_XY[HN_SANTSUI][1]
        txt1 = '\n三対 $61$61$22$22$53$53\n 5点 ＋ボーナス'
        if self.rule_santsui:
            txt2 = '*Cあり'+txt1
        else:
            y += 1
            txt2 = '*Dなし'+txt1
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[HN_SANTSUI][0]-1,y,P3,txt2,tm=120))

    def click_title_sanshiki(self):
        pyxel.play(3, 3)  # 選択音
        self.rule_sanshiki = not self.rule_sanshiki
        y = RULE_BTN_XY[HN_SANSHIKI][1]
        txt1 = '\n三色 $32$32$62$63$63$66\n 3点 ボーナスなし\nついでに完成のみ'
        if self.rule_sanshiki:
            txt2 = '*Eあり'+txt1
        else:
            y += 1
            txt2 = '*Dなし'+txt1
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[HN_SANSHIKI][0]-1,y,P3,txt2,tm=120))

    def click_title_reach(self):
        pyxel.play(3, 3)  # 選択音
        #self.rule_reach = not self.rule_reach
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[RL_REACH][0]-1, RULE_BTN_XY[RL_REACH][1]+1,P3,'未実装',tm=60,col=13))

    def click_title_ron(self):
        pyxel.play(3, 3)  # 選択音
        #self.rule_ron = not self.rule_ron
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[RL_RON][0]-1, RULE_BTN_XY[RL_RON][1]+1,P3,'未実装',tm=60,col=13))

    def click_title_10pt(self):
        pyxel.play(3, 3)  # 選択音
        self.rule_10pt = not self.rule_10pt
        y = RULE_BTN_XY[RL_10PT][1]
        if self.rule_10pt:
            txt = '*A2周（8回）か\n10点以上で終了'
        else:
            y += 1
            txt = '*B得点にかかわらず\n2周（8回）で終了'
        self.balloon.clear()
        self.balloon.append(Balloon(RULE_BTN_XY[RL_10PT][0]-1,y,P3,txt,tm=120))

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title='Rikka 1.3', capture_sec=60)
        pyxel.load('assets/Rikka.pyxres')
        pyxel.mouse(True)
        self.bgm = []
        for fn in ('bgm_title','bgm_play1','bgm_play2','bgm_play3'):
            with open(f"assets/{fn}.json", "rt") as fin:
                self.bgm.append(json.loads(fin.read()))
        self.bgm_n = 1
        self.blink = Blinking(0, 0, WIDTH, HEIGHT)
        self.shoot = Shooting(0, 0, WIDTH, HEIGHT, 1000)
        self.star = Star(0, 0, WIDTH, HEIGHT, 150)
        self.balloon = []  # 吹き出し
        self.conft = []  # 紙吹雪
        self.reveal = False
        self.consecutive_highround, self.consecutive_round = 0, 0
        self.consecutive_highscore, self.consecutive_score = 0, 0
        self.ruleset()
        self.gamestart()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.blink.update()
        self.shoot.update()
        self.star.update()
        self.holddown()
        for i in reversed(range(len(self.balloon))):
            if self.balloon[i].update():
                del self.balloon[i]
        if self.st==ST_TITLE:
            if pyxel.play_pos(0) is None:
                for ch, sound in enumerate(self.bgm[0]):
                    pyxel.sounds[ch].set(*sound)
                    pyxel.play(ch, ch, loop=True)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                if RIKKA_BTN_X-4<=pyxel.mouse_x<RIKKA_BTN_X+16+4 and RIKKA_BTN_Y<=pyxel.mouse_y<RIKKA_BTN_Y+14:
                    self.click_title_rikka()
                elif RULE_BTN_XY[HN_MUSOU][0]-4<=pyxel.mouse_x<RULE_BTN_XY[HN_MUSOU][0]+16+4 and RULE_BTN_XY[HN_MUSOU][1]<=pyxel.mouse_y<RULE_BTN_XY[HN_MUSOU][1]+14:
                    self.click_title_musou()
                elif RULE_BTN_XY[HN_KIKOU][0]-4<=pyxel.mouse_x<RULE_BTN_XY[HN_KIKOU][0]+16+4 and RULE_BTN_XY[HN_KIKOU][1]<=pyxel.mouse_y<RULE_BTN_XY[HN_KIKOU][1]+14:
                    self.click_title_kikou()
                elif RULE_BTN_XY[HN_SANTSUI][0]-4<=pyxel.mouse_x<RULE_BTN_XY[HN_SANTSUI][0]+16+4 and RULE_BTN_XY[HN_SANTSUI][1]<=pyxel.mouse_y<RULE_BTN_XY[HN_SANTSUI][1]+14:
                    self.click_title_santsui()
                elif RULE_BTN_XY[HN_SANSHIKI][0]-4<=pyxel.mouse_x<RULE_BTN_XY[HN_SANSHIKI][0]+16+4 and RULE_BTN_XY[HN_SANSHIKI][1]<=pyxel.mouse_y<RULE_BTN_XY[HN_SANSHIKI][1]+14:
                    self.click_title_sanshiki()
                elif RULE_BTN_XY[RL_REACH][0]-4<=pyxel.mouse_x<RULE_BTN_XY[RL_REACH][0]+16+4 and RULE_BTN_XY[RL_REACH][1]<=pyxel.mouse_y<RULE_BTN_XY[RL_REACH][1]+14:
                    self.click_title_reach()
                elif RULE_BTN_XY[RL_RON][0]-4<=pyxel.mouse_x<RULE_BTN_XY[RL_RON][0]+16+4 and RULE_BTN_XY[RL_RON][1]<=pyxel.mouse_y<RULE_BTN_XY[RL_RON][1]+14:
                    self.click_title_ron()
                elif RULE_BTN_XY[RL_10PT][0]<=pyxel.mouse_x<RULE_BTN_XY[RL_10PT][0]+32 and RULE_BTN_XY[RL_10PT][1]<=pyxel.mouse_y<RULE_BTN_XY[RL_10PT][1]+26:
                    self.click_title_10pt()
                elif START_BTN_X<=pyxel.mouse_x<START_BTN_X+24 and START_BTN_Y<=pyxel.mouse_y<START_BTN_Y+12:
                    pyxel.play(3, 3)  # 選択音
                    self.balloon.clear()
                    self.cnt = 0
                    pyxel.stop()
                    self.st = ST_DEAL
        elif self.st==ST_DEAL:
            if self.cnt==0:
                self.river = self.tile[0:MAX_TILE-20]  # len()=22
                self.rnd_sq = [r for r in range(RIVER_NUM)]  # len()=25
                self.p_shuffle(self.rnd_sq)
                self.tile_n = 0
            if self.cnt<len(self.river):  # 22
                self.dsp_river[self.rnd_sq[self.cnt]] = [self.cnt,pyxel.rndi(0,3),pyxel.rndi(0,5),1 if RIVER_OPEN else 0]  # len()=25
            else:
                self.hand[self.tile_n%4].append(self.tile[-1-self.tile_n])
                self.tile_n += 1
                if self.tile_n>=20:
                    #self.hand[OWN] = [[2,1],[2,2],[2,3],[4,2],[2,5]]  # __DEBUG__OWN手牌
                    #self.hand[P1] = [[1,1],[2,2],[3,3],[4,4],[5,5]]  # __DEBUG__ P1手牌
                    #self.hand[P3] = [[1,1],[2,2],[3,3],[4,4],[5,5]]  # __DEBUG__ P2手牌
                    #self.river[0] = [6,6]  # __DEBUG__ 河牌0
                    #self.river[1] = [2,1]  # __DEBUG__ 河牌1
                    #self.dsp_river[0] = [0,pyxel.rndi(0,3),pyxel.rndi(0,5),1]  # __DEBUG__ 河牌0表
                    #self.dsp_river[1] = [1,pyxel.rndi(0,3),pyxel.rndi(0,5),1]  # __DEBUG__ 河牌1表
                    if pyxel.play_pos(0) is None:
                        for ch, sound in enumerate(self.bgm[self.bgm_n]):
                            pyxel.sounds[ch].set(*sound)
                            pyxel.play(ch, ch, loop=True)
                    self.st = ST_NEXT
            pyxel.play(3, 6)  # 配る音
            self.cnt += 1
        elif self.st==ST_NEXT:
            self.turn = NEXT[self.turn]  # 次の番
            if self.turn==OWN:
                self.message_pick(OWN) # 取るメッセージ, Player, self.pickedtileface
                self.win_river_n = self.generate_pickup_cndi(self.hand[OWN])  # 取るアドバイスのため
                self.st = ST_PICK
            else:
                self.cnt = 0
                self.st = ST_COM_PICK
        elif self.st==ST_COM_PICK:
            self.cnt += 1
            if self.cnt==10:  # メッセージ
                pickup_n = self.com_pickup(self.hand[self.turn])  # 取る牌,上がるかどうか
                self.pickedtile = self.river[pickup_n][:]
                self.tmp_dsp_river_n = self.river_n2dsp_river_n(pickup_n)  # 河牌番号(0～21)から河表示番号(0～24)
                self.pickedtileface = self.dsp_river[self.tmp_dsp_river_n][3]  # オープン1,クローズ0
                self.message_pick(self.turn) # 取るメッセージ, Player, self.pickedtileface
            elif self.cnt==30:  # 選ぶ
                self.dsp_river_n = self.tmp_dsp_river_n
                pyxel.play(3, 7)  # 取る音／捨てる音
            elif self.cnt==50:  # 取る
                x, y = TILE_XY[self.turn][2]+TILE_XY[self.turn][4]*len(self.hand[self.turn]), TILE_XY[self.turn][3]+TILE_XY[self.turn][5]*len(self.hand[self.turn])
                self.movetile = River2hand_opp(*self.river_pos(self.dsp_river_n), x,y, self.pickedtile if self.pickedtileface else [-1,-1], (self.turn==P2))
                self.del_dspriver(self.dsp_river_n) # 河牌表示番号(0～24)から河牌を削除
                self.dsp_river_n = DISABLE
                self.handopen[self.turn][-1] = OP_FACE if self.pickedtileface else OP_BACK
                self.st = ST_COM_PICK_MOVE
        elif self.st==ST_COM_PICK_MOVE:
            if self.movetile.update():
                del self.movetile
                if self.turn in (P1,P2):
                    self.tile_rotate(self.pickedtile)
                self.hand[self.turn].append(self.pickedtile)
                if self.pickedtileface:  # オープン1,クローズ0
                    self.obvi_hand[self.turn].append(self.pickedtile)  # 明らかな手牌
                    self.consoleout_text(f'P{self.turn} 手牌 {self.obvi_hand[self.turn]}')  # __DEBUG__
                pyxel.play(3, 7)  # 取る音／捨てる音
                self.cnt = 0
                self.st = ST_COM_DISCARD
        elif self.st==ST_COM_DISCARD:
            self.cnt += 1
            if self.cnt==10:
                self.handopen[self.turn][-1] = OP_STAND  # 取った牌を入れる
            elif self.cnt==20:  # アガる／捨てる
                self.win_hn, self.win_sc = self.chk_hand(self.hand[self.turn])
                self.generate_discard_cndi(self.hand[self.turn])
                if self.tactic[self.turn]==TA_RIKKA:
                    win_or_dicard = self.win_or_dicard_rikka(self.hand[self.turn])
                elif self.tactic[self.turn]==TA_SANREN:
                    win_or_dicard = self.win_or_discard_sanren(self.hand[self.turn])
                elif self.tactic[self.turn]==TA_ISSHIKI:
                    win_or_dicard = self.win_or_discard_isshiki(self.hand[self.turn])
                elif self.tactic[self.turn]==TA_MUSOU and self.rule_musou:
                    win_or_dicard = self.win_or_discard_musou(self.hand[self.turn])
                elif self.tactic[self.turn]==TA_KIKOU and self.rule_kikou:
                    win_or_dicard = self.win_or_discard_kikou(self.hand[self.turn])
                elif self.tactic[self.turn]==TA_SANTSUI and self.rule_santsui:
                    win_or_dicard = self.win_or_discard_santsui(self.hand[self.turn])
                else:
                    win_or_dicard = self.win_or_discard_common(self.hand[self.turn])
                if win_or_dicard==-1:  # アガる
                    self.win_handname[self.turn], self.addscore[self.turn] = self.win_hn, self.win_sc
                    self.hand[self.turn] = [x[:] for x in self.win_sequence]
                    self.win_player = self.turn
                    self.judge_player = self.turn
                    self.message_win(self.turn, self.win_hn, self.win_sc) # 相手アガるメッセージ
                    self.cnt = 0
                    self.st = ST_JUDGE_OPEN
                else:  # 捨てる
                    self.discard_n = win_or_dicard
                    if self.message_discard(self.turn, self.win_sc): # 相手捨てるメッセージ
                        pass
                    else:
                        self.cnt=40
            elif self.cnt==45:
                discardtile = self.hand[self.turn][self.discard_n][:]
                self.handopen[self.turn][self.discard_n] = OP_HIDDEN  # 非表示
                spc_cndi = [i for i,x in enumerate(self.dsp_river) if x[0]==DISABLE]  # 河表示の空候補
                self.spc_dsp_river_n = self.p_choice(spc_cndi)
                self.river.append(discardtile)
                x, y = TILE_XY[self.turn][2]+TILE_XY[self.turn][4]*self.discard_n, TILE_XY[self.turn][3]+TILE_XY[self.turn][5]*self.discard_n
                self.movetile = Hand2river(x,y, *self.river_pos(self.spc_dsp_river_n), discardtile, (self.turn==P2))
                pyxel.play(3, 7)  # 取る音／捨てる音
                self.st = ST_COM_DISCARD_MOVE
        elif self.st==ST_COM_DISCARD_MOVE:
            if self.movetile.update():
                del self.movetile
                self.dsp_river[self.spc_dsp_river_n] = [len(self.river)-1,pyxel.rndi(0,3),pyxel.rndi(0,5),1]  # 牌番号,回転0～3,ずれ0～5,オープン1(クローズ0)
                discardtile = self.hand[self.turn][self.discard_n]
                if discardtile in self.obvi_hand[self.turn]:  # 捨てた牌が明らかな手牌に含まれている
                    self.obvi_hand[self.turn].remove(discardtile)  # 明らかな手牌から捨てた牌を削除
                    self.consoleout_text(f'P{self.turn} 手牌 {self.obvi_hand[self.turn]}')  # __DEBUG__
                del self.hand[self.turn][self.discard_n]
                self.handopen[self.turn][self.discard_n] = OP_STAND  # 立ち
                self.discard_n = DISABLE
                self.st = ST_NEXT
        elif self.st==ST_PICK:  # 河から自牌を取る
            if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
                if self.own_n!=DISABLE or self.dsp_river_n!=DISABLE:
                    self.own_n, self.dsp_river_n = DISABLE, DISABLE
                    pyxel.play(3, 4)  # 取消し音
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                show_rule = self.cur_rule()  # ルールボタン
                show_score = self.cur_score()  # スコアボタン
                chara_n = self.cur_chara(pyxel.mouse_x, pyxel.mouse_y)  # キャラクタ枠
                sort_n = self.cur_sort(pyxel.mouse_x, pyxel.mouse_y)  # ソートボタン
                rotswap_n = self.cur_rotswap(pyxel.mouse_x, pyxel.mouse_y, len(self.hand[OWN]))  # 回転／交換ボタン
                old_own_n = self.own_n
                self.own_n = self.cur_own(pyxel.mouse_x, pyxel.mouse_y, len(self.hand[OWN]), old_own_n)  # 自牌選択
                old_dsp_n = self.dsp_river_n
                self.dsp_river_n = self.cur_river(pyxel.mouse_x, pyxel.mouse_y)  # カーソル位置から河表示番号(0～24)
                if chara_n!=DISABLE:  # キャラクタ枠
                    if chara_n==OWN:
                        pickup_n = self.pickup_common(self.win_river_n)
                        self.dsp_river_n = self.river_n2dsp_river_n(pickup_n)  # 河牌番号(0～21)から河表示番号(0～24)
                        self.chara_own_pickup_msg(self.river[pickup_n] if self.dsp_river[self.dsp_river_n][3] else [0,0])
                    else:
                        self.chara_opp_msg(chara_n)
                elif show_rule:
                    self.rule_msg()
                elif show_score:
                    self.score_msg()
                elif sort_n!=DISABLE:  # ソート
                    pyxel.play(3, 3)  # 選択音
                    self.hand_sort(self.hand[OWN], sort_n)
                elif rotswap_n!=DISABLE:
                    pyxel.play(3, 3)  # 選択音
                    if old_own_n==DISABLE or rotswap_n==old_own_n:  # 回転
                        self.tile_rotate(self.hand[OWN][rotswap_n])
                    else:  # 交換
                        self.tile_swap(OWN, rotswap_n, old_own_n)
                elif self.own_n!=DISABLE and old_own_n!=DISABLE:  # 自牌選択中
                    pyxel.play(3, 3)  # 選択音
                    if self.own_n==old_own_n:  # 回転
                        self.tile_rotate(self.hand[OWN][old_own_n])
                    else:  # 交換
                        self.tile_swap(OWN, self.own_n, old_own_n)
                    self.own_n = DISABLE
                elif self.dsp_river_n!=DISABLE:  # 河牌選択中
                    river_n = self.dsp_river[self.dsp_river_n][0]  # 河表示番号(0～24)から河牌番号(0～21)
                    if self.dsp_river_n==old_dsp_n:  # 同じ牌選択で自牌へ
                        pyxel.play(3, 7)  # 取る音／捨てる音
                        self.pickedtile = self.river[river_n][:]
                        self.pickedtileface = self.dsp_river[self.dsp_river_n][3]
                        self.movetile = River2hand(*self.river_pos(self.dsp_river_n), TILE_XY[OWN][0]+16*len(self.hand[OWN]),TILE_XY[OWN][1], self.pickedtile if self.pickedtileface else [-1,-1])
                        self.del_dspriver(self.dsp_river_n) # 河表示番号(0～24)から河牌を削除
                        self.dsp_river_n = DISABLE
                        self.st = ST_PICK_MOVE
                    elif river_n==DISABLE:
                        self.dsp_river_n = DISABLE
                        if old_dsp_n!=DISABLE:
                            pyxel.play(3, 4)  # 取消し音
                    else:
                        pyxel.play(3, 3)  # 選択音
                elif self.own_n!=DISABLE:
                    pyxel.play(3, 3)  # 選択音
                elif old_own_n!=DISABLE or old_dsp_n!=DISABLE:
                    pyxel.play(3, 4)  # 取消し音
        elif self.st==ST_PICK_MOVE:  # 河から自牌に移動
            if self.movetile.update():
                del self.movetile
                self.hand[OWN].append(self.pickedtile)
                if self.pickedtileface:  # オープン1,クローズ0
                    self.obvi_hand[OWN].append(self.pickedtile)  # 明らかな手牌
                    self.consoleout_text(f'P0 手牌 {self.obvi_hand[OWN]}')  # __DEBUG__
                #self.hand[OWN] = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]]  # __DEBUG__ アガり確認
                self.handname_own, self.handscore_own = self.chk_hand(self.hand[OWN])
                self.message_discard(OWN, self.handscore_own) # 自分捨てるメッセージ
                self.st = ST_DISCARD
        elif self.st==ST_DISCARD:  # 自牌を河に捨てる
            if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
                if self.own_n!=DISABLE or self.winning_n!=DISABLE:
                    self.own_n, self.winning_n = DISABLE, DISABLE
                    pyxel.play(3, 4)  # 取消し音
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.handopen[OWN][-1] = OP_STAND  # 立ち
                show_rule = self.cur_rule()  # ルールボタン
                show_score = self.cur_score()  # スコアボタン
                chara_n = self.cur_chara(pyxel.mouse_x, pyxel.mouse_y)  # キャラクタ枠
                sort_n = self.cur_sort(pyxel.mouse_x, pyxel.mouse_y)  # ソートボタン
                rotswap_n = self.cur_rotswap(pyxel.mouse_x, pyxel.mouse_y, len(self.hand[OWN]))  # 回転／交換ボタン
                old_own_n = self.own_n
                self.own_n = self.cur_own(pyxel.mouse_x, pyxel.mouse_y, len(self.hand[OWN]), old_own_n)  # 自牌選択
                old_winning_n = self.winning_n
                self.winning_n = self.cur_winning(pyxel.mouse_x, pyxel.mouse_y)  # アガりボタン
                if chara_n!=DISABLE:  # キャラクタ枠
                    if chara_n==OWN:
                        self.pickedtileface = 0  # オープン1,クローズ0
                        self.win_hn, self.win_sc = self.chk_hand(self.hand[OWN])
                        self.generate_discard_cndi(self.hand[OWN])
                        win_or_dicard = self.win_or_discard_common(self.hand[OWN])
                        if win_or_dicard==-1:
                            self.winning_n = self.handname_own
                            self.chara_own_win_msg()  # 自分選択時のアガるメッセージ
                        else:
                            self.own_n = win_or_dicard
                            self.chara_own_discard_msg(self.hand[OWN][self.own_n])  # 自分選択時の捨てるメッセージ
                    else:
                        self.chara_opp_msg(chara_n)
                elif show_rule:
                    self.rule_msg()
                elif show_score:
                    self.score_msg()
                elif sort_n!=DISABLE:  # ソート
                    pyxel.play(3, 3)  # 選択音
                    self.hand_sort(self.hand[OWN], sort_n)
                elif rotswap_n!=DISABLE:
                    pyxel.play(3, 3)  # 選択音
                    if old_own_n==DISABLE or rotswap_n==old_own_n:  # 回転
                        self.tile_rotate(self.hand[OWN][rotswap_n])
                    else:  # 交換
                        self.tile_swap(OWN, rotswap_n, old_own_n)
                elif self.own_n!=DISABLE and old_own_n!=DISABLE:  # 自牌選択中
                    if self.own_n==old_own_n:  # 自牌捨てる
                        pyxel.play(3, 7)  # 取る音／捨てる音
                        discardtile = self.hand[OWN][self.own_n][:]
                        self.handopen[OWN][self.own_n] = OP_HIDDEN  # 非表示
                        spc_cndi = [i for i,x in enumerate(self.dsp_river) if x[0]==DISABLE]  # 河表示の空候補
                        self.spc_dsp_river_n = self.p_choice(spc_cndi)
                        self.river.append(discardtile)
                        self.movetile = Hand2river(TILE_XY[OWN][0]+16*self.own_n,TILE_XY[OWN][1], *self.river_pos(self.spc_dsp_river_n), discardtile)
                        self.st = ST_DISCARD_MOVE
                    else:  # 交換
                        pyxel.play(3, 3)  # 選択音
                        self.tile_swap(OWN, self.own_n, old_own_n)
                        self.own_n = DISABLE
                elif not self.winning_n in (DISABLE, HN_NONE):
                    if old_winning_n==DISABLE:  # クリック1回目
                        pyxel.play(3, 3)  # 選択音
                        self.hand[OWN] = [x[:] for x in self.win_sequence]
                    else:  # クリック2回目
                        self.win_handname[OWN], self.addscore[OWN] = self.handname_own, self.handscore_own
                        self.win_player = OWN
                        self.judge_player = OWN
                        self.message_win(OWN, self.handname_own, self.handscore_own)  # 自分アガるメッセージ
                        self.cnt = 0
                        self.st = ST_JUDGE_OPEN
                elif self.own_n!=DISABLE:
                    pyxel.play(3, 3)  # 選択音
                elif old_own_n!=DISABLE or old_winning_n!=DISABLE:
                    pyxel.play(3, 4)  # 取消し音
        elif self.st==ST_DISCARD_MOVE:  # 自牌から河に移動
            if self.movetile.update():
                del self.movetile
                self.dsp_river[self.spc_dsp_river_n] = [len(self.river)-1,pyxel.rndi(0,3),pyxel.rndi(0,5),1]  # 牌番号,回転0～3,ずれ0～5,オープン
                discardtile = self.hand[self.turn][self.own_n]
                if discardtile in self.obvi_hand[OWN]:  # 捨てた牌が明らかな手牌に含まれている
                    self.obvi_hand[OWN].remove(discardtile)  # 明らかな手牌から捨てた牌を削除
                    self.consoleout_text(f'P0 手牌 {self.obvi_hand[OWN]}')  # __DEBUG__
                del self.hand[OWN][self.own_n]
                self.handopen[OWN][self.own_n] = OP_STAND  # 立ち
                self.own_n = DISABLE
                self.handname_own, self.handscore_own = HN_NONE, 0
                self.st = ST_NEXT
        elif self.st==ST_JUDGE_OPEN:
            pyxel.stop()
            if self.cnt<len(self.hand[self.judge_player]):  #　牌を1つずつ倒す
                self.handopen[self.judge_player][self.cnt] = OP_FACE  # 倒し表牌
                self.cnt += 1
            elif self.judge_player==self.win_player:
                self.cnt = 0
                self.st = ST_JUDGE
            else:
                self.cnt += 1
                if self.cnt==10:
                    p = self.judge_player
                    x, y = TILE_XY[p][2]+TILE_XY[p][4]*len(self.hand[p]), TILE_XY[p][3]+TILE_XY[p][5]*len(self.hand[p])
                    self.movetile = River2hand_opp(*self.river_pos(self.dsp_river_n), x,y, self.pickedtile, (self.turn==P2))
                    self.del_dspriver(self.dsp_river_n) # 河牌表示番号(0～24)から河牌を削除
                    self.dsp_river_n = DISABLE
                    self.cnt = 0
                    self.st = ST_JUDGE_MOVE
        elif self.st==ST_JUDGE:
            self.cnt += 1
            if self.cnt==20:
                self.judge_player = NEXT[self.judge_player]
                if self.judge_player==self.win_player:  # 判定一巡したらラウンド終了
                    pyxel.play(3, 11)  # アガリ音
                    self.st = ST_ROUNDEND
                else:
                    cfm_hn, add_sc, self.pickup_n = self.chk_1by1(self.hand[self.judge_player], tsuide=True)
                    if add_sc:
                        self.message_tsuide(self.judge_player, cfm_hn, add_sc)  # ついでに完成メッセージ
                    else:
                        self.cnt = 10
            elif self.cnt==40:  # ウェイト
                self.pickedtile = self.river[self.pickup_n][:]
                self.dsp_river_n = self.river_n2dsp_river_n(self.pickup_n)  # 河牌番号(0～21)から河表示番号(0～24)
                self.cnt = 0
                self.st = ST_JUDGE_OPEN
        elif self.st==ST_JUDGE_MOVE:
            if self.movetile.update():
                del self.movetile
                self.handopen[self.judge_player][len(self.hand[self.judge_player])] = OP_FACE  # 倒し表牌
                self.hand[self.judge_player].append(self.pickedtile)
                self.win_handname[self.judge_player], self.addscore[self.judge_player] = self.chk_hand(self.hand[self.judge_player], tsuide=True)
                self.hand[self.judge_player] = [x[:] for x in self.win_sequence]
                self.cnt = 0
                self.st = ST_JUDGE
        elif self.st==ST_ROUNDEND:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                show_rule = self.cur_rule()  # ルールボタン
                show_score = self.cur_score()  # スコアボタン
                chara_n = self.cur_chara(pyxel.mouse_x, pyxel.mouse_y)  # キャラクタ枠
                if chara_n!=DISABLE:  # キャラクタ枠
                    self.chara_roundend_msg(chara_n)
                elif show_rule:
                    self.rule_msg()
                elif show_score:
                    self.score_msg()
                else:
                    pyxel.play(3, 3)  # 選択音
                    for p in (OWN, P1, P2, P3):
                        self.score[p] += self.addscore[p]
                    if self.round_n>=8 or (self.rule_10pt and max(self.score.values())>=10):
                        self.win_list = [i for i,x in enumerate(self.score.values()) if x==max(self.score.values())]
                        if OWN in self.win_list:
                            self.confetti = Confetti(0, 0, WIDTH, HEIGHT)  # 紙吹雪
                            pyxel.play(3, 10)  # 勝ち音
                            self.consecutive_round += 1
                            if self.consecutive_round>self.consecutive_highround:
                                self.consecutive_highround = self.consecutive_round
                            self.consecutive_score += self.score[OWN]
                            if self.consecutive_score>self.consecutive_highscore:
                                self.consecutive_highscore = self.consecutive_score
                        else:
                            self.consecutive_round = 0
                            self.consecutive_score = 0
                            pyxel.play(3, 12)  # 負け音
                        self.st = ST_GAMEEND
                    else:
                        self.roundstart()
                        self.cnt = 0
                        self.st = ST_DEAL
        elif self.st==ST_GAMEEND:
            if OWN in self.win_list:
                self.confetti.update()
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                show_rule = self.cur_rule()  # ルールボタン
                show_score = self.cur_score()  # スコアボタン
                chara_n = self.cur_chara(pyxel.mouse_x, pyxel.mouse_y)  # キャラクタ枠
                if chara_n!=DISABLE:  # キャラクタ枠
                    self.chara_gameend_msg(chara_n)
                elif show_rule:
                    self.rule_msg()
                elif show_score:
                    self.score_msg()
                else:
                    pyxel.play(3, 3)  # 選択音
                    if OWN in self.win_list:
                        del self.confetti
                    self.gamestart()
                    self.st = ST_TITLE

    def cur_own(self, x, y, n, selected):  # カーソル位置から自牌番号
        px = (x-TILE_XY[OWN][0])//16
        py = (y-TILE_XY[OWN][1])//36
        return px if 0<=px<n and py==0 else DISABLE

    def cur_rotswap(self, x, y, n):  # カーソル位置から回転／交換ボタン番号
        px = (x-TILE_XY[OWN][0])//16
        py = (y-TILE_XY[OWN][1]-ROT_BTN_DY)//16
        return px if 0<=px<n and py==0 else DISABLE

    def cur_sort(self, x, y):  # カーソル位置からソートボタン番号
        px = (x-TILE_XY[OWN][0]+16)//16
        py = (y-TILE_XY[OWN][1]-2)//16
        return py if px==0 and py==1 else DISABLE

    def cur_river(self, x, y):  # カーソル位置から河表示番号(0～24)
        py = (y-RIVER_Y)//16
        px = (x+4-RIVER_X)//16 if py%2 else (x-4-RIVER_X)//16
        return py*RIVER_LINE+px if 0<=px<RIVER_LINE and 0<=py<RIVER_LINE else DISABLE

    def cur_winning(self, x, y):  # カーソル位置からアガりボタン
        return self.handname_own if HN_BTN_X<=x<HN_BTN_X+16 and HN_BTN_Y<=y<HN_BTN_Y+24 else DISABLE

    def cur_chara(self, x, y):  # カーソル位置からキャラクタ枠番号
        for p in (OWN, P1, P2, P3):
            if CHARA_XY[p][0]<=x<CHARA_XY[p][0]+20 and CHARA_XY[p][1]<=y<CHARA_XY[p][1]+22:
                return p
        return DISABLE

    def cur_rule(self):  # カーソル位置からルールボタン
        return 2<=pyxel.mouse_x<18 and HEIGHT-7<=pyxel.mouse_y<HEIGHT-1

    def cur_score(self):  # カーソル位置からスコアボタン
        return self.consecutive_round>=1 and CHARA_XY[OWN][0]<=pyxel.mouse_x<CHARA_XY[OWN][0]+20 and CHARA_XY[OWN][1]-7<=pyxel.mouse_y<CHARA_XY[OWN][1]-1

    def river_pos(self, n):  # 河表示番号(0～24)から表示位置
        x, y = n%RIVER_LINE, n//RIVER_LINE
        px = RIVER_X+16*x-4 if y%2 else RIVER_X+16*x+4
        py = RIVER_Y+16*y
        return px, py

    def draw_grid(self):  # グリッド
        for i in range(GRID_LINE):
            pyxel.line(15+i*16, 0, 15+i*16, 16*GRID_LINE-1, 1)  # 縦線
            pyxel.line(0, 15+i*16, 16*GRID_LINE-1, 15+i*16, 1)  # 横線

    def draw_title(self, n=0):  # タイトル
        pict.startplayer(16*2+7,16*3-7)
        pict.small_tile(16*1+4,16*3-8, (3-1+n)%6+1,(1-1+n)%6+1, 0, 0)  # 内側
        pict.small_tile(16*1+8,16*2-8, (4-1+n)%6+1,(2-1+n)%6+1, 1, 0)
        pict.small_tile(16*2+5,16*1+4, (3-1+n)%6+1,(1-1+n)%6+1, 2, 0)
        pict.small_tile(16*3-1,16*2-8, (4-1+n)%6+1,(2-1+n)%6+1, 3, 0)
        pict.small_tile(16*3+3,16*3-8, (1-1+n)%6+1,(3-1+n)%6+1, 0, 0)
        pict.small_tile(16*3-1,16*3+2, (2-1+n)%6+1,(4-1+n)%6+1, 1, 0)
        pict.small_tile(16*2+5,16*3+6, (1-1+n)%6+1,(3-1+n)%6+1, 2, 0)
        pict.small_tile(16*2-8,16*3+2, (2-1+n)%6+1,(4-1+n)%6+1, 3, 0)
        pict.small_tile(16*0+2,16*2+3, (5-1+n)%6+1,(4-1+n)%6+1, 0, 0)  # 外側
        pict.small_tile(16*0+2,16*3-3, (6-1+n)%6+1,(5-1+n)%6+1, 0, 0)
        pict.small_tile(16*0+6,16*1+3, (4-1+n)%6+1,(3-1+n)%6+1, 1, 0)
        pict.small_tile(16*1-6,16*1-6, (6-1+n)%6+1,(5-1+n)%6+1, 1, 0)
        pict.small_tile(16*1+2,16*0+5, (4-1+n)%6+1,(3-1+n)%6+1, 1, 0)
        pict.small_tile(16*2  ,16*0+2, (5-1+n)%6+1,(4-1+n)%6+1, 2, 0)
        pict.small_tile(16*3-6,16*0+2, (6-1+n)%6+1,(5-1+n)%6+1, 2, 0)
        pict.small_tile(16*3+5,16*0+5, (4-1+n)%6+1,(3-1+n)%6+1, 3, 0)
        pict.small_tile(16*4-3,16*1-6, (6-1+n)%6+1,(5-1+n)%6+1, 3, 0)
        pict.small_tile(16*4+1,16*1+3, (4-1+n)%6+1,(3-1+n)%6+1, 3, 0)
        pict.small_tile(16*4+4,16*2+3, (4-1+n)%6+1,(5-1+n)%6+1, 0, 0)
        pict.small_tile(16*4+4,16*3-3, (5-1+n)%6+1,(6-1+n)%6+1, 0, 0)
        pict.small_tile(16*4+1,16*3+7, (3-1+n)%6+1,(4-1+n)%6+1, 1, 0)
        pict.small_tile(16*4-3,16*4  , (5-1+n)%6+1,(6-1+n)%6+1, 1, 0)
        pict.small_tile(16*3+5,16*4+5, (3-1+n)%6+1,(4-1+n)%6+1, 1, 0)
        pict.small_tile(16*3-6,16*5-8, (4-1+n)%6+1,(5-1+n)%6+1, 2, 0)
        pict.small_tile(16*2  ,16*5-8, (5-1+n)%6+1,(6-1+n)%6+1, 2, 0)
        pict.small_tile(16*1+2,16*4+5, (3-1+n)%6+1,(4-1+n)%6+1, 3, 0)
        pict.small_tile(16*1-6,16*4  , (5-1+n)%6+1,(6-1+n)%6+1, 3, 0)
        pict.small_tile(16*0+6,16*3+7, (3-1+n)%6+1,(4-1+n)%6+1, 3, 0)
        pict.small_tile(16*2+5,16*6-6, (2-1+n)%6+1,(1-1+n)%6+1, 2, 0)  # 縦
        pict.small_tile(16*2+5,16*7-6, (6-1+n)%6+1,(5-1+n)%6+1, 2, 0)
        if self.consecutive_round==0 and self.consecutive_highround==0:
            pict.small_tile(16*2+5,16*8-6, (4-1+n)%6+1,(3-1+n)%6+1, 2, 0)
            pict.small_tile(16*2+5,16*9-6, (2-1+n)%6+1,(1-1+n)%6+1, 2, 0)
        else:
            if self.consecutive_round>=1:
                pict.textbox(20, 16*8-6, '連チャン中', 0)
                pict.textbox(20, 16*8-7, '連チャン中', 10)
                pict.textbox(12, 16*8+7, f'最高 {self.consecutive_highround} 回 {self.consecutive_highscore}点', 0)
                pict.textbox(12, 16*8+6, f'*6最高 *E{self.consecutive_highround}*6 回 *E{self.consecutive_highscore}*6点')
                pict.textbox(12, 16*9+4, f'現在 {self.consecutive_round} 回 {self.consecutive_score}点', 0)
                pict.textbox(12, 16*9+3, f'*6現在 *A{self.consecutive_round}*6 回 *A{self.consecutive_score}*6点')
            else:
                pict.textbox(16, 16*8+1, '連チャン記録', 0)
                pict.textbox(16, 16*8  , '連チャン記録', 6)
                pict.textbox(12, 16*8+14, f'最高 {self.consecutive_highround} 回 {self.consecutive_highscore}点', 0)
                pict.textbox(12, 16*8+13, f'*6最高 *E{self.consecutive_highround}*6 回 *E{self.consecutive_highscore}*6点')
        pict.handname(RIKKA_BTN_X, RIKKA_BTN_Y, HN_RIKKA, True)  # 六華
        pyxel.rect(16*5-4, 16*4+8, 66, 68, 1)  # ルール枠
        pyxel.rectb(16*5-4, 16*4+8, 66, 68, 12)
        pict.addrule(16*6-6, 16*3+8)  # 追加ルール
        pict.handname(RULE_BTN_XY[HN_MUSOU][0], RULE_BTN_XY[HN_MUSOU][1]+(0 if self.rule_musou else 1), HN_MUSOU, self.rule_musou)
        pict.handname(RULE_BTN_XY[HN_KIKOU][0], RULE_BTN_XY[HN_KIKOU][1]+(0 if self.rule_kikou else 1), HN_KIKOU, self.rule_kikou)
        pict.handname(RULE_BTN_XY[HN_SANTSUI][0], RULE_BTN_XY[HN_SANTSUI][1]+(0 if self.rule_santsui else 1), HN_SANTSUI, self.rule_santsui)
        pict.handname(RULE_BTN_XY[HN_SANSHIKI][0], RULE_BTN_XY[HN_SANSHIKI][1]+(0 if self.rule_sanshiki else 1), HN_SANSHIKI, self.rule_sanshiki)
        pict.rule(RULE_BTN_XY[RL_REACH][0], RULE_BTN_XY[RL_REACH][1]+(0 if self.rule_reach else 1), RL_REACH, self.rule_reach)
        pict.rule(RULE_BTN_XY[RL_RON][0], RULE_BTN_XY[RL_RON][1]+(0 if self.rule_ron else 1), RL_RON, self.rule_ron)
        pict.rule(RULE_BTN_XY[RL_10PT][0], RULE_BTN_XY[RL_10PT][1]+(0 if self.rule_10pt else 1), RL_10PT, self.rule_10pt)
        pict.start(START_BTN_X, START_BTN_Y)  # スタートボタン

    def draw_round(self):  # ラウンド数
        self.textshadow(WIDTH-8, HEIGHT-7, f'R{self.round_n}', 13)

    def draw_rule_btn(self):  # ルールボタン
        self.textshadow(2, HEIGHT-7, 'RULE', 13)

    def draw_score_btn(self):  # ハイスコアボタン
        self.textshadow(CHARA_XY[OWN][0], CHARA_XY[OWN][1]-7, 'SCORE', 13)

    def draw_charaframe(self):  # キャラクタ枠
        for p in (OWN, P1, P2, P3):
            pyxel.rect(CHARA_XY[p][0], CHARA_XY[p][1], 20, 22, (pyxel.frame_count//4%4)+7 if self.st==ST_GAMEEND and p in self.win_list else 1)
            if self.st==ST_ROUNDEND:
                pyxel.rectb(CHARA_XY[p][0], CHARA_XY[p][1], 20, 22, (pyxel.frame_count//4%4)+7 if self.addscore[p] else 12)
            else:
                pyxel.rectb(CHARA_XY[p][0], CHARA_XY[p][1], 20, 22, 10 if self.turn==p else 12)

    def draw_chara(self, colorful):  # キャラクタ
        for p in (OWN, P1, P2, P3):
            pict.chara(CHARA_XY[p][0]+2, CHARA_XY[p][1]+3, self.chara[p], (colorful and p==self.turn) or p in self.win_list, p in (P2, P3))
        pict.startplayer(CHARA_XY[self.startplayer][0]-1, CHARA_XY[self.startplayer][1]-1, self.startplayer==self.turn)

    def textshadow(self, x, y, txt, col=7, shadowcol=0, lowerright=False):  # 影文字
        if lowerright:
            pyxel.text(x+1, y, txt, shadowcol)
            pyxel.text(x+1, y+1, txt, shadowcol)
        pyxel.text(x, y+1, txt, shadowcol)
        pyxel.text(x, y, txt, col)

    def draw_score(self):  # 得点
        for p in (OWN, P1, P2, P3):
            self.textshadow(CHARA_XY[p][0]+2, CHARA_XY[p][1]+15, f'{self.score[p]}', lowerright=True)

    def draw_addscore(self):  # 追加点
        for p in (OWN, P1, P2, P3):
            if self.addscore[p]:
                self.textshadow(CHARA_XY[p][0]+11, CHARA_XY[p][1]+15, f'+{self.addscore[p]}', 14, lowerright=True)

    def draw_rivertile(self, n, sz):  # 河牌
        tl = self.dsp_river[n]
        if tl[0]!=DISABLE:
            px, py = self.river_pos(n)
            if tl[3]:  # 表
                if sz==SZ_SMALL:
                    pict.small_tile(px,py, self.river[tl[0]][0],self.river[tl[0]][1], tl[1], tl[2])
                elif sz==SZ_MID:
                    pict.mid_tile(px+2,py-4, self.river[tl[0]][0],self.river[tl[0]][1], True if self.turn in (OWN, P2) else False)
            else:  # 裏
                if sz==SZ_SMALL:
                    pict.small_tile(px,py, 0,0, tl[1],tl[2])
                elif sz==SZ_MID:
                    pict.mid_tile(px+2,py-4, 0,0, True if self.turn in (OWN, P2) else False)

    def draw_river(self):  # 河
        for i in range(RIVER_NUM):
            if i!=self.dsp_river_n:
                self.draw_rivertile(i, SZ_SMALL)
        if self.dsp_river_n!=DISABLE:
            self.draw_rivertile(self.dsp_river_n, SZ_MID)  # 選択河牌

    def draw_owntile(self):  # 自牌
        for i in range(len(self.hand[OWN])):
            if self.handopen[OWN][i]==OP_HIDDEN:  # 非表示
                pass
            elif self.handopen[OWN][i]==OP_FACE:  # 倒し表
                pict.large_tile(TILE_XY[OWN][0]+16*i,TILE_XY[OWN][1], self.hand[OWN][i][0],self.hand[OWN][i][1], vert=True, thk=1)
            else:  # 立ち0
                pict.large_tile(TILE_XY[OWN][0]+16*i,TILE_XY[OWN][1]-4 if self.own_n==i else TILE_XY[OWN][1], self.hand[OWN][i][0],self.hand[OWN][i][1], vert=True, thk=-1)

    def draw_opptile(self):  # 相手牌
        for i in range(len(self.hand[P1])):  # 左P1
            x2, y2, thk2 = TILE_XY[P1][2]+TILE_XY[P1][4]*i, TILE_XY[P1][3]+TILE_XY[P1][5]*i, 1 if i==len(self.hand[P1])-1 else 0
            if self.handopen[P1][i]==OP_HIDDEN:  # 非表示
                pass
            elif self.handopen[P1][i]==OP_BACK:  # 倒し裏
                pict.mid_tile(x2,y2, -1,-1, vert=False, thk=thk2)
            elif P1_OPEN or self.reveal or self.handopen[P1][i]==OP_FACE:  # 倒し表
                pict.mid_tile(x2,y2, self.hand[P1][i][1],self.hand[P1][i][0], vert=False, thk=thk2)
            else:  # 立ち
                x, y, thk = TILE_XY[P1][0]+TILE_XY[P1][4]*i, TILE_XY[P1][1]+TILE_XY[P1][5]*i, (i==len(self.hand[P1])-1)
                pict.mid_stand(x, y, dlc=1, thk=thk)
        for i in range(len(self.hand[P2])):  # 対P2
            x2, y2 = TILE_XY[P2][2]+TILE_XY[P2][4]*i, TILE_XY[P2][3]+TILE_XY[P2][5]*i
            if self.handopen[P2][i]==OP_HIDDEN:  # 非表示
                pass
            elif self.handopen[P2][i]==OP_BACK:  # 倒し裏
                pict.mid_tile(x2,y2, -1,-1)
            elif P2_OPEN or self.reveal or self.handopen[P2][i]==OP_FACE:  # 倒し表
                pict.mid_tile(x2,y2, self.hand[P2][i][1],self.hand[P2][i][0])
            else:  # 立ち
                x, y = TILE_XY[P2][0]+TILE_XY[P2][4]*i, TILE_XY[P2][1]+TILE_XY[P2][5]*i
                pict.mid_stand(x,y, dlc=2, thk=True)
        for i in range(len(self.hand[P3])):  # 右P3
            x2, y2, thk2 = TILE_XY[P3][2]+TILE_XY[P3][4]*i, TILE_XY[P3][3]+TILE_XY[P3][5]*i, (i==0) 
            if self.handopen[P3][i]==OP_HIDDEN:  # 非表示
                pass
            elif self.handopen[P3][i]==OP_BACK:  # 倒し裏
                pict.mid_tile(x2,y2, -1,-1, vert=False, thk=thk2)
            elif P3_OPEN or self.reveal or self.handopen[P3][i]==OP_FACE:  # 倒し表
                pict.mid_tile(x2,y2, self.hand[P3][i][0],self.hand[P3][i][1], vert=False, thk=thk2)
            else:  # 立ち
                x, y, thk = TILE_XY[P3][0]+TILE_XY[P3][4]*i, TILE_XY[P3][1]+TILE_XY[P3][5]*i, (1 if i==0 else 0)
                pict.mid_stand(x,y, dlc=3, thk=thk)

    def draw_rotswap_btn(self):  # 回転／交換ボタン
        for i in range(len(self.hand[OWN])):
            if self.own_n==DISABLE or i==self.own_n:
                pict.rotate(TILE_XY[OWN][0]+16*i+4,TILE_XY[OWN][1]+ROT_BTN_DY)
            else:
                pict.swap(TILE_XY[OWN][0]+16*i+4,TILE_XY[OWN][1]+ROT_BTN_DY)

    def draw_sort_btn(self):  # ソートボタン
        pict.sort(TILE_XY[OWN][0]-16,TILE_XY[OWN][1]+23)

    def draw_handname(self):  # 役名
        for p in (OWN, P1, P2, P3):
            pict.handname(CHARA_XY[p][0]+2, CHARA_XY[p][1]+2, self.win_handname[p], True)

    def draw_gameend(self):  # ゲーム終了
        for p in (OWN, P1, P2, P3):
            if p in self.win_list:
                pict.crown(CROWN_XY[p][0], CROWN_XY[p][1])
        if OWN in self.win_list:
            self.confetti.draw()  # 紙吹雪

    def draw(self):
        pyxel.cls(5)
        if DRAW_GRID:
            self.draw_grid()  # グリッド
        self.blink.draw()
        self.shoot.draw()
        self.star.draw()
        if self.reveal:  # オープンモード
            self.textshadow(2, HEIGHT-14, 'OPEN', 13, 0)
        if self.st==ST_TITLE:
            self.draw_title(-pyxel.frame_count//64)
        else:
            self.draw_round()
            self.draw_charaframe()
            self.draw_chara(not self.st in (ST_ROUNDEND, ST_GAMEEND))
            self.draw_score()
            self.draw_opptile()  # 相手牌
            self.draw_owntile()  # 自牌
            self.draw_river()
            self.draw_rule_btn()
            if self.consecutive_round>=1:
                self.draw_score_btn()
        if self.st==ST_PICK:  # 河から自牌を取る
            pict.actionmessage(TILE_XY[OWN][0]+16*len(self.hand[OWN])+2, TILE_XY[OWN][1]+27, AM_DRAW, self.dsp_river_n!=DISABLE)  # 「ツモる」文字
            self.draw_sort_btn() # ソートボタン
            self.draw_rotswap_btn()  # 回転／交換ボタン
        elif self.st==ST_DISCARD:  # 自牌を河に捨てる
            if self.handname_own and self.own_n==DISABLE:
                pict.handname(HN_BTN_X, HN_BTN_Y+1 if self.winning_n==DISABLE else HN_BTN_Y, self.handname_own, self.winning_n!=DISABLE)  # 「役名」文字
                pict.actionmessage(HN_BTN_X, HN_BTN_Y+14 if self.winning_n==DISABLE else HN_BTN_Y+13, AM_WINNING, self.winning_n!=DISABLE)  # 「アガる」文字
                self.textshadow(HN_BTN_X+1, HN_BTN_Y+26 if self.winning_n==DISABLE else HN_BTN_Y+25, f'+{self.handscore_own}', 13 if self.winning_n==DISABLE else 10)  # 得点
            else:
                pict.actionmessage(TILE_XY[OWN][0]+16*len(self.hand[OWN])+2, TILE_XY[OWN][1]+27, AM_DISCARD, self.own_n!=DISABLE)  # 「すてる」文字
            if self.own_n!=DISABLE:
                pict.discard(TILE_XY[OWN][0]+16*self.own_n+4, TILE_XY[OWN][1]+32)  # すてるマーク
            self.draw_sort_btn() # ソートボタン
            self.draw_rotswap_btn()  # 回転／交換ボタン
        elif self.st==ST_ROUNDEND:
            self.draw_handname()  # 役名
            self.draw_addscore()
        elif self.st==ST_GAMEEND:
            self.draw_gameend()
        if self.st in (ST_COM_PICK_MOVE,ST_COM_DISCARD_MOVE,ST_PICK_MOVE,ST_DISCARD_MOVE,ST_JUDGE_MOVE):
            self.movetile.draw()
        for bln in self.balloon:
            bln.draw()

App()
