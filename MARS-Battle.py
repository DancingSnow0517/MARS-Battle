# -*- coding: utf-8 -*-
import random
import time
from threading import Thread
Playerlist = []
Deathlist = []
Tick = 300
Size = 3000
Statu = False

class NextPlayer(Thread):
    def __init__(self,server):
        super().__init__()
        self.shutdown_flag = False
        self.server = server
    def run(self):
        global gap
        global PlayerPos
        while not self.shutdown_flag:
            server = self.server
            server.say('进入线程')
            PlayerlistLoad(server,None)
            time.sleep(0.05)
            List = hebin()
            print(List)
            x = []
            y = []
            z = []
            for i in range(len(List)):
                PosLoad(server,None,i)
                x.append(i)
                y.append(i)
                z.append(i)
                time.sleep(0.05)
                x[i] = PlayerPos[0]
                #server.say(x[i])
                y[i] = PlayerPos[1]
                z[i] = PlayerPos[2]
            for i in range(len(List)):
                Posi = []
                Posi.append(x[i])
                Posi.append(y[i])
                Posi.append(z[i])
                Min = 999999
                for j in range(len(List)):
                    if i != j:
                        Posj = []
                        Posj.append(x[j])
                        Posj.append(y[j])
                        Posj.append(z[j])
                        juli(server,Posi,Posj)
                        time.sleep(0.05)
                        #server.say(gap)
                        if gap < Min:
                            Min = gap
                        #server.say(gap)
                server.execute('title ' + List[i] + ' actionbar {"text":"' + '最近的玩家距离你 §a' + str(Min) + '§r 米"}')

class bossbar(Thread):
    def __init__(self,server):
        super().__init__()
        self.shutdown_flag = False
        self.server = server
    def run(self):
        global Tick
        server = self.server
        #server.say('进入线程')
        if self.shutdown_flag:
            return
        Wait = Tick/5*2
        server.execute('bossbar add timer {"text":"timer"}')
        server.execute('bossbar set minecraft:timer color green')
        server.execute('bossbar set minecraft:timer max ' + str(int(Wait)))
        server.execute('bossbar set minecraft:timer players @a')
        for i in range(int(Wait)):
            if self.shutdown_flag:
                return
            server.execute('bossbar set minecraft:timer value ' + str(int(Wait - i)))
            server.execute('bossbar set minecraft:timer name ' + '{"text":"§a在 §c' + str(int(Wait - i)) + ' §a秒后开始缩圈"}')
            time.sleep(1)
        server.execute('bossbar set minecraft:timer color red')
        server.execute('bossbar set minecraft:timer max ' + str(int(Tick - Wait)))
        for i in range(int(Tick - Wait)):
            if self.shutdown_flag:
                return
            server.execute('bossbar set minecraft:timer value ' + str(int(Tick - Wait - i)))
            server.execute('bossbar set minecraft:timer name ' + '{"text":"§e在 §c' + str(int(Tick - Wait - i)) + ' §e秒后缩圈结束"}')
            time.sleep(1)

def juli(server,i,j,info = None):
    global gap
    if info == None:
        cmd = 'distance from {0} {1} {2} to {3} {4} {5}'.format(str(i[0]),str(i[1]),str(i[2]),str(j[0]),str(j[1]),str(j[2]))
        server.execute(cmd)
    else:
        #server.say('计算')
        content = info.content
        #server.say('|' + content.split(': ')[1] + '|')
        gap = int((content.split(': ')[1]).split('.')[0])

def hebin():
    global Deathlist
    global Playerlist
    new = []
    for i in Playerlist:
        if i not in Deathlist:
            new.append(i)
    return new

def NextSize(Now):
    return random.randint(int(Now / 2),int(Now/3*2))

def rand(Plist):
    if len(Plist) <= 2:
        return None
    print(len(Plist))
    pos = []
    random.seed(time.time())
    r = random.randint(0,len(Plist) - 1)
    for i in range(0,len(Plist)):
        while (r == i) or (r in pos):
            if i == len(Plist)-1 and r == i:
                    return rand(Plist)
            random.seed(time.time())
            r = random.randint(0,len(Plist)-1)
            print('r:' + str(r))
        pos.append(i)
        pos[i] = r
    return pos

def Change(server,rand):
    global PlayerPos
    x = []
    y = []
    z = []
    if len(hebin()) == 2:
        PosLoad(server,None,0)
        x.append(0)
        y.append(0)
        z.append(0)
        time.sleep(0.05)
        x[0] = PlayerPos[0]
        y[0] = PlayerPos[1]
        z[0] = PlayerPos[2]
        server.execute('tp ' + hebin()[0] + ' ' + hebin()[1])
        time.sleep(0.1)
        server.execute('tp ' + hebin()[1] + ' ' + x[0] + ' ' + y[0] + ' ' + z[0])
        return
    for i in range(len(hebin())):
        PosLoad(server,None,i)
        x.append(i)
        y.append(i)
        z.append(i)
        time.sleep(0.05)
        x[i] = PlayerPos[0]
        #server.say(x[i])
        y[i] = PlayerPos[1]
        z[i] = PlayerPos[2]
    for i in range(len(hebin())):
        server.execute('tp ' + hebin()[i] + ' ' + x[rand[i]] + ' ' + y[rand[i]] + ' ' + z[rand[i]])

