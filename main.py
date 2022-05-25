import random
import threading
import time
from threading import Thread
from time import sleep

import pygame as pygame


class SlideShow:
    photo_number: int
    BOARDING = pygame.transform.scale(pygame.image.load("pictures/bus_boarding.png"), (800, 600))
    DRIVER = pygame.transform.scale(pygame.image.load("pictures/bus_driver.png"), (800, 600))
    DRIVING = pygame.transform.scale(pygame.image.load("pictures/bus_driving.png"), (800, 600))
    STOP = pygame.transform.scale(pygame.image.load("pictures/bus_stop.png"), (800, 600))
    NO_TICKET = pygame.transform.scale(pygame.image.load("pictures/no_ticket.png"), (800, 600))
    INSPECTION = pygame.transform.scale(pygame.image.load("pictures/ticket_inspection.png"), (800, 600))

    WINDOW = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("the bus problem")

    current_image = DRIVING

    pictures_dictionary = {"boarding": BOARDING,
                           "driver": DRIVER,
                           "driving": DRIVING,
                           "stop": STOP,
                           "no_ticket": NO_TICKET,
                           "inspection": INSPECTION}

    def change_picture(self, key: str):
        self.current_image = self.pictures_dictionary[key]

    def draw(self):
        while True:
            self.WINDOW.blit(self.current_image, (0, 0))
            pygame.display.update()
            time.sleep(0.01)

    def give_honey(self):
        bus_stop = BusStop()
        bus = Bus()
        bus_thread = Thread(target=bus.drive, args=(bus_stop, slide_show))

        passengers = list()
        for index in range(55):
            passenger = Passenger()
            passenger_thread = Thread(target=passenger.arrive_bus_stop, args=(bus, bus_stop, slide_show))
            passengers.append((passenger_thread, passenger))
            passenger_thread.start()

        for passenger in passengers:
            if passenger[1].inside:
                passenger[0].join()

        bus_thread.start()

        bus_thread.join()


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
        if random.random() > 0.1:
            self.ticket_inspector = True
        else:
            self.ticket_inspector = False
        self.line = random.randint(1, 3)

    def drive(self, active_bus_stop: BusStop, slide: SlideShow):
        print(f"Bus line {self.line} arriving")
        slide.change_picture("driving")
        self.position = self.positions[0]
        if self.ticket_inspector > 0.1:
            with self._lock:
                print("Ticket inspector is coming!")
                slide.change_picture("inspection")
                sleep(1)

        if active_bus_stop.passengers_number != 0 and not self.full:
            self.position = self.positions[1]
            while active_bus_stop.passengers_number > 0:
                print("Waiting for all passengers boarded")
                with self._lock:
                    slide.change_picture("boarding")
                    sleep(2)

        print(f"passenger number: {self.passengers}")
        print("Bus departing...")
        with self._lock:
            slide.change_picture("driver")
            sleep(2)
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

    def arrive_bus_stop(self, active_bus: Bus, active_bus_stop: BusStop, slide: SlideShow):
        sleep(3)
        if not self.on_bus_stop:
            print(f"Passenger arriving bus stop for line {self.line}")
            sleep(2)
            self.on_bus_stop = True
            print("Passenger arrived bus stop")
            with self._lock:
                slide.change_picture("stop")
                sleep(5)

        if self.cheat < 0.05:
            with self._lock:
                self.bus_ticket = True

        while self.line != active_bus.line:
            sleep(1)

        while active_bus.ticket_inspector and not self.bus_ticket:
            if self.first:
                with self._lock:
                    slide.change_picture("no_ticket")
                    print("Oops! Ticket inspector caught passenger red-handed... 280 pln 😎😩")
                    sleep(5)
                self.first = False

        while not self.inside:
            if active_bus.position == active_bus.positions[0] and self.on_bus_stop:
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


slide_show = SlideShow()

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("myculture.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(9999999)
    thread_draw = Thread(target=slide_show.draw)
    thread_honey = Thread(target=slide_show.give_honey)
    thread_draw.start()
    thread_honey.start()
