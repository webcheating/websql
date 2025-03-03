import argparse

##############################################

parser = argparse.ArgumentParser(description="webcheating")
parser.add_argument("-u", "--url", type=str, required=True, help="target URL")
parser.add_argument("-m", "--mode", required=True, help="dump mode (table, column, entity, entity-count, table-test, column-test, entity-test)")
parser.add_argument("-o", "--offset", type=int, default=0, help="start offset (default: 0)")
parser.add_argument("-T", "--table", required=False, help="table to enumerate")
parser.add_argument("-C", "--column", required=False, help="column to enumerate")
args = parser.parse_args()

usr_url = args.url
usr_mode = args.mode
usr_offset = args.offset
usr_table = args.table
usr_column = args.column

##############################################

true_code = 301
false_code = 404  
#special_chars = "_.@-:;,/|!#$%^&*(){}[]=+~ "
special_chars = "_.@-:;[](){}/|!#$%^&*=+~"


