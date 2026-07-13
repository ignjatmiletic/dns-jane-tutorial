from dataclasses import dataclass
import struct
import dataclasses

@dataclass
class DNSHeader:
    id: int
    flag: int
    num_questions : int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

class DNSQuestion:
    name: bytes
    type_: int
    class_: int



def header_to_bytes(header):
    pass


def question_to_bytes(question):
    pass




