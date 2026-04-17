#!/usr/bin/env python3
"""
TikTok ALL-IN-ONE Bot v2.1 - Username → Auto Room → Enter + Views/Hearts
CLI: python tiktok_bot.py kaito -t 300 -v 2000 -m live
"""

from urllib.parse import urlencode
import os, sys, ssl, time, random, threading, requests, hashlib, argparse, re, colorama
from colorama import Fore, Style, Back
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

colorama.init(autoreset=True)

# ALL BUILT-IN DATA (expanded for reliability)
DOMAINS = ["api-h2.tiktokv.com", "api22-core-c-useast1a.tiktokv.com", "api19-core-c-useast1a.tiktokv.com", "api16-core-c-useast1a.tiktokv.com"]
LOCALES = ["en_US", "es_ES", "fr_FR", "de_DE", "it_IT", "pt_BR", "ja_JP", "ko_KR"]
REGIONS = ["US", "ES", "FR", "DE", "IT", "BR", "JP", "KR"]
TIMEZONES = ["America/New_York", "Europe/Madrid", "Europe/Paris", "Europe/Berlin", "Europe/Rome", "America/Sao_Paulo", "Asia/Tokyo", "Asia/Seoul"]
OFFSETS = ["-28800", "-21600", "-14400", "0", "3600", "7200", "32400", "32400"]

VIDEO_IDS = [f"7{random.randint(12345678901234, 99999999999999)}" for _ in range(20)]
ROOM_IDS = [f"69{random.randint(45678901234567, 99999999999999)}" for _ in range(10)]
SESSIONS = [os.urandom(16).hex() for _ in range(8)]
DEVICES = [
    f"{random.randint(10**17,10**18-1)}:{random.randint(10**17,10**18-1)}:{random.randint(10**17,10**18-1)}:{random.randint(10**17,10**18-1)}"
    for _ in range(10)
]

