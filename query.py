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
    fields = dataclasses.astuple(header)

    return struct.pack('!HHHHHH', *fields)


def question_to_bytes(question):
    return question.name + struct.pack("!HH", question.type_, question.class_)




