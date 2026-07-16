from query import DNSHeader, DNSQuestion, build_query, response
from dataclasses import dataclass
import struct
from io import BytesIO
from typing import List

@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes


@dataclass
class DNSPaket:
    header: DNSHeader
    question: List[DNSQuestion]
    #menjacemo ovo
    answer: List[DNSRecord]
    authority: List[DNSRecord]
    additionals: List[DNSRecord]

Type_A = 1
Type_NS = 2


def parse_header(reader):
    items = struct.unpack('!HHHHHH', reader.read(12)) #svaki od H je 2 bajtni intiger pa ima ukupno 12 bajtova koje treba procitati

    return DNSHeader(*items)



#Procita duzinu jednog bajta, cita toliko bajtova(znaci jedan), radi to dok duzina ne bude 0, i onda spaja sve delove sa tackom(example.com)
def decode_name(reader):
    parts = []
    while(length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000: #ako postoji 11000000 znaci da je kompresovan
            parts.append(decode_name_compressed(length, reader))
            break
        else:
            parts.append(reader.read(length))
    return b'.'.join(parts)


def decode_name_compressed(length, reader):
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = struct.unpack('!H', pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result


def parse_question(reader):
    name = decode_name(reader) #sad imamo ime
    data = reader.read(4) #sledeca cetri bajta su podaci vezani za tip i klasu
    type_, class_ = struct.unpack('!HH', data)
    return DNSQuestion(name, type_, class_)


def parse_record(reader):
    name = decode_name(reader)
    # tip, klasa, ttl, i duzina podataka su zaj 10 bajtova (2 + 2 + 4 + 2 = 10)
    # pa citamo 10
    data = reader.read(10)
    # HHIH znaci 2-byte int, 2-byte-int, 4-byte int, 2-byte int
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data) 
    if type_ == Type_NS: # here's the code we're adding
        data = decode_name(reader)
    elif type_ == Type_A:
        data = ip_to_string(reader.read(data_len))
    else:
        data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)


def parse_dns_paket(data):
    reader = BytesIO(data)
    header = parse_header(reader)
    questions = [parse_question(reader) for _ in range(header.num_questions)]
    answers = [parse_record(reader) for _ in range(header.num_answers)]
    authorities = [parse_record(reader) for _ in range(header.num_authorities)]
    additionals = [parse_record(reader) for _ in range(header.num_additionals)]

    return DNSPaket(header, questions, answers, authorities, additionals)


def ip_to_string(ip):
    return '.'.join(str(b) for b in ip)
