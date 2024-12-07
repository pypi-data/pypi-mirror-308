BitStuffing='''
def bit_stuffing(data: str) -> str:
    stuffed_data = ""
    consecutive_ones = 0
    
    for bit in data:
        if bit == '1':
            consecutive_ones += 1
            stuffed_data += bit
            if consecutive_ones == 5:
                stuffed_data += '0'
                consecutive_ones = 0
        else:
            stuffed_data += bit
            consecutive_ones = 0 
    
    return stuffed_data

def bit_unstuffing(stuffed_data: str) -> str:
    unstuffed_data = ""
    consecutive_ones = 0

    i = 0
    while i < len(stuffed_data):
        bit = stuffed_data[i]
        if bit == '1':
            consecutive_ones += 1
            unstuffed_data += bit
            if consecutive_ones == 5:

                i += 1
                consecutive_ones = 0
        else:
            unstuffed_data += bit
            consecutive_ones = 0 
        i += 1
    
    return unstuffed_data

data = "111110001111111000111"
print("Original data:      ", data)
stuffed = bit_stuffing(data)
print("Stuffed data:       ", stuffed)
unstuffed = bit_unstuffing(stuffed)
print("Unstuffed data:     ", unstuffed)
'''

ByteStuffing='''
def byte_stuffing(data: bytes, delimiter: bytes = b'\x7E', escape: bytes = b'\x7D') -> bytes:
    stuffed_data = bytearray()
    
    for byte in data:
        if byte == delimiter[0]:
            stuffed_data.extend(escape + bytes([byte ^ 0x20]))
        elif byte == escape[0]:
            stuffed_data.extend(escape + bytes([byte ^ 0x20]))
        else:
            stuffed_data.append(byte)
    
    return bytes(stuffed_data)

def byte_unstuffing(stuffed_data: bytes, delimiter: bytes = b'\x7E', escape: bytes = b'\x7D') -> bytes:
    unstuffed_data = bytearray()
    i = 0
    
    while i < len(stuffed_data):
        byte = stuffed_data[i]
        if byte == escape[0] and i + 1 < len(stuffed_data):
            unstuffed_data.append(stuffed_data[i + 1] ^ 0x20)
            i += 2
        else:
            unstuffed_data.append(byte)
            i += 1
    
    return bytes(unstuffed_data)

data = b'\x12\x7E\x45\x7D\x78\x7E\x56'
print("Original data:      ", data)
stuffed = byte_stuffing(data)
print("Stuffed data:       ", stuffed)
unstuffed = byte_unstuffing(stuffed)
print("Unstuffed data:     ", unstuffed)
'''

CharacterCount='''
def character_count(frames):
    final_string = ""
    for frame in frames:
        length = str(len(frame) + 1)
        final_string += length + frame
    return final_string

no_of_frames = int(input("Enter the number of frames: "))
frames = []

for i in range(no_of_frames):
    frame = input(f"Enter frame {i + 1}: ")
    frames.append(frame)

result = character_count(frames)
print("Result:", result)

'''

CyclicRedundancyCheck='''
# import zlib

# data = b"Hello, CRC!"

# crc32_checksum = zlib.crc32(data)

# print(f"CRC32 Checksum: {crc32_checksum:#010x}")

def calculate_crc(data: bytes, polynomial: int, initial_value: int = 0xFFFFFFFF):
    crc = initial_value
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF

data = b"Hello, CRC!"

polynomial = 0xEDB88320

custom_crc32_checksum = calculate_crc(data, polynomial)

print(f"Custom CRC32 Checksum: {custom_crc32_checksum:#010x}")

'''

