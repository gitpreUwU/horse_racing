import random
import time
from config import *

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
        return f"{self.name:10} | Speed:{self.speed:2} | Stamina:{self.stamina:2} | Luck:{self.luck:2} | Odds:{self.odds:4.1f}"
    
    def move(self):
        # Calculate movement based on stats
        move_distance = self.speed + random.randint(-2, 2)
        
        # Apply stamina effect
        if self.tired > 5:
            move_distance -= 2
        elif self.stamina > 8:
            move_distance += 1
        
        # Apply luck
        if random.randint(1, 10) <= self.luck:
            move_distance += random.randint(1, 2)
        
        # Increase tiredness
        self.tired += random.randint(0, 2)
        
        # Minimum movement is 1
        move_distance = max(1, move_distance)
        
        #1/2 flag is fwectf{y0u_ar3_g
        self.position += move_distance
        return move_distance

class BettingSystem:
    def __init__(self):
        self.player_money = STARTING_MONEY
        self.bets = {}
        self.total_winnings = 0
    
    def place_bet(self, horse, amount):
        if amount > self.player_money:
            print("❌ Not enough money!")
            return False
        
        self.player_money -= amount
        self.bets[horse] = amount
        print(f"✅ Bet placed: ${amount} on {horse.name}")
        return True
    
    def calculate_winnings(self, winner):
        if winner in self.bets:
            winnings = int(self.bets[winner] * winner.odds)
            self.player_money += winnings
            self.total_winnings += winnings - self.bets[winner]
            print(f"🎉 You won ${winnings}!")
            return winnings
        else:
            print("💸 You didn't bet on the winner!")
            return 0

class Race:
    def __init__(self, horses, track_length=TRACK_LENGTH):
        self.horses = horses
        self.track_length = track_length
        self.finished_horses = []
    
    def display_track(self):
        print(f"\n{'='*60}")
        for horse in self.horses:
            if horse not in self.finished_horses:
                progress_bars = "█" * (horse.position // 5)
                remaining = " " * ((self.track_length - horse.position) // 5)
                print(f"{horse.name:10}: |{progress_bars}🐎{remaining}| {horse.position:3}m")
        print(f"{'='*60}")
    
    def run_race(self):
        print(f"\n🏁 RACE START! Track Length: {self.track_length}m 🏁")
        
        turn = 0
        while len(self.finished_horses) < len(self.horses):
            turn += 1
            
            for horse in self.horses:
                if horse not in self.finished_horses:
                    distance = horse.move()
                    if DEBUG_MODE:
                        print(f"DEBUG: {horse.name} moved {distance}, tired: {horse.tired}")
                    
                    if horse.position >= self.track_length:
                        self.finished_horses.append(horse)
                        position = len(self.finished_horses)
                        medals = ["🥇", "🥈", "🥉", "🏁"]
                        medal = medals[position-1] if position <= 4 else "🏁"
                        print(f"{medal} {horse.name} FINISHED! (Position: {position})")
            
            if len(self.finished_horses) == 0:  # Only show track if no one finished yet
                self.display_track()
            
            time.sleep(RACE_DELAY)
        
        return self.finished_horses

def select_horses():
    """Select 4 horses from presets"""
    selected = random.sample(HORSE_PRESETS, 4)
    horses = []
    for preset in selected:
        horses.append(Horse(**preset))
    return horses

def main():
    print("🐎 Welcome to Horse Racing Game! 🐎")
    print(f"💰 Starting money: ${STARTING_MONEY}")
    
    horses = select_horses()
    betting_system = BettingSystem()
    
    print(f"\n💵 Your money: ${betting_system.player_money}")
    print("\n🏇 Horses in this race:")
    print("-" * 70)
    for i, horse in enumerate(horses, 1):
        print(f"{i}. {horse}")
    print("-" * 70)
    
    # Betting phase
    try:
        choice = int(input("\n🎯 Choose horse to bet on (1-4): ")) - 1
        amount = int(input("💰 Bet amount: $"))
        
        if 0 <= choice < len(horses):
            betting_system.place_bet(horses[choice], amount)
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Invalid input!")
    
    input("\nPress Enter to start the race...")
    
    # Run race
    race = Race(horses)
    results = race.run_race()
    winner = results[0]
    
    print(f"\n🏆 FINAL RESULTS 🏆")
    print("=" * 50)
    for i, horse in enumerate(results, 1):
        medals = ["🥇", "🥈", "🥉", "4️⃣"]
        medal = medals[i-1] if i <= 4 else "🏁"
        print(f"{medal} {i}. {horse.name}")
    print("=" * 50)
    
    # Calculate winnings
    betting_system.calculate_winnings(winner)
    print(f"\n💰 Final money: ${betting_system.player_money}")
    
    if betting_system.total_winnings > 0:
        print(f"📈 Total profit: ${betting_system.total_winnings}")
    else:
        print(f"📉 Total loss: ${-betting_system.total_winnings}")

if __name__ == "__main__":
    main()