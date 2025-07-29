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
    
    def move(self):
        # Calculate movement based on stats
        move_distance = self.speed + random.randint(-2, 2)
        
        # Apply stamina effect
        if self.tired > 5:
            move_distance -= 2
        
        # Apply luck
        if random.randint(1, 10) <= self.luck:
            move_distance += 1
        
        # Increase tiredness
        self.tired += random.randint(0, 2)
        
        # Minimum movement is 1
        move_distance = max(1, move_distance)
        
        self.position += move_distance
        return move_distance

class Race:
    def __init__(self, horses, track_length=100):
        self.horses = horses
        self.track_length = track_length
        self.finished_horses = []
    
    def run_race(self):
        print(f"\n{'='*50}")
        print("RACE START!")
        print(f"{'='*50}")
        
        turn = 0
        while len(self.finished_horses) < len(self.horses):
            turn += 1
            print(f"\nTurn {turn}:")
            
            for horse in self.horses:
                if horse not in self.finished_horses:
                    distance = horse.move()
                    print(f"{horse.name}: moved {distance} (+{horse.position})")
                    
                    if horse.position >= self.track_length:
                        self.finished_horses.append(horse)
                        print(f"🏆 {horse.name} FINISHED! (Position: {len(self.finished_horses)})")
            
            time.sleep(0.5)
        
        return self.finished_horses

def main():
    print("Welcome to Horse Racing Game!")
    
    # Create horses
    horses = [
        Horse("Thunder", 8, 7, 6),
        Horse("Lightning", 9, 5, 7),
        Horse("Storm", 6, 9, 5),
        Horse("Wind", 7, 8, 8)
    ]
    
    print("\nHorses in this race:")
    for i, horse in enumerate(horses, 1):
        print(f"{i}. {horse}")
    
    # Run race
    race = Race(horses)
    results = race.run_race()
    
    print(f"\n{'='*50}")
    print("FINAL RESULTS:")
    print(f"{'='*50}")
    for i, horse in enumerate(results, 1):
        print(f"{i}. {horse.name}")

if __name__ == "__main__":
    main()