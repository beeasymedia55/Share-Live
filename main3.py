import asyncio
import aiohttp
import os
import random
import re
import sys
import time
import threading
import binascii
from urllib.parse import urlencode, urlparse
from pystyle import Center, Colorate, Colors, Write, System

# Import SignerPy - ensure you have the library installed
try:
    import SignerPy
except ImportError:
    print("Please install SignerPy: pip install SignerPy")

class State:
    success = 0
    fails = 0
    start_time = time.time()
    is_running = False
    # Specific proxies provided
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

class TikTokEngine:
    @staticmethod
    def extract_id(url):
        match = re.search(r'/video/(\d+)|/live/(\d+)|(\d{18,20})', url)
        return next((m for m in match.groups() if m), None) if match else None

    async def worker(self, session, sem, target_id, mode):
        endpoints = {
            "1": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",
            "2": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/share/",
            "3": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/favorite/",
            "4": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/check/live/enter/",
            "5": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/live/share/"
        }
        
        url = endpoints[mode]
        
        while State.is_running:
            async with sem:
                try:
                    # 1. Setup Proxy
                    raw = random.choice(State.PROXIES)
                    p = raw.split(':')
                    proxy_auth = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
                    
                    # 2. Setup Device Params
                    device_id = str(random.randint(10**18, 10**19))
                    params = {
                        "device_id": device_id,
                        "version_code": "400304",
                        "device_platform": "android",
                        "item_id" if mode in ["1","2","3"] else "room_id": target_id
                    }
                    query = urlencode(params)
                    
                    # 3. Generate Signatures using PySigner
                    # Format: PySigner.XG(query, data, cookies)
                    # For simple stats/shares, data and cookies are often empty
                    sig = SignerPy.XG(query, "", "") 
                    
                    headers = {
                        "User-Agent": "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; Pixel 6)",
                        "X-Gorgon": sig.get("X-Gorgon"),
                        "X-Khronos": sig.get("X-Khronos")
                    }
                    
                    async with session.post(url, params=params, headers=headers, proxy=proxy_auth, timeout=8, ssl=False) as r:
                        if r.status == 200:
                            State.success += 1
                        else:
                            State.fails += 1
                except Exception:
                    State.fails += 1
                await asyncio.sleep(0.01)

def live_stats_ui():
    """Threaded function to update Termux title and overlay stats"""
    while True:
        if State.is_running:
            elapsed = time.time() - State.start_time
            rps = State.success / elapsed if elapsed > 0 else 0
            # Update System Title for Termux/Console
            System.Title(f"TOK-LIVE | OK: {State.success} | ERR: {State.fails} | Speed: {rps:.1f} r/s")
        time.sleep(0.5)

async def start_boost(name, mode_id):
    url_input = Write.Input(f"\nEnter {name} URL/ID > ", Colors.blue_to_white, interval=0.001)
    target_id = TikTokEngine.extract_id(url_input)
    
    if not target_id:
        print(Colorate.Horizontal(Colors.red_to_white, "[-] Invalid Target."))
        return

    threads = int(Write.Input("Threads (Recommend 50-200 for Termux) > ", Colors.blue_to_white))
    
    State.success, State.fails, State.is_running = 0, 0, True
    State.start_time = time.time()
    
    sem = asyncio.Semaphore(threads)
    engine = TikTokEngine()
    
    print(Colorate.Horizontal(Colors.green_to_blue, f"[*] Sending {name} to ID: {target_id}..."))
    
    async with aiohttp.ClientSession() as session:
        tasks = [engine.worker(session, sem, target_id, mode_id) for _ in range(threads)]
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            State.is_running = False

async def main():
    # Start the Live Stats background thread
    threading.Thread(target=live_stats_ui, daemon=True).start()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = r"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
     [ PY-SIGNER + LIVE STATS EDITION ]
        """
        print(Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(banner)))
        print(Colorate.Horizontal(Colors.blue_to_white, "\n[1] Views [2] Shares [3] Favs [4] Live Enter [5] Live Share [0] Exit"))
        
        choice = Write.Input("\nSelection >> ", Colors.blue_to_white, interval=0.001)
        
        modes = {"1":"Views", "2":"Shares", "3":"Hearts", "4":"Live Enter", "5":"Live Share"}
        if choice in modes:
            await start_boost(modes[choice], choice)
        elif choice == "0":
            sys.exit()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
