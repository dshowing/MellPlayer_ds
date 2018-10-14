#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Starter

Created on 2017-03-05
@author: Mellcap
'''

from mellplayer.controller import mell_ui, initial_player
from mellplayer.watcher import time_watcher, key_watcher
from mellplayer.login import login

def main():

    Login = login
    Login.wechat()


    # print('Initial Player...')
    # initial_player()
    # time_watcher()
    # key_watcher()
    # mell_ui.display()

if __name__ == '__main__':
    main()
