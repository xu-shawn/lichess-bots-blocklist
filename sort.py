with open("blocklist") as file:
    names = file.read().splitlines()

with open("blocklist", "w") as file:
    file.write("\n".join(sorted(set(names))))
