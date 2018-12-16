# coding:utf-8
import requests
import urllib
import json
from urllib import parse
import random
import bs4
from bs4 import BeautifulSoup
import re
import traceback
import time

#缺少对
# 歌曲分类，歌词，风格，其他歌名
#1.抓取所有的分类的id，然后拼接出对应的分类的链接
#2.访问分类的链接，抓于歌名的相关信息的获取取所有歌单的详细页面的链接
#3.访问详细页面的链接，抓取所有歌曲的详细页面的链接
#4.抓取歌曲的信息，并将歌曲名传递给download_music实现，下载对应音乐文件


def getMusicClassList(classList):
    url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_tag_conf.fcg'
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    ua = random.choice(user_agent_list)
    headers = {
        'user-agent': ua,
        'cookie':'tvfe_boss_uuid=64b6b2786eaf1f75; pgv_pvid=6995182145; pgv_pvi=3893107712; pt2gguin=o0616019674; RK=IUqxal2BQ7; ptcz=9d55483937dfb247e5c48de0bc63b2f40231f50b3db6ed1d5552e9e12f1cc8ef; o_cookie=616019674; pac_uid=1_616019674; ptui_loginuin=616019674; ts_refer=www.baidu.com/link; ts_uid=8403956730; _ga=GA1.2.1961417591.1543309296; yq_index=0; logout_page=; pgv_si=s9796213760; pgv_info=ssid=s9210033334; yqq_stat=0; ts_last=y.qq.com/portal/playlist.html',
        'referer':'https://y.qq.com/portal/playlist.html'
    }
    paramter = {
        'g_tk': '5381',
        'jsonpCallback': 'getPlaylistTags',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'jsonp',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq',
        'needNewCode': '0'
    }
    # 此处注释选用为高匿伪装IP，进行IP欺骗
    proxies = {
        'http': 'http://121.31.195.209:8123',
        'https': 'https://118.190.94.224:9001'
    }
    html = requests.get(url, headers=headers, params=paramter)
    html.encoding = 'utf-8'
    for i in range(5):
        res = json.loads(html.text.lstrip('getPlaylistTags(').rstrip(')'))['data']['categories'][i+1]['items']
        if res != []:
            for t_item in res:
                item = t_item['categoryId']      # 获取音乐类别对应的代号
                classList.append(item)

def getPlaylistId(playList, classList):
    count = 0
    n = len(classList)
    for i in classList:
        url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': 'tvfe_boss_uuid=64b6b2786eaf1f75; pgv_pvid=6995182145; pgv_pvi=3893107712; pt2gguin=o0616019674; RK=IUqxal2BQ7; ptcz=9d55483937dfb247e5c48de0bc63b2f40231f50b3db6ed1d5552e9e12f1cc8ef; o_cookie=616019674; pac_uid=1_616019674; ptui_loginuin=616019674; ts_refer=www.baidu.com/link; ts_uid=8403956730; _ga=GA1.2.1961417591.1543309296; pgv_si=s1013340160; pgv_info=ssid=s7672041533; yplayer_open=1; qqmusic_fromtag=66; yq_playschange=0; yq_playdata=; player_exist=1; yqq_stat=0; ts_last=y.qq.com/n/yqq/playsquare/3833853300.html; yq_index=6',
            'referer': 'https://y.qq.com/portal/playlist.html'
        }
        paramter = {
            # 'picmid': '1',
            # 'rnd': '0.7409337691594351',
            'g_tk': '5381',
            'jsonpCallback': 'getPlaylist',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'jsonp',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0',
            'categoryId': i,
            'sortId': '5',
            'sin': '0',
            'ein': '29'
        }
        # 此处注释选用为高匿伪装IP，进行IP欺骗
        proxies = {
            'http': 'http://118.187.58.34:53281',
            'https': 'https://222.171.251.43:40149'
        }
        html = requests.get(url, headers=headers, params=paramter)
        res = json.loads(html.text.lstrip('getPlaylist(').rstrip(')'))['data']['list']
        if res != []:
            for t_item in res:
                ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')  # 用于去掉非法字符
                item = t_item['dissid']  # 获取音乐类别对应的代号
                playList.append(item)
        count = count + 1
        print("\r爬取歌单-当前进度:{:.2f}%".format(count * 100 / n), end="")


