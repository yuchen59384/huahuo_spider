import datetime
import time
import requests
# import time
import logging
from crawler.moudle.Kol import kol,FansPortrait,Distribution
# from crawler.moudle.Fans import fans
from crawler.spider import note_spider
from crawler.moudle.Note import note
# from crawler.influxdb_write import *
logger = logging.getLogger(__name__)
kol_list_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/search?region_id' \
               '=&second_region_id=&partition_id=&second_partition_id=&nickname=&upper_mid=&task_type=1&order_bys' \
               '=&is_include_potential_upper=0&min_fans_num=&max_fans_num=&content_tag_id=&style_tag_id=0&provider_id' \
               '=&cooperation_types=&min_task_price=&max_task_price=&male_attention_user_rates' \
               '=&female_attention_user_rates=&attention_user_ages=&attention_user_regionIds=&bus_type=&gender=&page' \
               '=%s&size=10 '
kol_detail_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait?upper_mid=%s&mcn_id=%s'
# type=1个人作品&type=2商业作品
note_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/mcn/upper/representative/list?type=%s&upper_mid=%s'
# type=1稿件互动量趋势&type=3稿件播放量趋势
note_trend_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait/draft/trend?upper_mid=%s&trend_type=%s'
# type=1用户总量&type=2用户增量趋势
user_trend_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait/attention_user/trend?upper_mid=%s&query_type=%s'


class HuahuoSpider:
    def __init__(self):
        # self.cookies = redis_conn.get('huahuo_cookies')
        # self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            # 'Cache-Control': 'Cache-Control',
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'referer': 'https: // huahuo.bilibili.com /',
            # 'Cookie': "buvid3=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; CURRENT_FNVAL=80; _uuid=4B863C8E-6B58-97B1-606B-85532448409371226infoc; blackside_state=1; rpdid=|(k)~u~llm~l0J'uYkluJlJ~R; LIVE_BUVID=AUTO9816260765750788; PVID=1; CURRENT_QUALITY=80; fingerprint=dbc7bfd959757b6f95e94521221f5ac5; fingerprint=dbc7bfd959757b6f95e94521221f5ac5; buvid_fp=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; buvid_fp_plain=F8A71246-1135-465C-A640-69D00A03F3B1167612infoc; buvid_fp_plain=F8A71246-1135-465C-A640-69D00A03F3B1167612infoc; SESSDATA=f348ee61%2C1642395630%2Cc7365%2A71; bili_jct=c3f069308865b414a82430a68ce6183c; DedeUserID=631203615; DedeUserID__ckMd5=e682082c7fc54b31; sid=cb4we9j7; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjEsInByb3h5TmFtZSI6IuW8leWTjeaWh-WMluS8oOWqkijljqbpl6gp5pyJ6ZmQ5YWs5Y-4LeWVhuWNleiKseeBq-W5s-WPsCIsImRlcGFydG1lbnRJZCI6MTY5LCJpc3MiOiLlvJXlk43mlofljJbkvKDlqpIo5Y6m6ZeoKeaciemZkOWFrOWPuC3llYbljZXoirHngavlubPlj7AiLCJtaWQiOjYzMTIwMzYxNSwiSU5EVVNUUllfQVVESVQiOjIsInR5cGUiOjQsImRlcGFydG1lbnRUeXBlIjo0LCJJU19ORVdfQ1VTVE9NRVIiOjAsIkVOVEVSUFJJU0VfQVVESVQiOjEsIklTX0NPUkVfQUdFTlQiOjAsImV4cCI6MTYyNzQ0ODQzMiwibWFnaWNfbnVtYmVyIjoiQ09NTUVSQ0lBTE9SREVSIiwiaWF0IjoxNjI2ODQzNjMyLCJqdGkiOiIxNjUzMzMiLCJwcm94eUlkIjoxOTg1NzMxLCJJU19LQV9BQ0NPVU5UIjowfQ.pdORnKj4RKzJOUu_DIocxzcfuqZf_MkXsNl20WZ79pk"
            'Cookie': "buvid3=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; CURRENT_FNVAL=80; _uuid=4B863C8E-6B58-97B1-606B-85532448409371226infoc; blackside_state=1; rpdid=|(k)~u~llm~l0J'uYkluJlJ~R; LIVE_BUVID=AUTO9816260765750788; CURRENT_QUALITY=80; buvid_fp=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; bp_video_offset_631203615=553184997388351064; bp_t_offset_631203615=553838227550270004; PVID=1; fingerprint=9397fa4173d40ce11bf6ac8a59474bcb; buvid_fp_plain=B23D8929-AC25-444D-B3D1-ADB06014A0A453951infoc; SESSDATA=0ed458ac%2C1643609375%2C0011c%2A81; bili_jct=aef991e5e685ed1eadfc7ae4b615d75e; DedeUserID=631203615; DedeUserID__ckMd5=e682082c7fc54b31; sid=lcvxxk9h; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjEsInByb3h5TmFtZSI6IuW8leWTjeaWh-WMluS8oOWqkijljqbpl6gp5pyJ6ZmQ5YWs5Y-4LeWVhuWNleiKseeBq-W5s-WPsCIsImRlcGFydG1lbnRJZCI6MTY5LCJpc3MiOiLlvJXlk43mlofljJbkvKDlqpIo5Y6m6ZeoKeaciemZkOWFrOWPuC3llYbljZXoirHngavlubPlj7AiLCJtaWQiOjYzMTIwMzYxNSwiSU5EVVNUUllfQVVESVQiOjIsInR5cGUiOjQsImRlcGFydG1lbnRUeXBlIjo0LCJJU19ORVdfQ1VTVE9NRVIiOjAsIkVOVEVSUFJJU0VfQVVESVQiOjEsIklTX0NPUkVfQUdFTlQiOjAsImV4cCI6MTYyODY2MjE3NywibWFnaWNfbnVtYmVyIjoiQ09NTUVSQ0lBTE9SREVSIiwiaWF0IjoxNjI4MDU3Mzc3LCJqdGkiOiIxNjUzMzMiLCJwcm94eUlkIjoxOTg1NzMxLCJJU19LQV9BQ0NPVU5UIjowfQ.LF4lqerWnU7VUUgJrfyKtg34ToiLJSqwYldYVR6tfpg"
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
        self.page = 1
        self.total = 50
        self.crawled = 0
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='../logs/huahuo_spider.log')

    def get_kol_list(self, update=True):
        while self.crawled < 50:
            while True:
                try:
                    resp1 = requests.get(kol_list_url % self.page, headers=self.headers)
                except Exception as e:
                    # record('huahuo', 'error')
                    logger.exception(e)
                    continue
                if resp1.status_code == 200:
                    break
            resp_dict = resp1.json()
            self.total = resp_dict['result']['total']
            print('up主总数量为',self.total)
            logger.info(f'need crowl kol num: {self.total}')
            for item in resp_dict['result']['data']:
                self.mid = item['upper_mid']
                self.k = kol(user_id=str(self.mid))
                # if not self.k:
                #     self.k= kol(user_id=str(self.mid))
