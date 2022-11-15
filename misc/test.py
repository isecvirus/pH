from urllib.request import urlopen
from json import load


def ipInfo(ip):
    url = 'https://ipinfo.io/' + ip + '/json'

    res = urlopen(url)
    data = load(res)

    for attr in data.keys():
        print(attr,' '*13+'\t->\t',data[attr])