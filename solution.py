import random,pygame,warnings,re,sys,copy
#import os,threading,traceback,sys,re,time,numpy,gc,collections
import pandas as pd
import numpy as np
from pygame.locals import *
import seaborn as sns
import itertools as it
import matplotlib.pyplot as plt
from scipy import stats,integrate

def Bars(l,cols=[],*,filename):
    if not l:
        return
    x = l
    if cols:
        ux = cols
    else:
        ux = list(set(x))
    y = [x.count(t) / len(x) for t in ux]
    plt.figure(figsize=(16, 9))
    sns.barplot(ux, y)
    plt.savefig(filename)
    plt.show()
    print(ux)

class Outest_Frame():
    # data init
    simu_num = 600 #FIXME 模拟次数，越大耗费时间越长

    # seaborn init

    # pygame init
    size = width,height = 640,640
    pygame.init()
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Texas Holder Simulation Project")
    bgpic = pygame.image.load('bg.png').convert_alpha()
    bgpic = pygame.transform.smoothscale(bgpic, size)
    btpic = pygame.image.load('button.png').convert_alpha()
    checking_btn_list = []
    suitspic = []
    suitspic.append(pygame.image.load('s1.png').convert_alpha())
    suitspic.append(pygame.image.load('s2.png').convert_alpha())
    suitspic.append(pygame.image.load('s3.png').convert_alpha())
    suitspic.append(pygame.image.load('s4.png').convert_alpha())
    for i,C in enumerate(suitspic):
        suitspic[i] = pygame.transform.smoothscale(C, (25, 25))
    pygame.display.set_icon(suitspic[3])

    def checkbutton(thebutton, mouse_x, mouse_y, **kwargs):
        try:
            temp_bool = thebutton.rect.collidepoint(mouse_x, mouse_y)
            return temp_bool
        except:
            warnings.warn("出现异常啦！")

    def print_text(font, x, y, text, color=(255, 255, 255), alpha=0,size = 24):
        if not font:
            font = pygame.font.Font("hwxw.TTF", size)
        imgText = font.render(text, True, color)
        rect = imgText.get_rect()
        if alpha > 0:  # 设置字的透明度，有bug无效，暂时不改 # 注记 要设置alpha要convert而不能convert_alpha
            imgText = imgText.convert_alpha()
            imgText.set_alpha(alpha)
        Outest_Frame.screen.blit(imgText, (x, y))

    @classmethod
    def main(cls):
        index = 0
        running = True
        stage = 0
        method_for_stage1 = -1
        layout_switch = 0
        btns = [0] * 6
        btns[0] = cls.Button(cls.screen, "随机测验", (100, 150, 150))
        btns[1] = cls.Button(cls.screen, "静态分析", (100, 150, 150))
        btns[2] = cls.Button(cls.screen, "动态分析", (100, 150, 150))
        btns[3] = cls.Button(cls.screen, "分布分析", (100, 150, 150))
        btns[4] = cls.Button(cls.screen, "联网测试", (100, 150, 150))
        btns[5] = cls.Button(cls.screen, "联系作者", (100, 150, 150))
        data = {}
        f_btns = {}
        f_btns["Retry"] = cls.Button(cls.screen, "ReStart", (100, 100, 250))
        f_btns["Retry"].width = 80
        f_btns["Retry"].height = 30
        f_btns["Retry"].text_size = 20
        f_btns["Retry"].prep_msg("ReStart")
        f_btns["Back"] = cls.Button(cls.screen, "Back", (100, 100, 250))
        f_btns["Back"].width = 80
        f_btns["Back"].height = 30
        f_btns["Back"].text_size = 20
        f_btns["Back"].prep_msg("Back")
        f_btns["Execute"] = cls.Button(cls.screen, "Execute", (100, 100, 250))
        f_btns["Execute"].width = 80
        f_btns["Execute"].height = 30
        f_btns["Execute"].text_size = 20
        f_btns["Execute"].prep_msg("Execute")
        f_btns["Inquire"] = cls.Button(cls.screen, "Inquire", (100, 100, 250))
        f_btns["Inquire"].width = 80
        f_btns["Inquire"].height = 30
        f_btns["Inquire"].text_size = 20
        f_btns["Inquire"].prep_msg("Inquire")

        card_windows = [[None] * 7 for _ in range(8)]
        for i in range(8):
            for j in range(7):
                card_windows[i][j] = Outest_Frame.Card(cls.screen,"A")
                if j in [0,1]:
                    card_windows[i][j].PX = (0.06 + 0.08 * j) * cls.width
                else:
                    card_windows[i][j].PX = (0.06 + 0.06 + 0.08 * j) * cls.width
                card_windows[i][j].PY = (0.09 + 0.1 * i) * cls.height
                card_windows[i][j].player_id = i
                card_windows[i][j].slot_id = j

        while running:
            index += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if event.button in [1,3]: # 按下左键或按下右键
                        if stage == 0:
                            if cls.checkbutton(btns[0], mouse_x, mouse_y):
                                stage = 1
                                method_for_stage1 = 0
                                layout_switch = 1
                            if cls.checkbutton(btns[1], mouse_x, mouse_y):
                                stage = 1
                                method_for_stage1 = 1
                                layout_switch = 1
                            if cls.checkbutton(btns[2], mouse_x, mouse_y):
                                stage = 1
                                method_for_stage1 = 2
                                layout_switch = 1
                            if cls.checkbutton(btns[5], mouse_x, mouse_y):
                                stage = 1
                                method_for_stage1 = 5
                                layout_switch = 0
                        if stage == 1:
                            cancel_frame_flag = 1
                            if method_for_stage1 != 5:
                                if cls.checkbutton(f_btns["Retry"], mouse_x, mouse_y):
                                    layout_switch = 1
                            if cls.checkbutton(f_btns["Back"], mouse_x, mouse_y):
                                stage -= 1
                            if method_for_stage1 in [1,2]:
                                if cls.checkbutton(f_btns["Execute"], mouse_x, mouse_y):
                                    try:
                                        working_layout.randomly_fixing_test()
                                    except:
                                        layout_switch = 1
                                if cls.checkbutton(f_btns["Inquire"], mouse_x, mouse_y):
                                    data["Inquire"] = {}
                                    data["Inquire"]["type_distribution"] = []
                                    data["Inquire"]["win_ct"] = []
                                    Inquire_t_wl = copy.deepcopy(working_layout)
                                    ct = 0
                                    while ct <= cls.simu_num:
                                        ct += 1
                                        try:
                                            working_layout = copy.deepcopy(Inquire_t_wl)
                                            working_layout.randomly_fixing_test()
                                            for i, c in enumerate(working_layout.players):
                                                if i >= method_for_stage1:
                                                    c.visible = 0
                                            data["Inquire"]["type_distribution"].append(working_layout.players[0].type)
                                            if method_for_stage1 == 2:
                                                if 1 in working_layout.max_indexs and 2 in working_layout.max_indexs:
                                                    data["Inquire"]["win_ct"].append("Even")
                                                if 1 in working_layout.max_indexs and 2 not in working_layout.max_indexs:
                                                    data["Inquire"]["win_ct"].append("Player - 1 wins !")
                                                if 1 not in working_layout.max_indexs and 2 in working_layout.max_indexs:
                                                    data["Inquire"]["win_ct"].append("Player - 2 wins !")

                                        except:
                                            layout_switch = 1
                                            data["Inquire"]["type_distribution"].append("Exception")
                                    if method_for_stage1 == 1:
                                        x = data["Inquire"]["type_distribution"]
                                        Bars(x,cols=['high_card', 'one_pair', 'two_pairs', 'three_of_a_kind', 'straight', 'flush','full_house','four_of_a_kind','straight_flush'],filename='Inquire_Fixing_Deck.png')
                                    if method_for_stage1 == 2:
                                        x = data["Inquire"]["win_ct"]
                                        Bars(x,cols=['Even', 'Player - 1 wins !', 'Player - 2 wins !'], filename='Inquire_Win_Count.png')

                            if "working_layout" in vars():
                                if method_for_stage1 in [1,2]:
                                    for i in range(8):
                                        if players[i].visible:
                                            for j in range(7):
                                                if event.button == 1:
                                                    if cls.checkbutton(card_windows[i][j], mouse_x, mouse_y):
                                                        card_windows[i][j].pop_menu(type="rank")
                                                        cancel_frame_flag = 0
                                                if event.button == 3:
                                                    if cls.checkbutton(card_windows[i][j], mouse_x, mouse_y):
                                                        card_windows[i][j].pop_menu(type="suit")
                                                        cancel_frame_flag = 0
                            for c in Outest_Frame.checking_btn_list:
                                if cls.checkbutton(c, mouse_x, mouse_y):
                                    cancel_frame_flag = 1
                                    I = c.back.player_id
                                    J = c.back.slot_id
                                    if hasattr(c,"suit"):
                                        flag = 0
                                        setting_value = c.suit
                                    elif hasattr(c,"rank"):
                                        flag = 1
                                        setting_value = c.rank
                                    if J in [0,1]:
                                        working_layout.players[I].private_cards[J][flag] = setting_value
                                    if J not in [0,1]:
                                        working_layout.public_cards[J-2][flag] = setting_value

                            if cancel_frame_flag:
                                Outest_Frame.checking_btn_list = []

            pygame.display.flip()
            index = 0 if index >= 1000 else index
            cls.timer.tick(60)
            cls.screen.blit(cls.bgpic,(0,0))
            if stage == 0: # menu stage
                for i,b in enumerate(btns):
                    if i == 4 or i == 3:
                        pass
                    else:
                        b.PX = 0.07 * cls.width
                        b.PY = (0.07 + 0.12 * i) * cls.height
                        b.draw_button()
                Outest_Frame.print_text(None, .06 * cls.width, .01 * cls.height, "Texas Holder Simulation Project  (c) Group - 3.zjc ", (0, 75, 50), size=25)

            if stage == 1: # work stage
                if method_for_stage1 == 0:
                    if layout_switch == 1:
                        layout_switch = 0
                        working_layout = MainLayout()
                        working_layout.randomly_test(8)
                    players = working_layout.players
                    public_cards = working_layout.public_cards

                if method_for_stage1 == 1:
                    if layout_switch == 1:
                        layout_switch = 0
                        working_layout = MainLayout()
                        working_layout.players = [Player() for _ in range(8)]
                        for i,c in enumerate(working_layout.players):
                            if i:
                                c.visible = 0

                if method_for_stage1 == 2:
                    if layout_switch == 1:
                        layout_switch = 0
                        working_layout = MainLayout()
                        working_layout.players = [Player() for _ in range(8)]
                        for i,c in enumerate(working_layout.players):
                            if i > 1:
                                c.visible = 0

                if method_for_stage1 == 5:
                    working_layout = MainLayout()
                    Outest_Frame.print_text(None, .03 * cls.width, .01 * cls.height, "Author: ZJC", (0, 0, 0), size=25)
                    Outest_Frame.print_text(None, .03 * cls.width, .06 * cls.height, "Wechat: zjczmyg / 13918536850", (0, 0, 0), size=25)
                    Outest_Frame.print_text(None, .03 * cls.width, .11 * cls.height, "Email: 1115436971@qq.com / zjc_m@outlook.com", (0, 0, 0), size=25)
                    for i, c in enumerate(working_layout.players):
                        c.visible = 0

                players = working_layout.players
                public_cards = working_layout.public_cards

                for i in range(8):
                    if players[i].visible:
                        for j in range(7):
                            if j <= 1:
                                try:
                                    card_windows[i][j].msg = str(players[i].private_cards[j][1])
                                except TypeError:
                                    card_windows[i][j].msg = "?"
                                try:
                                    card_windows[i][j].suit = int(players[i].private_cards[j][0])
                                except TypeError:
                                    card_windows[i][j].suit = -1
                                try:
                                    if players[i].private_cards[j] in players[i].highest_cards.cards:
                                        card_windows[i][j].green_highlight = 1
                                    else:
                                        card_windows[i][j].green_highlight = 0
                                except:
                                    card_windows[i][j].green_highlight = 0
                                finally:
                                    card_windows[i][j].draw_button()
                            elif j > 1:
                                try:
                                    card_windows[i][j].msg = str(public_cards[j-2][1])
                                except TypeError:
                                    card_windows[i][j].msg = "?"
                                try:
                                    card_windows[i][j].suit = int(public_cards[j-2][0])
                                except TypeError:
                                    card_windows[i][j].suit = -1
                                try:
                                    if public_cards[j-2] in players[i].highest_cards.cards:
                                        card_windows[i][j].green_highlight = 1
                                    else:
                                        card_windows[i][j].green_highlight = 0
                                except:
                                    card_windows[i][j].green_highlight = 0
                                finally:
                                    card_windows[i][j].draw_button()
                            if hasattr(card_windows[i][j],"sub_ui_list") and 0:
                                l = card_windows[i][j].sub_ui_list
                                for c in l:
                                    if c.visible:
                                        c.draw_button()
                for c in Outest_Frame.checking_btn_list:
                    if c.visible:
                        c.draw_button()

                if method_for_stage1 != 5:
                    Outest_Frame.print_text(None, .03 * cls.width, .01 * cls.height, "Players'",(0,0,0),size = 20)
                    Outest_Frame.print_text(None, .03 * cls.width, .04 * cls.height, "Private Cards", (0, 0, 0), size=20)
                    Outest_Frame.print_text(None, .25 * cls.width, .01 * cls.height, "Public Cards", (0, 0, 0), size=20)
                    Outest_Frame.print_text(None, .68 * cls.width, .01 * cls.height, "Deck Type", (0, 0, 0), size=20)
                #Outest_Frame.print_text(None, .91 * cls.width, .01 * cls.height, "Win", (0, 0, 0), size=20)
                for i in range(8):
                    if players[i].visible:
                        Outest_Frame.print_text(None, .68 * cls.width, (.09 + (.1 * i)) * cls.height, re.sub('_', ' ', players[i].type), (0, 0, 0), size=20)
                        if i + 1 in working_layout.max_indexs:
                            Outest_Frame.print_text(None, .9 * cls.width, (.09 + (.1 * (i))) * cls.height, "Win", (100, 100, 0), size=20)

                b = f_btns['Retry']
                b.PX = 0.2 * cls.width
                b.PY = 0.9 * cls.height
                b.draw_button()
                b = f_btns['Back']
                b.PX = 0.05 * cls.width
                b.PY = 0.9 * cls.height
                b.draw_button()
                if method_for_stage1 in [1,2]:
                    b = f_btns['Execute']
                    b.PX = 0.35 * cls.width
                    b.PY = 0.9 * cls.height
                    b.draw_button()
                    b = f_btns['Inquire']
                    b.PX = 0.5 * cls.width
                    b.PY = 0.9 * cls.height
                    b.draw_button()

            pygame.display.update()
        pygame.display.update()

    class Button():
        def __init__(self, screen, msg="", color=(255, 255, 0), type=0, description=""):
            self.screen = screen
            self.screen_rect = screen.get_rect()  # 引入整个大屏幕的参数
            self.width,self.height,self.text_size = 200,50,40
            self.type = type
            self.font = pygame.font.SysFont("华文新魏", self.text_size)
            self.msg = msg
            self.description = description
            self.mission = ""
            self.activated = True
            self.text_color = color
            self.PX,self.PY = 0,0
            self.rect = pygame.Rect(self.PX, self.PY, self.width, self.height)  # 设置矩形大小
            self.prep_msg(msg)
            self.rect.move(self.PX, self.PY)  # 屏幕移动

        def prep_msg(self, msg):
            i = -1
            if msg.isdigit():
                i = int(msg)
                if i <= 9:
                    msg = str(i+1)
                if i == 10:
                    msg = "J"
                if i == 11:
                    msg = "Q"
                if i == 12:
                    msg = "K"
                if i == 13:
                    msg = "A"
            if msg == "None" or msg == "-1":
                msg = "?"
            self.font = pygame.font.SysFont("华文新魏", self.text_size)
            self.msg_image = self.font.render(msg, True, self.text_color)
            if i >= 0:
                self.msg_image = pygame.transform.smoothscale(self.msg_image, (19,22))


        def draw_button(self):
            # 绘制的时候调用该函数
            if self.type == 0 or self.type == "pick_rank":
                Gbtn = pygame.transform.smoothscale(Outest_Frame.btpic, (self.width, self.height))
            else:
                if hasattr(self,"suit"):
                    if self.suit == -1:
                        Gbtn = None
                    else:
                        Gbtn = Outest_Frame.suitspic[self.suit-1]
                else:
                    Gbtn = None
            if self.type == "pick_rank" or self.type == "pick_suit":
                aw = self.msg_image.get_width()
                bw = self.width

                if self.type == "pick_suit":
                    Gbtn = pygame.transform.smoothscale(Outest_Frame.btpic, (self.width, self.height))
                    self.screen.blit(Gbtn, (self.PX, self.PY))
                    Gbtn = Outest_Frame.suitspic[self.suit-1]
                    self.screen.blit(Gbtn, (self.PX + (bw - aw) / 4, self.PY))
                else:
                    self.screen.blit(Gbtn, (self.PX, self.PY))

                self.screen.blit(self.msg_image, (self.PX + (bw - aw) / 2 - 0, self.PY - 0 * self.height))
                self.rect = pygame.Rect(self.PX, self.PY, self.width, self.height)
                self.visible = True
            elif self.type == 0:
                self.screen.blit(Gbtn, (self.PX, self.PY))
                aw = self.msg_image.get_width()
                bw = self.width
                self.screen.blit(self.msg_image, (self.PX + (bw - aw) / 2 - 0, self.PY - 0 * self.height))
                self.rect = pygame.Rect(self.PX, self.PY, self.width, self.height)
                self.visible = True
            elif self.type == "card":
                self.prep_msg(self.msg)
                if Gbtn:
                    self.screen.blit(Gbtn, (self.PX, self.PY))
                aw = self.msg_image.get_width()
                bw = self.width
                self.screen.blit(self.msg_image, (self.PX - 16 / 1 - 0, self.PY - 0 * self.height))
                self.rect = pygame.Rect(self.PX, self.PY, self.width, self.height)
                self.visible = True
                if self.green_highlight == 0:
                    pygame.draw.rect(self.screen, [0, 0, 50], [self.PX - 18, self.PY, self.width + 18, self.height], 3)
                else:
                    pygame.draw.rect(self.screen, [60, 200, 60], [self.PX - 18, self.PY, self.width + 18, self.height], 3)

        def init_rect(self):
            self.rect = pygame.Rect(self.PX, self.PY, self.width, self.height)

    class Card(Button):
        def __init__(self, screen, msg="", l=[1, 1], suit=0):
            # suit 1-4
            # rank 1-13
            super().__init__(screen,msg,color=(0,0,0))
            self.l = l
            self.type = "card"
            self.width, self.height, self.text_size = 30, 30, 25
            self.prep_msg(msg)
            self.suit = suit
            self.green_highlight = 0

        def __iter__(self):
            yield self.l

        def __getitem__(self, key):
            return self.l[key]

        def pop_menu(self,type="rank",**kwargs):
            Outest_Frame.checking_btn_list = []
            self.sub_ui_list = []
            if type == "rank":
                for i in range(1,14):
                    b = Outest_Frame.Button(Outest_Frame.screen, "", (33, 33, 75))
                    b.rank = i
                    b.width = 50
                    b.height = 30
                    b.text_size = 20
                    b.PX = self.PX
                    b.PY = self.PY + (i + 0) * self.height
                    b.type = "pick_rank"
                    b.back = self
                    msg = ""
                    if i <= 9:
                        msg = str(i)
                    if i == 10:
                        msg = "J"
                    if i == 11:
                        msg = "Q"
                    if i == 12:
                        msg = "K"
                    if i == 13:
                        msg = "A"
                    b.prep_msg(msg)
                    b.visible = 1
                    self.sub_ui_list.append(b)
            if type == "suit":
                for i in range(1,5):
                    b = Outest_Frame.Button(Outest_Frame.screen, "", (100, 100, 250))
                    b.suit = i
                    b.width = 50
                    b.height = 30
                    b.text_size = 20
                    b.PX = self.PX
                    b.PY = self.PY + (i + 0) * self.height
                    b.type = "pick_suit"
                    b.back = self
                    msg = ""
                    b.visible = 1
                    self.sub_ui_list.append(b)
            Outest_Frame.checking_btn_list = self.sub_ui_list

