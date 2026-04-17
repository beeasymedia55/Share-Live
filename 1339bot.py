#!/usr/bin/env python3
"""
TikTok ALL-IN-ONE Bot v2.1 - FIXED SYNTAX
CLI: python tiktok_bot.py kaito -t 300 -v 2000 -m live
"""

from urllib.parse import urlencode
import os, sys, ssl, time, random, threading, requests, hashlib, argparse, re
import urllib.parse
import colorama
from colorama import Fore, Style, Back
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

colorama.init(autoreset=True)

# ALL BUILT-IN DATA
DOMAINS = ["api-h2.tiktokv.com", "api22-core-c-useast1a.tiktokv.com", "api19-core-c-useast1a.tiktokv.com"]
LOCALES = ["en_US", "es_ES", "fr_FR", "de_DE", "it_IT", "pt_BR"]
REGIONS = ["US", "ES", "FR", "DE", "IT", "BR"]
TIMEZONES = ["America/New_York", "Europe/Madrid", "Europe/Paris"]
OFFSETS = ["-28800", "-21600", "0", "3600"]

VIDEO_IDS = ["7123456789012345678", "7234567890123456789", "7345678901234567890"]
ROOM_IDS = ["694567890123456789", "695678901234567890"]
SESSIONS = ["abc123def456ghi789jkl", "xyz789uvw123rst456mno"]
DEVICES = [
    "123456789012345678:123456789012345678:123456789012345678:123456789012345678",
    "987654321098765432:987654321098765432:987654321098765432:987654321098765432"
]

VERSIONS = ["270204", "260104"]
RESOLUTIONS = ["900*1600", "720*1280"]
DPIS = ["240", "300"]

# GLOBAL STATS
reqs = success = fails = rps = active_threads = enters = heartbeats = 0
_lock = threading.Lock()
running = True

class Gorgon:
    def __init__(self, params=None, unix=None):
        self.unix = unix or int(time.time())
        self.params = params or ""
    
    def get_value(self):
        seed = f"seed={self.unix}&{self.params}&_={random.randint(100000,999999)}"
        return hashlib.md5(seed.encode()).hexdigest()

class TikTokRoomDetector:
    @staticmethod
    def detect_room(username):
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'})
        
        try:
            url = f"https://www.tiktok.com/@{username}"
            resp = session.get(url, timeout=10, verify=False)
            room_match = (re.search(r'"roomId"\s*:\s*"(\d+)"', resp.text) or 
                         re.search(r'"roomId":\s*(\d+)', resp.text))
            if room_match:
                return int(room_match.group(1))
        except:
            pass
        
        return None

def get_headers(device_id, install_id, cdid, openudid):
    return {
        'User-Agent': f'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 TikTok/{random.choice(VERSIONS)} Mobile Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': f"{random.choice(LOCALES)}-{random.choice(REGIONS)}",
        'X-Bytedance-Device-ID': device_id,
        'X-Bytedance-Install-ID': install_id,
        'X-Bytedance-Openudid': openudid,
        'X-Bytedance-Cdid': cdid,
        'X-Bytedance-Sessionid': random.choice(SESSIONS),
        'X-Bytedance-Appid': '1180',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.tiktok.com',
        'Referer': 'https://www.tiktok.com/',
    }

def get_params():
    return {
        'aid': '1988', 'app_name': 'tiktok_web', 'device_platform': 'web_mobile',
        'device_id': str(random.randint(10**18, 10**19-1)), 'os_version': '12',
        'region': random.choice(REGIONS), 'tz_name': random.choice(TIMEZONES),
        'app_language': random.choice(LOCALES), 'tz_offset': random.choice(OFFSETS),
        'channel': 'googleplay', 'msToken': str(random.randint(10**12, 10**13-1)),
        '_rticket': str(random.randint(10**9, 10**10-1))
    }

# FIXED LIVE ROOM BOT (your main focus)
def send_live_views(device_id, install_id, cdid, openudid, target_room_id=None):
    global reqs, success, fails, enters, heartbeats
    room_id = target_room_id or random.choice(ROOM_IDS)
    
    # ENTER ROOM
    try:
        params_dict = get_params()
        params = urlencode(params_dict)
        payload = f"room_id={room_id}&hold_living_room=1&is_login=1"
        sig = Gorgon(params=params).get_value()
        
        headers = get_headers(device_id, install_id, cdid, openudid)
        headers['X-Bogus'] = sig
        
        domain = random.choice(DOMAINS)
        resp = requests.post(f"https://{domain}/webcast/room/enter/?{params}", 
                           data=payload, headers=headers, verify=False, timeout=8)
        reqs += 1
        
        if resp.status_code == 200:
            with _lock:
                enters += 1
                success += 1
        else:
            with _lock:
                fails += 1
    except Exception as e:
        with _lock:
            fails += 1
    
    # HEARTBEAT LOOP
    for _ in range(8):  # 8 heartbeats per enter
        if not running:
            break
        try:
            params_dict = get_params()
            params = urlencode(params_dict)
            payload = f"room_id={room_id}&heartbeat_type=pb"
            sig = Gorgon(params=params).get_value()
            
            headers = get_headers(device_id, install_id, cdid, openudid)
            headers['X-Bogus'] = sig
            
            domain = random.choice(DOMAINS)
            resp = requests.post(f"https://{domain}/webcast/heartbeat/?{params}", 
                               data=payload, headers=headers, verify=False, timeout=6)
            reqs += 1
            
            if resp.status_code == 200:
                with _lock:
                    heartbeats += 1
                    success += 1
            else:
                with _lock:
                    fails += 1
            
            sleep(random.uniform(28, 42))
        except Exception as e:
            with _lock:
                fails += 1
            break

