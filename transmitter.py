import socket
import struct
import datetime
import time
import hmac
import hashlib
import random

class Transmitter:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def generate_hash(self, current_key, seed_interval):
        current_epoch_time = int(time.time())
        seed_value = current_epoch_time // seed_interval
        combined_string = f"{current_key}_{seed_value}"
        hash_object = hashlib.sha256(combined_string.encode())
        hash_value = hash_object.hexdigest()
        rotated_hash = hash_value[-seed_interval:] + hash_value[:-seed_interval]
        return rotated_hash

    def random_delay(self):
        random_delay = random.uniform(0, 1)
        print(f"Introducing a random delay of {random_delay:.2f} seconds")
        time.sleep(random_delay)

    def transmit_message(self):
        try:
            receiver_1 = '224.0.0.1'
            port_1 = 5000

            receiver_2 = '224.0.0.1'
            port_2 = 5001

            while True:
                time.sleep(2)
                HASH_VALID_DURATION = 10
                KEY = "demokey"
                KEY = self.generate_hash(KEY, HASH_VALID_DURATION)

                sof = "0D"
                identifier = "A1D16B"
                date_time = str(hex(int(time.time())))

                message = ''
                message += sof
                message += identifier
                message += date_time

                self.random_delay()
                mac = str(hmac.new(key=KEY.encode(), msg=message.encode(), digestmod="sha1").hexdigest())

                message += mac

                self.sock.sendto(message.encode(), (receiver_1, port_1))
                self.sock.sendto(message.encode(), (receiver_2, port_2))
                print("Message sent.")

        except Exception as e:
            print("Error: ", e)
        finally:
            self.sock.close()

if __name__ == "__main__":
    transmitter_instance = Transmitter()
    transmitter_instance.transmit_message()
