#!/usr/bin/env python3
# Name:     targetinfo.py
# Purpose:  Check an IP against hackertarget API
# By:       Jerry Gamblin (Updated for Python 3)
# -----------------------------------------------

import os
import sys
import json
import hashlib
import argparse
import re
import socket
import urllib.request
import urllib.parse

def color(text, color_code):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return text
    return f'\x1b[{color_code}m{text}\x1b[0m'

def red(text):
    return color(text, 31)

def blue(text):
    return color(text, 34)

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'YenHack-Client'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching data: {e}"

if __name__ == "__main__":
    my_ip = fetch_url('https://api.ipify.org').strip()

    print(blue('Get Reverse DNS, GeoIP, NMAP, Traceroute and pulls HTTP Headers for an IP address'))
    print(blue('A quick and dirty script by @jgamblin'))
    print('\n')
    print(red(f'Your public IP address is {my_ip}'))
    print('\n')

    # Get IP To SCAN
    resp = input(blue(f'Would you like target info about {my_ip}? (Y/N): '))

    if resp.lower() in ["yes", "y"]:
        badip = my_ip
    else:
        badip = input(blue("What IP would you like to check?: "))

    print('\n')

    # IP INFO
    encoded_ip = urllib.parse.quote(badip.strip())
    reversed_dns = fetch_url(f'https://api.hackertarget.com/reverseiplookup/?q={encoded_ip}')
    geoip = fetch_url(f'https://api.hackertarget.com/geoip/?q={encoded_ip}')
    nmap = fetch_url(f'https://api.hackertarget.com/nmap/?q={encoded_ip}')
    httpheaders = fetch_url(f'https://api.hackertarget.com/httpheaders/?q={encoded_ip}')
    tracert = fetch_url(f'https://api.hackertarget.com/mtr/?q={encoded_ip}')

    print(red('Reverse DNS Information:'))
    print(blue(reversed_dns))
    print('\n')
    print(red('GEOIP Information:'))
    print(blue(geoip))
    print('\n')
    print(red('NMAP of Target (Only Ports: 21,25,80 and 443):'))
    print(blue(nmap))
    print('\n')
    print(red('HTTP Headers:'))
    print(blue(httpheaders))
    print('\n')
    print(red('Trace Route:'))
    print(blue(tracert))
    print('\n')
