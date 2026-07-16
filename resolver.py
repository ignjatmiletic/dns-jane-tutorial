from query import header_to_bytes, question_to_bytes, encode_dns_name, build_query, DNSHeader, DNSQuestion, Type_A
from parser import DNSRecord, DNSPaket, parse_header, parse_question, parse_dns_paket, ip_to_string, Type_NS
import socket


def send_query(ip_address, domain_name, record_type):
    query = build_query(domain_name, record_type)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, (ip_address, 53))

    data, _ = sock.recvfrom(1024)
    return parse_dns_paket(data)


response = send_query("216.239.32.10", "google.com", Type_A)


def get_answer(packet):
    # return the first A record in the Answer section
    for x in packet.answer:
        if x.type_ == Type_A:
            return x.data


def get_nameserver_ip(packet):
    # return the first A record in the Additional section
    for x in packet.additionals:
        if x.type_ == Type_A:
            return x.data
        

def get_nameserver(packet):
    # return the first NS record in the Authority section
    for x in packet.authority:
        if x.type_ == Type_NS:
            return x.data.decode('utf-8')
        

def resolve(domain_name, record_type):
    nameserver = "198.41.0.4"
    while True:
        print(f"Querying {nameserver} for {domain_name}")
        response = send_query(nameserver, domain_name, record_type)
        if ip := get_answer(response):
            return ip
        elif nsIP := get_nameserver_ip(response):
            nameserver = nsIP
        # New case: look up the nameserver's IP address if there is one
        elif ns_domain := get_nameserver(response):
            nameserver = resolve(ns_domain, Type_A)
        else:
            raise Exception("something went wrong")




print(resolve("twitter.com", Type_A))

