import os

import jieba
import requests
# import time
import logging
from crawler.moudle.Note import note
from crawler.moudle.Kol import kol
import datetime
from multiprocessing.dummy import Pool

logger = logging.getLogger(__name__)
class NoteSpider:
    def __init__(self, mid='',aids=[],is_business=False):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='../logs/huahuo_spider.log')
        self.user_space_url = 'https://api.bilibili.com/x/space/top/arc?vmid=%s&jsonp=jsonp'  # aid cid
        self.video_list_url = 'http://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&pn=1&order=pubdate'  # tlist vlist #user主页
        self.note_tag_url = 'http://api.bilibili.com/x/tag/archive/tags?aid=%s'
        self.note_detail_url = 'http://api.bilibili.com/x/web-interface/view?aid=%s'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            # 'Cache-Control': 'Cache-Control',
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
        }
        proxy03 = {
            'proxyServer': 'http://http-cla.abuyun.com:9030',
            'proxyAuth': "HR7SF2R6ZW8Q272C:18FED964F0594218",
        }

        # request proxy
        self.REQUEST_PROXY = {
            "http": "http://" + proxy03['proxyAuth'] + '@' + proxy03['proxyServer'][7:],
            "https": "http://" + proxy03['proxyAuth'] + '@' + proxy03['proxyServer'][7:]
        }
        self.mid = mid
        self.aids=aids
        self.brands_dict=self.load_brands_dict()
        self.is_business=is_business


    # up主主页获取视频list
    def get_video_list(self):
        if self.mid:
            while True:
                try:
                    resp = requests.get(self.video_list_url % self.mid, headers=self.headers)
                except Exception as e:
                    # record('huahuo', 'error')
                    logger.exception(e)
                    continue
                if resp.status_code == 200:
                    break
            resp_dict = resp.json()
            note_urls=[]
            num=10 #爬起每个up主笔记数量
            for i in range(1, num+1):
                aid = resp_dict['data']['list']['vlist'][i]['aid']
                # tag_urls.append(self.note_tag_url % str(aid))
                n = note.objects(note_id=str(aid)).first()
                if not n:
                #     continue
                # else:
                    logger.info(f"add new note: {str(aid)}")
                note_urls.append(self.note_detail_url % str(aid))
        elif self.aids:

            note_urls = []
            for aid in self.aids:
                note_urls.append(self.note_detail_url % aid)
        else:
            return

        N=len(note_urls) #进程数量
        pool = Pool(N)
        pool.map(self.get_note_detail,note_urls)
        # pool.map(self.get_note_tag, self.dic)
        pool.close()
        pool.join()

        # 更新用户视频数据
        # self.stat_dict = {}
        # for cate_id, item in resp_dict['data']['list']['tlist'].items():
        #     self.stat_dict[item['name']] = item['count']
        # logger.info(f'update video_category for user: {self.mid}')

        # note.video_category=stat_dict
        # for video in resp_dict['data']['list']['vlist']:
        #     #只获取新笔记
        #     note = Note.objects(note_id=str(video['aid'])).first()
        #     if note and not self.force_all:
        #         continue
        #     self.logger.info(f"crawing note: {video['aid']}")
        #     aid=video['aid']
        #     self.get_note_tag(aid)
        #     # time.sleep(0.1)
        #     self.get_note_detail(aid)

    # 为视频添加标签
    def get_note_tag(self, aid):
        while True:
            try:
                resp = requests.get(url=self.note_tag_url%aid, headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                logger.exception(e)
            if resp.status_code == 200:
                break
        resp_dict = resp.json()
        tag_list = []
        for item in resp_dict['data']:
            tag_list.append(item['tag_name'])
        logger.info(f'update tag for note: {str(aid)}')
        # note.update(
        #     tags=tag_list
        # )
        return tag_list

    # 解析视频详情页
    def get_note_detail(self, urls):
        while True:
            try:
                resp = requests.get(urls, headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                logger.exception(e)
            if resp.status_code == 200:
                break
        resp_dict = resp.json()
        resp_dict['data']['type'] = 'video'
        note_dict = resp_dict['data']
        # if not note:
        #     note = Note(note_id=str(note_dict['aid']))
        #     if note_dict['tname'] not in filter_category:
        #         note.mentioned_brands = parse_brands([note_dict['title'], note_dict['desc']])
        #         if note.mentioned_brands:
        #             record('user_note', 'add_brands')
        #     if logger:
        #         logger.info(f'create note: {note.note_id}')
        #     else:
        #         print(f'create note: {note.note_id}')
        # else:
        #     if logger:
        #         logger.info(f'update note: {note.note_id}')
        #     else:
        #         print(f'update note: {note.note_id}')
        aid=str(note_dict['aid'])
        n = note(note_id=aid)
        if self.is_business:
            n.is_business=True
        n.cid = str(note_dict['cid'])
        n.bvid = str(note_dict['bvid'])
        n.user_id = str(note_dict['owner']['mid'])
        n.title = note_dict['title']
        n.head_photo = note_dict['pic']
        # if 'type' in note_dict:
        n.type = note_dict['type']
        n.category = note_dict['tname']
        n.desc = note_dict['desc']
        # if 'tag' in note_dict:
        #     note.tags = note_dict['tag'].split(',')
        n.publish_time = datetime.datetime.utcfromtimestamp(note_dict['pubdate'])
        n.video_comment = note_dict['stat']['danmaku']
        n.comment = note_dict['stat']['reply']
        n.view = note_dict['stat']['view']
        n.share = note_dict['stat']['share']
        n.collect = note_dict['stat']['favorite']
        n.like = note_dict['stat']['like']
        n.coin = note_dict['stat']['coin']
        # n.dislike = note_dict['stat']['dislike']
        n.his_rank = note_dict['stat']['his_rank']
        tags = self.get_note_tag(aid)
        # n.mentioned_brands = self.get_note_brand(note_dict['title'],tags,aid) #提到品牌
        n.tags = tags
        k = kol.objects(user_id=n.user_id).first()
        if k:
            n.fans_view = round(float(k.fans_num) / float(n.view), 3)
        n.save()
        logger.info(f'update detail for note: {str(aid)}')

    def load_brands_dict(self): #读取文件，获取brand字典
        crawler_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        brands_dict_file = os.path.join(os.path.join(crawler_path, 'res'), 'brands_with_alias.txt')
        brands_official_map = {}
        with open(brands_dict_file, 'r',encoding='UTF-8') as f:
            for line in f.readlines():
                brands_with_syn = line.strip().split('\t')
                brand_main = brands_with_syn[0]
                for b in brands_with_syn:
                    brands_official_map[b.lower()] = brand_main
        return brands_official_map

    def get_note_brand(self,title,tags,aid): #获取匹配品牌
        for b in self.brands_dict:
            jieba.add_word(b)
        brands = []
        for word in jieba.cut(title):
            if word.lower() in self.brands_dict:
                brands.append(self.brands_dict[word.lower()])
        for tag in tags:
            if tag.lower() in self.brands_dict:
                brands.append(self.brands_dict[tag.lower()])
        if brands:
            logger.info(f'update brands for note: {str(aid)}')
        return brands
# if __name__ == '__main__':
#     s = NoteSpider('145149047')
#     s.get_video_list()
