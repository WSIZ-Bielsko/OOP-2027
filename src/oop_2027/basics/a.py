from random import randint
from time import sleep


class Car:
    # attributes / fields
    name: str
    serial_number: int     # declaration

    # constructor
    def __init__(self, name):
        self.name = name
        self.serial_number = randint(1000, 9999)
        print(f"Car {self.name} is being created")

    # methods
    def __repr__(self):
        return f"Car {self.name}, serial number: {self.serial_number}"

    def start(self):
        print(f"Car {self.name} is starting")

    def turn_off(self):
        print(f"Car {self.name} is turning off")




if __name__ == '__main__':
    bmw_car = Car('BMW')
    mahindra_car = Car('Mahindra')
    maruti_car = Car('Maruti')

    print(id(bmw_car.serial_number))
    print(id(maruti_car.serial_number))
    print(id(mahindra_car.serial_number))


    w = [bmw_car, mahindra_car, maruti_car]
    print(w)

