import random
import time

class Horse:
    def __init__(self, name, speed, stamina, luck):
        self.name = name
        self.speed = speed  # 1-10
        self.stamina = stamina  # 1-10
        self.luck = luck  # 1-10
        self.position = 0
        self.tired = 0
    
    def __str__(self):
        return f"{self.name} (Speed:{self.speed}, Stamina:{self.stamina}, Luck:{self.luck})"

def main():
    print("Welcome to Horse Racing Game!")
    
    # Create horses
    horses = [
        Horse("Thunder", 8, 7, 6),
        Horse("Lightning", 9, 5, 7),
        Horse("Storm", 6, 9, 5),
        Horse("Wind", 7, 8, 8)
    ]
    
    for horse in horses:
        print(horse)

if __name__ == "__main__":
    main()