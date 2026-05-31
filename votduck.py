import asyncio
import aiohttp
import random
import string
import time
import logging
import os
from pathlib import Path
from typing import Set, Tuple
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class DiscordUsernameChecker:
    def __init__(self):
        self.checked: Set[str] = set()
        self.available_count = 0
        self.unavailable_count = 0
        self.request_count = 0
        self.start_time = time.time()
        
        self._load_checked()

    def _load_checked(self):
        for file in [os.getenv('CHECKED_FILE'), os.getenv('AVAILABLE_FILE'), os.getenv('UNAVAILABLE_FILE')]:
            if Path(file).exists():
                with open(file, 'r', encoding='utf-8') as f:
                    self.checked.update(line.strip() for line in f if line.strip())

    def _save_username(self, username: str, available: bool):
        file = os.getenv('AVAILABLE_FILE') if available else os.getenv('UNAVAILABLE_FILE')
        with open(file, 'a', encoding='utf-8') as f:
            f.write(username + '\n')
        with open(os.getenv('CHECKED_FILE'), 'a', encoding='utf-8') as f:
            f.write(username + '\n')

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        self.clear_screen()
        print("\033[96m" + r"""
██╗   ██╗ ██████╗ ████████╗██████╗ ██╗   ██╗ ██████╗██╗  ██╗
██║   ██║██╔═══██╗╚══██╔══╝██╔══██╗██║   ██║██╔════╝██║ ██╔╝
██║   ██║██║   ██║   ██║   ██║  ██║██║   ██║██║     █████╔╝ 
╚██╗ ██╔╝██║   ██║   ██║   ██║  ██║██║   ██║██║     ██╔═██╗ 
 ╚████╔╝ ╚██████╔╝   ██║   ██████╔╝╚██████╔╝╚██████╗██║  ██╗
  ╚═══╝   ╚═════╝    ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝
        """ + "\033[0m")
        print("\033[93m              VOTDuck v2.1 - Rare Username Hunter 🦆\033[0m")
        print("\033[95m         .env Support | API v10 | Improved\033[0m")
        print("\033[95m         Made with AI by Aby377\033[0m")
        print("=" * 80)

    def generate_username(self) -> str:
        length = random.randint(int(os.getenv('MIN_LENGTH')), int(os.getenv('MAX_LENGTH')))
        rare_chars = 'xqzvkjywm'
        normal_chars = string.ascii_lowercase + "0123456789"
        
        username = []
        for i in range(length):
            if random.random() < float(os.getenv('RARE_LETTER_BIAS', 0.72)):
                username.append(random.choice(rare_chars))
            else:
                username.append(random.choice(normal_chars))
        
        if length >= 4 and random.random() < 0.15:
            pos = random.randint(1, length-2)
            username[pos] = random.choice(['_', '.'])
            
        return ''.join(username)

    async def send_webhook(self, username: str):
        webhook_url = os.getenv('WEBHOOK_URL')
        if not webhook_url:
            return

        content = f"<@{os.getenv('PING_USER_ID')}>"
        if os.getenv('PING_ROLE_ID'):
            content += f" <@&{os.getenv('PING_ROLE_ID')}>"

        embed = {
            "title": "🎉 **RARE USERNAME FOUND!**",
            "description": f"`{username}` ist **verfügbar**!",
            "color": 0x00ff00,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        payload = {"content": content, "embeds": [embed]}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload, timeout=10) as resp:
                    if resp.status not in (200, 204):
                        logger.warning(f"Webhook failed: {resp.status}")
        except Exception as e:
            logger.error(f"Webhook error: {e}")

    async def check_username(self, session: aiohttp.ClientSession, username: str) -> Tuple[str, bool]:
        if username in self.checked:
            return username, False

        self.checked.add(username)
        self.request_count += 1

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": "https://discord.com/"
        }

        try:
            async with session.get(
                f"https://discord.com/api/v10/users/{username}/profile",
                headers=headers,
                timeout=15
            ) as resp:
                
                if resp.status == 429:
                    retry_after = int(resp.headers.get('Retry-After', 5))
                    logger.warning(f"⚠️ Rate Limit → Waiting {retry_after}s")
                    await asyncio.sleep(retry_after + random.uniform(0.5, 1.5))
                    return await self.check_username(session, username)

                if resp.status == 404:
                    self.available_count += 1
                    self._save_username(username, True)
                    logger.info(f"\033[92m✅ FOUND: {username} 🦆\033[0m")
                    await self.send_webhook(username)
                    return username, True
                else:
                    self.unavailable_count += 1
                    self._save_username(username, False)
                    return username, False

        except Exception:
            await asyncio.sleep(1)
            return username, False

    def print_stats(self):
        elapsed = time.time() - self.start_time
        rpm = int(self.request_count / (elapsed / 60)) if elapsed > 0 else 0
        
        print(f"\r\033[97mChecked: \033[94m{len(self.checked):,}\033[97m | "
              f"\033[92mAvailable: {self.available_count} 🦆\033[97m | "
              f"\033[91mUnavailable: {self.unavailable_count}\033[97m | "
              f"\033[93mRPM: {rpm:,}\033[0m    ", end='', flush=True)

    async def run_checker(self, total: int = 100000):
        self.start_time = time.time()
        
        connector = aiohttp.TCPConnector(limit=int(os.getenv('MAX_CONCURRENT', 25)), ttl_dns_cache=300)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            checked_start = len(self.checked)
            
            while len(self.checked) - checked_start < total:
                batch = []
                blacklist = os.getenv('BLACKLIST_WORDS', '').split(',')
                
                for _ in range(int(os.getenv('BATCH_SIZE'))):
                    if len(self.checked) - checked_start >= total:
                        break
                    username = self.generate_username()
                    if any(bad in username.lower() for bad in blacklist):
                        continue
                    batch.append(username)

                tasks = [self.check_username(session, u) for u in batch]
                await asyncio.gather(*tasks)

                self.print_stats()
                await asyncio.sleep(float(os.getenv('BATCH_DELAY', 1.8)))

        print("\n\n\033[92mFinished! Happy hunting! 🦆🦆\033[0m")