def main(server):
    global Deathlist
    global Playerlist
    global Tick
    global Statu 
    global Size
    global a
    Flag = 0
    Damage = 0.1
    MSize = Size
    Statu = True
    Deathlist = []
    server.execute('worldborder center 0 0')
    server.execute('worldborder set ' + str(MSize) + ' 0')
    server.execute('gamemode survival @a')
    server.execute('clear')
    server.execute('advancement revoke @a everything')
    server.say('Game start')
    PlayerlistLoad(server,None)
    time.sleep(0.1)
    server.execute('spreadplayers 0 0 300 1400 under 100 false @a') 
    server.execute('effect give @a minecraft:regeneration 5 255')
    server.execute('effect give @a minecraft:saturation 5 255')
    while len(hebin()) > 1:
        if Flag != 0:
            server.execute('worldborder damage amount ' + str(Damage))
            #server.say(Damage)
            Damage += 0.05
            #server.say('进度条开启')
        if Flag != 0:
            a = bossbar(server)
            a.start()
        Wait = Tick/5*2
        #server.say(Wait)
        time.sleep(Wait)
        if Statu == False:
            a.shutdown_flag = True
            server.execute('bossbar remove minecraft:timer')
            server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
            server.execute('gamemode adventure @a')
            break

        if Flag !=0:
            MSize = NextSize(MSize)
            #server.say(MSize)
            server.execute('worldborder set ' + str(MSize) + ' ' + str(int(Tick - Wait)))
            server.say('开始缩圈')
        time.sleep(Tick - Wait - 10)

        if Statu == False:
            a.shutdown_flag = True
            server.execute('bossbar remove minecraft:timer')
            server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
            server.execute('gamemode adventure @a')
            break

        server.say('10s后随机交换位置')
        server.execute('execute at @a run playsound minecraft:block.note_block.pling player @p ~ ~ ~ 1 2')

        for i in range(7):
            server.say('§c' + str(10 - i))
            time.sleep(1)
            if Statu == False:
                a.shutdown_flag = True
                server.execute('bossbar remove minecraft:timer')
                server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
                server.execute('gamemode adventure @a')
                break
        
        server.say('§c3')
        server.execute('execute at @a run playsound minecraft:entity.arrow.hit_player player @p ~ ~ ~ 1 0.5')
        time.sleep(1)
        if Statu == False:
            a.shutdown_flag = True
            server.execute('bossbar remove minecraft:timer')
            server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
            server.execute('gamemode adventure @a')
            break
        server.say('§c2')
        server.execute('execute at @a run playsound minecraft:entity.arrow.hit_player player @p ~ ~ ~ 1 0.5')
        time.sleep(1)
        if Statu == False:
            a.shutdown_flag = True
            server.execute('bossbar remove minecraft:timer')
            server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
            server.execute('gamemode adventure @a')
            break
        server.say('§c1')
        server.execute('execute at @a run playsound minecraft:entity.arrow.hit_player player @p ~ ~ ~ 1 1')
        PlayerlistLoad(server,None)
        time.sleep(0.1)
        if len(hebin()) == 1:
            a.shutdown_flag = True
            server.execute('bossbar remove minecraft:timer')
            server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
            server.execute('gamemode adventure @a')
            break

        Flag += 1
        PlayerlistLoad(server,None)
        time.sleep(0.1)

        Change(server,rand(hebin()))
    
def PosLoad(server,info,Num = None):
    global Playerlist
    if Num == None:
        content = info.content
        Mid = ((content.split(': ')[1]).split('[')[1]).split(']')[0]
        position = Mid.split('d, ')
        position[2] = position[2].split('d')[0]
        return position
    else:
        server.execute('data get entity ' + Playerlist[Num] + ' Pos')

def PlayerlistLoad(server,info):
    if info == None:
        server.execute('list')
    else:
        content = info.content
        PlayerStr = content.split(': ')[1]
        Playerlist = PlayerStr.split(', ')
        return Playerlist

def on_load(server,old):
    server.add_help_message('!!list','获取列表')

def on_info(server,info):
    global Playerlist
    global PlayerPos
    content = info.content
    if 'Manhattan' in content:
        #server.say(content)
        juli(server,None,None,info)
    if 'There are' in content and 'players online' in content:
        Playerlist = PlayerlistLoad(server,info)
        #server.say(PlayerlistLoad(server,info))
        #server.say(str(len(Playerlist)) + ' ')
    if  'has the following entity data:' in  content:
        #server.say('X:' + PosLoad(server,info)[0] + ' Y:' + PosLoad(server,info)[1] + ' Z:' + PosLoad(server,info)[2])
        PlayerPos = PosLoad(server,info)
def on_death_message(server, death_message):
    global Deathlist
    global Playerlist
    global Statu
    Name = death_message.split(' ')[0]
    Deathlist.append(Name)
    time.sleep(0.1)
    server.execute('gamemode adventure ' + Name)
    if Statu == True:
        server.say('玩家 §6' + Name + '§r 出局')
        server.execute('gamemode spectator ' + Name)
        if len(hebin()) == 1:
            server.say('游戏结束 ' + hebin()[0] + ' 获胜')
            server.execute('bossbar remove minecraft:timer')
            server.execute('worldborder set 10000 0')
            server.execute('execute in minecraft:overworld run tp @a 3.02 140.00 -99.95')
            server.execute('gamemode adventure @a')
            Statu = False
            a.shutdown_flag = True
            #b.shutdown_flag = True
def on_player_joined(server, player):
    global Deathlist
    if Statu == True:
        server.execute('gamemode spectator ' + player)
        Deathlist.append(player)
    server.tell(player,'使用§6/trigger Timer§r来查看规则')

def on_user_info(server, info):
    global Playerlist
    content = info.content
    if content == '!!start':
        if Statu:
            server.say('不要重复开局，游戏已经开始了')
        else:
            main(server)
    if content == '!!bar':
        global a
        a = bossbar(server)
        a.start()
    if content == '!!t':
        server.execute('bossbar set minecraft:timer name {"text":"\u6d4b\u8bd5","color":"red"}')
