from urllib.parse import urlencode
from pystyle import *
from random import choice
import os, sys, ssl, re, time, random, threading, requests, hashlib, json, base64, uuid, binascii
from console.utils import set_title
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

# Attempt to import SignerPy for X-Gorgon generation
try:
    import SignerPy
except ImportError:
    pass

System.Title("HAHA LMAO CRACKED BY PRONSMODS - INTEGRATED ROOM RESOLVER & EU-IDC")

def Banner():
    Banner1 = r"""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ████████╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ██████╔╝██║   ██║   ██║   
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██╗██║   ██║   ██║   
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝                                                                            
    """
    print(Center.XCenter(Colorate.Vertical(Colors.yellow_to_green, Banner1, 2)))

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())

# Load Resource Files
def load_file(name):
    if os.path.exists(name):
        with open(name, "r") as f: return f.read().splitlines()
    return []

__localesLanguage = load_file("locale_lang.txt")
__regions = load_file("region_lang.txt")
__tzname = load_file("region_timezone.txt")
__aweme_id = load_file("video_links.txt")
__room_id_list = load_file("room_id.txt")
__session_id = load_file("sessions.txt")

__domains = ["api16-core-c-alisg.tiktokv.com", "api19-core-c-useast1a.tiktokv.com"]
__devices = ["SM-G9900", "SM-N976N", "SM-G975F", "Pixel 6"]

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

def get_proxy():
    raw = random.choice(PROXIES)
    p = raw.split(':')
    return {"http": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}", "https": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"}

# --- ROOM ID RESOLVER ---
def getRoomID(username):
    print(Colorate.Horizontal(Colors.blue_to_white, f"[*] Resolving Room ID for @{username}..."))
    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "*/*",
        "Referer": f"https://www.tiktok.com/@{username}/live",
    }
    url = f"https://www.tiktok.com/api-live/user/room/?aid=1988&uniqueId={username}"
    try:
        response = requests.get(url, headers=headers, proxies=get_proxy(), timeout=10).json()
        room_id = response["data"]["user"]["roomId"]
        print(Colorate.Horizontal(Colors.green_to_white, f"[+] Success! Room ID: {room_id}"))
        return room_id
    except Exception:
        print(Colorate.Horizontal(Colors.red_to_white, "[-] Failed to resolve Room ID. Check if user is LIVE."))
        return None

# --- SIGNATURE ENGINE ---
def get_signatures(params, data, cookie):
    try:
        return SignerPy.XG(params, data, cookie)
    except:
        return {"X-Gorgon": "", "X-Khronos": str(int(time.time()))}

# --- SENDING FUNCTIONS ---
def sendLiveViews(did, iid, cdid, openudid, room_id):
    global success, fails
    try:
        url = "https://webcast16-normal-useastred.tiktokv.eu/webcast/room/enter/"
        params = urlencode({
            "device_id": did, "iid": iid, "room_id": room_id, "version_code": "400304",
            "device_platform": "android", "aid": "1233",
            "store-idc": "no1a", "tt-target-idc": "eu-ttp2", "d_ticket": "27"
        })
        payload = f"room_id={room_id}&hold_living_room=1&enter_source=live_cell"
        sig = get_signatures(params, payload, "d_ticket=27")
        
        headers = {
            "X-Gorgon": sig.get("X-Gorgon"), "X-Khronos": sig.get("X-Khronos"),
            "Cookie": "d_ticket=27", "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = r.post(url, params=params, data=payload, headers=headers, proxies=get_proxy(), verify=False)
        if response.json().get('status_code') == 0:
            success += 1
            print(Colorate.Horizontal(Colors.cyan_to_blue, f'[+] Live Entry | Room: {room_id} | Total: {success}'))
        else: fails += 1
    except: fails += 1

# [Omitted other send functions for brevity, but they remain identical to your stupid (1).py logic]

def rpsm_loop():
    while True:
        initial = success
        time.sleep(1)
        set_title(f"Success: {success} | Fails: {fails} | RPS: {success - initial}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    Banner()
    
    if not os.path.exists("devices.txt"):
        with open("devices.txt", "w") as f: f.write("did:iid:cdid:openudid")
    with open("devices.txt", "r") as f:
        devices = f.read().splitlines()

    print(Colorate.Horizontal(Colors.green_to_yellow, "[1] Views [2] Favorite [3] Share [4] Like [5] Followers [6] Live Stream"))
    sendType = int(Write.Input("Option > ", Colors.green_to_yellow, interval=0.0001))
    
    target_room_id = ""
    if sendType == 6:
        print(Colorate.Horizontal(Colors.cyan_to_blue, "\n[1] Enter Room ID Manually\n[2] Resolve via Username"))
        sub_opt = Write.Input("Choice > ", Colors.white_to_green)
        if sub_opt == "1":
            target_room_id = Write.Input("Enter Room ID > ", Colors.white_to_green)
        else:
            user = Write.Input("Enter Username (e.g. kaito) > ", Colors.white_to_green)
            target_room_id = getRoomID(user)
            if not target_room_id: sys.exit()

    threads = int(Write.Input("Threads > ", Colors.green_to_yellow, interval=0.0001))
    amountTosend = int(Write.Input("Hits > ", Colors.green_to_yellow, interval=0.0001))
    
    success, fails = 0, 0
    threading.Thread(target=rpsm_loop, daemon=True).start()
    
    while success < amountTosend:
        device = random.choice(devices)
        if ":" not in device: device = f"{random.randint(10**18, 10**19)}:{random.randint(10**18, 10**19)}:{uuid.uuid4()}:{binascii.hexlify(os.urandom(8)).decode()}"
        did, iid, cdid, openudid = device.split(':')
        
        if sendType == 6:
            for _ in range(threads):
                threading.Thread(target=sendLiveViews, args=[did, iid, cdid, openudid, target_room_id]).start()
        # [Add other sendType conditions here as per your original file]
        
        time.sleep(1)
        if success >= amountTosend: break
