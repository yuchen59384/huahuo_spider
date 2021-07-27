from influxdb import InfluxDBClient
# from bilibili.crawler.settings import ENV, DOMAIN_HOST, INFLUXDB
import socket
# 监控日志
INFLUXDB = 'spider'

# DB base info
DBNAME = 'huahuo'
AUTH_DB = 'red'
DOMAIN_HOST = 'localhost'
PORT = 27017
ENV = "prod" if socket.gethostname().startswith("redigital") else "dev"


client = InfluxDBClient(DOMAIN_HOST, 8086,'jiran','yuchen59384')
# 创建 database
client.create_database(DBNAME)
# switch 到 database
client.switch_database(DBNAME)

def write(measurement, tags={}, fields={}):
    client.write_points([{
        "measurement": measurement,
        "tags": tags,
        "fields": fields
    }])

def record(method, status):
    # if not ENV == "prod":
    #     return
    write(method, {"status": status}, {"num": 1})


def record_num(method, status, num):
    if not ENV == "prod":
        return
    write(method, {"status": status}, {"num": num})

