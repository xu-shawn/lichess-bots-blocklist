for file in ("blocklist", "whitelist", "sloplist"):
    with open(file, 'r') as f:
        usernames = f.readlines()
    usernames.sort(key=lambda s:(s.lower(), s))
    newusernames = []
    for username in usernames:
        if not newusernames or newusernames[-1] != username:
            newusernames.append(username)
    with open(file, 'w') as f:
        f.writelines(newusernames)