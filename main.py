import concurrent.futures
import logging
from threading import Thread
import time
from time import sleep
from duplicity.asyncscheduler import threading


class BusStop:
    indexes = [1, 2, 3]
    passengers_number: int
    index: int

    def __init__(self):
        self.passengers_number = 0
        self.index = 1


class Bus:
    positions = ["arriving", "stop", "departed"]  # enum
    position: str
    full: bool
    passengers: int

    def __init__(self):
        self.position = self.positions[0]
        self.full = False
        self.passengers = 0
        self._lock = threading.Lock()

    def drive(self, active_bus_stop: BusStop):
        print("Bus arriving")
        sleep(5)
        if active_bus_stop.passengers_number != 0 and not self.full:
            self.position = self.positions[1]
            while active_bus_stop.passengers_number > 0:
                print("Waiting for all passengers boarded")

        print("Bus departing...")
        self.position = self.positions[2]


class Passenger:
    on_bus_stop: bool
    bus_ticket: bool
    inside: bool
    name: int
    first: int

    def __init__(self):
        self.on_bus_stop = False
        self.bus_ticket = True
        self.inside = False
        self.first = 0
        self._lock = threading.Lock()

    def arrive_bus_stop(self, active_bus: Bus, active_bus_stop: BusStop):
        if not self.on_bus_stop:
            logging.info("Passenger arriving bus stop")
            time.sleep(2)
            self.on_bus_stop = True
            logging.info("Passenger arrived bus stop")

        while not self.inside:
            if active_bus.position == active_bus.positions[0] and self.on_bus_stop:
                active_bus_stop.passengers_number += 1
                if self.first == 0:
                    print("Passenger can board the bus")
                    self.first = 1
                while not active_bus.position == active_bus.positions[1]:
                    print("Waiting for the bus to stop")
                print("Passenger boarding bus")
                if active_bus.passengers < 50:
                    with self._lock:
                        print("twoja stara")
                        active_bus.passengers += 1
                        active_bus_stop.passengers_number -= 1
                        self.inside = True
                        self.on_bus_stop = False
                        print("Passenger boarded")
                else:
                    print("Keep waiting")


if __name__ == '__main__':
    bus_stop = BusStop()
    bus = Bus()
    bus_thread = Thread(target=bus.drive, args=(bus_stop,))

    passengers = list()
    for index in range(51):
        passenger = Passenger()
        passenger_thread = Thread(target=passenger.arrive_bus_stop, args=(bus, bus_stop))
        passengers.append((passenger_thread, passenger))
        passenger_thread.start()

    for passenger in passengers:

        print("twoja stara to kopara a twuj stary jom odpala")
        if passenger[1].inside:
            passenger[0].join()

    bus_thread.start()

    bus_thread.join()
