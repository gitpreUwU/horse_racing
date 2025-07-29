import json
import time
from datetime import datetime

class RaceReplay:
    def __init__(self, race_data):
        self.race_data = race_data
        self.horses = race_data["horses"]
        self.results = race_data["results"]
        
    def play_replay(self):
        print(f"\n🎬 RACE REPLAY - {self.race_data['timestamp'][:19]} 🎬")
        print("=" * 60)
        
        print("🏇 Horses in this race:")
        for i, horse in enumerate(self.horses, 1):
            print(f"{i}. {horse['name']} (Speed:{horse['speed']} Stamina:{horse['stamina']} Luck:{horse['luck']})")
        
        print("\n🏁 Replaying race simulation...")
        time.sleep(1)
        
        # Animated replay visualization
        for turn in range(6):
            print(f"\nTurn {turn + 1}:")
            for horse in self.horses:
                # Create visual progress bar
                position = min(turn * 3 + horse['speed'] // 3, 15)
                progress = "█" * position + "🐎" + " " * (15 - position)
                print(f"{horse['name']:10}: |{progress}|")
            time.sleep(0.7)
        
        print(f"\n🏆 FINAL RACE RESULTS:")
        print("=" * 40)
        for i, horse_name in enumerate(self.results, 1):
            medals = ["🥇", "🥈", "🥉", "4️⃣"]
            medal = medals[i-1] if i <= 4 else "🏁"
            print(f"{medal} {i}. {horse_name}")
        
        # Show betting results
        bet_info = self.race_data.get("player_bet", 0)
        winnings = self.race_data.get("winnings", 0)
        
        if bet_info > 0:
            print(f"\n💰 Player bet: ${bet_info}")
            if winnings > bet_info:
                profit = winnings - bet_info
                print(f"🎉 Player won: ${winnings} (Profit: ${profit})")
            else:
                print(f"💸 Player lost: ${bet_info}")
        else:
            print("\n👀 Player did not bet on this race")

def show_replay_menu():
    """Show available replays and let user select one"""
    try:
        with open("race_stats.json", 'r') as f:
            stats = json.load(f)
        
        races = stats.get("races", [])
        if not races:
            print("❌ No races to replay!")
            return
        
        print("\n🎬 Available Replays:")
        print("-" * 50)
        
        # Show last 10 races
        recent_races = races[-10:] if len(races) > 10 else races
        for i, race in enumerate(recent_races, 1):
            timestamp = race['timestamp'][:19].replace('T', ' ')
            winner = race['results'][0] if race['results'] else 'Unknown'
            bet_result = "🎉 Won" if race.get('winnings', 0) > race.get('player_bet', 0) else "💸 Lost" if race.get('player_bet', 0) > 0 else "👀 No bet"
            print(f"{i:2}. {timestamp} | Winner: {winner:10} | {bet_result}")
        
        try:
            choice = int(input(f"\nSelect replay (1-{len(recent_races)}): ")) - 1
            if 0 <= choice < len(recent_races):
                replay = RaceReplay(recent_races[choice])
                replay.play_replay()
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Invalid input!")
            
    except FileNotFoundError:
        print("❌ No race data found!")
    except json.JSONDecodeError:
        print("❌ Error reading race data!")

if __name__ == "__main__":
    show_replay_menu()