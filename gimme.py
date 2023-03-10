#!/usr/bin/env python3
# @_shafiqaiman_
import pyperclip
import netifaces, argparse, base64, json, sys, re
from netifaces import AF_INET

def decodeb64(string):
    b64_bytes = string.encode("ascii")
    str_bytes = base64.b64decode(b64_bytes)
    sstring = str_bytes.decode("ascii")
    return sstring

def options(shell_name, ip, port, type="/bin/bash"):
    try:
        with open('./shellz.json', 'r') as f:
            data = json.loads(f.read())
            for line in data["shell_list"]:
                if line['name'] == shell_name.lower():
                    oneline = line['shell']
                    d = decodeb64(oneline)
                    d1 = d.replace("CHANGE_LHOST", ip)
                    d2 = d1.replace("CHANGE_LPORT", port)
                    d3 = d2.replace("CHANGE_TYPE", type)
                    pyperclip.copy(d2)
                    return f"[!] The payload has been copied to your clipboard.\n\n[>] {d3}"
    except FileNotFoundError:
        return "Error: [shellz.json] not found!"
            
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('shell', nargs='?')
parser.add_argument('ipaddress', nargs='?')
parser.add_argument('port', nargs='?')
parser.add_argument('-h', '--help', action="store_true")
parser.add_argument('-l', '--list', action="store_true")
parser.add_argument('-t', '--type')
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if __name__ == '__main__':
    if ((args.list or args.help) and args.shell and args.ipaddress and args.port) or ((args.list or args.help) and args.shell and args.ipaddress) or ((args.list or args.help) and args.shell) or (args.list and args.help and args.type) or (args.list and args.help) or (args.type and args.help):
        print("Error: something wrong!")

    elif args.shell and args.ipaddress and args.port or args.type:
        if args.type != None:
            try:
                ip = netifaces.ifaddresses(args.ipaddress)[AF_INET][0]['addr']
                opt = options(args.shell, ip, args.port, args.type)
                if opt != None:
                    print(opt)
                else:
                    print("Error: something wrong!")
            except:
                aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",args.ipaddress)
                if aa:
                    ip = aa.group()
                    opt = options(args.shell, ip, args.port, args.type)
                    if opt != None:
                        print(opt)
                    else:
                        print(f"Error: [{args.shell}] doesn't exist!")
                else:
                    print(f"Error: [{args.ipaddress}] invalid ipaddress!")
        else:
            try:
                ip = netifaces.ifaddresses(args.ipaddress)[AF_INET][0]['addr']
                opt = options(args.shell, ip, args.port)
                if opt != None:
                    print(opt)
                else:
                    print("Error: something wrong!")
            except:
                aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",args.ipaddress)
                if aa:
                    ip = aa.group()
                    opt = options(args.shell, ip, args.port)
                    if opt != None:
                        print(opt)
                    else:
                        print(f"Error: [{args.shell}] doesn't exist!")
                else:
                    print(f"Error: [{args.ipaddress}] invalid ipaddress!")

    elif (args.shell and args.ipaddress) or (args.shell):
        print("Error: something wrong!")

    elif args.help:
        print(f"Usage: {sys.argv[0]} [-h][-l] [shell] [ipaddress] [port]\n")
        print("""Positional Arguments:
        shell       type of reverse shell
        ipaddress   local ip address
        port        listening port
        """)
        print("""Options:
        -l, --list  listing all shells available
        -t, --type  type of shell
        -h, --help  show this help message and exit
        """)
        print(f"Example: {sys.argv[0]} bash tun0 4444")
        print(f"Example: {sys.argv[0]} bash 10.10.10.10 4444")
        
    elif args.list:
        try:
            with open('./shellz.json', 'r') as f:
                print("[!] Listing all shells available.\n")
                count = 0
                data = json.loads(f.read())              
                for line in sorted(data['shell_list'], key=lambda k: k['name']):
                    count +=1
                    print(f"{count}) {line['name'].title()}")
        except FileNotFoundError:
            print("Error: [shellz.json] not found!")

