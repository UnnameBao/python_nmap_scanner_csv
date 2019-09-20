#enconding:utf-8
'''
    @Author:	b0ring
    @MySite:	https://unnamebao.github.io/
    @Date:		2019-09-19 16:11:06
    @Version:	1.0.0
'''

import nmap
import gevent
from gevent import monkey,pool
from gevent import sleep
import getopt
import sys
import csv
from gevent.lock import BoundedSemaphore

sem = BoundedSemaphore(1)
sem2 = BoundedSemaphore(0)
monkey.patch_all()
port_list = [1,7,19,21,22,23,25,31,42,53,67,69,79,80,99,102,109,110,113,119,135,137,138,139,143,161,177,389,443,456,513,544,548,553,555,568,569,635,636,666,993,1001,1011,1024]
port_list = [str(port) for port in port_list]
port_str  = ",".join(port_list)
ip_port_dict = {}
flag = [1000,]

def scan(ip_addr):
    nm = nmap.PortScanner()
    res = nm.scan(ip_addr,port_str,"")
    try:
        ports_res = res["scan"][ip_addr]["tcp"]
    except:
        print(flag[0])
        flag[0] -= 1
        return
    port_open_list = []
    for port in sorted(ports_res.keys()):
        if ports_res[port]["state"] == "open":
            port_open_list.append(port)
    if len(port_open_list) == 0:
        flag[0] -= 1
        return
    ip_port_dict[ip_addr] = ".".join([str(port) for port in port_open_list]).replace("21.22.23","21-23").replace("137.138.139","137-139")
    flag[0] -= 1

def process_ip_list(ip_list,output_file,start):
    ip_list_num = len(ip_list)
    for ip_pointer in range(start,start + ip_list_num,1000):
        sem.acquire()
        print("[*] Start scanning at",ip_pointer)
        print(ip_port_dict)
        ip_port_dict.clear()
        with open("scan.log","a") as f:
            f.write(str(ip_pointer))
        pool_ = pool.Pool(200)
        gevent_list = []
        for ip_addr in ip_list[ip_pointer:ip_pointer + 1000]:
            g = pool_.spawn(scan,ip_addr)
            gevent_list.append(g)
        gevent.joinall(gevent_list)
        headers = ["IP","端口"]
        while flag[0] > 0:
            pass
        with open(output_file,'a') as csv_file:
            csv_write = csv.writer(csv_file)
            if ip_pointer == 0:
                csv_write.writerow(headers)
            csv_write.writerows(list(ip_port_dict.items()))
        flag[0] = 1000
        sem.release()

def main(argv):
    input_file = ""
    start = 0
    number = 10000
    output_file = "res.csv"
    try:
        opts,args = getopt.getopt(argv,"hi:s:n:o:",["input","start","number","output"])
    except getopt.GetoptError:
        print("[*] Useage: python3 nmap_scanner.py -i <inputfile> -s <startline> -n <number of lines>")
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-h":
            print("[*] Useage: python3 nmap_scanner.py -i <inputfile> -s <startline> -n <number of lines> -o <outputfile>")
            sys.exit(0)
        elif opt in ("-i","--input"):
            input_file = arg
        elif opt in ("-s","--start"):
            try:
                start = int(arg)
            except:
                print("[*] Start must be integer!")
                sys.exit(2)
        elif opt in ("-n","--number"):
            try:
                number = int(arg)
            except:
                print("[*] Number must be integer!")
        elif opt in ("-o","--output"):
            output_file = arg

    print("[*] The input file is:%s."%input_file)
    print("[*] Start line will be:",start,"and will process",number,"lines.")
    print("[*] Ready for scanning.")
    with open(input_file,"r") as f:
        ip_list = f.readlines()[start:start + number]
        ip_list = [ip_addr.strip() for ip_addr in ip_list]
        process_ip_list(ip_list,output_file,start)


if __name__ == '__main__':
    main(sys.argv[1:])