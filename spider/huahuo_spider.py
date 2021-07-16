import requests
import time
import logging

logger = logging.getLogger(__name__)
kol_list_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/search?region_id' \
               '=&second_region_id=&partition_id=&second_partition_id=&nickname=&upper_mid=&task_type=1&order_bys' \
               '=&is_include_potential_upper=0&min_fans_num=&max_fans_num=&content_tag_id=&style_tag_id=0&provider_id' \
               '=&cooperation_types=&min_task_price=&max_task_price=&male_attention_user_rates' \
               '=&female_attention_user_rates=&attention_user_ages=&attention_user_regionIds=&bus_type=&gender=&page' \
               '=%s&size=10 '
kol_detail_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait?upper_mid=%s&mcn_id=%s'
#type=1个人作品&type=2商业作品
note_url='https://huahuo.bilibili.com/commercialorder/api/web_api/v1/mcn/upper/representative/list?type=%s&upper_mid=%s'
#type=1稿件互动量趋势&type=3稿件播放量趋势
note_trend_url='https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait/draft/trend?upper_mid=%s&trend_type=%s'
#type=1用户总量&type=2用户增量趋势
user_trend_url='https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait/attention_user/trend?upper_mid=%s&query_type=%s'

class HuahuoSpider:
    def __init__(self):
        # self.cookies = redis_conn.get('huahuo_cookies')
        # self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            # 'Cache-Control': 'Cache-Control',
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Cookie':"buvid3=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; CURRENT_FNVAL=80; _uuid=4B863C8E-6B58-97B1-606B-85532448409371226infoc; blackside_state=1; rpdid=|(k)~u~llm~l0J'uYkluJlJ~R; LIVE_BUVID=AUTO9816260765750788; PVID=1; CURRENT_QUALITY=80; fingerprint=dbc7bfd959757b6f95e94521221f5ac5; fingerprint=dbc7bfd959757b6f95e94521221f5ac5; buvid_fp=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; buvid_fp_plain=637C6AB6-17D0-46F6-AEA3-D8ACD4840DD1138400infoc; buvid_fp_plain=637C6AB6-17D0-46F6-AEA3-D8ACD4840DD1138400infoc; SESSDATA=a4b299fa%2C1641982754%2C6fe59%2A71; bili_jct=1813cda8aa0b517d16f67ecac36c8877; DedeUserID=631203615; DedeUserID__ckMd5=e682082c7fc54b31; sid=66pv5orr; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjEsInByb3h5TmFtZSI6IuW8leWTjeaWh-WMluS8oOWqkijljqbpl6gp5pyJ6ZmQ5YWs5Y-4LeWVhuWNleiKseeBq-W5s-WPsCIsImRlcGFydG1lbnRJZCI6MTY5LCJpc3MiOiLlvJXlk43mlofljJbkvKDlqpIo5Y6m6ZeoKeaciemZkOWFrOWPuC3llYbljZXoirHngavlubPlj7AiLCJtaWQiOjYzMTIwMzYxNSwiSU5EVVNUUllfQVVESVQiOjIsInR5cGUiOjQsImRlcGFydG1lbnRUeXBlIjo0LCJJU19ORVdfQ1VTVE9NRVIiOjAsIkVOVEVSUFJJU0VfQVVESVQiOjEsIklTX0NPUkVfQUdFTlQiOjAsImV4cCI6MTYyNzAzNTU1NywibWFnaWNfbnVtYmVyIjoiQ09NTUVSQ0lBTE9SREVSIiwiaWF0IjoxNjI2NDMwNzU3LCJqdGkiOiIxNjUzMzMiLCJwcm94eUlkIjoxOTg1NzMxLCJJU19LQV9BQ0NPVU5UIjowfQ.jpkUz5LxQidMrS_-k3vbQv4I-nk5rj1u7xoVssPJTW4"
            'Cookie':"buvid3=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; CURRENT_FNVAL=80; _uuid=4B863C8E-6B58-97B1-606B-85532448409371226infoc; blackside_state=1; rpdid=|(k)~u~llm~l0J'uYkluJlJ~R; LIVE_BUVID=AUTO9816260765750788; PVID=1; DedeUserID=410282523; DedeUserID__ckMd5=0f009d0a30b0f8dc; CURRENT_QUALITY=80; SESSDATA=90732c41,1641898573,feb44*71; bili_jct=964d2fb37470ccde4d22f2ac64239fe2; sid=je9ldkrk; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjAsImlzcyI6Il_pm6jovrB5dSIsIm1pZCI6NDEwMjgyNTIzLCJJTkRVU1RSWV9BVURJVCI6MCwidHlwZSI6NCwiZGVwYXJ0bWVudFR5cGUiOjAsIklTX05FV19DVVNUT01FUiI6MSwiRU5URVJQUklTRV9BVURJVCI6MCwiZXhwIjoxNjI2OTUxODgxLCJtYWdpY19udW1iZXIiOiJDT01NRVJDSUFMT1JERVIiLCJpYXQiOjE2MjYzNDcwODEsImp0aSI6IiIsIklTX0tBX0FDQ09VTlQiOjB9.9wvpfYk2KYgZ8Kd7V8r9vNTTkfVogwffdjeEanuaFAw; fingerprint=dbc7bfd959757b6f95e94521221f5ac5; fingerprint=dbc7bfd959757b6f95e94521221f5ac5; buvid_fp=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; buvid_fp_plain=637C6AB6-17D0-46F6-AEA3-D8ACD4840DD1138400infoc; buvid_fp_plain=637C6AB6-17D0-46F6-AEA3-D8ACD4840DD1138400infoc"
        }
        self.page = 1
        self.total = 100000
        self.crawled = 0
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename=f'/data/logs/huahuo_spider.log')
        # self.list_mids=[]
        # self.list_mcn_ids = []

    def get_kol_list(self, update=True):
        while self.crawled <25:
                # self.total:
            while True:
                try:
                    resp = requests.get(kol_list_url % self.page, headers=self.headers)
                except Exception as e:
                    print(e)
                    # record('huahuo', 'error')
                    logger.exception(e)
                if resp.status_code == 200:
                    break
            resp_dict = resp.json()
            print(resp_dict)
            # time.sleep(3)
            self.total = resp_dict['result']['total']
            for item in resp_dict['result']['data']:
                self.crawled += 1
                if self.crawled % 50 == 0:
                    logger.info(f'now crawled {self.crawled} users')
                mid=item['upper_mid']
                mcn_id=item['mcn_id']
                name=item['nickname']
                print('-' * 10,name, '-' * 10)
                print('-' * 10, '1', '-' * 10)
                self.get_kol_detail(mid,mcn_id)
                time.sleep(0.5)
                print('-' * 10, '2', '-' * 10)
                time.sleep(0.5)
                self.get_note('1',mid) #_personal
                print('-' * 10, '3', '-' * 10)
                time.sleep(0.5)
                self.get_note('2',mid) #_commercial
                print('-' * 10, '4', '-' * 10)
                time.sleep(0.5)
                self.get_note_trend(mid,'1') #_interact
                print('-' * 10, '5', '-' * 10)
                time.sleep(0.5)
                self.get_note_trend(mid,'3') #_play
                print('-' * 10, '6', '-' * 10)
                time.sleep(0.5)
                self.get_user_trend(mid,'1') #_total
                print('-' * 10, '7', '-' * 10)
                self.get_user_trend(mid,'2') #_increment
                time.sleep(0.5)
            logger.info(f'crawled page: {self.page}')
            self.page += 1

    def get_kol_detail(self, mid,mcn_id):
        while True:
            try:
                resp = requests.get(kol_detail_url % (mid,mcn_id), headers=self.headers)
            except Exception as e:
                print(e)
                # record('huahuo', 'error')
                # logger.exception(e)
            if resp.status_code == 200:
                break
        resp_dict = resp.json()['result']
        fans_like_num = resp_dict['fans_like_num']  # 粉丝获赞
        fans_num = resp_dict['fans_num']  # 粉丝数
        gender_desc = resp_dict['gender_desc']  # 性别
        head_img = resp_dict['head_img']  # 头像
        nickname = resp_dict['nickname']  # 名称
        partition_name = resp_dict['partition_name']  # 分区
        second_partition_name = resp_dict['second_partition_name']
        signature = resp_dict['signature'] # 签名
        tags = resp_dict['tags']
        upper_prices = resp_dict['upper_prices']  # 服务报价

        average_barrage_cnt = resp_dict['average_barrage_cnt']  # 平均弹幕数
        average_collect_cnt = resp_dict['average_collect_cnt'] # 平均收藏数
        average_comment_cnt = resp_dict['average_comment_cnt'] # 平均评论数
        average_interactive_rate = resp_dict['average_interactive_rate']  # 作品互动率
        average_like_cnt = resp_dict['average_like_cnt'] # 平均点赞数
        average_play_cnt = resp_dict['average_play_cnt']  # 平均播放数
        attention_user_distributed_tags = resp_dict['attention_user_distributed_tags']  # 用户分布
        attention_user_feature_tags = resp_dict['attention_user_feature_tags']  # 用户特征
        age_distributions = resp_dict['age_distributions']  # 年龄分布
        sax_distributions = resp_dict['sax_distributions']  # 性别分布
        top_region_distributions = resp_dict['top_region_distributions']  # 地区分布
        device_distributions = resp_dict['device_distributions']  # 设备分布
        print(average_collect_cnt)
        print(average_like_cnt)


    def get_note(self,type,mid):
        while True:
            try:
                resp = requests.get(note_url % (type,mid), headers=self.headers)
            except Exception as e:
                print(e)
                # record('huahuo', 'error')
                # logger.exception(e)
            if resp.status_code == 200:
                break
        if type == '1':
            note_trend_list = resp.json()['result']
            print(note_trend_list)
        if type == '2':
            note_trend_list = resp.json()['result']
            print(note_trend_list)

    def get_note_trend(self,mid,type):
        while True:
            try:
                resp = requests.get(note_trend_url % (mid,type), headers=self.headers)
            except Exception as e:
                print(e)
                # record('huahuo', 'error')
                # logger.exception(e)
            if resp.status_code == 200:
                break
        if type == '1':
            note_personal_trend_list=resp.json()['result']
            print(note_personal_trend_list)
        if type == '3':
            note_play_trend_list=resp.json()['result']
            print(note_play_trend_list)

    def get_user_trend(self,mid,type):
        while True:
            try:
                resp = requests.get(user_trend_url % (mid,type), headers=self.headers)
            except Exception as e:
                print(e)
                # record('huahuo', 'error')
                # logger.exception(e)
            if resp.status_code == 200:
                break
        if type == '1':
            user_total_trend_list = resp.json()['result']
            print(user_total_trend_list)
        if type == '2':
            user_increment_trend_list = resp.json()['result']
            print(user_increment_trend_list)

if __name__ == '__main__':
    s = HuahuoSpider()
    s.get_kol_list()
