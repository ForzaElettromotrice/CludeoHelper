from colorama import Fore

people = ["white", "scarlet", "peacock", "mustard", "green", "plum"]
weapons = ["candlestick", "wrench", "rope", "knife", "lead_pipe"]
places = ["conservatory", "study", "lounge", "secret_passage", "hall", "kitchen", "biliard_room", "library", "dining_room", "ballroom"]

info = { "people": set(people), "weapons": set(weapons), "places": set(places), "who has it": { }, "who has it not": { }, "guesses": [] }

def check_guesses(n: int):
    for i, guess in enumerate(info["guesses"]):
        from_player, to_player, who, what, where = guess
        triple = { who, what, where }
        copy = triple.copy()
        for elm in copy:
            if info["who has it"][elm] != to_player and info["who has it"][elm] != -1:
                triple.discard(elm)
            if to_player in info["who has it not"][elm]:
                triple.discard(elm)
        if len(triple) == 1:
            elm = triple.pop()
            info["who has it"][elm] = to_player
            info["who has it not"][elm] = set(i for i in range(n) if i != to_player)
            for _set in [info["people"], info["weapons"], info["places"]]:
                _set.discard(elm)

def infer(n: int):
    for k, v in info["who has it not"].items():
        if len(v) == n:
            if k in people:
                info["people"] = { k }
            elif k in weapons:
                info["weapons"] = { k }
            elif k in places:
                info["places"] = { k }

def guess(n: int):
    from_player, to_player, who, what, where = input("Insert guess (from_player to_player who what where): ").split()
    current = int(to_player)

    while int(from_player) != current:
        info["guesses"].append((int(from_player), current, who, what, where))
        if input(f"({from_player}, {to_player}, {who}, {what}, {where}) Responded? (Y/n): ").lower() == 'n':
            info["who has it not"][who].add(current)
            info["who has it not"][what].add(current)
            info["who has it not"][where].add(current)
            current = (current + 1) % n
            continue
        break

    for _ in range(len(info["guesses"])):
        check_guesses(n)

    infer(n)

def debug_print():
    print("People:", info["people"])
    print("Weapons:", info["weapons"])
    print("Places:", info["places"])
    print("Who has it:", info["who has it"])
    print("Who has it not:", info["who has it not"])
    print("Guesses:")
    for guess in info["guesses"]:
        print(guess)

def pretty_print():
    print("""▄▖▄▖▄▖▄▖▖ ▄▖
▙▌▙▖▌▌▙▌▌ ▙▖
▌ ▙▖▙▌▌ ▙▖▙▖\n""")
    for person in people:
        if person in info["people"]:
            if len(info["people"]) == 1:
                print(f"{Fore.GREEN} - {person.title()}{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW} - {person.title()}{Fore.RESET}")
        else:
            print(f"{Fore.RED} - {person.title()}{Fore.RESET}")
    print("""▖  ▖▄▖▄▖▄▖▄▖▖ ▖▄▖
▌▞▖▌▙▖▌▌▙▌▌▌▛▖▌▚ 
▛ ▝▌▙▖▛▌▌ ▙▌▌▝▌▄▌\n""")
    for weapon in weapons:
        if weapon in info["weapons"]:
            if len(info["weapons"]) == 1:
                print(f"{Fore.GREEN} - {weapon.title()}{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW} - {weapon.title()}{Fore.RESET}")
        else:
            print(f"{Fore.RED} - {weapon.title()}{Fore.RESET}")
    print("""▄▖▖ ▄▖▄▖▄▖▄▖
▙▌▌ ▌▌▌ ▙▖▚ 
▌ ▙▖▛▌▙▖▙▖▄▌\n""")
    for place in places:
        if place in info["places"]:
            if len(info["places"]) == 1:
                print(f"{Fore.GREEN} - {place.title()}{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW} - {place.title()}{Fore.RESET}")
        else:
            print(f"{Fore.RED} - {place.title()}{Fore.RESET}")

if __name__ == '__main__':
    n = int(input("Insert number of players: "))
    print("Now insert the cards you have")
    hand = set([input("Card: ").lower() for _ in range(18 // n)])

    if 18 % n != 0:
        print("Now insert the common cards")
    common = set([input("Card: ").lower() for _ in range(18 % n)])

    hand = hand.union(common)

    for elm in people + weapons + places:
        if elm in hand:
            info["who has it"][elm] = 0
            info["who has it not"][elm] = { i for i in range(n) if i != 0 }
            for _set in [info["people"], info["weapons"], info["places"]]:
                _set.discard(elm)
        else:
            info["who has it"][elm] = -1
            info["who has it not"][elm] = { 0 }

    while True:
        action = input("1 - Guess\n2 - Print table\nAction: ")
        match action:
            case "1":
                guess(n)
            case "2":
                pretty_print()
            case "3":
                debug_print()
            case "exit":
                break
            case _:
                print("Invalid action!")
