# modules/game_analyzer.py
import os
import json
import logging
from datetime import datetime

# Assuming ROOT_DIR and get_config are available via core.config
try:
    from core.config import get_config, ROOT_DIR
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(current_dir)
    print(f"Warning: Could not import from core.config. Using ROOT_DIR: {ROOT_DIR}")
    def get_config(key, default=None):
        if key == "paths.logs":
            return os.path.join(ROOT_DIR, "logs")
        if key == "v2_3.postgame_reports" :
             return True # Default to true for standalone testing
        return default

logger = logging.getLogger(__name__)

class GameAnalyzer:
    """Analyzes game data to generate post-game reports."""
    def __init__(self):
        self.log_dir = get_config("paths.logs", os.path.join(ROOT_DIR, "logs"))
        self.report_dir = os.path.join(self.log_dir, "match_reports")
        os.makedirs(self.report_dir, exist_ok=True)
        self.enabled = get_config("v2_3.postgame_reports", True)
        if self.enabled:
            logger.info("Game Analyzer initialized. Reports will be saved to: " + self.report_dir)
        else:
             logger.info("Game Analyzer is disabled in config.yaml.")

    def generate_report(self, game_data: dict, coaching_log: list, summoner_name: str) -> Optional[dict]:
        """
        Generates a post-game report based on collected game data and coaching interactions.

        Args:
            game_data (dict): Comprehensive data collected during the match 
                              (e.g., events, player stats, vision score, objectives taken/lost).
            coaching_log (list): A list of coaching suggestions made during the game, 
                                including whether they were followed (needs implementation).
            summoner_name (str): The name of the player being coached.

        Returns:
            dict: The generated match report, or None if disabled or error occurs.
        """
        if not self.enabled:
            logger.debug("Post-game report generation is disabled.")
            return None
            
        if not game_data or not isinstance(game_data, dict):
             logger.warning("Cannot generate report: Invalid game_data received.")
             return None

        try:
            match_id = game_data.get("match_id", f"unknown_{datetime.now().strftime("%Y%m%d%H%M%S")}")
            report_timestamp = datetime.now().isoformat()
            logger.info(f"Generating post-game report for match {match_id} for player {summoner_name}")

            report = {
                "report_id": f"report_{match_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}",
                "match_id": match_id,
                "summoner_name": summoner_name,
                "report_generated_at": report_timestamp,
                "game_summary": self._summarize_game(game_data),
                "performance_metrics": self._extract_performance_metrics(game_data, summoner_name),
                "tactical_analysis": self._analyze_tactics(game_data, coaching_log),
                "coaching_summary": self._summarize_coaching(coaching_log)
            }

            # Save the report
            report_filename = f"match_{match_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
            report_path = os.path.join(self.report_dir, report_filename)
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4, ensure_ascii=False)
            logger.info(f"Post-game report saved to: {report_path}")

            return report

        except Exception as e:
            logger.exception(f"Error generating post-game report for match {match_id}: {e}")
            return None

    def _summarize_game(self, game_data: dict) -> dict:
        """Extracts basic game summary information."""
        # Placeholder: Extract relevant summary data like duration, win/loss, teams
        return {
            "duration_seconds": game_data.get("game_duration", 0),
            "result": game_data.get("win_status", "Unknown"), # Requires win/loss info in game_data
            "champion_played": game_data.get("player_champion", "Unknown"), # Requires player champ info
            "lane": game_data.get("player_lane", "Unknown"), # Requires player lane info
            # Add team compositions if available
        }

    def _extract_performance_metrics(self, game_data: dict, summoner_name: str) -> dict:
        """Extracts key performance indicators (KPIs) for the player."""
        # Placeholder: Extract KDA, CS/min, Vision Score, Damage Dealt/Taken etc.
        # This requires detailed player stats within game_data, keyed possibly by summoner_name
        player_stats = game_data.get("player_stats", {}).get(summoner_name, {})
        duration_minutes = game_data.get("game_duration", 1) / 60.0
        if duration_minutes == 0: duration_minutes = 1 # Avoid division by zero
        
        kda_ratio = "N/A"
        kills = player_stats.get("kills", 0)
        deaths = player_stats.get("deaths", 0)
        assists = player_stats.get("assists", 0)
        if deaths > 0:
             kda_ratio = round((kills + assists) / deaths, 2)
        elif kills + assists > 0:
             kda_ratio = "Perfect"
             
        return {
            "kda": f"{kills}/{deaths}/{assists}",
            "kda_ratio": kda_ratio,
            "cs_total": player_stats.get("creep_score", 0),
            "cs_per_minute": round(player_stats.get("creep_score", 0) / duration_minutes, 1),
            "vision_score": player_stats.get("vision_score", 0),
            "damage_dealt_to_champions": player_stats.get("damage_dealt_champions", 0),
            "damage_taken": player_stats.get("damage_taken", 0),
            # Add more metrics like gold earned, objective damage, etc.
        }

    def _analyze_tactics(self, game_data: dict, coaching_log: list) -> dict:
        """
        Performs tactical analysis based on game events and coaching interactions.
        Identifies potential mistakes or good plays.
        """
        # Placeholder: Analyze game events (fights, objectives, rotations) 
        # and correlate with coaching log and game state.
        major_successes = []
        major_failures = []
        
        # Example: Analyze fights based on game_data events
        # fight_events = game_data.get("fight_events", [])
        # for fight in fight_events:
        #     if fight.get("outcome") == "loss" and fight.get("outnumbered"): 
        #         major_failures.append(f"Teamfight lost near {fight.get("location")} at {fight.get("timestamp")}s (outnumbered {fight.get("team_size")}v{fight.get("enemy_size")})")
        #     elif fight.get("outcome") == "win" and fight.get("player_involved") and fight.get("is_pickoff"):
        #          major_successes.append(f"Successful pickoff near {fight.get("location")} at {fight.get("timestamp")}s")

        # Example: Analyze objectives
        # objective_events = game_data.get("objective_events", [])
        # for obj in objective_events:
        #      if obj.get("type") == "BARON" and obj.get("stolen"):
        #           major_failures.append("Baron stolen at {obj.get("timestamp")}s")
        #      elif obj.get("type") == "DRAGON" and obj.get("secured") and obj.get("fight_won_before"):
        #           major_successes.append("Dragon secured after winning teamfight at {obj.get("timestamp")}s")

        # Placeholder for more complex analysis (wave management, reset timing, roaming)
        # This would require much more detailed game state information in game_data

        return {
            "major_successes": major_successes, # List of strings describing good plays
            "major_failures": major_failures,   # List of strings describing tactical errors
            "wave_management_notes": [], # e.g., "Missed opportunity to freeze wave at 8:30"
            "reset_timing_notes": [],    # e.g., "Reset without pushing wave at 12:15, losing tempo"
            "roaming_notes": [],         # e.g., "Successful roam bot lane at 9:00 after pushing mid"
        }

    def _summarize_coaching(self, coaching_log: list) -> dict:
        """Summarizes the coaching interactions during the game."""
        suggestions_made = len(coaching_log)
        suggestions_followed = 0 # Requires tracking if advice was followed
        missed_opportunities = [] # Suggestions ignored that might have been beneficial

        # Placeholder: Iterate through coaching_log to determine followed/ignored
        # for entry in coaching_log:
        #     if entry.get("status") == "followed":
        #         suggestions_followed += 1
        #     elif entry.get("status") == "ignored" and entry.get("potential_impact") == "high":
        #         missed_opportunities.append(entry.get("suggestion_text"))

        return {
            "suggestions_made": suggestions_made,
            "suggestions_followed": suggestions_followed, # Needs implementation
            "missed_opportunities": missed_opportunities, # Needs implementation
            "key_advice_given": [log.get("suggestion_text") for log in coaching_log[:5]] # Example: first 5 suggestions
        }

