import threading
import random
from time import sleep


class BusStop:
    passengers_number: int
    index: int

    def __init__(self):
        self.passengers_number = 0
        self.index = 1


class Bus:
    positions = ("arriving", "stop", "departed", "based")
    position: str
    line: int
    passengers: int
    ticket_inspector: bool
    check: float

    def __init__(self):
        self.position = self.positions[3]
        self.full = False
        self.passengers = 0
        self._lock = threading.Lock()
        self.ticket_inspector = False
        self.line = random.randint(1, 3)
        self.check = random.random()

    def drive(self, active_bus_stop: BusStop):
        print(self.check)
        print(f"Bus line {self.line} arriving")
        self.position = self.positions[0]
        if self.check > 0.1:
            print("Ticket inspector is coming!")
            self.ticket_inspector = True

        sleep(10)

        if active_bus_stop.passengers_number != 0 and not self.full:
            self.position = self.positions[1]
            while active_bus_stop.passengers_number > 0:
                print("Waiting for all passengers boarded")
                sleep(10)

        print(f"passenger number: {self.passengers}")
        print("Bus departing...")
        self.position = self.positions[2]
