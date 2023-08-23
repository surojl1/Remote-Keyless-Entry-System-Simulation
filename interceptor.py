import socket
import struct
import sys
import time

class Interceptor:
    def __init__(self):
        self.buffer = []

    def intercept(self):
        multicast_group = "224.0.0.1"
        multicast_port = 5000

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', multicast_port))

        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            try:
                data, address = sock.recvfrom(1024)
                self.savetomemory(str(data.decode()))
                print(f"Received message: {data.decode()} from {address}")

            except KeyboardInterrupt:
                print("Interceptor stopped by the user.")
                break

            except Exception as e:
                print("Error: ", e)

        sock.close()

    def replay(self):
        with open('memory.dat', 'r') as file:
            replay_data = file.readline()
            self.unlock(replay_data)

    def unlock(self, recorded_packet):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        try:
            receiver_ip = '224.0.0.1'
            port = 5001

            while True:
                time.sleep(2)
                sock.sendto(recorded_packet.encode(), (receiver_ip, port))
                print("Replay Message sent.")

        except Exception as e:
            print("Error: ", e)
        finally:
            sock.close()

    def savetomemory(self, data):
        with open('memory.dat', 'w') as file:
            file.write(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    mode = sys.argv[1]
    interceptor_replayer = Interceptor()

    if mode == "capture":
        interceptor_replayer.intercept()
    elif mode == 'replay':
        interceptor_replayer.replay()
    else:
        print('Unknown mode!!!')
