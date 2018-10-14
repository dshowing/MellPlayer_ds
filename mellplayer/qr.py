#/usr/bin/env python
# -*- encoding : utf-8 -*-
# created by dshowing

import qrcode

class QR(object):

    def __init__(self, STEP):
        self.STEP = STEP

    def str2qr(self, text):
        """
        把给定的字符串生成一个对应的二维码
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=self.STEP,
            border=0,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image()
        return self.qr2ascii(img)

    def qr2ascii(self, image):
        """
        从二维码图片生成ascii二维码
        """
        string = ''
        image = image.convert('L')  # 转为灰白模式
        width, height = image.size

        pix = image.load()
        for i in range(0, width, self.STEP):
            for j in range(0, height, self.STEP):
                p = pix[i, j]
                p = '██' if p > 0 else '  '
                string += p
            string += '\n'
        return string
        #print string

    def showqr(self, url):

        qrcode = self.str2qr(url)
        return qrcode


# a = 'https://open.weixin.qq.com/connect/confirm?uuid=021lO27PXTaqOwbx'
# qr = QR(10)
# qr.showqr(a)
