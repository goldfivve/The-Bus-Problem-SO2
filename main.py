import logging
from threading import Thread
import time
from time import sleep

from duplicity.asyncscheduler import threading


class BusStop:
    indexes = [1, 2, 3]
    riders_number: int
    index: int

    def __init__(self):
        self.riders_number = 0
        self.index = 1

    def update(self):
        self.riders_number += 1


class Bus:
    positions = ["arriving", "stop", "departed"]
    position: str
    full: bool
    bus_stop: BusStop
    riders: int

    def __init__(self, position, full, bus_stop: BusStop):
        self.position = position
        self.full = full
        self.bus_stop = bus_stop
        self._lock = threading.Lock()

    def drive(self, bus_stop: BusStop):
        print("Bus arriving")
        sleep(5)
        if bus_stop.riders_number == 0:
            self.position = self.positions[2]
        elif bus_stop.riders_number is not 0:
            self.position = self.position[1]

        with self._lock:
            if self.riders == BusStop.riders_number:
                self.position = self.positions[2]


class Rider:
    on_bus_stop: bool
    bus_ticket: bool
    inside: bool
    name: int

    def __init__(self):
        self.on_bus_stop = False
        self.bus_ticket = True
        self.inside = False
        self._lock = threading.Lock()

    def arrive_bus_stop(self, bus: Bus):
        if not self.on_bus_stop:
            logging.info("Thread %d: arriving bus stop", self.name)
            self._lock.acquire()
            time.sleep(2)
            self.on_bus_stop = True
            if self.bus_ticket is True:
                BusStop.riders_number += 1
            self._lock.release()
            logging.info("Thread %d: arrived bus stop", self.name)

        if bus.position is "arriving" and self.on_bus_stop is True:
            print("Rider can board the bus")
            if bus.position is "stop":
                with self._lock:
                    if self.bus_ticket and bus.riders < 50:
                        bus.riders += 1
                        self.inside = True
                    # else:
                    # zakoncz watek


if __name__ == '__main__':
    print('PyCharm')
    rider_thread = Thread(target=Rider.arrive_bus_stop, args=(False, True, False))
    bus_thread = Thread(target=Bus.drive)

    rider_thread.join()
    bus_thread.join()
