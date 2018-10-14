#/usr/bin/env python
# -*- encoding : utf-8 -*-
# created by dshowing

import sys
import qrcode

from mellplayer.api import Netease
from mellplayer.qr import QR


class login(object):

    def wechat(self):

        str_addr = 'https://open.weixin.qq.com/connect/confirm?uuid='
        url = "https://music.163.com/api/sns/authorize"
        str = Netease.wechat_request(url)

        print('str is: %s' %str)
        qr_text = str_addr + str
        #return qr_text

        qr = QR(10)
        return qr.showqr(qr_text)



