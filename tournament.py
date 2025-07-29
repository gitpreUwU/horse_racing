import random
from config import HORSE_PRESETS
from horse_racing import Horse, Race, BettingSystem

class Tournament:
    def __init__(self, num_races=3):
        self.num_races = num_races
        self.all_horses = [Horse(**preset) for preset in HORSE_PRESETS]
        self.tournament_results = []
        self.player_total_winnings = 0
        
    def run_tournament(self):
        print("🏆 TOURNAMENT MODE 🏆")
        print(f"Racing {self.num_races} races with different horses!")
        print("=" * 60)
        
        betting_system = BettingSystem()
        betting_system.player_money = 2000  # Extra money for tournament
        
        for race_num in range(1, self.num_races + 1):
            print(f"\n🏇 RACE {race_num}/{self.num_races} 🏇")
            print("-" * 40)
            
            # Select 4 random horses for this race
            race_horses = random.sample(self.all_horses, 4)
            
            # Reset horse positions for new race
            for horse in race_horses:
                horse.position = 0
                horse.tired = 0
            
            print(f"💰 Current money: ${betting_system.player_money}")
            print("\nHorses in this race:")
            for i, horse in enumerate(race_horses, 1):
                print(f"{i}. {horse}")
            
            # Betting
            bet_placed = False
            try:
                choice = int(input(f"\n🎯 Bet on horse (1-4, 0 to skip): "))
                if choice > 0:
                    amount = int(input("💰 Bet amount: $"))
                    if 1 <= choice <= 4:
                        if betting_system.place_bet(race_horses[choice-1], amount):
                            bet_placed = True
            except ValueError:
                print("❌ Invalid input, skipping bet!")
            
            input(f"\nPress Enter to start race {race_num}...")
            
            # Run the race
            race = Race(race_horses, track_length=80)  # Shorter races for tournament
            results = race.run_race()
            
            # Show results
            print(f"\n🏁 RACE {race_num} RESULTS:")
            for i, horse in enumerate(results, 1):
                medals = ["🥇", "🥈", "🥉", "4️⃣"]
                medal = medals[i-1] if i <= 4 else ""
                print(f"{medal} {i}. {horse.name}")
            
            # Calculate winnings
            winnings = betting_system.calculate_winnings(results[0])
            self.tournament_results.append({
                'race': race_num,
                'winner': results[0].name,
                'bet_placed': bet_placed,
                'winnings': winnings
            })
            
            if race_num < self.num_races:
                input("\nPress Enter to continue to next race...")
        
        # Tournament summary
        self.show_tournament_summary(betting_system)
    
    def show_tournament_summary(self, betting_system):
        print("\n" + "=" * 60)
        print("🏆 TOURNAMENT COMPLETE! 🏆")
        print("=" * 60)
        
        total_winnings = 0
        races_won = 0
        
        for result in self.tournament_results:
            race_num = result['race']
            winner = result['winner']
            winnings = result['winnings']
            
            if winnings > 0:
                races_won += 1
                total_winnings += winnings
                print(f"Race {race_num}: {winner} 🎉 Won ${winnings}")
            else:
                print(f"Race {race_num}: {winner} 💸 Lost bet")
        
        print("-" * 60)
        print(f"Final Money: ${betting_system.player_money}")
        print(f"Races Won: {races_won}/{self.num_races}")
        
        if betting_system.player_money > 2000:
            profit = betting_system.player_money - 2000
            print(f"🎉 Tournament Profit: ${profit}")
            
            # Easter egg for big winners
            if profit > 5000:
                print("\n🎊 INCREDIBLE! You're a racing legend! 🎊")
                print("Secret achievement unlocked: Master Bettor")
                # Hidden message for CTF
                import base64
                secret_msg = "U2VjcmV0IGFjaGlldmVtZW50OiBZb3UgZm91bmQgdGhlIGhpZGRlbiBtZXNzYWdlIQ=="
                print(f"Debug: {base64.b64decode(secret_msg).decode()}")
        else:
            loss = 2000 - betting_system.player_money
            print(f"💸 Tournament Loss: ${loss}")
            print("Better luck next time! 🍀")

if __name__ == "__main__":
    tournament = Tournament(3)
    tournament.run_tournament()