# Example Usage (for testing within the module)
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG, format=\"%(asctime)s - %(name)s - %(levelname)s - %(message)s\")
#     analyzer = GameAnalyzer()
#
#     # Simulate game data and coaching log
#     mock_game_data = {
#         "match_id": "NA1_987654321",
#         "game_duration": 1850, # seconds (~30 mins)
#         "win_status": "Win",
#         "player_champion": "Lux",
#         "player_lane": "Mid",
#         "player_stats": {
#             "TestPlayer123": {
#                 "kills": 8,
#                 "deaths": 2,
#                 "assists": 15,
#                 "creep_score": 210,
#                 "vision_score": 45,
#                 "damage_dealt_champions": 35000,
#                 "damage_taken": 15000
#             }
#         },
#         # Add mock events if needed for tactical analysis testing
#         "fight_events": [
#              {"outcome": "loss", "outnumbered": True, "location": "dragon_pit", "timestamp": 1200, "team_size": 4, "enemy_size": 5},
#              {"outcome": "win", "player_involved": True, "is_pickoff": True, "location": "mid_lane", "timestamp": 950}
#         ]
#     }
#     mock_coaching_log = [
#         {"suggestion_text": "Push mid wave before roaming bot", "status": "ignored", "potential_impact": "high"},
#         {"suggestion_text": "Ward the enemy raptors", "status": "followed"},
#         {"suggestion_text": "Avoid fighting outnumbered at dragon", "status": "ignored", "potential_impact": "high"},
#         {"suggestion_text": "Consider resetting after this wave", "status": "followed"}
#     ]
#
#     if analyzer.enabled:
#         report = analyzer.generate_report(mock_game_data, mock_coaching_log, "TestPlayer123")
#         if report:
#             print("--- Generated Report ---")
#             print(json.dumps(report, indent=2))
#         else:
#             print("Failed to generate report.")
#     else:
#          print("Game Analyzer is disabled.")

