from enum import Enum


class RideStatus(Enum):
    IDLE = 1
    CREATED = 2
    WITHDRAWN = 3
    COMPLETED = 4


class Ride:

    AMT_PER_KM = 20

    def __init__(self, id=None, origin=None, dest=None, No_of_seats=None):
        self.id = id
        self.origin = origin
        self.dest = dest
        self.No_of_seats = No_of_seats
        self.rideStatus = RideStatus.IDLE

# isPriority - BONUS
    def calculateFare(self, isPriority):
        dist = self.dest-self.origin
        if self.No_of_seats < 2:
            return dist*self.AMT_PER_KM*(0.75 if isPriority else 1)
        else:
            return dist*self.No_of_seats*self.AMT_PER_KM*(0.5 if isPriority else 1)


class Person:
    '''
    This was created for name inheritance because driver and rider will also have name
    '''

    def __init__(self, name):
        self.name = name


class Driver(Person):
    def __init__(self, name):
        super().__init__(name)


class Rider(Person):
    def __init__(self, name):
        super().__init__(name)

        self.__allRides = []

    def createRide(self, id, origin, dest, seats):
        if origin >= dest:
            print("origin > dest; invalid can't create a ride")
        currentRide = Ride()
        currentRide.id = id
        currentRide.origin = origin
        currentRide.dest = dest
        currentRide.No_of_seats = seats
        currentRide.rideStatus = RideStatus.CREATED
        self.__allRides.append(currentRide)

    def updateRide(self, id, origin, dest, seats):
        for ride in reversed(self.__allRides):
            if ride.id == id:
                break

        if ride.rideStatus != RideStatus.CREATED:
            print("Ride wasn't in progress. Can't update ride")
            return

        # found the ride to be updated - UPDATING....
        ride.origin = origin
        ride.dest = dest
        ride.No_of_seats = seats

    def withdrawRide(self, id):
        for ride in reversed(self.__allRides):
            if ride.id == id:
                break

        if ride.rideStatus != RideStatus.CREATED:
            print("Ride wasn't in progress. Can't withdraw ride")
            return

        # found the ride to be updated - WITHDRAWING....
        ride.rideStatus = RideStatus.WITHDRAWN

        # here we can also remove the withdrawn ride from the allRides list

        self.__allRides.remove(ride)

    def closeRide(self, id):
        for ride in reversed(self.__allRides):
            if ride.id == id:
                break

        if ride.rideStatus != RideStatus.CREATED:
            print("Ride wasn't in progress. Can't close ride")
            return

        # found the ride to be updated - CLOSING....
        ride.rideStatus = RideStatus.COMPLETED

        return ride.calculateFare(len(self.__allRides) >= 10)


# property decorators can be used to implement getters and setters
a = Rider("Ram")
b = Driver("Shyam")
a.createRide(1, 10, 20, 1)
a.createRide(2, 10, 20, 3)
# a.withdrawRide(1)
print(a.closeRide(2))
# print(r.calculateFare(False))
