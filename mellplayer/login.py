#/usr/bin/env python
# -*- encoding : utf-8 -*-
# created by dshowing
# Login func in here

import sys
import qrcode

from mellplayer.api import Netease
from mellplayer.qr import QR


class login(object):

    def wechat(self):
        '''
        生成微信二维码
        '''
        str_addr = 'https://open.weixin.qq.com/connect/confirm?uuid='
        url = "https://music.163.com/api/sns/authorize"
        netease = Netease()
        str_qrcd = netease.wechat_request(url)

        qr_text = str_addr + str_qrcd

        qr = QR(10)
        print(qr.showqr(qr_text))





