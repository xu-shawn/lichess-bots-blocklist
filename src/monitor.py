import requests
import json
import time

# --- Configuration --- #
MIN_ELO = 2900
CHECK_INTERVAL_SECONDS = 60
LICHESS_API_URL = "https://lichess.org/api/bot/online"

def monitor_high_rated_bots():
    """
    Main function to continuously monitor for high-rated bots on Lichess.
    """
    print("--- Starting Lichess BOT Monitor ---")
    print("Parsing block list...")

    with open("blocklist") as f:
        blocklist = set(line.strip() for line in f)

    print(f"Found {len(blocklist)} names")

    print(f"Looking for online bots with any rating > {MIN_ELO}")
    print(f"Checking for new bots every {CHECK_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop the script.")
    print("-" * 35)

    while True:
        try:
            printed_bots_this_cycle = set()
            found_any_bot = False

            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"[{current_time}] Fetching list of online bots...")

            response = requests.get(LICHESS_API_URL, stream=True, timeout=20)
            
            response.raise_for_status()

            blocked_count = 0

            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    bot_data = json.loads(line)
                    username = bot_data.get('username')
                    
                    if username in printed_bots_this_cycle:
                        continue

                    if 'perfs' not in bot_data:
                        continue

                    if username in blocklist:
                        blocked_count += 1
                        continue

                    for game_type, stats in bot_data['perfs'].items():
                        rating = stats.get('rating')
                        if rating and rating > MIN_ELO:
                            print(f"  > FOUND: Bot '{username}' has a {game_type.upper()} rating of {rating}")
                            printed_bots_this_cycle.add(username)
                            found_any_bot = True
                            break
                
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode a line from the stream: {line}")

            print(f"Hidden {blocked_count} blocked bots")

            if not found_any_bot and not blocked_count:
                print("  No online bots found above the ELO threshold in this check.")

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Lichess API: {e}")
            print("Will retry after the interval.")
        except KeyboardInterrupt:
            print("\n--- Monitor stopped by user. Goodbye! ---")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print(f"\nWaiting for {CHECK_INTERVAL_SECONDS} seconds before the next check...")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    monitor_high_rated_bots()
