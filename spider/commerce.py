import json
import re
import time

import requests

from crawler.moudle.Note import note

class Bili_commentspider():
    def __init__(self):
        # self.bv_list = bv_list
        self.page=6
        self.maxpage=50
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'cookie': "buvid3=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; CURRENT_FNVAL=80; _uuid=4B863C8E-6B58-97B1-606B-85532448409371226infoc; blackside_state=1; rpdid=|(k)~u~llm~l0J'uYkluJlJ~R; LIVE_BUVID=AUTO9816260765750788; CURRENT_QUALITY=80; buvid_fp=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; bp_video_offset_631203615=553184997388351064; bp_t_offset_631203615=553838227550270004; PVID=1; fingerprint=9397fa4173d40ce11bf6ac8a59474bcb; buvid_fp_plain=B23D8929-AC25-444D-B3D1-ADB06014A0A453951infoc; SESSDATA=0ed458ac%2C1643609375%2C0011c%2A81; bili_jct=aef991e5e685ed1eadfc7ae4b615d75e; DedeUserID=631203615; DedeUserID__ckMd5=e682082c7fc54b31; sid=lcvxxk9h; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjEsInByb3h5TmFtZSI6IuW8leWTjeaWh-WMluS8oOWqkijljqbpl6gp5pyJ6ZmQ5YWs5Y-4LeWVhuWNleiKseeBq-W5s-WPsCIsImRlcGFydG1lbnRJZCI6MTY5LCJpc3MiOiLlvJXlk43mlofljJbkvKDlqpIo5Y6m6ZeoKeaciemZkOWFrOWPuC3llYbljZXoirHngavlubPlj7AiLCJtaWQiOjYzMTIwMzYxNSwiSU5EVVNUUllfQVVESVQiOjIsInR5cGUiOjQsImRlcGFydG1lbnRUeXBlIjo0LCJJU19ORVdfQ1VTVE9NRVIiOjAsIkVOVEVSUFJJU0VfQVVESVQiOjEsIklTX0NPUkVfQUdFTlQiOjAsImV4cCI6MTYyODY2MjE3NywibWFnaWNfbnVtYmVyIjoiQ09NTUVSQ0lBTE9SREVSIiwiaWF0IjoxNjI4MDU3Mzc3LCJqdGkiOiIxNjUzMzMiLCJwcm94eUlkIjoxOTg1NzMxLCJJU19LQV9BQ0NPVU5UIjowfQ.LF4lqerWnU7VUUgJrfyKtg34ToiLJSqwYldYVR6tfpg"

        }
        self.headers_ = {
            'referer': 'http://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            # 'cookie': "buvid3=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; CURRENT_FNVAL=80; _uuid=4B863C8E-6B58-97B1-606B-85532448409371226infoc; blackside_state=1; rpdid=|(k)~u~llm~l0J'uYkluJlJ~R; LIVE_BUVID=AUTO9816260765750788; CURRENT_QUALITY=80; buvid_fp=B819C4DB-FD06-F51B-80EA-71556561769370634infoc; bp_video_offset_631203615=553184997388351064; bp_t_offset_631203615=553838227550270004; PVID=1; fingerprint=9397fa4173d40ce11bf6ac8a59474bcb; buvid_fp_plain=B23D8929-AC25-444D-B3D1-ADB06014A0A453951infoc; SESSDATA=0ed458ac%2C1643609375%2C0011c%2A81; bili_jct=aef991e5e685ed1eadfc7ae4b615d75e; DedeUserID=631203615; DedeUserID__ckMd5=e682082c7fc54b31; sid=lcvxxk9h; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjEsInByb3h5TmFtZSI6IuW8leWTjeaWh-WMluS8oOWqkijljqbpl6gp5pyJ6ZmQ5YWs5Y-4LeWVhuWNleiKseeBq-W5s-WPsCIsImRlcGFydG1lbnRJZCI6MTY5LCJpc3MiOiLlvJXlk43mlofljJbkvKDlqpIo5Y6m6ZeoKeaciemZkOWFrOWPuC3llYbljZXoirHngavlubPlj7AiLCJtaWQiOjYzMTIwMzYxNSwiSU5EVVNUUllfQVVESVQiOjIsInR5cGUiOjQsImRlcGFydG1lbnRUeXBlIjo0LCJJU19ORVdfQ1VTVE9NRVIiOjAsIkVOVEVSUFJJU0VfQVVESVQiOjEsIklTX0NPUkVfQUdFTlQiOjAsImV4cCI6MTYyODY2MjE3NywibWFnaWNfbnVtYmVyIjoiQ09NTUVSQ0lBTE9SREVSIiwiaWF0IjoxNjI4MDU3Mzc3LCJqdGkiOiIxNjUzMzMiLCJwcm94eUlkIjoxOTg1NzMxLCJJU19LQV9BQ0NPVU5UIjowfQ.LF4lqerWnU7VUUgJrfyKtg34ToiLJSqwYldYVR6tfpg"

        }
        self.kol_list_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/search?region_id=&second_region_id=&partition_id=&second_partition_id=&nickname=&upper_mid=&task_type=1&order_bys=&is_include_potential_upper=0&min_fans_num=&max_fans_num=&content_tag_id=&style_tag_id=0&provider_id=&cooperation_types=&min_task_price=&max_task_price=&male_attention_user_rates=&female_attention_user_rates=&attention_user_ages=&attention_user_regionIds=&bus_type=&gender=&page=%s&size=10 '
        self.kol_detail_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait?upper_mid=%s&mcn_id=%s'
        # type=1个人作品&type=2商业作品
        self.note_url = 'https://huahuo.bilibili.com/commercialorder/api/web_api/v1/mcn/upper/representative/list?type=2&upper_mid=%s'

    def get_oid(self,bv):
        base_url='https://www.bilibili.com/video/%s'
        r = requests.get(base_url%bv, headers=self.headers)
        res = r.text
        patten = '</script><script>window.__INITIAL_STATE__={"aid":(\d*)'
        try:
            return re.findall(patten, res)[0]
        except Exception as e:
            return



    def get_note(self,mid):
        while True:
            try:
                resp = requests.get(self.note_url % (mid), headers=self.headers)
            except Exception as e:
                # record('huahuo', 'error')
                # logger.exception(e)
                print(e)
                continue
            if resp.status_code == 200:
                break
        print('请求商业笔记成功')
        for item in resp.json()['result']:
            av_id = item['av_id']
            bv_id = item['bv_id']
            n=note(note_id=str(av_id),user_id=mid)
            comment_cnt = item['comment_cnt']
            title = item['title']
            n.title=title
            oid= self.get_oid(bv_id)
            if oid:
                content = self.comment_parse(oid)
                if content:
                    n.upper_comment=content.replace('\n','')
                n.save()
                print('updete：',bv_id)
            else:
                print('oid获取失败')


    def comment_parse(self,oid):
        while True:
            comment_url = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=%s&type=1&oid=%s&mode=3&plat=2&_=1627223958211'

            resp = requests.get(url=comment_url % ('1', oid), headers=self.headers_)
            resp_dict = json.loads(resp.text)
            # comments = resp_dict['data']['replies']
            # for comment in comments:
            #     content = comment.get('content').get('message').replace('\n', '')
            #     cmt = ''.join(re.findall(r'[\u4e00-\u9fa5]', content))
            try:
                return resp_dict['data']['top']['upper']['content']['message']
            except Exception as e:
                return

    def get_kol_list(self):
        while self.page <= self.maxpage:
            print('start',self.page)
            # time.sleep(0.5)
            resp_dict = requests.get(url=self.kol_list_url % str(self.page), headers=self.headers).json()
            crawled=1
            for item in resp_dict['result']['data']:
                mid = item['upper_mid']
                mcn_id = item['mcn_id']
                name = item['nickname']
                print('第%d页，第%d个kol'%(self.page,crawled),end='   ')
                self.get_note(str(mid))
                crawled = crawled+1
            self.page = self.page + 1

if __name__ == '__main__':
    # list=[
    #     'BV1No4y1S7TT','BV1J54y1J7kD','BV1JU4y1n7AJ','BV1Yo4y1Q71P','BV1Jy4y1j79i','BV1tb4y1r7Wv','BV1bv411n7yN','BV1764y167Lp'
    #     ,'BV1qg411M7ND', 'BV1CU4y137FJ', 'BV1VB4y1K7eL', 'BV15L411p7M8' ,'BV1L64y1t7ks', 'BV1Wv411n7FK' ,
    #     'BV1iM4y1K7DH','BV1Xb4y1k714', 'BV1KL411p7PA'
    # ]
    # list=['BV1U5411T7tV']
    s=Bili_commentspider()
    s.get_kol_list()
