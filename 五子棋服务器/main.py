#encoding:utf-8
import pygame
from pygame.locals import *
import sys
import math
import storn
from socket import *
import select

pygame.init()


BLACK = (0,0,0)
WHITE = (255,255,255)

#TCP服务
HOST = ''                   #地址
POST = 21578                #端口
BUFSIZ = 2048               
ADDR = (HOST,POST)
tcpsersock = socket(AF_INET,SOCK_STREAM)
tcpsersock.bind(ADDR)
tcpsersock.listen(5)


inputs = [tcpsersock]


#判断是否有子
def isempty(me,targert):
    a = False
    for i in targert:
        if i.location() == me.location():
            a = True
    return a


#判断是否有五子连线
def iswin(targert):
    x = []
    y = []
    for i in range(0,15):
        x.append(28+i*40)
    for i in range(0,15):
        y.append(28+i*40)
    for each in targert:
        (a,b) = each.location()
        
        #x轴方向
        num_x = 0
        c = a - 40
        d = a + 40
        while c > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c,b):
                    num_x += 1
                    isbreak = False
            if not isbreak:
                c -= 40
            else:
                break 
        while d < 615:
            isbreak = True 
            for i in targert:
                if i.location() == (d,b):
                    num_x += 1
                    isbreak = False
            if not isbreak:
                d += 40
            else:
                break
        num_x += 1
        
        #y轴方向
        num_y = 0
        e = b - 40
        f = b + 40
        while e > 0:
            isbreak = True
            for i in targert:
                if i.location() == (a,e):
                    num_y += 1
                    isbreak = False
            if not isbreak:        
                e -= 40
            else:
                break
        while f < 615:
            isbreak = True
            for i in targert:
                if i.location() == (a,f):
                    num_y += 1
                    isbreak = False
            if not isbreak:
                f += 40
            else:
                break
        num_y += 1
        
        #西北，东南方向
        num_en = 0
        c1 = a - 40
        c2 = b - 40
        c3 = a + 40
        c4 = b + 40
        while c1>0 and c2>0:
            isbreak = True
            for i in targert:
                if i.location() == (c1,c2):
                    num_en += 1
                    isbreak = False
            if not isbreak:
                c1 -= 40
                c2 -= 40
            else:
                break
        while c3 < 615 and c4 < 615:
            isbreak = True
            for i in targert:
                isbreak = True
                if i.location() == (c3,c4):
                    num_en += 1
                    isbreak = False
            if not isbreak:
                c3 += 40
                c4 += 40
            else:
                break
        num_en += 1

        #东北，东南方向
        num_wn = 0
        c5 = a + 40
        c6 = b - 40
        c7 = a - 40
        c8 = b + 40
        while c5 < 615 and c6 > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c5,c6):
                    num_wn += 1
                    isbreak = False
            if not isbreak:
                c5 += 40
                c6 -= 40
            else:
                break
        while c7 > 0 and c8 < 615:
            isbreak = True
            for i in targert:
                isbreak = True
                if i.location() == (c3,c4):
                    num_wn += 1
                    isbreak = False
            if not isbreak:
                c7 -= 40
                c8 += 40
            else:
                break
        num_wn += 1
        if num_x >= 5 or num_y >= 5 or num_en >= 5 or num_wn >= 5:
            return True
    return False
    

  
