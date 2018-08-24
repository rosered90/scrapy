# _*_ coding:utf-8 _*_
from wxpy import *
import random

bot = Bot()
embed()

number = random.randint(0,9)
#找好友
my_friends = bot.friends().search(u'噗咚')[0]
my_friends.send('%s次元美少女吧向你问好！！'%number)

