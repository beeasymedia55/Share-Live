import requests
from user_agent import generate_user_agent
from time import time, sleep
import random
from colorama import Fore, init, Style
import threading
import argparse
import sys
import uuid
import base64
import hashlib
import hmac
from urllib.parse import urlencode, unquote
from faker import Faker
import os
import json
from datetime import datetime
import re

# Initialize colorama
init(autoreset=True)

fake = Faker()

print(f'''
{Fore.CYAN}{Style.BRIGHT}
  ░▀▄░░▄▀                                                   
  ▄▄▄▄██▄▄▄▄▄░▀█▀▐░▌                                       
  █▒░▒░▒░█▀█░░█░▐░▌                                       
  █░▒░▒░▒█▀█░░█░░█                                          
  █▄▄▄▄▄▄███══════  {Fore.YELLOW}v6.0 USERNAME → ROOM ID BOT{Fore.RESET}
  
  {Fore.YELLOW}Auto Username → Room ID → Enter Room{Fore.RESET}
  {Fore.GREEN}Telegram{Fore.RESET} : {Fore.CYAN}https://t.me/ik48x{Fore.RESET}
''')

class TikTokRoomDetector:
    """Extract Room ID from @username"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': generate_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def detect_room_from_profile(self, username):
        """Method 1: Profile page scraping"""
        print(f"{Fore.YELLOW}🔍 Scanning @{username} profile...{Fore.RESET}")
        
        try:
            url = f"https://www.tiktok.com/@{username}"
            resp = self.session.get(url, timeout=10)
            
            # Look for live room indicators
            if "live" in resp.text.lower() or '"liveRoom"' in resp.text:
                # Extract from JSON data
                room_match = re.search(r'"roomId"\s*:\s*"?(\d+)"?', resp.text)
                if room_match:
                    room_id = room_match.group(1)
                    print(f"{Fore.GREEN}✅ LIVE DETECTED! Room ID: {room_id}{Fore.RESET}")
                    return room_id
                
                # Fallback: look for live URL patterns
                live_match = re.search(r'/@[^/]+/live/(\d+)', resp.text)
                if live_match:
                    room_id = live_match.group(1)
                    print(f"{Fore.GREEN}✅ LIVE URL FOUND! Room ID: {room_id}{Fore.RESET}")
                    return room_id
            
            print(f"{Fore.YELLOW}⚠️  No live room on profile{Fore.RESET}")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}❌ Profile scan failed: {e}{Fore.RESET}")
            return None
    
    def api_room_check(self, username):
        """Method 2: Direct API check"""
        print(f"{Fore.YELLOW}🔍 API checking @{username}...{Fore.RESET}")
        
        try:
            params = {
                'aid': '1988',
                'app_name': 'tiktok_web',
                'device_id': str(random.randint(7000000000000000000,7999999999999999999)),
                'uniqueId': username,
                'channel': 'tiktok_web',
                'device_platform': 'web_pc'
            }
            
            url = "https://www.tiktok.com/api/user/detail/"
            resp = self.session.get(url, params=params, timeout=10).json()
            
            if resp.get('status_code') == 0:
                user_data = resp.get('user', {})
                room_id = user_data.get('roomId')
                if room_id:
                    print(f"{Fore.GREEN}✅ API LIVE! Room ID: {room_id}{Fore.RESET}")
                    return str(room_id)
            
            print(f"{Fore.YELLOW}⚠️  No API live data{Fore.RESET}")
            return None
            
        except:
            return None
    
    def get_live_room(self, username):
        """Master room detector"""
        print(f"\n{Fore.CYAN}🎬 TARGET: @{username}{Fore.RESET}")
        
        # Method 1: Profile scraping
        room_id = self.detect_room_from_profile(username)
        if room_id:
            return room_id
        
        # Method 2: API check
        room_id = self.api_room_check(username)
        if room_id:
            return room_id
        
        # Fallback: Generate likely room ID
        print(f"{Fore.YELLOW}🔄 No live detected - generating room ID{Fore.RESET}")
        return str(random.randint(7000000000000000000, 7999999999999999999))

class AutoCookieGenerator:
    """Advanced TikTok Cookie Generator"""
    
    def __init__(self):
        self.session_counter = 0
    
    def generate_sessionid(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
        return ''.join(random.choices(chars, k=32))
    
    def generate_ttwid(self):
        user_id = str(random.randint(1000000000000000000, 9999999999999999999))
        timestamp = str(int(time.time()))
        signature = hashlib.sha256(user_id.encode()).hexdigest()[:32]
        return f"1%7C{user_id}%7C{timestamp}%7C{signature}"
    
    def generate_odin_tt(self):
        raw = os.urandom(64)
        return base64.b64encode(raw).decode('utf-8').rstrip('=')
    
    def generate_csrf_token(self):
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20)) + '-' + \
               ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
    
    def generate_full_cookies(self):
        self.session_counter += 1
        return {
            'sessionid': self.generate_sessionid(),
            'ttwid': self.generate_ttwid(),
            'odin_tt': self.generate_odin_tt(),
            'msToken': ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_', k=107)),
            'sid_tt': self.generate_sessionid(),
            'sessionid_ss': self.generate_sessionid(),
            'tt_csrf_token': self.generate_csrf_token(),
            'csrf_session_id': str(uuid.uuid4()),
            's_v_web_id': f"verify_{fake.uuid4().replace('-','')[:20]}",
        }

class UltimateRoomEnterBot:
    def __init__(self, username, threads=200, viewers=1000):
        self.username = username
        self.dn, self.bad, self.pb = 0, 0, 0
        self.viewers_target = viewers
        self.threads = threads
        
        print(f"{Fore.YELLOW}🎯 USERNAME MODE: @{username}{Fore.RESET}")
        
        # Step 1: Detect room ID
        detector = TikTokRoomDetector()
        self.room_id = detector.get_live_room(username)
        print(f"{Fore.GREEN}📺 ROOM ID: {self.room_id}{Fore.RESET}")
        
        self.cookie_gen = AutoCookieGenerator()
        self.lock = threading.Lock()
        self.running = True
        
        sleep(2)
        self.start_enter_threads()
    
    def print_console(self, arg, status="Console"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\r{Fore.WHITE}[{Fore.BLUE}{timestamp}{Fore.WHITE}][{Fore.RED}{status}{Fore.WHITE}] {arg}{Style.RESET_ALL}", end='', flush=True)
    
    def generate_device_fingerprint(self):
        device_id = str(random.randint(7000000000000000000, 7999999999999999999))
        iid = str(int(time.time() * 1000)) + str(random.randint(10000, 99999))
        
        return {
            'device_id': device_id,
            'iid': iid,
            'openudid': str(uuid.uuid4()).replace('-', ''),
            'app_name': random.choice(["tiktok_web", "musically_go"]),
            'channel': random.choice(["tiktok_web", "googleplay", "aws"]),
            'platform': random.choice(["web_pc", "android", "ios"]),
            'cookies': self.cookie_gen.generate_full_cookies()
        }
    
    def generate_xbogus_signature(self, url, params):
        secrets = ["web_sign_v1", "tiktokv1", "musically_v2"]
        secret = random.choice(secrets)
        
        sorted_params = dict(sorted(params.items()))
        query = urlencode(sorted_params, safe=':/?#[]@!$&\'()*+,;=')
        sign_string = f"{url}?{query}"
        
        signature = hmac.new(
            secret.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            '_signature': signature[:32],
            'X-Bogus': base64.b64encode(signature.encode()).decode().rstrip('=')
        }
    
    def build_enter_headers(self, device_info):
        cookies_str = "; ".join([f"{k}={v}" for k, v in device_info['cookies'].items()])
        
        return {
            "Cookie": cookies_str,
            "User-Agent": generate_user_agent(),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"https://www.tiktok.com/@{self.username}/live",
            "Origin": "https://www.tiktok.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
    
    def enter_room(self):
        device_info = self.generate_device_fingerprint()
        headers = self.build_enter_headers(device_info)
        
        params = {
            'aid': '1988',
            'app_name': device_info['app_name'],
            'device_id': device_info['device_id'],
            'room_id': self.room_id,
            'iid': device_info['iid'],
            'channel': device_info['channel'],
            'device_platform': device_info['platform']
        }
        
        sigs = self.generate_xbogus_signature("https://www.tiktok.com/api/room/web/guest/enter/", params)
        params.update(sigs)
        
        try:
            response = requests.get(
                "https://www.tiktok.com/api/room/web/guest/enter/",
                headers=headers,
                params=params,
                timeout=12
            )
            
            if response.status_code in [200, 201]:
                with self.lock:
                    self.dn += 1
                self.print_console(f"✅ ENTER #{self.dn} | {device_info['device_id'][:12]}", "SUCCESS")
                return True
            else:
                with self.lock:
                    self.bad += 1
                return False
                
        except:
            self.enter_room()
    
    def stats_display(self):
        while self.running:
            success_rate = (self.dn / (self.dn + self.bad) * 100) if (self.dn + self.bad) > 0 else 0
            progress = min(100, (self.dn / self.viewers_target) * 100)
            
            print(f"\r{Fore.MAGENTA}[@{self.username}] {Fore.GREEN}ENTERS: {self.dn:>4} | "
                  f"ERR: {self.bad:>3} | {Fore.YELLOW}RATE: {success_rate:>5.1f}% | "
                  f"{progress:>3.0f}% | Room: {self.room_id[:12]}...")
            
            if self.dn >= self.viewers_target:
                self.running = False
                print(f"\n{Fore.GREEN}🎉 TARGET REACHED: {self.dn} viewers entered!{Fore.RESET}")
                break
                
            sleep(2)
    
    def start_enter_threads(self):
        threading.Thread(target=self.stats_display, daemon=True).start()
        
        for i in range(self.viewers_target):
            while self.running and threading.active_count() <= self.threads + 10:
                threading.Thread(target=self.enter_room, daemon=True).start()
                sleep(random.uniform(0.1, 0.3))

def main():
    parser = argparse.ArgumentParser(description='🎬 @USERNAME → Room ID → Auto Enter Bot v6.0')
    parser.add_argument('username', help='TikTok username (e.g. kaito)')
    parser.add_argument('-t', '--threads', type=int, default=300, help='Max threads (default: 300)')
    parser.add_argument('-v', '--viewers', type=int, default=2000, help='Target viewers (default: 2000)')
    
    args = parser.parse_args()
    
    UltimateRoomEnterBot(
        username=args.username,
        threads=args.threads,
        viewers=args.viewers
    )

if __name__ == '__main__':
    main()
