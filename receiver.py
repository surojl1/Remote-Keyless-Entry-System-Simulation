import socket
import struct
import hmac
import time
import numpy as np
import hashlib
import random

MAX_FAILED_ATTEMPTS = 5
MAX_WRONG_MAC_ATTEMPTS = 3
TIMESTAMP_THRESHOLD = 5

# lockout duration in seconds
LOCKOUT_DURATION = 300 

# lockout status
is_locked_out = False

# lockout start time
lockout_start_time = 0

# Dictionary to store wrong MAC attempt counts
wrong_signal_attempt = []

# Parameters for jamming pattern detection
JAMMING_PATTERN_THRESHOLD = 1000

# Number of channels available
# for frequency hopping
NUM_CHANNELS = 10

# generate channel to start with
current_channel = random.randint(0, NUM_CHANNELS - 1)

class Receiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        multicast_group = "224.0.0.1"
        multicast_port = 5001
        self.sock.bind(('', multicast_port))
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def lockout_vehicle(self):
        global is_locked_out, lockout_start_time
        if not is_locked_out:
            print("Locking out receiver due to brute force attack.")
            is_locked_out = True
            lockout_start_time = time.time()
        if is_locked_out and time.time() - lockout_start_time >= LOCKOUT_DURATION:
            print("Lockout period has ended. Receiver is now unlocked.")
            is_locked_out = False
            lockout_start_time = 0

    def receive(self):
        global is_locked_out, lockout_start_time
        while True:
            try:
                unlock = True
                data, address = self.sock.recvfrom(1024)
                print(f"Received message: {data.decode()} from {address}")
                
                if self.detect_jamming_pattern(data.decode()):
                    print("Jamming pattern detected!!!")
                    unlock = False
                    continue
                if self.validate_code(data.decode()):
                    unlock = True
                else:
                    unlock = False
                if self.detect_brute_force(data.decode()):
                    print("Brute force attack detected!!!")
                    unlock = False
                if self.detect_replay_attack(data.decode()):
                    print("Replay attack detected!!!")
                    unlock = False
                if is_locked_out == True:
                    print('Vehicle locked due to brute force attack!!')
                    if time.time() - lockout_start_time >= LOCKOUT_DURATION:
                        print("Lockout period has ended. Receiver is now unlocked.")
                        is_locked_out = False
                        lockout_start_time = 0
                if unlock == True and is_locked_out == False:
                    self.unlock_door()
                    wrong_signal_attempt.clear()
                self.random_delay()
            except KeyboardInterrupt:
                print("Receiver stopped by the user.")
                break
            except Exception as e:
                print("Error: ", e)
        self.sock.close()

    def detect_brute_force(self, received_packet):
        if self.validate_code(received_packet) == False:
            wrong_signal_attempt.append(received_packet)
            if len(wrong_signal_attempt) >= MAX_FAILED_ATTEMPTS:
                self.lockout_vehicle()
                return "Brute force attack detected!!"

    def detect_replay_attack(self, received_packet):
        timestamp = self.extract_timestamp(received_packet)
        current_timestamp = int(time.time())
        received_timestamp = int(timestamp, 16)
        if abs(current_timestamp - received_timestamp) > TIMESTAMP_THRESHOLD or received_timestamp > current_timestamp:
            return "Replay attack detected!!!"

    def detect_jamming_pattern(self, received_packet):
        jamming_signal = self.extract_jamming_signal(received_packet)
        jamming_energy = np.sum(np.square(jamming_signal))
        if jamming_energy > JAMMING_PATTERN_THRESHOLD:
            self.switch_channel()
            return True

    def extract_timestamp(self, received_packet):
        return received_packet[8:18]

    def extract_jamming_signal(self, received_packet):
        jamming_signal_str = received_packet[50:]
        try:
            jamming_signal = np.array(list(map(float, jamming_signal_str.split())))
        except:
            jamming_signal = np.linspace(0, 0, 0)
        return jamming_signal

    def validate_code(self, received_packet):
        if received_packet[0] == '0' and \
           received_packet[1] == 'D' and \
           received_packet[2] == 'A' and \
           received_packet[3] == '1' and \
           received_packet[4] == 'D' and \
           received_packet[5] == '1' and \
           received_packet[6] == '6' and \
           received_packet[7] == 'B':
           received_mac = received_packet[-40:]
           message_without_mac = received_packet[:-40]
           KEY = "demokey"
           HASH_VALID_DURATION = 10
           KEY = self.get_hash(KEY, HASH_VALID_DURATION)
           expected_mac = hmac.new(key=KEY.encode(), msg=message_without_mac.encode(), digestmod="sha1").hexdigest()
           if received_mac == expected_mac:
             return True
           else:
                print("MAC validation failed.")
                return False
        else:
            return False

    def get_hash(self, current_key, seed_interval):
        current_epoch_time = int(time.time())
        seed_value = current_epoch_time // seed_interval
        combined_string = f"{current_key}_{seed_value}"
        hash_object = hashlib.sha256(combined_string.encode())
        hash_value = hash_object.hexdigest()
        rotated_hash = hash_value[-seed_interval:] + hash_value[:-seed_interval]
        return rotated_hash

    def switch_channel(self):
        global current_channel
        current_channel = (current_channel + 1) % NUM_CHANNELS
        print(f"Hopped to channel {current_channel}")

    def random_delay(self):
        random_delay = random.uniform(0, 1)
        print(f"Introducing a random delay of {random_delay:.2f} seconds")
        time.sleep(random_delay)

    def unlock_door(self):
        print('Door unlocked!!')

if __name__ == "__main__":
    receiver_instance = Receiver()
    receiver_instance.receive()
