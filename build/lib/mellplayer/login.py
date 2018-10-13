#/usr/bin/env python
# -*- encoding : utf-8 -*-
# created by dshowing

import sys
import qrcode

from mellplayer.api import Netease
from mellplayer.qr import QR


class login(object):

    def wechat(self):

        #str_addr = 'https://open.weixin.qq.com/connect/confirm?uuid='
        url = "https://music.163.com/api/sns/authorize?snsType=10&clientType=web2&callbackType=Login&forcelogin=true"
        str = Netease.qr_request(url)

        qr_text = str_addr + str
        #return qr_text

        QR.showqr(qr_text)