def main():
        
    clock = pygame.time.Clock()

    bg_size = 615,615

    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption('五子棋')
    bg_image = pygame.image.load('image/bg.png').convert_alpha()  #背景图片

    #背景音乐
    bg_sound = pygame.mixer.music.load('sound/bg_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #棋子
    white_chesses = []
    black_chesses = []
    chesses = []

    #标志轮到哪方下棋
    isplay = False

    #标志是否连接
    islink = False

    #标志是否结束游戏
    result = False

    # 标志人与人
    is_people = False

    # 标志人与电脑
    is_ai = False

    # 标志是否做出选择
    is_choise = False

    #标志是否关闭声音
    is_have_sound = True

    #输赢
    font1 = pygame.font.Font('font/12345.TTF',35)
    win_text = font1.render("You Lose!!!",True,WHITE)
    win_text_rect = win_text.get_rect()
    win_text_rect.left,win_text_rect.top = (bg_size[0]-win_text_rect.width)//2,\
                                           (bg_size[1]-win_text_rect.height)//2
    lose_text = font1.render("You Win...",True,WHITE)
    lose_text_rect = lose_text.get_rect()
    lose_text_rect.left,lose_text_rect.top = (bg_size[0]-lose_text_rect.width)//2,\
                                           (bg_size[1]-lose_text_rect.height)//2
    play_text = font1.render("Play Again",True,WHITE)
    play_text_rect = play_text.get_rect()

    # 登入选项
    text1 = font1.render(u"玩家与玩家",True, WHITE)
    text1_rect = text1.get_rect()
    text1_rect.left, text1_rect.top = (bg_size[0] - text1_rect.width) // 2, \
                                      (bg_size[1] - text1_rect.height) // 2 - 100
    text2 = font1.render(u'玩家与玩家',True, WHITE)
    text2_rect = text2.get_rect()
    text2_rect.left, text2_rect.top = (bg_size[0] - text1_rect.width) // 2, \
                                      (bg_size[1] - text1_rect.height) // 2
    text3 = font1.render(u'声音：  开',True, WHITE)
    text3_rect = text3.get_rect()
    text3_rect.left, text3_rect.top = (bg_size[0] - text3_rect.width) // 2, \
                                      (bg_size[1] - text3_rect.height) // 2 + 100
    text4 = font1.render(u'声音：  关',True, WHITE)
    text4_rect = text4.get_rect()
    text4_rect.left, text4_rect.top = (bg_size[0] - text4_rect.width) // 2, \
                                     (bg_size[1] - text4_rect.height) // 2 + +100

    running  = True 

    while running:

        screen.blit(bg_image,(0,0))

        #绘制棋子
        if is_choise:
            if chesses:
                for i in chesses:
                    screen.blit(i.image,i.location())

        # 绘制选项
        if not is_choise:
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if text1_rect.left <= pos[0] <= text1_rect.left + 170 and \
                                        text1_rect.top <= pos[1] <= text1_rect.top + 30:
                    is_choise = True
                    is_people = True
                if text1_rect.left <= pos[0] <= text1_rect.left + 170 and \
                                                text1_rect.top + 100 <= pos[1] <= text1_rect.top + 130:
                    is_choise = True
                    is_ai = True
                if text1_rect.left <= pos[0] <= text1_rect.left + 160 and \
                                                text1_rect.top + 200 <= pos[1] <= text1_rect.top + 230:
                    is_have_sound = not is_have_sound
                    if not is_have_sound:
                        pygame.mixer.stop()
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play()

        #接收cli的消息
        rs,ws,es = select.select(inputs,[],[],0)
        for r in rs:
            if r is tcpsersock:
                tcpclisock,addr = tcpsersock.accept()
                inputs.append(tcpclisock)
                print 'connenct'
            else:
                try:
                    data = r.recv(BUFSIZ)
                    disconnected = not data
                    islink = True
                except socket.error:
                    disconnected = True
                    islink = False
                if disconnected:
                    inputs.remove(r)
                else:
                    if not isplay:
                        me = storn.Storn_White(eval(data))
                        white_chesses.append(me)
                        chesses.append(me)
                        isplay = True

        
        for event in pygame.event.get():
            if event.type == QUIT:
                if islink:
                    tcpclisock.close()
                tcpsersock.close()
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and not result:
                    if isplay and islink:
                        pos = pygame.mouse.get_pos()
                        me = storn.Storn_Black(pos)
                        if not isempty(me,chesses):
                            black_chesses.append(me)
                            chesses.append(me)
                            tcpclisock.send(str(pos))
                            isplay = False
                        else:
                            del(me)

         #判断输赢
        if iswin(black_chesses):
            screen.blit(win_text,win_text_rect)
            screen.blit(play_text,(win_text_rect.left,win_text_rect.top + 80))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if win_text_rect.left < pos[0] < win_text_rect.right and\
                   win_text_rect.top < pos[1] < win_text_rect.top + 80:
                    main()
            result = True
        if iswin(white_chesses):
            screen.blit(lose_text,lose_text_rect)
            screen.blit(play_text,(win_text_rect.left,win_text_rect.top + 80))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if win_text_rect.left < pos[0] < win_text_rect.right and\
                   win_text_rect.top < pos[1] < win_text_rect.top + 80:
                    main()
            result = True
       
            
        pygame.display.flip()

        clock.tick(60)
        
if __name__ == '__main__':
    main()
