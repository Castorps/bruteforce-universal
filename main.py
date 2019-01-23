from module.bruter import Bruter
from module.const import (combos_max, combos_start, proxies_minimum)
from module.proxy_manager import ProxyManager
from module.proxy_scraper import ProxyScraper

import argparse
from asciimatics.screen import Screen
from collections import deque
from sys import (path, platform)
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
        screen.print_at(' ' * 80, 0, i+1)

    
def main(screen):

    parser = argparse.ArgumentParser()
    parser.add_argument('combo_file', help='The path to your combolist', type=str)
    parser.add_argument('proxy_file', help='The path to your proxylist', type=str)
    parser.add_argument('bots', help='How many bots you want to use', type=int)
    args = parser.parse_args()
    
    if 'linux' in platform or 'darwin' in platform:
        path_separator = '/'
            
    elif 'win' in platform:
        path_separator = '\\'
        
    else:
        path_separator = '/'
    
    path_output_file = path[0] + path_separator + 'output.txt'
    path_hits_file = path[0] + path_separator + 'hits.txt'
    
    screen.print_at('Bruter Status:' + ' ' * 9 + 'Creating Combo Queue', 2, 1)
    screen.refresh()
    combo_queue = create_combo_queue(args.combo_file)
    
    screen_clear(screen, 1)
    screen.print_at('Bruter Status:' + ' ' * 9 + 'Getting Proxies', 2, 1)
    screen.refresh()
    proxy_scraper = ProxyScraper(args.proxy_file)
    proxy_scraper.scrape()

    proxy_manager = ProxyManager()
    proxy_manager.put(proxy_scraper.get())
    proxy_manager_thread = Thread(target=proxy_manager.start)
    proxy_manager_thread.daemon = True
    proxy_manager_thread.start()

    screen_clear(screen, 1)
    screen.print_at('Bruter Status:' + ' ' * 9 + 'Starting Bots', 2, 1)
    screen.refresh()
    engine = Bruter(args.bots, combo_queue, proxy_manager, path_hits_file)
    engine.start()

    tested_per_min = 0
    attempts_per_min = 0
    tested_before_last_min = 0
    attempts_before_last_min = 0
    tested_per_min_list = deque(maxlen=5)
    attempts_per_min_list = deque(maxlen=5)

    time_start = time()
    time_checked = time_start
    time_output = time_start

    try:
        while len(combo_queue):
            time_now = time()
            time_running = time_now - time_start
            hours, rem = divmod(time_running, 3600)
            minutes, seconds = divmod(rem, 60)
            time_running_format = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)

            screen_clear(screen, 16)
            screen.print_at('Bruter Status:' + ' ' * 9 + 'Running', 2, 1)
            screen.print_at('Time:' + ' ' * 18 + time_running_format, 2, 3)
            screen.print_at('Bots:' + ' ' * 18 + str(len(engine.bots)), 2, 4)
            screen.print_at('Hits:' + ' ' * 18 + str(engine.hits), 2, 5)
            screen.print_at('Combolist:' + ' ' * 13 + args.combo_file, 2, 7)
            screen.print_at('Combolist Position:' + ' ' * 4 + str(engine.tested + combos_start), 2, 8)
            screen.print_at('Loaded Combos:' + ' ' * 9 + str(len(combo_queue)), 2, 9)
            screen.print_at('Loaded Proxies:' + ' ' * 6 + str(proxy_manager.size), 2, 10)
            screen.print_at('Last Combo:' + ' ' * 12 + engine.last_combo[0] + ':' + engine.last_combo[1], 2, 11)
            screen.print_at('Tested:' + ' ' * 16 + str(engine.tested), 2, 13)
            screen.print_at('Attempts:' + ' ' * 14 + str(engine.tested + engine.retries), 2, 14)
            screen.print_at('Tested/min:' + ' ' * 12 + str(tested_per_min), 2, 15)
            screen.print_at('Attempts/min:' + ' ' * 10 + str(attempts_per_min), 2, 16)
            screen.refresh()

            if (time_now - time_checked) >= 60:
                time_checked = time_now
                tested_last_min = engine.tested - tested_before_last_min
                attempts_last_min = (engine.tested + engine.retries) - attempts_before_last_min
                tested_per_min_list.append(tested_last_min)
                attempts_per_min_list.append(attempts_last_min)
                tested_per_min = round(sum(tested_per_min_list) / len(tested_per_min_list), 2)
                attempts_per_min = round(sum(attempts_per_min_list) / len(attempts_per_min_list), 2)
                tested_before_last_min = engine.tested
                attempts_before_last_min = (engine.tested + engine.retries)

            if (time_now - time_output) >= 5:
                time_output = time_now
                output = ('Time: ' + time_running_format + '\n'
                          'Hits: ' + str(engine.hits) + '\n'
                          'Combolist Position: ' + str(engine.tested + combos_start) + '\n')

                output_file = open(path_output_file, 'w', encoding='utf-8', errors='ignore')
                output_file.write(output)
                output_file.close()
                
            if proxy_manager.size < proxies_minimum:
                screen_clear(screen, 1)
                screen.print_at('Bruter Status:' + ' ' * 9 + 'Getting Proxies', 2, 1)
                screen.refresh()
                proxy_scraper.scrape()
                proxy_manager.put(proxy_scraper.get())

            sleep(0.25)

    except KeyboardInterrupt:
        output = ('Time: ' + time_running_format + '\n'
                  'Hits: ' + str(engine.hits) + '\n'
                  'Combolist Position: ' + str(engine.tested + combos_start) + '\n')

        output_file = open(path_output_file, 'w', encoding='utf-8', errors='ignore')
        output_file.write(output)
        output_file.close()

    screen_clear(screen, 1)
    screen.print_at('Bruter Status:' + ' ' * 9 + 'Stopping', 2, 1)
    screen.refresh()
    engine.stop()
    proxy_manager.stop()
    proxy_manager_thread.join()

    exit()


if __name__ == '__main__':
    Screen.wrapper(main)