HammingCode='''
def calculate_parity_positions(data_length):
    """Calculate positions of parity bits (powers of 2)."""
    i = 0
    positions = []
    while 2**i <= data_length + i + 1:
        positions.append(2**i - 1)
        i += 1
    return positions


def generate_hamming_code(data):
    """Generate Hamming code from input binary data."""
    data = list(map(int, data))
    m = len(data) 
    parity_positions = calculate_parity_positions(m)
    n = m + len(parity_positions) 
    encoded = [0] * n

    j = 0
    for i in range(n):
        if i in parity_positions:
            continue 
        encoded[i] = data[j]
        j += 1

    for parity_pos in parity_positions:
        parity = 0
        for i in range(n):
            if (i + 1) & (parity_pos + 1): 
                parity ^= encoded[i]
        encoded[parity_pos] = parity

    return ''.join(map(str, encoded))


def correct_hamming_code(encoded):
    """Detect and correct errors in the received Hamming code."""
    encoded = list(map(int, encoded))
    n = len(encoded)
    parity_positions = calculate_parity_positions(n)
    error_position = 0

    for parity_pos in parity_positions:
        parity = 0
        for i in range(n):
            if (i + 1) & (parity_pos + 1): 
                parity ^= encoded[i]
        if parity != 0:
            error_position += parity_pos + 1

    if error_position != 0:
        print(f"Error detected at position: {error_position}")
        encoded[error_position - 1] ^= 1 
        print("Error corrected.")
    else:
        print("No error detected.")

    parity_positions_set = set(parity_positions)
    decoded = [encoded[i] for i in range(n) if i not in parity_positions_set]

    return ''.join(map(str, decoded)), ''.join(map(str, encoded))


def main():
    """Main function to interact with the user."""
    while True:
        print("\n--- Hamming Code Generator and Corrector ---")
        print("1. Generate Hamming Code")
        print("2. Correct Hamming Code")
        print("3. Exit")

        def case_generate_hamming():
            data = input("Enter the binary data (e.g., 1011): ")
            if not all(c in '01' for c in data):
                print("Invalid input! Please enter binary data only.")
                return
            hamming_code = generate_hamming_code(data)
            print(f"Hamming Code: {hamming_code}")

        def case_correct_hamming():
            encoded = input("Enter the received Hamming code: ")
            if not all(c in '01' for c in encoded):
                print("Invalid input! Please enter binary data only.")
                return
            decoded_data, corrected_code = correct_hamming_code(encoded)
            print(f"Corrected Code: {corrected_code}")
            print(f"Decoded Data: {decoded_data}")

        def case_exit():
            print("Exiting...")
            exit(0)

        switch_case = {
            '1': case_generate_hamming,
            '2': case_correct_hamming,
            '3': case_exit
        }

        choice = input("Enter your choice (1, 2, or 3): ").strip()
        switch_case.get(choice, lambda: print("Invalid choice! Please try again."))()


if __name__ == "__main__":
    main()


'''

SelectiveRepeat='''
import time
import random
class SelectiveRepeat:
    def __init__(self, window_size, total_frames):
        self.window_size = window_size
        self.total_frames = total_frames
        self.sent_frames = [None] * total_frames
        self.ack_received = [False] * total_frames
        self.current_frame = 0
    def send_frame(self, frame_num):
        if self.sent_frames[frame_num] is None:
            print(f"Sending frame {frame_num}")
            self.sent_frames[frame_num] = True
            time.sleep(1)
    def receive_ack(self, frame_num):
        ack = random.choice([True, False])
        if ack:
            print(f"ACK received for frame {frame_num}")
            self.ack_received[frame_num] = True
        else:
            print(f"NACK for frame {frame_num}")
    def send_frames(self):
        while not all(self.ack_received):
            for i in range(self.window_size):
                frame_num = (self.current_frame + i) % self.total_frames
                if not self.ack_received[frame_num]:
                    self.send_frame(frame_num)
            for i in range(self.window_size):
                frame_num = (self.current_frame + i) % self.total_frames
                if not self.ack_received[frame_num]:
                    self.receive_ack(frame_num)
            self.current_frame = (self.current_frame + 1) % self.total_frames
sr = SelectiveRepeat(window_size=4, total_frames=10)
sr.send_frames()
'''

GoBack='''
import time
import random

class GoBackN:
    def __init__(self, window_size, total_frames):
        self.window_size = window_size
        self.total_frames = total_frames
        self.sent_frames = 0
        self.ack_received = 0 
    def send_frames(self):
        while self.ack_received < self.total_frames:
            for i in range(self.window_size):
                if self.sent_frames < self.total_frames:
                    print(f"Sending frame {self.sent_frames}")
                    self.sent_frames += 1
                    time.sleep(1)
            for i in range(self.window_size):
                if self.ack_received < self.total_frames:
                    ack = random.choice([True, False])
                    if ack:
                        print(f"ACK received for frame {self.ack_received}")
                        self.ack_received += 1
                    else:
                        print(f"Frame {self.ack_received} lost, resending from this frame")
                        self.sent_frames = self.ack_received
                        break
gbn = GoBackN(window_size=4, total_frames=10)
gbn.send_frames()
'''

StopandWait='''
import time
import random

class StopAndWait:
    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.sent_frames = [None] * total_frames
        self.ack_received = [False] * total_frames
        self.current_frame = 0

    def send_frame(self, frame_num):
        if self.sent_frames[frame_num] is None:
            print(f"Sending frame {frame_num}")
            self.sent_frames[frame_num] = True
            time.sleep(1)

    def receive_ack(self, frame_num):
        ack = random.choice([True, False])
        if ack:
            print(f"ACK received for frame {frame_num}")
            self.ack_received[frame_num] = True
        else:
            print(f"NACK for frame {frame_num}")

    def send_frames(self):
        while not all(self.ack_received):
            frame_num = self.current_frame
            if not self.ack_received[frame_num]:
                self.send_frame(frame_num)
                self.receive_ack(frame_num)
                if self.ack_received[frame_num]:
                    self.current_frame += 1
            time.sleep(1) 
sw = StopAndWait(total_frames=10)
sw.send_frames()
'''

