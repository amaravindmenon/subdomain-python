#!/usr/bin/python3

''' imports '''
import requests
import urllib3
import time
import sys
import argparse


''' take in target values '''
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--domain', type=str, required = True, help='Target Domain')
    parser.add_argument('-o' ,'--output', type=str, required = False, help='output to file')
    return parser.parse_args()


''' banner of the program '''
def banner():
    print('--------------------')
    print('By Techsoftmedia')
    print('---------------------')
    print('')
    print('Get all the subdomains')
    time.sleep(1)


''' parse host from scheme, to use for certificate transperancy abuse '''    
def parse_url(url):
    try:
        host = urllib3.util.url.parse_url(url).host
    except Exception as e:
        print('[+] Invalid domain, try again')
        sys.exit(1)
    return host

'''  write to file '''
def file(subdomain,outputfile):
    with open(output_file,'a') as fp:
        fp.write(subdomain + '\n')
        fp.close()


def main():
    banner()
    subdomains = []

    args = parse_args()
    target = parse_url(args.domain)
    output = args.output

    req = requests.get(f'https://crt.sh/?q=%.{target}&output=json')

    if req.status_code !=200:
        print("[+] Information not available")
        sys.exit(1)

    for (key,value) in enumerate(req.json()):
        subdomains.append(value['name_value'])
        
    print(f"\n[+] ---Target: {target} ---- [+]\n")

    subs = sorted(set(subdomains))

    for s in subs:
        print(f"[+] {s}\n")
        if output is not None:
            file(s,output)

    print("\n\n [+] All the subdomains has been found")



if __name__=='__main__':
    main()

    
