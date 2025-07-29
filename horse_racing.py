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
        self.odds = self.calculate_odds()
    
    def calculate_odds(self):
        # Calculate odds based on stats
        total_stats = self.speed + self.stamina + self.luck
        base_odds = 30 - total_stats
        return max(1.2, base_odds / 10)
    
    def __str__(self):
        return f"{self.name} (Speed:{self.speed}, Stamina:{self.stamina}, Luck:{self.luck}, Odds:{self.odds:.1f})"
    
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

class BettingSystem:
    def __init__(self):
        self.player_money = 1000
        self.bets = {}
    
    def place_bet(self, horse, amount):
        if amount > self.player_money:
            print("Not enough money!")
            return False
        
        self.player_money -= amount
        self.bets[horse] = amount
        print(f"Bet placed: ${amount} on {horse.name}")
        return True
    
    def calculate_winnings(self, winner):
        if winner in self.bets:
            winnings = int(self.bets[winner] * winner.odds)
            self.player_money += winnings
            print(f"You won ${winnings}!")
            return winnings
        else:
            print("You didn't bet on the winner!")
            return 0

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
                    progress = "█" * (horse.position // 5) + "○"
                    print(f"{horse.name:10}: {progress} ({horse.position}m)")
                    
                    if horse.position >= self.track_length:
                        self.finished_horses.append(horse)
                        print(f"🏆 {horse.name} FINISHED! (Position: {len(self.finished_horses)})")
            
            time.sleep(0.3)
        
        return self.finished_horses

def main():
    print("Welcome to Horse Racing Game!")
    print("Starting money: $1000")
    
    # Create horses
    horses = [
        Horse("Thunder", 8, 7, 6),
        Horse("Lightning", 9, 5, 7),
        Horse("Storm", 6, 9, 5),
        Horse("Wind", 7, 8, 8)
    ]
    
    betting_system = BettingSystem()
    
    print(f"\nYour money: ${betting_system.player_money}")
    print("\nHorses in this race:")
    for i, horse in enumerate(horses, 1):
        print(f"{i}. {horse}")
    
    # Betting phase
    try:
        choice = int(input("\nChoose horse to bet on (1-4): ")) - 1
        amount = int(input("Bet amount: $"))
        
        if 0 <= choice < len(horses):
            betting_system.place_bet(horses[choice], amount)
        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid input!")
    
    # Run race
    race = Race(horses)
    results = race.run_race()
    winner = results[0]
    
    print(f"\n{'='*50}")
    print("FINAL RESULTS:")
    print(f"{'='*50}")
    for i, horse in enumerate(results, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "💔"
        print(f"{medal} {i}. {horse.name}")
    
    # Calculate winnings
    betting_system.calculate_winnings(winner)
    print(f"\nFinal money: ${betting_system.player_money}")

if __name__ == "__main__":
    main()