SubnetMask='''
def get_ip_class_and_subnet(ip):
    octets = ip.split('.')
    
    if len(octets) != 4:
        return 'Invalid IP address', 'N/A'

    try:
        octets = [int(octet) for octet in octets]
        
        if any(octet < 0 or octet > 255 for octet in octets):
            return 'Invalid IP address', 'N/A'
        
        first_octet = octets[0]

        if first_octet >= 1 and first_octet <= 127:
            ip_class = 'Class A'
            subnet_mask = '255.0.0.0'
        elif first_octet >= 128 and first_octet <= 191:
            ip_class = 'Class B'
            subnet_mask = '255.255.0.0'
        elif first_octet >= 192 and first_octet <= 223:
            ip_class = 'Class C'
            subnet_mask = '255.255.255.0'
        elif first_octet >= 224 and first_octet <= 239:
            ip_class = 'Class D (Multicast)'
            subnet_mask = 'N/A'
        elif first_octet >= 240 and first_octet <= 255:
            ip_class = 'Class E (Reserved)'
            subnet_mask = 'N/A'
        else:
            ip_class = 'Unknown'
            subnet_mask = 'N/A'
        
        return ip_class, subnet_mask

    except ValueError:
        return 'Invalid IP address', 'N/A'


ip_address = input("Enter an IP address: ")
ip_class, subnet_mask = get_ip_class_and_subnet(ip_address)
print(f"IP Address: {ip_address}")
print(f"Class: {ip_class}")
print(f"Subnet Mask: {subnet_mask}")
'''

BellmanFord='''

def bellman_ford(graph, start):
    
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0  

    
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    
    for u in graph:
        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                print("Graph contains negative weight cycle")
                return None

    return distances



graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('D', 3)],
    'D': [('A', -1)]
}

start = 'A'
shortest_paths = bellman_ford(graph, start)
if shortest_paths:
    print(f"Shortest paths from {start}: {shortest_paths}")
'''

Dijikstra='''
import heapq

def dijkstra(graph, start):
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]  

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('D', 3)],
    'D': [('A', -1)]  
}

start = 'A'
shortest_paths = dijkstra(graph, start)
print(f"Shortest paths from {start}: {shortest_paths}")
'''

LeakyBucket='''
class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity  
        self.leak_rate = leak_rate  
        self.water = 0  

    def add(self, packets):
        
        if self.water + packets > self.capacity:
            print(f"Overflow: Discarding {packets} packets.")
            self.water = self.capacity  
        else:
            self.water += packets
            print(f"Added {packets} packets. Current water level: {self.water}")

    def leak(self, time):
        
        leaked = min(self.water, self.leak_rate * time)
        self.water -= leaked
        print(f"Leaked {leaked} packets. Current water level: {self.water}")


bucket = LeakyBucket(10, 2)
bucket.add(5)
bucket.add(6)
bucket.leak(3)
'''

TokenBucket='''
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity  
        self.refill_rate = refill_rate  
        self.tokens = 0  
        self.last_refill_time = 0

    def add_tokens(self, time):
        
        self.tokens = min(self.capacity, self.tokens + self.refill_rate * time)
        print(f"Tokens added. Current token count: {self.tokens}")

    def consume_token(self):
        if self.tokens > 0:
            self.tokens -= 1
            print("Token consumed. Packet sent.")
        else:
            print("No tokens available. Packet delayed.")


bucket = TokenBucket(10, 1)  
bucket.add_tokens(5)  
bucket.consume_token()  
bucket.add_tokens(5)  
'''

cn_exp = {
    'BitStuffing.py': BitStuffing,
    'ByteStuffing.py': ByteStuffing,
    'CharacterCount.py': CharacterCount,
    'CyclicRedundancyCheck.py': CyclicRedundancyCheck,
    'HammingCode.py': HammingCode,
    'SelectiveRepeat.py': SelectiveRepeat,
    'GoBack.py': GoBack,
    'StopandWait.py': StopandWait,
    'SubnetMask.py': SubnetMask,
    'BellmanFord.py': BellmanFord,
    'Dijikstra.py': Dijikstra,
    'LeakyBucket.py': LeakyBucket,
    'TokenBucket.py': TokenBucket
}

def cn_():
    for filename, content in cn_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(cn_exp[exp])