import threading
import random
from time import sleep

from Bus import Bus, BusStop


class Passenger:
    on_bus_stop: bool
    bus_ticket: bool
    inside: bool
    name: int
    first: bool
    line: int
    cheat: float

    def __init__(self):
        self.on_bus_stop = False
        self.bus_ticket = False
        self.inside = False
        self.first = True
        self._lock = threading.Lock()
        self.line = random.randint(1, 3)
        self.cheat = random.random()

    def arrive_bus_stop(self, active_bus: Bus, active_bus_stop: BusStop):
        sleep(3)
        if not self.on_bus_stop:
            print(f"Passenger arriving bus stop for line {self.line}")
            sleep(2)
            self.on_bus_stop = True
            print("Passenger arrived bus stop")

        if self.cheat < 0.05:
            with self._lock:
                self.bus_ticket = True

        while active_bus.ticket_inspector and not self.bus_ticket:
            if self.first:
                print("Oops! Ticket inspector caught passenger red-handed... 280 pln 😎😩")
                self.first = False

        while not self.inside:
            if active_bus.position == active_bus.positions[0] and self.on_bus_stop and self.line == active_bus.line:
                active_bus_stop.passengers_number += 1
                if not self.first:
                    print("Passenger can board the bus")
                while not active_bus.position == active_bus.positions[1]:
                    if not self.first:
                        print("Waiting for the bus to stop")
                        self.first = True
                print("Passenger boarding bus")
                if active_bus.passengers < 50:
                    with self._lock:
                        active_bus.passengers += 1
                        active_bus_stop.passengers_number -= 1
                        self.inside = True
                        self.on_bus_stop = False
                        print("Passenger boarded")
                else:
                    print("Keep waiting")
                    active_bus_stop.passengers_number -= 1
