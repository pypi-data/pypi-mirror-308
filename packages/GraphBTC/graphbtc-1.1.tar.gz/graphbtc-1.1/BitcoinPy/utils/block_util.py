"""Helper methods for extracting raw data from the Bitcoin blockchain. For more details, see
BitcoinGraph white paper"""
import hashlib
import re
import binascii
import struct
import base58
import bech32
from BitcoinPy.utils import opcodes


def uint1(stream):
    return ord(stream.read(1))


def uint2(stream):
    return struct.unpack('H', stream.read(2))[0]


def uint4(stream):
    return struct.unpack('I', stream.read(4))[0]


def uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]


def encode_uint2(value):
    return struct.pack('H', value)


def encode_uint4(value):
    return struct.pack('I', value)


def encode_uint8(value):
    return struct.pack('Q', value)


def hash32(stream):
    return stream.read(32)[::-1]


def varint(stream):
    size = uint1(stream)

    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint2(stream)
    if size == 0xfe:
        return uint4(stream)
    if size == 0xff:
        return uint8(stream)
    return -1


def compact_size(value):
    if value <= 252:
        return hash_string(struct.pack('B', value))
    if 252 < value <= 65535:
        return f"fd{hash_string(encode_uint2(value))}"
    if 65535 < value <= 4294967295:
        return f"fe{hash_string(encode_uint4(value))}"
    return f"ff{hash_string(encode_uint8(value))}"


def str_to_little_endian(value):
    big = bytearray(value)
    big.reverse()
    return ''.join(f"{n:02X}" for n in big).lower()


def hash_string(byte_buffer):
    return "".join('{:02x}'.format(b) for b in byte_buffer)


def pubkey_to_address(hex_string):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(bytearray.fromhex(hex_string))
    rip.update(sha.digest())
    return hash_to_address(f"00{rip.hexdigest()}")


def hash_to_address(key_hash):
    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(key_hash))
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]

    return base58.b58encode(bytes(bytearray.fromhex(key_hash + checksum))).decode('utf-8')


def segwit_hash_to_address(hex_string):
    spk = binascii.unhexlify(hex_string)
    version = spk[0] - 0x50 if spk[0] else 0
    program = spk[2:]
    return bech32.encode('bc', version, program)


def decipher_script(script):
    if script is None:
        return []
    stack = []
    while len(script) > 0:
        next_op = ord(script[:1])
        if next_op <= int(0x60):
            push_code = opcodes.PUSH_DATA[hash_string(script[:1])]
            stack.append(push_code)
            if 'BYTES' in push_code:
                bytes_size = int(re.findall(r'\d+', push_code)[0])
                stack.append(hash_string(script[1:bytes_size+1]))
                script = script[bytes_size:]
            if 'DATA' in push_code:
                num_bytes_pushed = int(re.findall(r'\d+', push_code)[0])
                bytes_size = hash_string(script[1:1+num_bytes_pushed])
                stack.append(bytes_size)
                script = script[1+num_bytes_pushed:]
                if len(script) > 0:
                    stack.append(hash_string(script[:int(bytes_size, 16)]))
                    script = script[int(bytes_size, 16):]
        elif int(0x60) < next_op <= int(0x6a):
            stack.append(opcodes.CONTROL_FLOW[hash_string(script[:1])])
        elif int(0x6a) < next_op <= int(0x7d):
            stack.append(opcodes.STACK_OPERATORS[hash_string(script[:1])])
        elif int(0x7d) < next_op <= int(0x82):
            stack.append(opcodes.STRINGS[hash_string(script[:1])])
        elif int(0x82) < next_op <= int(0x8a):
            stack.append(opcodes.BITWISE_LOGIC[hash_string(script[:1])])
        elif int(0x8a) < next_op <= int(0xa5):
            stack.append(opcodes.NUMERIC[hash_string(script[:1])])
        elif int(0xa5) < next_op <= int(0xaf):
            stack.append(opcodes.CRYPTOGRAPHY[hash_string(script[:1])])
        else:
            stack.append(opcodes.OTHER[hash_string(script[:1])])
        script = script[1:]
    return stack


def raw_bytes_to_id(byte_buffer):
    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(byte_buffer))
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    return hash_string(bytearray.fromhex(sha.hexdigest())[::-1])


def is_p2pk(script_stack):
    return (("OP_PUSHBYTES_65" == script_stack[0] or "OP_PUSHBYTES_33" == script_stack[0])
            and script_stack[-1] == "OP_CHECKSIG"
            )


def is_p2pkh(script_stack):
    return (script_stack[0] == "OP_DUP"
            and script_stack[1] == "OP_HASH160"
            and script_stack[-1] == "OP_CHECKSIG"
            and script_stack[-2] == "OP_EQUALVERIFY"
            )


def is_p2ms(script_stack):
    return ("OP_" in script_stack[0]
            and script_stack[-1] == "OP_CHECKMULTISIG"
            and "OP_" in script_stack[-2]
            )


def is_p2sh(script_stack):
    return (script_stack[0] == "OP_HASH160"
            and "OP_PUSHBYTES" in script_stack[1]
            and script_stack[-1] == "OP_EQUAL"
            )


def is_op_return(script_stack):
    return (script_stack[0] == "OP_RETURN"
            and "OP_PUSH" in script_stack[1]
            and len(script_stack) == 3
            )


def is_p2wpkh(script_stack):
    return (script_stack[0] == "OP_0"
            and script_stack[1] == "OP_PUSHBYTES_20"
            and len(script_stack) == 3
            )


def is_p2wsh(script_stack):
    return (script_stack[0] == "OP_0"
            and script_stack[1] == "OP_PUSHBYTES_32"
            and len(script_stack) == 3
            )
