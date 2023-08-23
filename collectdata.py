import time
import random
import jammer
import receiver
import transmitter
import bruteforce
import interceptor

class Simulation:
    def __init__(self):
        self.successful_access = 0
        self.unsuccessful_access = 0
        self.replay_attacks_detected = 0
        self.jamming_patterns_detected = 0
        self.brute_force_lockouts = 0

    def simulate(self):
        jammer_module = jammer.Jammer()
        receiver_module = receiver.Receiver()
        transmitter_module = transmitter.Transmitter()
        brute_force_module = bruteforce.BruteForce()
        interceptor_module = interceptor.Interceptor()

        for _ in range(1):  # Simulate for 1800 seconds
            # Simulate jamming
            jammer_module.start_jamming()
            print('yess')

            # Simulate transmitter sending signals
            signal_sent = transmitter_module.transmit_signal()

            print('yesss')

            # Simulate receiver processing signals
            access_granted = receiver_module.process_received_signal(signal_sent)

            # Simulate replay attack
            replay_detected = interceptor_module.detect_replay(signal_sent)

            # Simulate brute force attack
            brute_force_detected = brute_force_module.detect_brute_force(signal_sent)

            if access_granted:
                self.successful_access += 1
            else:
                self.unsuccessful_access += 1

            if replay_detected:
                self.replay_attacks_detected += 1

            if jammer_module.is_jamming_detected():
                self.jamming_patterns_detected += 1

            if brute_force_detected:
                self.brute_force_lockouts += 1
                time.sleep(300)  # Lockout duration

            time.sleep(1)  # Simulate 1 second time interval

    def get_simulation_results(self):
        return {
            "Successful Access": self.successful_access,
            "Unsuccessful Access": self.unsuccessful_access,
            "Replay Attacks Detected": self.replay_attacks_detected,
            "Jamming Patterns Detected": self.jamming_patterns_detected,
            "Brute Force Lockouts": self.brute_force_lockouts
        }

if __name__ == "__main__":
    simulation = Simulation()
    simulation.simulate()
    results = simulation.get_simulation_results()
    for metric, value in results.items():
        print(f"{metric}: {value}")
