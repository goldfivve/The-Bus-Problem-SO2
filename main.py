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
    positions = ["arriving", "stop", "departed"]
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
            while self.passengers != active_bus_stop.passengers_number:
                print("Waiting for all passengers boarded")
                sleep(5)

        print("Bus departing...")
        self.position = self.positions[2]


class Passenger:
    on_bus_stop: bool
    bus_ticket: bool
    inside: bool
    name: int

    def __init__(self):
        self.on_bus_stop = False
        self.bus_ticket = True
        self.inside = False
        self._lock = threading.Lock()

    def arrive_bus_stop(self, active_bus: Bus, active_bus_stop: BusStop):
        if not self.on_bus_stop:
            logging.info("Passenger arriving bus stop")
            time.sleep(2)
            self.on_bus_stop = True
            if self.bus_ticket is True:
                active_bus_stop.passengers_number += 1
            logging.info("Passenger arrived bus stop")

        while not self.inside:
            if active_bus.position == "arriving" and self.on_bus_stop:
                print("Passenger can board the bus")
                while not active_bus.positions[1]:
                    print("Waiting for the bus to stop")
                if active_bus.position == "stop":
                    print("Passenger boarding bus")
                    if self.bus_ticket and active_bus.passengers < 50:
                        active_bus.passengers += 1
                        self.inside = True
                        print("Passenger boarded")
                    else:
                        print("Keep waiting")


if __name__ == '__main__':
    print('PyCharm')
    bus_stop = BusStop()
    passenger = Passenger()
    bus = Bus()
    passenger_thread = Thread(target=passenger.arrive_bus_stop, args=(bus, bus_stop,))
    bus_thread = Thread(target=bus.drive, args=(bus_stop,))

    passenger_thread.start()
    bus_thread.start()

    passenger_thread.join()
    bus_thread.join()