#                 #     record(f'huahuo', 'new_kol')
                #     logger.info(f"start crawl new kol: {str(self.mid)}, nickname: {item['nickname']}")
                # else:
                logger.info(f"start crawl kol: {str(self.mid)}, nickname: {item['nickname']}")
                mcn_id = item['mcn_id']
                name = item['nickname']
                self.crawled += 1
                print('正在爬取第%d页第%d个up主——%s' % (self.page, self.crawled, name))
                if self.crawled % 50 == 0:
                    logger.info(f'now crawled {self.crawled} users')
                self.get_kol_detail(self.mid, mcn_id)
                print('1')
                logger.info(f'update detail for note: {str(self.mid)}')
                self.get_note('1', self.mid)# _personal
                print('2')
                aids=self.get_note('2', self.mid)
                s2 = note_spider.NoteSpider(aids=aids,is_business=True)
                s2.get_video_list() #_commercial
                print('3')

                # self.get_note('2', self.mid)
                self.get_note_trend(self.mid, '1')  # _interact
                self.get_note_trend(self.mid, '3')  # _play
                print('4')
                self.get_user_trend(self.mid, '1')  # _total
                self.get_user_trend(self.mid, '2')  # _increment
                print('5')
                logger.info(f'update trend for note: {str(self.mid)}')
                s2 = note_spider.NoteSpider(str(self.mid))
                s2.get_video_list()
                print('6')

                # record(f'huahuo', 'note_update')
                #计算剩余时间
                end = time.time()
                run_time = int(end - start)
                need_time=run_time/self.crawled*(self.total-self.crawled)
                print('剩余爬取时间:',str(datetime.timedelta(seconds=need_time)))
                logger.info(f"Remaining time: {str(datetime.timedelta(seconds=need_time))}")
            self.page += 1
            logger.info(f'crawled page: {self.page}')

    def get_kol_detail(self, mid, mcn_id):
        while True:
            try:
                resp = requests.get(kol_detail_url % (mid, mcn_id), headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                logger.exception(e)
                continue
            if resp.status_code == 200:
                break
        # 保存kol数据
        resp_dict = resp.json()['result']

        self.k.fans_like_num = resp_dict['fans_like_num']  # 粉丝获赞
        self.k.fans_num = resp_dict['fans_num']  # 粉丝数
        self.k.gender_desc = resp_dict['gender_desc']  # 性别
        self.k.head_img = resp_dict['head_img']  # 头像
        self.k.nickname = resp_dict['nickname']  # 名称
        self.k.partition_name = resp_dict['partition_name']  # 分区
        self.k.second_partition_name = resp_dict['second_partition_name']
        self.k.signature = resp_dict['signature']  # 签名
        if resp_dict['mcn_company_name'] and resp_dict['mcn_company_name'] != "花火计划个人UP主商业合作":
            self.k.mcn_company_name=resp_dict['mcn_company_name']
        self.k.tags = resp_dict['tags']
        self.k.upper_prices = resp_dict['upper_prices']  # 服务报价
        self.k.average_barrage_cnt = resp_dict['average_barrage_cnt']  # 平均弹幕数
        self.k.average_collect_cnt = resp_dict['average_collect_cnt']  # 平均收藏数
        self.k.average_comment_cnt = resp_dict['average_comment_cnt']  # 平均评论数
        self.k.average_interactive_rate = resp_dict['average_interactive_rate']  # 作品互动率
        self.k.average_like_cnt = resp_dict['average_like_cnt']  # 平均点赞数
        self.k.average_play_cnt = resp_dict['average_play_cnt']  # 平均播放数
        # 保存粉丝数据
        f=FansPortrait()
        f.attention_user_distributed_tags = resp_dict['attention_user_distributed_tags']  # 用户分布
        f.attention_user_feature_tags = resp_dict['attention_user_feature_tags']  # 用户特征
        age_distributions = resp_dict['age_distributions']  # 年龄分布
        sax_distributions = resp_dict['sax_distributions']  # 性别分布
        top_region_distributions = resp_dict['top_region_distributions']  # 地区分布
        device_distributions = resp_dict['device_distributions']  # 设备分布
        for age in age_distributions:
            age_distribution = Distribution()
            age_distribution.name=age['section_desc']
            age_distribution.value=age['count']
            f.age_distributions.append(age_distribution)
        for sax in sax_distributions:
            sax_distribution = Distribution()
            sax_distribution.name = sax['section_desc']
            sax_distribution.value = sax['count']
            f.sax_distributions.append(sax_distribution)
        for top_region in top_region_distributions:
            top_region_distribution = Distribution()
            top_region_distribution.name = top_region['section_desc']
            top_region_distribution.value = top_region['count']
            f.top_region_distributions.append(top_region_distribution)
        for device in device_distributions:
            device_distribution = Distribution()
            device_distribution.name = device['section_desc']
            device_distribution.value = device['count']
            f.device_distributions.append(device_distribution)
        self.k.fansPortrait=f
        for item in resp_dict['upper_prices']:
            if item["cooperation_type_desc"] == '植入视频':  #
                if item['platform_price']:
                    self.k.implant_platform_price = item['platform_price']
                if item['discount_price']:
                    self.k.implant_discount_price = item['discount_price']
            elif item["cooperation_type_desc"] == '定制视频':
                if item['platform_price']:
                    self.k.custom_platform_price = item['platform_price']
                if item['discount_price']:
                    self.k.custom_discount_price = item['discount_price']
            elif item["cooperation_type_desc"] == '直发动态':
                if item['platform_price']:
                    self.k.direct_message_platform_price = item['platform_price']
                if item['discount_price']:
                    self.k.direct_message_discount_price = item['discount_price']
            elif item["cooperation_type_desc"] == '转发动态':
                if item['platform_price']:
                    self.k.forward_message_discount_price = item['platform_price']
                if item['discount_price']:
                    self.k.forward_message_platform_price = item['discount_price']
        self.k.save()

        # record(f'huahuo', 'kol update')

    def get_note(self, type, mid):
        while True:
            try:
                resp2 = requests.get(note_url % (type, mid), headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                logger.exception(e)
                continue
            if resp2.status_code == 200:
                break
        if type == '1':
            self.k.personal_note = resp2.json()['result']
            # print(note_trend_list)
            self.k.save()
        if type == '2':
            self.k.commercial_note = resp2.json()['result']
            # print(note_trend_list)
            self.k.save()
            aids=[]
            # for item in resp2.json()['result']:
            #     aid =item['av_id']
            #     n= note.objects(note_id=aid).first()
            #     if not n:
            #         aids.append(str(aid))
            #     else:
            #         n.updatae(
            #             is_business=True
            #         )
            # return aids


    def get_note_trend(self, mid, type):
        while True:
            try:
                resp0 = requests.get(note_trend_url % (mid, type), headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                logger.exception(e)
                continue
            if resp0.status_code == 200:
                break

        if type == '1':
            self.k.note_interact_trend = resp0.json()['result']
            # print(note_personal_trend_list)
        if type == '3':
            self.k.note_play_trend = resp0.json()['result']
            # print(note_play_trend_list)

        self.k.save()

    def get_user_trend(self, mid, type):
        while True:
            try:
                resp1 = requests.get(user_trend_url % (mid, type), headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                logger.exception(e)
                continue
            if resp1.status_code == 200:
                break

        if type == '1':
            self.k.user_total_trend = resp1.json()['result']
        if type == '2':
            self.k.user_Increment_trend = resp1.json()['result']
        self.k.save()


if __name__ == '__main__':
    start = time.time()
    s = HuahuoSpider()
    s.get_kol_list()
