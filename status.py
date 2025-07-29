import json
import os
from datetime import datetime

class RaceStats:
    def __init__(self):
        self.stats_file = "race_stats.json"
        self.stats = self.load_stats()
    
    def load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"races": [], "horses": {}, "player": {"total_bets": 0, "total_winnings": 0}}
    
    def save_stats(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def record_race(self, horses, results, player_bet, winnings):
        race_data = {
            "timestamp": datetime.now().isoformat(),
            "horses": [{"name": h.name, "speed": h.speed, "stamina": h.stamina, "luck": h.luck} for h in horses],
            "results": [h.name for h in results],
            "player_bet": player_bet,
            "winnings": winnings
        }
        
        self.stats["races"].append(race_data)
        
        # Update horse stats
        for i, horse in enumerate(results):
            if horse.name not in self.stats["horses"]:
                self.stats["horses"][horse.name] = {"races": 0, "wins": 0, "placements": []}
            
            self.stats["horses"][horse.name]["races"] += 1
            self.stats["horses"][horse.name]["placements"].append(i + 1)
            
            if i == 0:  # Winner
                self.stats["horses"][horse.name]["wins"] += 1
        
        # Update player stats
        self.stats["player"]["total_bets"] += player_bet if player_bet else 0
        self.stats["player"]["total_winnings"] += winnings if winnings else 0
        
        self.save_stats()
    
    def show_stats(self):
        print("\n📊 RACE STATISTICS 📊")
        print("=" * 50)
        
        total_races = len(self.stats["races"])
        print(f"Total races: {total_races}")
        
        if total_races > 0:
            print(f"Total money bet: ${self.stats['player']['total_bets']}")
            print(f"Total winnings: ${self.stats['player']['total_winnings']}")
            profit = self.stats['player']['total_winnings'] - self.stats['player']['total_bets']
            print(f"Net profit: ${profit}")
            
            print("\nHorse Performance:")
            print("-" * 30)
            for name, data in self.stats["horses"].items():
                if data["races"] > 0:
                    win_rate = (data["wins"] / data["races"]) * 100
                    avg_place = sum(data["placements"]) / len(data["placements"])
                    print(f"{name:10}: {data['wins']}/{data['races']} wins ({win_rate:5.1f}%) avg: {avg_place:.1f}")