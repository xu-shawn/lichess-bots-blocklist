import requests

from rich.progress import track

API_URL = "https://lichess.org/api/users"
BATCH_SIZE = 300  # maximum ids per request accepted by the endpoint

def get_lichess_user_statuses(*usernames: str) -> dict[str, str]:
    """Fetch the status of up to BATCH_SIZE users in a single request."""
    response = requests.post(API_URL, data=",".join(usernames), timeout=30)
    response.raise_for_status()
    found = {user["id"]: user for user in response.json()}

    statuses = {}
    for username in usernames:
        user = found.get(username.lower())
        if user is None:
            statuses[username] = "Not Found"
        elif user.get("disabled"):
            statuses[username] = "Closed"
        elif user.get("tosViolation"):
            statuses[username] = "Banned"
        else:
            statuses[username] = "Active"
    return statuses

def main() -> None:
    print("Parsing blocklist...")
    with open("blocklist") as f:
        usernames = sorted(set(line.strip() for line in f if line.strip()))
    print(f"Found {len(usernames)} names")

    removed_statuses = ["Closed", "Banned", "Not Found"]

    removed_users = set()
    active_count = 0

    batches = [usernames[i:i + BATCH_SIZE] for i in range(0, len(usernames), BATCH_SIZE)]
    for batch in track(batches, description="Checking batches..."):
        for user, status in get_lichess_user_statuses(*batch).items():
            if status in removed_statuses:
                removed_users.add(user)
            else:
                active_count += 1

    print(active_count)
    print("Removed users:")
    print("\n".join(sorted(removed_users)))

if __name__ == "__main__":
    main()