async def main():
    checker = DiscordUsernameChecker()
    
    while True:
        checker.print_banner()
        print("    [1] Start Checker")
        print("    [2] View Settings")
        print("    [3] Statistics")
        print("    [4] Exit")
        print("=" * 80)

        choice = input("\n    Selection: ").strip()

        if choice == "1":
            print("\n    🦆 Starting VOTDuck v2.1...\n")
            await asyncio.sleep(1)
            try:
                total = int(os.getenv('TOTAL_TO_CHECK', 100000))
                await checker.run_checker(total=total)
            except KeyboardInterrupt:
                print("\n\n    \033[93mStopped.\033[0m")
            input("\nPress Enter to return...")
            
        elif choice == "2":
            print("\n=== Current .env Settings ===")
            for key in ['MIN_LENGTH', 'MAX_LENGTH', 'BATCH_SIZE', 'BATCH_DELAY', 
                       'MAX_CONCURRENT', 'RARE_LETTER_BIAS', 'TOTAL_TO_CHECK']:
                print(f"{key} = {os.getenv(key)}")
            print("\nEdit the .env file and restart the script.")
            input("\nPress Enter...")
            
        elif choice == "3":
            checker.print_banner()
            print(f"    Checked:       {len(checker.checked):,}")
            print(f"    Available:     {checker.available_count} 🦆")
            print(f"    Unavailable:   {checker.unavailable_count}")
            input("\nPress Enter...")
            
        elif choice == "4":
            print("\n    Quack Quack! See you later 🦆")
            break


if __name__ == "__main__":
    try:
        import dotenv
    except ImportError:
        print("Installing python-dotenv...")
        os.system("pip install python-dotenv")
        import dotenv
    asyncio.run(main())