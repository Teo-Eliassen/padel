from typing import List, Dict

def generate_americano_rounds(
    players: List[str],
    courts: List[str],
    game_name: str
) -> List[Dict]:
    """
    Generate Americano rounds for padel.
    """
    total_courts = len(courts)
    max_players_per_round = total_courts * 4

    total_players = len(players)

    if total_players < 4:
        raise ValueError("At least 4 players are required.")
    elif total_players <= 7 and total_courts != 1:
        raise ValueError("Number of courts need to be 1 with less than 8 players")
    elif 8 <= total_players <= 11 and total_courts not in (1, 2):
        raise ValueError("Number of courts need to be 1-2 with less than 12 players")
    elif total_players == 12 and total_courts not in (2, 3):
        raise ValueError("Number of courts need to be 2-3 with 12 players")
    elif 13 <= total_players <= 15 and total_courts != 3:
        raise ValueError("Number of courts need to be 3 with 13-15 players")
    elif total_players == 16 and total_courts not in (3, 4):
        raise ValueError("Number of courts need to be 3-4 with 16 players")
    elif total_players > 16:
        raise ValueError("Too many playeres. Max players: 16")
    
    # Generate all rounds with fair rotation
    rounds = []
    rotation = players.copy()
    num_rounds = total_players - 1

    for round_number in range(1, num_rounds + 1):
        round_matches = []

        # Rotate players (circle rotation)
        rotation = rotation[1:] + rotation[:1]

        active_players = rotation[:max_players_per_round]
        benched_players = rotation[max_players_per_round:]

        for court in range(len(courts)):
            start = court * 4
            if start + 4 > len(active_players):
                break

            p1, p2, p3, p4 = active_players[start:start + 4]

            round_matches.append({
                "Game": game_name,
                "Round": round_number,  # Original round number
                "Court": courts[court],
                "Players": [[p1, p2], [p3, p4]]
            })

        if benched_players:
            round_matches.append({
                "Game": game_name,
                "Round": round_number,
                "Court": "Bench",
                "Players": benched_players
            })

        rounds.append(round_matches)

    return rounds

def reorder_rounds(schedule):
    """Rreorders rounds and flattens the lested list"""
    # Reorder rounds in a more interesting pattern
    # Strategy: Weave rounds from different parts of the sequence
    reorder_schedule = []
    
    # Create an interesting pattern: start, end, start+1, end-1, etc.
    left = 0
    right = len(schedule) - 1
    from_left = True
    
    while left <= right:
        if from_left:
            reorder_schedule.append(schedule[left])
            left += 1
        else:
            reorder_schedule.append(schedule[right])
            right -= 1
        from_left = not from_left
    
    # Flatten the nested list of rounds into a single schedule
    final_schedule = [round for item in reorder_schedule for round in item]
    return final_schedule

def display_schedule(schedule):
    print(schedule[0]["Game"]+":", end="\n"*2)

    round_numbers = []
    matches_count = 0

    for match in schedule:
        round_numbers.append(match["Round"])
        if match["Court"] == "Bench":
            bench_players = ', '.join(match["Players"])
            print(f"Round: {match["Round"]}, Bench: {bench_players}")

        else:
            print(f"Round: {match["Round"]}, Court: {match["Court"]}, Players:    {match["Players"][0][0]} & {match["Players"][0][1]} vs  {match["Players"][1][0]} & {match["Players"][1][1]}")
            matches_count += 1

    # Max number in Round
    print(f"Number of rounds {max(round_numbers)}")
    # Count of matches that are not on bench
    print(f"Number of matches {matches_count}\n")
    

def main():
    # players = [
    #     "Thomas",
    #     "Ine",
    #     "Tore",
    #     "Teo",
    #     "Anders F.",
    #     "Lima",
    #     "Ragnhild",
    #     "Andrine",
    #     "Stine",
    #     "Magnus",
    #     "Lars",
    #     "Wiktor",
    #     ]
    
    players = [ f"Player{i+1}" for i in range(9)]

    courts = [ f"Court{i+1}" for i in range(2)]

    game_name = "Americano 16.12.25"

    rounds = generate_americano_rounds(players, courts, game_name)

    schedule = reorder_rounds(rounds)

    display_schedule(schedule)

def test_generate_americano(number_of_players: int, number_of_courts: int):
    players = [ f"Player{i+1}" for i in range(number_of_players)]

    courts = [ f"Court{i+1}" for i in range(number_of_courts)]

    game_name = "Americano 16.12.25"

    try:
        rounds = generate_americano_rounds(players, courts, game_name)

        schedule = reorder_rounds(rounds)

    except ValueError as e:
        print(
            f"[ERROR] players={number_of_players}, courts={number_of_courts} → {e}"
        )
    else:
        print(
            f"[SUCCESS] players={number_of_players}, courts={number_of_courts}"
        )
        display_schedule(schedule)

if __name__ == "__main__":
    main()

    # for i in range(6):
    #     for j in range(18):
    #         test_generate_americano(number_of_players= j,number_of_courts= i)