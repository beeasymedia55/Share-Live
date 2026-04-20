import asyncio
import aiohttp
import os
import random
import re
import sys
import time
import uuid
import threading
import hashlib
import binascii
import string
import logging
from urllib.parse import urlencode
from pystyle import Center, Colorate, Colors, Write, System

# --- Configuration & Global State ---
logging.basicConfig(level=logging.ERROR)

class State:
    success = 0
    fails = 0
    start_time = time.time()
    is_running = False
    current_action = "Idle"
    # Your specific hardcoded proxy list
    PROXIES = [
        "31.59.20.176:6754:hxidjrjw:nylyfhelpvdx",
        "198.23.239.134:6540:hxidjrjw:nylyfhelpvdx",
        "45.38.107.97:6014:hxidjrjw:nylyfhelpvdx",
        "107.172.163.27:6543:hxidjrjw:nylyfhelpvdx",
        "198.105.121.200:6462:hxidjrjw:nylyfhelpvdx",
        "216.10.27.159:6837:hxidjrjw:nylyfhelpvdx",
        "142.111.67.146:5611:hxidjrjw:nylyfhelpvdx",
        "191.96.254.138:6185:hxidjrjw:nylyfhelpvdx",
        "31.58.9.4:6077:hxidjrjw:nylyfhelpvdx",
        "23.26.71.145:5628:hxidjrjw:nylyfhelpvdx"
    ]

# --- Device Identity Logic ---
class DeviceManager:
    DEVICES = [
        {"model": "SM-N976N", "ua": "com.zhiliaoapp.musically.go/260802 (Linux; U; Android 7.1.2; SM-N976N)"},
        {"model": "Pixel 6", "ua": "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; Pixel 6)"},
        {"model": "NE2211", "ua": "com.ss.android.ugc.trill/400304 (Linux; U; Android 13; NE2211)"}
    ]

    @staticmethod
    def get_params():
        return {
            "device_id": str(random.randint(10**18, 10**19)),
            "version_code": "400304",
            "app_name": "trill",
            "device_platform": "android",
            "cdid": str(uuid.uuid4()),
            "openudid": binascii.hexlify(os.urandom(8)).decode()
        }

# --- Core API Logic (Views, Shares, Live) ---
class TikTokEngine:
    @staticmethod
    def extract_id(url):
        match = re.search(r'/video/(\d+)|/live/(\d+)|(\d{18,20})', url)
        return next((m for m in match.groups() if m), None) if match else None

    async def worker(self, session, sem, target_id, mode):
        # 1:Views, 2:Shares, 3:Favs, 4:Live Enter, 5:Live Share
        endpoints = {
            "1": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",
            "2": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/share/",
            "3": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/favorite/",
            "4": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/check/live/enter/",
            "5": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/live/share/"
        }
        
        while State.is_running:
            async with sem:
                try:
                    # Proxy Rotation & Formatting
                    raw = random.choice(State.PROXIES)
                    p = raw.split(':')
                    proxy_auth = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
                    
                    dev = random.choice(DeviceManager.DEVICES)
                    params = DeviceManager.get_params()
                    params["item_id" if mode in ["1","2","3"] else "room_id"] = target_id
                    
                    async with session.post(endpoints[mode], params=urlencode(params), 
                                            headers={"User-Agent": dev["ua"]}, 
                                            proxy=proxy_auth, timeout=10, ssl=False) as r:
                        if r.status == 200: State.success += 1
                        else: State.fails += 1
                except:
                    State.fails += 1
                await asyncio.sleep(0.001)

# --- Account & Session Management ---
class AccountTools:
    @staticmethod
    def generate_session():
        sid = f"sid_gen_{binascii.hexlify(os.urandom(16)).decode()}"
        with open("sessions.txt", "a") as f:
            f.write(f"{sid}\n")
        return sid

    @staticmethod
    async def account_creator():
        email = f"{''.join(random.choices(string.ascii_lowercase, k=10))}@temp-mail.io"
        print(Colorate.Horizontal(Colors.yellow_to_red, f"[*] Created Identity: {email}"))
        print("[!] Registration requires valid X-Gorgon (SignerPy) for final step.")
        await asyncio.sleep(1.5)

# --- Interface & Orchestration ---
def title_updater():
    while True:
        if State.is_running:
            elapsed = time.time() - State.start_time
            rps = State.success / elapsed if elapsed > 0 else 0
            System.Title(f"SUCCESS: {State.success} | FAILS: {State.fails} | {rps:.1f} r/s | PROXIES: {len(State.PROXIES)}")
        time.sleep(0.5)

async def start_boost(name, mode_id):
    url = Write.Input(f"\nEnter {name} URL/ID > ", Colors.cyan_to_white, interval=0.001)
    target_id = TikTokEngine.extract_id(url)
    if not target_id:
        print("[-] Invalid ID resolved."); time.sleep(1); return

    threads = int(Write.Input("Thread Intensity > ", Colors.cyan_to_white))
    
    State.success, State.fails, State.is_running, State.current_action = 0, 0, True, name
    State.start_time = time.time()
    
    sem = asyncio.Semaphore(threads)
    engine = TikTokEngine()
    
    print(Colorate.Horizontal(Colors.green_to_blue, f"[*] Running {name} on {target_id}... (Ctrl+C to stop)"))
    
    async with aiohttp.ClientSession() as session:
        tasks = [engine.worker(session, sem, target_id, mode_id) for _ in range(threads)]
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            State.is_running = False
            print("\n[!] Returning to Menu.")

async def main():
    threading.Thread(target=title_updater, daemon=True).start()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = r"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
     [ THE ULTIMATE ROTATING-PROXY DASHBOARD ]
        """
        print(Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(banner)))
        
        print(Colorate.Horizontal(Colors.blue_to_white, """
    [1] High-Speed Views       [4] Live Entry Bot
    [2] Mass Share Video       [5] Live Stream Share
    [3] Favorite/Heart Bot     [6] Session Generator
    [7] Account Creator        [0] Exit Framework
        """))
        
        choice = Write.Input("Selection >> ", Colors.blue_to_white, interval=0.001)
        
        if choice in ["1", "2", "3", "4", "5"]:
            modes = {"1":"Views", "2":"Shares", "3":"Hearts", "4":"Live Enter", "5":"Live Share"}
            await start_boost(modes[choice], choice)
        elif choice == "6":
            sid = AccountTools.generate_session()
            print(f"\n[+] Generated SID: {sid}\n[*] Saved to sessions.txt"); time.sleep(2)
        elif choice == "7":
            await AccountTools.account_creator(); time.sleep(1)
        elif choice == "0":
            sys.exit()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
