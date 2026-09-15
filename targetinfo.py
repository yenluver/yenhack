#!/usr/bin/env python3
import os
import sys
import argparse
import urllib.request
import urllib.parse

def color(text, color_code):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return text
    return f'\x1b[{color_code}m{text}\x1b[0m'

def red(text): return color(text, 31)
def blue(text): return color(text, 34)

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'YenHack-Client'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching data: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Target Info Fetcher")
    parser.add_argument("-t", "--target", help="Target IP address", default=None)
    args, _ = parser.parse_known_args()

    my_ip = fetch_url('https://api.ipify.org').strip()
    
    print(blue('Get Reverse DNS, GeoIP, NMAP, Traceroute and HTTP Headers for an IP address'))
    print(red(f'Your public IP address is {my_ip}\n'))

    target_ip = args.target if args.target else my_ip
    print(red(f'Targeting IP: {target_ip}\n'))

    encoded_ip = urllib.parse.quote(target_ip.strip())
    print(red('Reverse DNS Information:'))
    print(blue(fetch_url(f'https://api.hackertarget.com/reverseiplookup/?q={encoded_ip}')) + '\n')
    
    print(red('GEOIP Information:'))
    print(blue(fetch_url(f'https://api.hackertarget.com/geoip/?q={encoded_ip}')) + '\n')
    
    print(red('NMAP of Target (Ports 21, 25, 80, 443):'))
    print(blue(fetch_url(f'https://api.hackertarget.com/nmap/?q={encoded_ip}')) + '\n')
    
    print(red('HTTP Headers:'))
    print(blue(fetch_url(f'https://api.hackertarget.com/httpheaders/?q={encoded_ip}')) + '\n')
    
    print(red('Trace Route:'))
    print(blue(fetch_url(f'https://api.hackertarget.com/mtr/?q={encoded_ip}')) + '\n')
