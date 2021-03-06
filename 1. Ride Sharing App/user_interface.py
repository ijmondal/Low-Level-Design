from enum import Enum

'''
single-user, single_ride
A interface is to be built between user and functionalities of the rider class.
'''


class RideStatus(Enum):
    IDLE = 1
    CREATED = 2
    WITHDRAWN = 3
    COMPLETED = 4


class System:
    def __init__(self, drivers=None, riders=list()) -> None:
        if drivers < 2 or len(riders) < 2:
            print("Not enough drivers or riders")

        self.__drivers = drivers
        self.__riders = riders

    def createRide(self, riderId, rideId, origin, dest, seats):
        if self.__drivers == 0:
            print("Not enough drivers; can't create ride")
            return

        for rider in self.__riders:
            if rider.getId() == riderId:
                rider.createRide(rideId, origin, dest, seats)
                self.__drivers -= 1
                return

    def updateRide(self, riderId, rideId, origin, dest, seats):

        for rider in self.__riders:
            if rider.getId() == riderId:
                rider.updateRide(rideId, origin, dest, seats)
                return

    def withdrawRide(self, riderId, rideId):

        for rider in self.__riders:
            if rider.getId() == riderId:
                rider.withdrawRide(rideId)
                self.__drivers -= 1
                return

    def closeRide(self, riderId):
        for rider in self.__riders:
            if rider.getId() == riderId:
                self.__drivers -= 1
                return rider.closeRide()

        print("ride could not be closed.")
        return 0


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
    def __init__(self, id, name):
        super().__init__(name)
        self.__currentRide = Ride()
        self.__completedRides = []
        self.__id = id

    def getId(self):
        return self.__id

    def createRide(self, id, origin, dest, seats):
        if origin >= dest:
            print("origin > dest; invalid can't create a ride")
        self.__currentRide.id = id
        self.__currentRide.origin = origin
        self.__currentRide.dest = dest
        self.__currentRide.No_of_seats = seats
        self.__currentRide.rideStatus = RideStatus.CREATED

    def updateRide(self, id, origin, dest, seats):
        if self.__currentRide.rideStatus == RideStatus.WITHDRAWN:
            print("ride already withdrawn, can't update ride")
        elif self.__currentRide.rideStatus == RideStatus.COMPLETED:
            print("ride already completed, can't update ride")
        else:
            # if upadte ride is called when ridestatus is IDLE; it will create a new ride.
            self.createRide(id, origin, dest, seats)

    def withdrawRide(self, id):
        if self.__currentRide.id != id:
            print("wrong ID as input. Cannot withdraw ride")
            return
        if self.__currentRide.rideStatus == RideStatus.IDLE:
            print("ride doesn't exist. Cannot withdraw ride")
            return
        elif self.__currentRide.rideStatus == RideStatus.COMPLETED:
            print("ride already completed. Cannot withdraw")
            return
        self.__currentRide.rideStatus = RideStatus.WITHDRAWN

    def closeRide(self):
        if self.__currentRide.rideStatus != RideStatus.CREATED:
            print("ride wasn't in progress. Invalid")
            return 0
        self.__currentRide.rideStatus = RideStatus.COMPLETED
        self.__completedRides.append(self.__currentRide)
        return self.__currentRide.calculateFare(len(self.__completedRides) >= 10)


# property decorators can be used to implement getters and setters
a = Rider(1, "Ram")
b = Driver("Shyam")
c = Rider(2, "Laxman")
d = Rider(3, "Sita")
L = [a, c, d]
s = System(3, L)
s.createRide(1, 1, 10, 20, 1)
s.createRide(2, 2, 10, 20, 3)
s.createRide(3, 1, 10, 20, 4)
print(s.closeRide(1))
s.withdrawRide(1, 1)
print(s.closeRide(2))


# a.createRide(1, 10, 20, 1)
# a.updateRide(1, 10, 20, 3)
# print(a.closeRide())
# print(r.calculateFare(False))