class Deck():
    def __init__(self,cards=[]):
        self.cards = cards
        self.colors = [x[0] for x in cards]
        self.values = [x[1] for x in cards]
        self.svalues = sorted(self.values) if self.values is not None else []
        self.hstcard = self.svalues[-1]
        self.colors_set = set(self.colors)
        self.values_set = set(self.values)
        self.high = 0
        self.type = 'default'

    def __len__(self):
        return len(self.cards)
        
    def see_high(self):
        pipeline = []
        pipeline.append(Deck.see_straight_flush)
        pipeline.append(Deck.see_four_of_a_kind)
        pipeline.append(Deck.see_full_house)
        pipeline.append(Deck.see_flush)
        pipeline.append(Deck.see_straight)
        pipeline.append(Deck.see_three_of_a_kind)
        pipeline.append(Deck.see_two_pairs)
        pipeline.append(Deck.see_one_pair)
        pipeline.append(Deck.see_high_card)
        for c in pipeline:
            if c(self) == 1:
                break
        return self.high

    def __repr__(self):
        if self.type == 'default':
            self.see_high()
        if len(self) == 5:
            return ("type:" + self.type + "; score:" + str(self.high) + "; cards:" + str(self.cards))
        else:
            return ("cards:" + str(self.cards))
    
    @property
    def sub_highest_deck(self):
        cdt_score = -1
        for x in it.combinations([0, 1, 2, 3, 4, 5, 6], 5):
            L = []
            for j in x:
                L.append(self.cards[j])
            temp_deck = Deck(L)
            temp_score = temp_deck.see_high()
            if temp_score > cdt_score:
                cdt_score, target = temp_score, temp_deck
        return target

    def see_straight_flush(self):
        if len(self.colors_set) >= 2:
            return 0
        flag2 = 0
        for i in [0]:
            flag = 0
            num = self.svalues[i]
            if self.svalues == [1, 2, 3, 4, 13]:
                pass
            else:
                for j in range(4):
                    if self.svalues[i+j+1] - self.svalues[i+j] == 1:
                        pass
                    else:
                        flag = 1
                        break
                if flag:
                    break
                self.type = 'straight_flush'
                flag2 = 1
        if not flag2:
            return 0
        self.high += 1e9
        if self.values != [1, 2, 3, 4, 13]:
            self.high += self.hstcard
        self.type = 'straight_flush'
        return 1
    
    def see_four_of_a_kind(self):
        if len(self.values_set) != 2:
            return 0
        for i in self.values_set:
            if self.values.count(i) in [2,3]:
                return 0
            if self.values.count(i) == 4:
                self.high += i * 100
            if self.values.count(i) == 1:
                self.high += i * 10
        self.high += 9e8
        self.type = 'four_of_a_kind'
        return 1
    
    def see_full_house(self):
        if len(self.values_set) != 2:
            return 0
        for i in self.values_set:
            if self.values.count(i) == 3:
                self.high += i * 100
            if self.values.count(i) == 2:
                self.high += i * 10
        self.high += 8e8
        self.type = 'full_house'
        return 1
    
    def see_flush(self):
        if len(self.colors_set) == 1:
            self.high += 7e8
            self.high += self.hstcard
            self.type = 'flush'
            return 1
        return 0
    
    def see_straight(self):
        if self.svalues == [1,2,3,4,13]:
            self.high += 6e8
            self.type = 'straight'
            return 1
        for i in [0]:
            flag = 0
            num = self.svalues[i]
            for j in range(4):
                if self.svalues[i+j+1] - self.svalues[i+j] == 1:
                    pass
                else:
                    flag = 1
                    break
            if flag:
                break
            self.high += 6e8
            self.high += self.hstcard
            self.type = 'straight'
            return 1
    
    def see_three_of_a_kind(self):
        L = []
        if len(self.values_set) != 3:
            return 0
        for i in self.values_set:
            if self.values.count(i) == 2:
                return 0
            if self.values.count(i) == 3:
                self.high += i * 100
            if self.values.count(i) == 1:
                L.append(i)
        self.high += 5e8
        self.high += max(L)
        self.type = 'three_of_a_kind'
        return 1
    
    def see_two_pairs(self):
        L = []
        if len(self.values_set) != 3:
            return 0
        for i in self.values_set:
            if self.values.count(i) == 2:
                L.append(i)
                self.high += i * 10
            if self.values.count(i) == 1:
                self.high += i
        self.high += 4e8
        self.high += max(L) * 10
        self.type = 'two_pairs'
        return 1
    
    def see_one_pair(self):
        L = []
        if len(self.values_set) != 4:
            return 0
        for i in self.values_set:
            if self.values.count(i) == 2:
                self.high += i * 100000
            if self.values.count(i) == 1:
                self.high += i
                L.append(i)
        L.sort()
        self.high += 3e8
        for i,j in enumerate(L):
            self.high += 14 ** i * j
        self.type = 'one_pair'
        return 1
    
    def see_high_card(self):
        self.high += 2e8
        for i,x in enumerate(self.svalues):
            self.high += (14 ** i) * x
        self.type = 'high_card'
        return 1

