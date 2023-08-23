import socket
import threading
import time
import random
import struct
import numpy as np

class Jammer:
    def __init__(self):
        self.jamming_patterns_detected = 0

    def jammer(self):
        # start at 5 seconds
        jamming_start = 5
        # set duration to 15
        jamming_duration = 30
        # set interval to 0.2 seconds
        jamming_interval = 0.5
        # set chunk size to 350 bytes at a time
        chunk_size = 350
        
        # parameters to generate jamming signal
        num_bursts = int(jamming_duration / jamming_interval)
        burst_duration = 0.03 
        max_frequency = 315000000
        min_amplitude = 0.2 
        max_amplitude = 0.6
        
        multicast_group = "224.0.0.1"
        multicast_port = 5001
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
        time.sleep(jamming_start)
        
        while True:
            # RKE jamming frequency in Hz
            jamming_frequency = 315000000
            jamming_amplitude = random.uniform(min_amplitude, max_amplitude)
            
            jamming_signal = generate_jamming_signal(
                burst_duration, jamming_frequency, jamming_amplitude
            )
            
            # Split signal into smaller chunks
            for i in range(0, len(jamming_signal), chunk_size):
                chunk = jamming_signal[i:i + chunk_size]
                chunk_str = " ".join(map(str, chunk))
                sock.sendto(chunk_str.encode(), (multicast_group, multicast_port))
                time.sleep(jamming_interval)
                
                # Increment the jamming pattern detected counter
                self.jamming_patterns_detected += 1

    def get_jamming_patterns_detected(self):
        return self.jamming_patterns_detected

def generate_jamming_signal(duration, frequency, amplitude):
    # sampling rate
    sampling_rate = 31100
    # number of samples per second
    num_samples = int(duration * sampling_rate)
    
    t = np.linspace(0, duration, num_samples)
    jamming_signal = amplitude * np.sin(2 * np.pi * frequency * t)
    
    return jamming_signal

if __name__ == "__main__":
    jammer_module = Jammer()

    jammer_thread = threading.Thread(target=jammer_module.jammer)
    jammer_thread.start()

    jammer_thread.join()