VERSIONS = ["270204", "260104", "250904", "240804"]
RESOLUTIONS = ["900*1600", "720*1280", "1080*1920"]
DPIS = ["240", "300", "360"]

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
        """Auto-detect live room ID from username"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        })
        
        # Method 1: Profile page scrape
        try:
            url = f"https://www.tiktok.com/@{username}"
            resp = session.get(url, timeout=10, verify=False)
            room_match = re.search(r'"roomId"\s*:\s*"(\d+)"', resp.text) or \
                        re.search(r'"roomId":\s*(\d+)', resp.text) or \
                        re.search(r'liveRoom["\']?["\']?[:=]\s*["\']?(\d+)["\']?', resp.text, re.I)
            if room_match:
                return int(room_match.group(1))
        except:
            pass
        
        # Method 2: User detail API
        try:
            api_url = f"https://www.tiktok.com/api/user/detail/?uniqueId={urllib.parse.quote(username)}"
            resp = session.get(api_url, timeout=8, verify=False)
            data = resp.json()
            room_id = data.get('user', {}).get('roomId') or data.get('liveRoom', {}).get('roomId')
            if room_id:
                return int(room_id)
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
        'device_id': str(random.randint(10**18, 10**19-1)), 'os_version': '12', 'os': 'android',
        'region': random.choice(REGIONS), 'tz_name': random.choice(TIMEZONES),
        'app_language': random.choice(LOCALES), 'tz_offset': random.choice(OFFSETS),
        'channel': 'googleplay', 'msToken': str(random.randint(10**12, 10**13-1)),
        '_rticket': str(random.randint(10**9, 10**10-1))
    }

# ENHANCED LIVE ROOM ENTER + HEARTBEAT
def send_live_views(device_id, install_id, cdid, openudid, target_room_id=None):
    global reqs, success, fails, enters, heartbeats
    room_id = target_room_id or random.choice(ROOM_IDS)
    
    # Step 1: Enter Room
    try:
        params_dict = get_params()
        params = urlencode(params_dict)
        payload = f"room_id={room_id}&hold_living_room=1&is_login=1&enter_source=general_search"
        sig = Gorgon(params=params).get_value()
        
        headers = get_headers(device_id, install_id, cdid, openudid)
        headers['X-Bogus'] = sig
        
        domain = random.choice(DOMAINS)
        resp = requests.post(f"https://{domain}/webcast/room/enter/?{params}", 
                           data=payload, headers=headers, verify=False, timeout=8)
        
        if resp.status_code == 200:
            with _lock:
                enters += 1
                success += 1
                reqs += 1
    except:
        with _lock: fails += 1
    
    # Step 2: Heartbeat loop (maintain view)
    heartbeat_count = 0
    while running and heartbeat_count < 10:  # 10 heartbeats per session
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
            
            if resp.status_code == 200:
                with _lock:
                    heartbeats += 1
                    success += 1
                    reqs += 1
                heartbeat_count += 1
            else:
                break
                
            sleep(random.uniform(25, 45))  # Realistic heartbeat timing
            
        except:
            break

# OTHER FUNCTIONS (unchanged but enhanced)
def sendViews(device_id, install_id, cdid, openudid): 
    global reqs, success, fails
    for _ in range(20):
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
            
            if resp.status_code == 200 and resp.json().get('status_code') == 0:
                with _lock: success += 1
            else:
                with _lock: fails += 1
        except: with _lock: fails += 1

# Simplified other functions (same pattern)...
def sendHearts(device_id, install_id, cdid, openudid):
    global reqs, success, fails
    for _ in range(20):
        try:
            video_id = random.choice(VIDEO_IDS)
            params_dict = get_params(); params_dict['aweme_id'] = video_id
            params = urlencode(params_dict)
            sig = Gorgon(params=params).get_value()
            
            headers = get_headers(device_id, install_id, cdid, openudid)
            headers['X-Bogus'] = sig
            
            domain = random.choice(DOMAINS)
            resp = requests.post(f"https://{domain}/aweme/v1/commit/item/digg/?{params}", 
                               headers=headers, verify=False, timeout=8)
            reqs += 1
            
            if resp.status_code == 200 and resp.json().get('status_code') == 0:
                with _lock: success += 1
            else:
                with _lock: fails += 1
        except: with _lock: fails += 1

def stats_loop():
    global rps
    while running:
        sleep(1)
        with _lock: rps = reqs

def print_dashboard(mode, username=None, room_id=None):
    global active_threads
    os.system('clear' if os.name=='posix' else 'cls')
    
    rate = (success / (success + fails) * 100) if (success + fails) > 0 else 0
    print(f"{Back.CYAN}{Fore.BLACK} 🎯 TikTok ALL-IN-ONE Bot v2.1{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'📺 LIVE' if mode=='live' else '🎥 VIDEO'} | Username: @{username or 'random'} | Room: {room_id or 'random'}{Style.RESET_ALL}")
    print("-" * 80)
    print(f"{Fore.GREEN}✅ Success: {success:>7,}  |  {Fore.RED}❌ Fails: {fails:>7,}  |  📊 Rate: {rate:>5.1f}%")
    print(f"{Fore.BLUE}📡 Requests: {reqs:>7,}  |  ⚡ RPS: {rps:>7,}  |  👥 Active: {active_threads:>5}")
    if mode == 'live':
        print(f"{Fore.MAGENTA}🚪 Enters: {enters:>7,}  |  💓 Heartbeats: {heartbeats:>10,}{Style.RESET_ALL}")
    print("-" * 80)

def signal_handler(sig, frame):
    global running
    print(f"\n{Fore.YELLOW}🛑 Shutting down...{Style.RESET_ALL}")
    running = False

def main():
    global running, active_threads
    
    parser = argparse.ArgumentParser(description="TikTok ALL-IN-ONE Bot")
    parser.add_argument('username', nargs='?', default=None, help="TikTok username (auto-detects room)")
    parser.add_argument('-t', '--threads', type=int, default=100, help="Threads (default: 100)")
    parser.add_argument('-v', '--views', type=int, default=10000, help="Target views (default: 10000)")
    parser.add_argument('-m', '--mode', choices=['views', 'hearts', 'live'], default='live', help="Mode (default: live)")
    
    args = parser.parse_args()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Auto-detect room if username provided
    target_room = None
    if args.username:
        print(f"{Fore.CYAN}🔍 Detecting room for @{args.username}...{Style.RESET_ALL}")
        target_room = TikTokRoomDetector.detect_room(args.username)
        if target_room:
            print(f"{Fore.GREEN}✅ Found live room: {target_room}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ No live room found, using random{Style.RESET_ALL}")
    
    mode_funcs = {'views': sendViews, 'hearts': sendHearts, 'live': send_live_views}
    func = mode_funcs[args.mode]
    
    print(f"\n🚀 Starting {args.threads} threads | Target: {args.views:,} | Mode: {args.mode.upper()}")
    print("Press Ctrl+C to stop\n")
    
    threading.Thread(target=stats_loop, daemon=True).start()
    start_time = time.time()
    
    while running and success < args.views:
        device = random.choice(DEVICES)
        did, iid, cdid, openudid = device.split(':')
        
        with _lock: active_threads += 1
        t = threading.Thread(target=lambda: (func(did, iid, cdid, openudid, target_room), globals().update(active_threads=active_threads-1)), daemon=True)
        t.start()
        
        if active_threads >= args.threads:
            sleep(0.05)
        
        if time.time() - start_time > 2:
            print_dashboard(args.mode, args.username, target_room)
            start_time = time.time()
    
    elapsed = time.time() - start_time
    print(f"\n🎉 TARGET REACHED!")
    print(f"✅ Success: {success:,} | ❌ Fails: {fails:,} | 📊 Total: {reqs:,}")
    print(f"⏱️ Time: {elapsed:.1f}s | ⚡ RPS: {rps:.0f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️ STOPPED | ✅ {success:,} | ❌ {fails:,} | 📊 {reqs:,}")
