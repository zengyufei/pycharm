import requests


def get_out_ip():
    url = r'http://www.trackip.net/'
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find('title') + 6:txt.find('/title') - 1]
    return (ip)


if __name__ == "__main__":
    ip = get_out_ip()
    print(ip)
