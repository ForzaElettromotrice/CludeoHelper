people = ["white", "scarlet", "peacock", "mustard", "green", "plum"]
weapons = ["candlestick", "wrench", "rope", "knife", "lead pipe"]
places = ["conservatory", "study", "lounge", "secret passage", "hall", "kitchen", "biliard room", "library", "dining room", "ballroom"]

info = { "people": set(people), "weapons": set(weapons), "places": set(places), "who has it": { }, "who has it not": { }, "guesses": [] }

def check_guesses(n: int):
    for i, guess in enumerate(info["guesses"]):
        from_player, to_player, who, what, where = guess
        triple = { who, what, where }

        for elm in triple:
            if info["who has it"][elm] != to_player and info["who has it"][elm] != -1:
                triple.remove(elm)
            if to_player in info["who has it not"][elm]:
                triple.remove(elm)
        if len(triple) == 1:
            elm = triple.pop()
            info["who has it"][elm] = to_player
            info["who has it not"][elm] = set(i for i in range(n) if i != to_player)

def guess(n: int):
    from_player, to_player, who, what, where = input("Insert guess (from_player to_player who what where): ").split()
    current = int(to_player)

    while int(from_player) != current:
        info["guesses"].append((int(from_player), current, who, what, where))
        if input("Responded? (Y/n): ").lower() == 'n':
            info["who has it not"][who].add(current)
            info["who has it not"][what].add(current)
            info["who has it not"][where].add(current)
            current = (current + 1) % n
            continue
        break

    check_guesses(n)

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
        else:
            info["who has it"][elm] = -1
            info["who has it not"][elm] = set()

    while True:
        action = input("1 - Guess\n2 - Hint\nAction: ")
        match action:
            case "1":
                guess(n)
            case "2":
                pass
            case "Stop":
                break
            case _:
                print("Invalid action!")
