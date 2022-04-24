from threading import Thread
import time
from time import sleep
from duplicity.asyncscheduler import threading
import random


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
            time.sleep(2)
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


if __name__ == '__main__':
    bus_stop = BusStop()
    bus = Bus()
    bus_thread = Thread(target=bus.drive, args=(bus_stop,))

    passengers = list()
    for index in range(55):
        passenger = Passenger()
        passenger_thread = Thread(target=passenger.arrive_bus_stop, args=(bus, bus_stop))
        passengers.append((passenger_thread, passenger))
        passenger_thread.start()

    for passenger in passengers:

        if passenger[1].inside:
            passenger[0].join()

    bus_thread.start()

    bus_thread.join()