class Player():
    def __init__(self):
        self.score = -1
        self.private_cards = [[None,None] for _ in range(2)]
        self.combined_cards = [[None,None] for _ in range(7)]
        self.highest_cards = [[None,None] for _ in range(5)]
        self.id = -1
        self.type = "default"
        self.visible = 1

class MainLayout():
    card1 = [1, 0]
    card2 = [0, 0]
    card_pack = []
    for i in range(4):
        for j in range(13):
            card_pack.append([i+1,j+1])

    def __init__(self):
        self.players = [Player() for _ in range(8)]
        self.public_cards = [[None,None] for _ in range(5)]
        self.max_indexs = []

    def randomly_test(self,player_num = 2):
        print(" === TEST START !  ===")
        my_pack = MainLayout.card_pack.copy()
        random.shuffle(my_pack)
        players = self.players = [Player() for _ in range(player_num)]
        private_cards = [[] for _ in range(player_num)] # private cards actually
        combined_decks = [[] for _ in range(player_num)]
        scores = [0 for _ in range(player_num)]
        for i in range(player_num):
            private_cards[i].append(my_pack.pop())
            private_cards[i].append(my_pack.pop())
        public_cards = []
        for _ in range(5):
            public_cards.append(my_pack.pop())
        self.public_cards = public_cards
        for i in range(player_num):
            combined_decks[i] = Deck(private_cards[i] + public_cards)

        print(" public cards " + str(public_cards))
        for i in range(player_num):
            players[i].score = scores[i] = combined_decks[i].sub_highest_deck.see_high()
            players[i].private_cards = private_cards[i]
            players[i].combined_cards = combined_decks[i]
            players[i].highest_cards = combined_decks[i].sub_highest_deck
            print(" === player {} ！ ===".format(i + 1))
            print("private cards" + str(private_cards[i]))
            print("sub highest cards: " + str(players[i].highest_cards))
            players[i].id = i + 1
            players[i].type = players[i].highest_cards.type
            players[i].visible = 1

        max_indexs = []
        for i,s in enumerate(scores):
            if s == max(scores):
                max_indexs.append(i)
        max_indexs = [x+1 for x in max_indexs]
        if len(max_indexs) == 1:
            print(" === player {} wins！ ===".format(max_indexs[0]))
        else:
            temp_str = str(max_indexs[0])
            for i in range(1,len(max_indexs)):
                temp_str += " and {}".format(max_indexs[i])
            print(" === player " + temp_str + " wins！ ===")
        self.max_indexs = max_indexs

    def randomly_fixing_test(self):
        #print(" === TEST FIXING START !  ===")
        my_pack = MainLayout.card_pack.copy()
        random.shuffle(my_pack)
        players = self.players
        player_num = len(players)
        private_cards =  [x.private_cards for x in players]# private cards actually
        combined_decks = [[] for _ in range(player_num)]
        scores = [0 for _ in range(player_num)]
        public_cards = self.public_cards
        #pack_clear
        check_pack = []
        for i in range(player_num):
            for j in [0,1]:
                if private_cards[i][j][0] and private_cards[i][j][1]:
                    if private_cards[i][j] in my_pack:
                        my_pack.remove(private_cards[i][j])
                        check_pack.append(private_cards[i][j])

        for i in range(5):
            if public_cards[i][0] and public_cards[i][1]:
                my_pack.remove(public_cards[i])
                check_pack.append(public_cards[i])

        #if len(set(check_pack)) != len(check_pack):
        #    return

        for i in range(player_num):
            for j in [0,1]:
                bool = 1
                if private_cards[i][j][0] and private_cards[i][j][1]:
                    pass
                if private_cards[i][j][0] and not private_cards[i][j][1]:
                    ct = 0
                    while ct <= 1000:
                        ct += 1
                        private_cards[i][j][1] = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
                        if private_cards[i][j] in my_pack:
                            my_pack.remove(private_cards[i][j])
                            break
                    if ct > 1000: assert 0
                if private_cards[i][j][1] and not private_cards[i][j][0]:
                    ct = 0
                    while ct <= 1000:
                        ct += 1
                        private_cards[i][j][0] = random.choice([1, 2, 3, 4])
                        if private_cards[i][j] in my_pack:
                            my_pack.remove(private_cards[i][j])
                            break
                    if ct > 1000: assert 0
        for i,c in enumerate(public_cards):
            if public_cards[i][0] and public_cards[i][1]:
                pass
            if public_cards[i][0] and not public_cards[i][1]:
                ct = 0
                while ct <= 1000:
                    ct += 1
                    public_cards[i][1] = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
                    if public_cards[i] in my_pack:
                        my_pack.remove(public_cards[i])
                        break
                if ct > 1000: assert 0
            if public_cards[i][1] and not public_cards[i][0]:
                ct = 0
                while ct <= 1000:
                    ct += 1
                    public_cards[i][0] = random.choice([1, 2, 3, 4])
                    if public_cards[i] in my_pack:
                        my_pack.remove(public_cards[i])
                        break
                if ct > 1000: assert 0
        for i in range(player_num):
            for j in [0,1]:
                if not private_cards[i][j][1] and not private_cards[i][j][0]:
                    private_cards[i][j] = my_pack.pop()
        for i, c in enumerate(public_cards):
            if not public_cards[i][0] and not public_cards[i][1]:
                public_cards[i] = my_pack.pop()

        #print(" public cards " + str(public_cards))
        for i in range(player_num):
            players[i].combined_cards = Deck(players[i].private_cards + public_cards)
            players[i].score = players[i].combined_cards.sub_highest_deck.see_high()
            players[i].highest_cards = players[i].combined_cards.sub_highest_deck
            #print(" === player {} ！ ===".format(i + 1))
            #print("private cards" + str(private_cards[i]))
            #print("sub highest cards: " + str(players[i].highest_cards))
            players[i].id = i + 1
            players[i].type = players[i].highest_cards.type
            if players[i].visible:
                scores[i] = players[i].score

        max_indexs = []
        for i,s in enumerate(scores):
            if s == max(scores):
                max_indexs.append(i)
        max_indexs = [x+1 for x in max_indexs]
        if len(max_indexs) == 1:
            #print(" === player {} wins！ ===".format(max_indexs[0]))
            pass
        else:
            temp_str = str(max_indexs[0])
            for i in range(1,len(max_indexs)):
                temp_str += " and {}".format(max_indexs[i])
            #print(" === player " + temp_str + " wins！ ===")
        self.max_indexs = max_indexs

# print(gc.collect())

if __name__ == '__main__':
    Outest_Frame.main()