def getSongList(playlist):
    count = 0
    n = len(playlist)
    for i in playlist:
        start = time.time()
        url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': 'tvfe_boss_uuid=64b6b2786eaf1f75; pgv_pvid=6995182145; pgv_pvi=3893107712; pt2gguin=o0616019674; RK=IUqxal2BQ7; ptcz=9d55483937dfb247e5c48de0bc63b2f40231f50b3db6ed1d5552e9e12f1cc8ef; o_cookie=616019674; pac_uid=1_616019674; ptui_loginuin=616019674; ts_refer=www.baidu.com/link; ts_uid=8403956730; _ga=GA1.2.1961417591.1543309296; pgv_si=s1013340160; pgv_info=ssid=s7672041533; qqmusic_fromtag=66; yqq_stat=0; yq_index=0; yplayer_open=1; yq_playschange=1; yq_playdata=s_0_1_5; player_exist=0; ts_last=y.qq.com/n/yqq/song/004LkueT3snRTI.html',
            'referer': 'https://y.qq.com/n/yqq/playsquare/' + i + '.html'
        }
        paramter = {
            'type': '1',
            'json': '1',
            'utf8': '1',
            'onlysong': '0',
            'disstid': i,
            'g_tk': '5381',
            'jsonpCallback': 'playlistinfoCallback',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'jsonp',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0'
        }
        html = requests.get(url, headers=headers, params=paramter)
        res = json.loads(html.text.lstrip('playlistinfoCallback(').rstrip(')'))['cdlist'][0]['songlist']
        for t_item in res:
            data = []
            if 'songmid' in t_item:
                item0 = str(t_item['songmid'])
                data.append(item0)
                if 'songid' in t_item:
                    item1 = str(t_item['songid'])
                    data.append(item1)
                    getSongInfo(data)
        count = count + 1
        end = time.time()
        print("\r当前进度:{:.2f}% 预计还需要：{:.2f}分钟".format(count * 100 / n, (n - count)*(end-start)/60), end="")

def getSongInfo(songList):
    fpath = 'D:\Coding\Python\python_test\py_pro\homeworkOfSpider\music.txt'
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'cookie': 'tvfe_boss_uuid=64b6b2786eaf1f75; pgv_pvid=6995182145; pgv_pvi=3893107712; pt2gguin=o0616019674; RK=IUqxal2BQ7; ptcz=9d55483937dfb247e5c48de0bc63b2f40231f50b3db6ed1d5552e9e12f1cc8ef; o_cookie=616019674; pac_uid=1_616019674; ptui_loginuin=616019674; ts_refer=www.baidu.com/link; ts_uid=8403956730; _ga=GA1.2.1961417591.1543309296; pgv_si=s1013340160; pgv_info=ssid=s7672041533; qqmusic_fromtag=66; yq_index=0; yplayer_open=1; yq_playschange=1; player_exist=0; yq_playdata=p_5711236686_1_5; yqq_stat=0; ts_last=y.qq.com/portal/playlist.html',
        'referer': 'https://y.qq.com/n/yqq/song/' + songList[0] + '.html'
    }
    paramter = {
        'disstid': songList[0],
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'jsonp',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq',
        'needNewCode': '0',
        'data': '{"songinfo":{"method":"get_song_detail_yqq","param":{"song_type":0,"song_mid":"' + songList[0] + '","song_id":' + songList[1] + '},"module":"music.pf_song_detail_svr"}}'
    }
    try:
        html = requests.get(url, headers=headers, params=paramter)
        res = json.loads(html.text)['songinfo']['data']
        data = {}
        data['歌名'] = res['track_info']['name']
        data['歌手'] = res['track_info']['singer'][0]['name']
        res_0 = res['info']
        if 'genre' in res_0:
            data['流派'] = res_0['genre']['content'][0]['value']
        if 'lan' in res_0:
            data['语种'] = res_0['lan']['content'][0]['value']
        with open(fpath, 'a', encoding='utf-8') as f:
            f.writelines(str(data) + '\n')
    except:
        traceback.print_exc()


def download_music(word, singer):
    #如下的代码完成了音乐文件的下载
    #word = '彩虹'
    res1 = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='+word)
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']['song']['list']
    mids = []
    songmids = []
    srcs = []
    songnames = []
    singers = []
    for j in jm1:
        try:
            mids.append(j['media_mid'])
            songmids.append(j['songmid'])
            songnames.append(j['songname'])
            singers.append(j['singer'][0]['name'])
        except:
            print('wrong')

    for n in range(0,len(mids)):
        res2 = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+songmids[n]+'&filename=C400'+mids[n]+'.m4a&guid=6612300644')
        jm2 = json.loads(res2.text)
        vkey = jm2['data']['items'][0]['vkey']
        srcs.append('http://dl.stream.qqmusic.qq.com/C400'+mids[n]+'.m4a?vkey='+vkey+'&guid=6612300644&uin=0&fromtag=66')

    print('For '+word+' Start download...')
    x = len(srcs)
    for m in range(0,x):
        if songnames[m]==word and singers[m]==singer:
            print(str(m)+'***** '+songnames[m]+' - '+singers[m]+'.mp3 *****'+' Downloading...')
            try:
                urllib.request.urlretrieve(srcs[m],'music/'+songnames[m]+' - '+singers[m]+'.mp3')
            except:
                x = x - 1
                print('Download wrong~')
    print('For ['+word+'] Download complete '+str(x)+'files !')

if __name__ == '__main__':
    class_list = []
    play_list = []
    getMusicClassList(class_list)
    # print(len(class_list))
    getPlaylistId(play_list, class_list)
    # print(len(play_list))
    getSongList(play_list)

    # 读取一行歌曲信息，将歌名作为输入，调用download_music函数下载一组歌曲
    f = open('music.txt', 'r',encoding='utf8')
    line = eval(f.readline())
    word = line['歌名']
    singer = line['歌手']
    download_music(word, singer)
    f.close()

