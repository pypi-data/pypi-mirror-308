import socket
import time

# 提取并转换 IP 地址
source_ip_hex = 'c0a80146'  # 192.168.1.70
destination_ip_hex = '12dcb641'  # 18.220.182.65

source_ip = socket.inet_ntoa(bytes.fromhex(source_ip_hex))
destination_ip = socket.inet_ntoa(bytes.fromhex(destination_ip_hex))

print("源 IP 地址：", source_ip)
print("目的 IP 地址：", destination_ip)

import struct

# 构建伪首部
source_ip_bytes = socket.inet_aton(source_ip)  # '192.168.1.70'
destination_ip_bytes = socket.inet_aton(destination_ip)  # '18.220.182.65'
reserved = b'\x00'
protocol = b'\x06'  # TCP 协议号为 6

# 计算 TCP 长度（TCP 头 + 数据）
tcp_segment_hex = 'd38c01bb51aed728000000008002faf000000000020405b40103030801010402'
tcp_segment_bytes = bytes.fromhex(tcp_segment_hex)
tcp_length = len(tcp_segment_bytes)
tcp_length_bytes = struct.pack('!H', tcp_length)  # 以网络字节序打包为 2 字节

# 组合伪首部
pseudo_header = source_ip_bytes + destination_ip_bytes + reserved + protocol + tcp_length_bytes

print("伪首部（hex）：", pseudo_header.hex())

# 校验和计算的数据
checksum_data = pseudo_header + tcp_segment_bytes

print("用于校验和计算的数据（hex）：", checksum_data.hex())


def calculate_checksum(data):
    # 如果数据长度为奇数，填充一个字节
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    # 以每 2 个字节为一组进行求和
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
        # 处理可能的进位
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # 对最终的和取反
    checksum = ~checksum & 0xFFFF
    return checksum


calculated_checksum = calculate_checksum(checksum_data)
print("计算得到的校验和：0x{:04x}".format(calculated_checksum))

time.sleep(5)