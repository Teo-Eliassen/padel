def generate_americano_rounds(
    players,
    courts,
    tournament
):
    """
    Generate Americano rounds for padel.
    """
    courts_len = len(courts)
    max_players_per_round = courts_len * 4
    players_len = len(players)

    if players_len < 4:
        raise ValueError("At least 4 players are required.")
    elif players_len <= 7 and courts_len != 1:
        raise ValueError("Number of courts need to be 1 with less than 8 players")
    elif 8 <= players_len <= 11 and courts_len not in (1, 2):
        raise ValueError("Number of courts need to be 1-2 with less than 12 players")
    elif players_len == 12 and courts_len not in (2, 3):
        raise ValueError("Number of courts need to be 2-3 with 12 players")
    elif 13 <= players_len <= 15 and courts_len != 3:
        raise ValueError("Number of courts need to be 3 with 13-15 players")
    elif players_len == 16 and courts_len not in (3, 4):
        raise ValueError("Number of courts need to be 3-4 with 16 players")
    elif players_len > 16:
        raise ValueError("Too many players. Max players: 16")

    rounds = []
    # Fix player[0], rotate the rest — standard round-robin circle method
    fixed = players[0]
    rotating = players[1:]
    num_rounds = players_len - 1  # correct: n-1 rounds for even n

    for round_number in range(1, num_rounds + 1):
        # Build the ring for this round: fixed + rotated slice
        ring = [fixed] + rotating
        active_players = ring[:max_players_per_round]

        round_matches = []
        for court in range(courts_len):
            start = court * 4
            if start + 4 > len(active_players):
                break

            p1, p2, p3, p4 = active_players[start:start + 4]
            round_matches.append({
                "Round": round_number,
                "Court": courts[court],
                "Players": [[p1, p2], [p3, p4]]
            })

        rounds.append(round_matches)

        # Rotate after assigning, so round 1 uses the original order
        rotating = rotating[-1:] + rotating[:-1]

    reordered_rounds = reorder_rounds(rounds=rounds)
    return reordered_rounds  # ← return the schedule, not a redirect

def reorder_rounds(rounds):
    """Rreorders rounds and flattens the nested list"""
    # Reorder rounds in a more interesting pattern
    # Strategy: Weave rounds from different parts of the sequence
    reorder_rounds = []
    
    # Create an interesting pattern: start, end, start+1, end-1, etc.
    left = 0
    right = len(rounds) - 1
    from_left = True
    
    while left <= right:
        if from_left:
            reorder_rounds.append(rounds[left])
            left += 1
        else:
            reorder_rounds.append(rounds[right])
            right -= 1
        from_left = not from_left
    
    # Flatten the nested list of rounds into a single schedule
    reordered_rounds = [round for item in reorder_rounds for round in item]
    return reordered_rounds

def display_rounds(rounds):
    print("Next tournamet:")

    round_numbers = []
    matches_count = 0

    for match in rounds:
        round_numbers.append(match["Round"])

        print(f"Round: {match["Round"]}, Court: {match["Court"]}, Players:    {match["Players"][0][0]} & {match["Players"][0][1]} vs  {match["Players"][1][0]} & {match["Players"][1][1]}")
        matches_count += 1

    # Max number in Round
    print(f"Number of rounds {max(round_numbers)}")
    # Count of matches that are not on bench
    print(f"Number of matches {matches_count}\n")


players = [
    "Thomas",
    "Inge",
    "Tore",
    "Teo",
    "Anders F.",
    "Lima",
    "Ragnhild",
    "Andrine",
    # "Stine",
    # "Magnus",
    # "Lars",
    # "Wiktor",
    ]
courts = [
    'court1', 
    'court2'
    ]
tournament = 1
roudns = generate_americano_rounds(players= players, courts= courts, tournament= tournament)

display_rounds(roudns)