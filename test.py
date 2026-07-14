import socket
from parser import parse_dns_paket, ip_to_string
from query import build_query


Type_A = 1

def lookup_domain(domain_name):
    query = build_query(domain_name, Type_A)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, ("8.8.8.8", 53))


    data, _ = sock.recvfrom(1024)
    response = parse_dns_paket(data)

    if response.answer:
        return ip_to_string(response.answer[0].data)
    else:
        return "Nema odgovora"


# t1 = lookup_domain('example.com')
# t2 = lookup_domain('recurse.com')
# t3 = lookup_domain('www.metafilter.com')
t4 = lookup_domain('www.facebook.com')

# print(t1)
# print(t2)
# print(t3)
print(t4)