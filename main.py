from threading import Thread
from Bus import BusStop, Bus
from Passenger import Passenger

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