def sendViews(device_id, install_id, cdid, openudid):
    global reqs, success, fails
    for _ in range(20):
        if not running:
            break
        try:
            video_id = random.choice(VIDEO_IDS)
            params = urlencode(get_params())
            payload = f"item_id={video_id}&play_delta=1"
            sig = Gorgon(params=params).get_value()
            
            headers = get_headers(device_id, install_id, cdid, openudid)
            headers['X-Bogus'] = sig
            
            domain = random.choice(DOMAINS)
            resp = requests.post(f"https://{domain}/aweme/v1/aweme/stats/?{params}", 
                               data=payload, headers=headers, verify=False, timeout=8)
            reqs += 1
            
            try:
                if resp.status_code == 200 and resp.json().get('status_code') == 0:
                    with _lock:
                        success += 1
                else:
                    with _lock:
                        fails += 1
            except:
                with _lock:
                    fails += 1
        except:
            with _lock:
                fails += 1

def sendHearts(device_id, install_id, cdid, openudid):
    global reqs, success, fails
    for _ in range(20):
        if not running:
            break
        try:
            video_id = random.choice(VIDEO_IDS)
            params_dict = get_params()
            params_dict['aweme_id'] = video_id
            params = urlencode(params_dict)
            sig = Gorgon(params=params).get_value()
            
            headers = get_headers(device_id, install_id, cdid, openudid)
            headers['X-Bogus'] = sig
            
            domain = random.choice(DOMAINS)
            resp = requests.post(f"https://{domain}/aweme/v1/commit/item/digg/?{params}", 
                               headers=headers, verify=False, timeout=8)
            reqs += 1
            
            try:
                if resp.status_code == 200 and resp.json().get('status_code') == 0:
                    with _lock:
                        success += 1
                else:
                    with _lock:
                        fails += 1
            except:
                with _lock:
                    fails += 1
        except:
            with _lock:
                fails += 1

def stats_loop():
    global rps
    while running:
        time.sleep(1)
        with _lock:
            rps = reqs

def print_dashboard(mode, username=None, room_id=None):
    os.system('clear' if os.name=='posix' else 'cls')
    
    rate = (success / max((success + fails), 1)) * 100
    print(f"{Back.CYAN}{Fore.BLACK} 🎯 TikTok Bot v2.1 - FIXED{Style.RESET_ALL}")
    print(f"{Fore.YELLOW} Mode: {mode.upper()} | User: @{username or 'random'} | Room: {room_id or 'random[-6:]'}{Style.RESET_ALL}")
    print("-" * 70)
    print(f"{Fore.GREEN}✅ Success: {success:>7,}  |  {Fore.RED}❌ Fails: {fails:>7,}  |  📊 {rate:>5.1f}%")
    print(f"{Fore.BLUE}📡 Total: {reqs:>7,}  |  ⚡ RPS: {rps:>7,}  |  👥 Threads: {active_threads:>4}")
    if mode == 'live':
        print(f"{Fore.MAGENTA}🚪 Enters: {enters:>7,}  |  💓 Heartbeats: {heartbeats:>9,}{Style.RESET_ALL}")
    print("-" * 70)

import signal
def signal_handler(sig, frame):
    global running
    print(f"\n{Fore.YELLOW}🛑 Stopping...{Style.RESET_ALL}")
    running = False

def main():
    global active_threads
    
    parser = argparse.ArgumentParser(description="TikTok Bot")
    parser.add_argument('username', nargs='?', default=None, help="Username (auto room detect)")
    parser.add_argument('-t', '--threads', type=int, default=100, help="Threads")
    parser.add_argument('-v', '--views', type=int, default=10000, help="Target views")
    parser.add_argument('-m', '--mode', choices=['views', 'hearts', 'live'], default='live', help="Mode")
    
    args = parser.parse_args()
    signal.signal(signal.SIGINT, signal_handler)
    
    # AUTO ROOM DETECTION
    target_room = None
    if args.username:
        print(f"{Fore.CYAN}🔍 Detecting @{args.username}...{Style.RESET_ALL}")
        target_room = TikTokRoomDetector.detect_room(args.username)
        if target_room:
            print(f"{Fore.GREEN}✅ Room found: {target_room}{Style.RESET_ALL}")
    
    mode_funcs = {'views': sendViews, 'hearts': sendHearts, 'live': send_live_views}
    func = mode_funcs[args.mode]
    
    print(f"\n🚀 {args.threads} threads | {args.views:,} target | {args.mode.upper()}")
    threading.Thread(target=stats_loop, daemon=True).start()
    
    start_time = time.time()
    while running and success < args.views:
        device = random.choice(DEVICES)
        did, iid, cdid, openudid = device.split(':')
        
        active_threads += 1
        t = threading.Thread(
            target=lambda: (func(did, iid, cdid, openudid, target_room), globals().update(active_threads=active_threads-1)),
            daemon=True
        )
        t.start()
        
        if active_threads >= args.threads:
            time.sleep(0.05)
        
        if time.time() - start_time > 2:
            print_dashboard(args.mode, args.username, target_room)
            start_time = time.time()
    
    print(f"\n🎉 DONE! ✅{success:,} | ❌{fails:,} | 📊{reqs:,}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️ STOPPED | ✅{success:,} | ❌{fails:,}")
