import requests

from rich.progress import track

def get_lichess_user_status(username: str) -> str:
    if not username or not isinstance(username, str):
        return "Error: Invalid username provided."
        
    api_url = f"https://lichess.org/api/user/{username}"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get('disabled'):
                return 'Closed'
            if data.get('tosViolation'):
                return 'Banned'
            return 'Active'

        elif response.status_code == 404:
            return 'Not Found'

        else:
            return f"Error: Lichess API returned status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error: A network error occurred: {e}"

def main() -> None:
    print("Parsing blocklist...")
    with open("blocklist") as f:
        usernames = set(line.strip() for line in f)
    print(f"Found {len(usernames)} names")

    removed_statuses = ['Closed', 'Banned', 'Not Found']

    removed_users = set()
    active_count = 0
    
    for user in track(usernames):
        status = get_lichess_user_status(user)
        if status in removed_statuses:
            removed_users.add(user)
        elif status == 'Active':
            active_count += 1
        else:
            print(f"Could not determine status for '{user}': {status}")

    print(active_count)
    print("Removed users:")
    print("\n".join(removed_users))

if __name__ == "__main__":
    main()
