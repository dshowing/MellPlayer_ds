#!/usr/bin/env python
# -*- coding: utf-8 -*-

#网易云资源爬取

'''
Netease Music API

Created on 2017-02-19
@author: Mellcap
'''
import sys
import requests
import json
from bs4 import BeautifulSoup

from mellplayer.utils.encrypt_utils import encrypted_request
from mellplayer.mell_logger import mell_logger


class Netease(object):

    def __init__(self):
        self.playlist_categories = []

    def wechat_request(self, url, method='GET', is_raw=True, data=None):
        '''
        调用微信二维码
        '''
        headers = {'appver': '2.0.2', 'Referer': 'http://music.163.com'}
        payload = {'snsType': '10', 'clientType': 'web2', 'callbackType': 'Login', 'forcelogin': 'true'}
        result = requests.get(url=url, headers=headers, params=payload)

        # if request failed, return False
        if not result.ok:
            return False

        h = result.text
        soup = BeautifulSoup(h, "html.parser")
        a = soup.find_all('img', {'class': 'qrcode lightBorder'})
        qrstr = str(a)
        qrcode = qrstr[-20:-4]
        #返回唯一的16位字串
        return qrcode


    def _request(self, url, payload=None, method='GET', is_raw=True, data=None):
        '''
        对requests简单封装
        '''
        headers = {'appver': '2.0.2', 'Referer': 'http://music.163.com'}
        if method == 'GET':
            result = requests.get(url=url, headers=headers, params=payload)   #添加了params参数，通过payload方式请求
        elif method == 'POST' and data:
            result = requests.post(url=url, data=data, headers=headers)
        # if request failed, return False
        if not result.ok:
            return False
        result.encoding = 'UTF-8'
        if is_raw:
            return json.loads(result.text)
        return result.text

#######################################
#    用户登陆后的请求信息
#######################################

    def user_id(self):
        '''
        用户ID
        http://music.163.com/
        '''
        url = 'http://music.163.com/'
        result = self._request(url)
        return result

    def user_name(self):
        '''
        用户name
        http://music.163.com/
        '''
        url = 'http://music.163.com/'
        result = self._request(url)
        return result

    def user_playlist(self, user_id):
        '''
        用户歌单（创建）
        http://music.163.com/#/my/m/music/playlist?id=30408531
        {id: 30408531}
        '''
        payload = {'id': 'user_id'}
        url = 'http://music.163.com/#/my/m/music/playlist'
        result = self._request(url, payload)
        return result

    def user_playlist_info(self, list_id):
        '''
        用户歌单详情
        http://music.163.com/#/my/m/music/playlist?id=30408531
        '''
        payload = {'id': 'list_id'}
        url = 'http://music.163.com/#/my/m/music/playlist'
        result = self._request(url, payload)
        return result

    def user_song_detail(self, song_id):
        '''
        歌曲详情
        https://music.163.com/#/song?id=254460
        https://music.163.com/#/song?id=1311319058
        '''
        payload = {'id': 'song_id'}
        url = 'https://music.163.com/#/song'
        result = self._request(url, payload)
        return result

    def user_lyric_detail(self, song_id):
        '''
        歌词详情
        http://music.163.com/api/song/lyric?os=osx&id=xxx&lv=-1&kv=-1&tv=-1
        使用mell作者api，不清楚怎么找到的？
        '''
        payload = {'lyric': 'song_id', 'os': 'osx', 'id':song_id, 'lv':'-1', 'kv':'-1', 'tv':'-1'}
        url = 'http://music.163.com/api/song'
        result = self._request(url, payload)
        return result

    def user_result_parse(self, data, parse_type):
        '''
        解析信息
        '''
        res = None
        if parse_type == 'category_playlists':
            res = [d['id'] for d in data['playlists']]

        # 播放列表
        elif parse_type == 'playlist_detail':
            tracks = data['result']['tracks']
            playlist_ids = [t['id'] for t in tracks]
            playlist_detail = {t['id']: {
                'song_id': t['id'],
                'song_name': t['name'],
                'song_url': t['mp3Url'],
                'song_artists': ' & '.join(map(lambda a: a['name'], t['artists']))
            } for t in tracks}
            res = (playlist_ids, playlist_detail)

        # 歌词信息
        elif parse_type == 'lyric_detail':
            if 'lrc' in data:
                res = {
                    'lyric': data['lrc']['lyric']
                }
            else:
                res = {
                    'lyric': 'no_lyric'
                }

        # 歌曲详情
        elif parse_type == 'song_detail_new':
            res = {d['id']: {
                'song_url': d['url'],
                'song_br': d['br']
            } for d in data['data']}

        return res



###############################################
#     游客歌单
###############################################

    def playlist_categories(self):
        '''
        分类歌单
        http://music.163.com/discover/playlist/
        '''
        url = 'http://music.163.com/discover/playlist/'
        result = self._request(url)
        return result

    def category_playlists(self, category='流行', offset=0, limit=50, order='hot', total='false'):
        '''
        分类详情
        http://music.163.com/api/playlist/list?cat=流行&order=hot&offset=0&total=false&limit=50
        '''
        url = 'http://music.163.com/api/playlist/list?cat=%s&order=%s&offset=%s&total=%s&limit=%s' % (category, order, offset, total, limit)
        result = self._request(url)
        return result

    def playlist_detail(self, playlist_id):
        '''
        歌单详情
        http://music.163.com/api/playlist/detail?id=xxx
        '''
        url = 'http://music.163.com/api/playlist/detail?id=%s' % playlist_id
        result = self._request(url)
        return result

    
    def song_detail(self, song_ids):
        '''
        歌曲详情
        http://music.163.com/api/song/detail?ids=[xxx, xxx]
        '''
        url = 'http://music.163.com/api/song/detail?ids=%s' % song_ids
        result = self._request(url)
        return result

    def song_detail_new(self, song_ids):
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        data = {'ids': song_ids, 'br': 320000, 'csrf_token': ''}
        data = encrypted_request(data)
        result = self._request(url, method="POST", data=data)
        return result

   
    def lyric_detail(self, song_id):
        '''
        歌词详情
        http://music.163.com/api/song/lyric?os=osx&id=xxx&lv=-1&kv=-1&tv=-1
        '''
        url = 'http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1' % song_id
        result = self._request(url)
        return result



    def parse_info(self, data, parse_type):
        '''
        解析信息
        '''
        res = None
        if parse_type == 'category_playlists':
            res = [d['id'] for d in data['playlists']]

        #播放列表
        elif parse_type == 'playlist_detail':
            tracks = data['result']['tracks']
            playlist_ids = [t['id'] for t in tracks]
            playlist_detail = {t['id']: {
                'song_id': t['id'],
                'song_name': t['name'],
                'song_url': t['mp3Url'],
                'song_artists': ' & '.join(map(lambda a: a['name'], t['artists']))
            } for t in tracks}
            res = (playlist_ids, playlist_detail)

        #歌词信息
        elif parse_type == 'lyric_detail':
            if 'lrc' in data:
                res = {
                    'lyric': data['lrc']['lyric']
                }
            else:
                res = {
                    'lyric': 'no_lyric'
                }

        #歌曲详情
        elif parse_type == 'song_detail_new':
            res = {d['id']: {
                'song_url': d['url'],
                'song_br': d['br']
            } for d in data['data']}

        return res
                
            
