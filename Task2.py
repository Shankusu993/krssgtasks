class Elevator(object):
    # States:
    directions = ["up", "down", "idle"]

    # Dunder methods
    def __init__(self, floors, starting_floor):
        self.floors = floors
        self.location = starting_floor
        self.destination = starting_floor
        self.direction = self.directions[-1]

    def __repr__(self):
        # A fun representation of elevator location:   1   2   3   4   #   6   7   8   9   10
        return "\t".join(
            ["#" if floor == self.location else str(floor) for floor in self.floors]
        )


    def is_idle(self):
        # Used by controller to check if elevator is idle
        return self.direction == "idle"

    def distance(self, floor):
        # Calculates distance between self and floor
        return abs(floor - self.location)

    """

    Private methods used within class only

    """

    def _dispatch(self, floor):
        # Sets internal state on elevator
        if floor < self.location:
            desired_direction = "down"
        elif floor > self.location:
            desired_direction = "up"
        else:
            desired_direction = "idle"

        self.direction = desired_direction
        self.destination = floor
        

    def _arrived(self, floor):
        # Called after every stop is reached to stop the elevator there and show its status
        print(self.__repr__())
        self.direction = "idle"

        




####################################################################################################################
####################################################################################################################
####################################################################################################################
#        Controller Below
####################################################################################################################
####################################################################################################################
####################################################################################################################


class Controller(object):
    elevator = None

    # Dunder methods
    def __init__(self, num_floors=10, starting=4, up_press=[1,3,5,7], down_press=[3,2,9], panic_press=[6,8,9,10] ):
        self.floors = [i for i in range(1, num_floors + 1)]
        self.starting = starting
        self.up_press = up_press
        self.down_press = down_press
        self.panic_press = panic_press        
        self.top_destination =    max([max(self.up_press),max(self.down_press),max(self.panic_press)])
        self.bot_destination =    min([min(self.up_press),min(self.down_press),min(self.panic_press)])
        Controller.elevator = Elevator(self.floors, self.starting)




  
    def find_follow_best_route(self):
        print(Controller.elevator)
        if Controller.elevator.location < self.bot_destination:
            for n in range(self.starting, self.top_destination+1):
                if n in self.up_press or n in self.panic_press:
                    Controller.elevator._dispatch(n)
                    Controller.elevator.location = n
                    Controller.elevator._arrived(n)        
            for k in range(max(self.down_press), min(self.down_press)-1,-1):
                if k in self.down_press:
                    Controller.elevator._dispatch(k)
                    Controller.elevator.location = k
                    Controller.elevator._arrived(k)

        elif Controller.elevator.location > self.top_destination:
            for n in range(self.starting, self.bot_destination-1,-1):
                if n in self.down_press or n in self.panic_press:
                    Controller.elevator._dispatch(n)
                    Controller.elevator.location = n
                    Controller.elevator._arrived(n)        
            for k in range(min(self.up_press), max(self.up_press)+1  ):
                if k in self.up_press:
                    Controller.elevator._dispatch(k)
                    Controller.elevator.location = k
                    Controller.elevator._arrived(k)

        elif Controller.elevator.distance(self.bot_destination) <= Controller.elevator.distance(self.top_destination):
            for n in range(self.starting, self.bot_destination-1, -1):
                if n in self.down_press or n in self.panic_press:
                    Controller.elevator._dispatch(n)
                    Controller.elevator.location = n
                    Controller.elevator._arrived(n)
                    if n in self.panic_press:
                        self.panic_press.remove(n)
                    if n in self.down_press:
                        self.down_press.remove(n)  
            if min(self.up_press) < Controller.elevator.location:
                for n in range(min(self.up_press), self.top_destination+1):
                    if n in self.up_press or n in self.panic_press:
                        Controller.elevator._dispatch(n)
                        Controller.elevator.location = n
                        Controller.elevator._arrived(n)
            elif min(self.up_press) >= Controller.elevator.location:
                for n in range(Controller.elevator.location , self.top_destination+1):
                    if n in self.up_press or n in self.panic_press:
                        Controller.elevator._dispatch(n)
                        Controller.elevator.location = n
                        Controller.elevator._arrived(n)

            for k in self.down_press[::-1]:
                    Controller.elevator._dispatch(k)
                    Controller.elevator.location = k
                    Controller.elevator._arrived(k)

        elif Controller.elevator.distance(self.bot_destination) > Controller.elevator.distance(self.top_destination):
            for n in range(self.starting, self.top_destination+1):
                if n in self.up_press or n in self.panic_press:
                    Controller.elevator._dispatch(n)
                    Controller.elevator.location = n
                    Controller.elevator._arrived(n)
                    if n in self.panic_press:
                        self.panic_press.remove(n)
                    if n in self.up_press:
                        self.up_press.remove(n)  
            if max(self.down_press) > Controller.elevator.location:
                for n in range(max(self.down_press), self.bot_destination-1,-1):
                    if n in self.down_press or n in self.panic_press:
                        Controller.elevator._dispatch(n)
                        Controller.elevator.location = n
                        Controller.elevator._arrived(n)
            elif max(self.down_press) <= Controller.elevator.location:
                for n in range(Controller.elevator.location , self.bot_destination-1,-1):
                    if n in self.down_press or n in self.panic_press:
                        Controller.elevator._dispatch(n)
                        Controller.elevator.location = n
                        Controller.elevator._arrived(n)

            for k in self.up_press:
                    Controller.elevator._dispatch(k)
                    Controller.elevator.location = k
                    Controller.elevator._arrived(k)





