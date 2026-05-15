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
        raise ValueError("Too many playeres. Max players: 16")
    
    # Generate all rounds with fair rotation
    rounds = []
    rotation = players.copy()
    num_rounds = players_len - 1

    for round_number in range(1, num_rounds + 1):
        round_matches = []

        # Rotate players (circle rotation)
        rotation = rotation[1:] + rotation[:1]

        active_players = rotation[:max_players_per_round]

        for court in range(courts_len):
            start = court * 4
            if start + 4 > len(active_players):
                break

            p1, p2, p3, p4 = active_players[start:start + 4]

            round_matches.append({
                "Round": round_number,  # Original round number
                "Court": courts[court],
                "Players": [[p1, p2], [p3, p4]]
            })

        rounds.append(round_matches)

    reordered_rounds =  reorder_rounds(rounds=rounds)

    return 

def reorder_rounds(rounds):
    """Rreorders rounds and flattens the nested list"""
    # Reorder rounds in a more interesting pattern
    # Strategy: Weave rounds from different parts of the sequence
    reorder_schedule = []
    
    # Create an interesting pattern: start, end, start+1, end-1, etc.
    left = 0
    right = len(rounds) - 1
    from_left = True
    
    while left <= right:
        if from_left:
            reorder_schedule.append(rounds[left])
            left += 1
        else:
            reorder_schedule.append(rounds[right])
            right -= 1
        from_left = not from_left
    
    # Flatten the nested list of rounds into a single schedule
    final_schedule = [round for item in reorder_schedule for round in item]
    return final_schedule

players = ['Tore', 'Teo', 'Lars', 'Inge']
courts = ['court1']
tournament = 1
generate_americano_rounds(players= players, courts= courts, tournament= tournament)