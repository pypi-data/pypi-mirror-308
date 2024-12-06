from ttlinks.protocol_stack.network_layer.IPv4.ipv4_parsers import IPv4PacketParser
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_units import IPv4Unit

ipv4_parser = IPv4PacketParser()
parsed_ipv4 = ipv4_parser.parse(b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\x00\x00\xc0\xa8\x01\x01\xc0\xa8\x01\x02')
ipv4_unit = IPv4Unit(**parsed_ipv4)
print(ipv4_unit.summary)