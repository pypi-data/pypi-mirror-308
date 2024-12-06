from ttlinks.protocol_stack.transport_layer.TCP.tcp_parsers import TCPParser
from ttlinks.protocol_stack.transport_layer.TCP.tcp_units import TCPUnit


class TCPPayload:
    @staticmethod
    def tcp_option_2_4_8_1_3():
        return bytes.fromhex('b2fe005076ee585300000000a002faf03c690000020405b40402080aa254b24a0000000001030307')

if __name__ == '__main__':


    # # # ----------------------TCP Parser----------------------
    tcp_parser = TCPParser()
    # # parsed_tcp = tcp_parser.parse(TCPPayload.with_option0())
    # # parsed_tcp = tcp_parser.parse(TCPPayload.with_ack_option_full_length())
    # parsed_tcp = tcp_parser.parse(TCPPayload.tcp_option_2_4_8_1_3())
    # tcp_unit = TCPUnit(**parsed_tcp)
    # print(tcp_unit.summary)
    # print(tcp_unit.attributes)
    # print(tcp_unit.as_bytes)
    # # print(hex(int.from_bytes(tcp_unit.payload, byteorder='big')))
    # for option in tcp_unit.options:
    #     print('-----------------')
    #     print(option.summary)
    #     print(option.attributes)
    #     print(option.as_bytes)


    # tcp_parser = TCPPacketParser()
    parsed_tcp = tcp_parser.parse(b'\x00\x50\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x50\x02\x20\x00\x00\x00\x00\x00\x00')
    tcp_unit = TCPUnit(**parsed_tcp)
    print(tcp_unit.summary)