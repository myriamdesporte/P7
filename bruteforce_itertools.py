"""
Brute-force algorithm to find the best combination of stock actions within a budget.
"""

import csv
import itertools

BUDGET = 500


def load_actions(filepath):
    """
    Load actions from a CSV file.

    Returns a list of tuples (name, cost, percent, profit).
    """
    actions = []
    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Actions #"]
            cost = float(row["Coût par action (en euros)"])
            profit_percent = float(row["Bénéfice (après 2 ans)"].replace("%", ""))
            profit_euros = cost * profit_percent / 100
            actions.append((name, cost, profit_percent, profit_euros))
    return actions


def find_best_combination(actions):
    """
    Explore all possible combinations of actions using itertools.

    Args:
        actions (list): List of all available actions.

    Returns:
        tuple: (best_profit, best_combination).
    """
    best_profit = 0
    best_combination = []

    for i in range(0, len(actions) + 1):
        for combo in itertools.combinations(actions, i):
            total_cost = sum(action[1] for action in combo)
            total_profit = sum(action[3] for action in combo)

            if total_cost <= BUDGET and total_profit > best_profit:
                best_profit = total_profit
                best_combination = combo

    return best_profit, best_combination


def main():
    """
    Main entry point of the program.
    - Load actions from CSV
    - Explore combinations with itertools
    - Print the best result
    """
    actions = load_actions("Data/Actions.csv")

    best_profit, best_combination = find_best_combination(actions)

    print("Best combination of stocks found:")
    if not best_combination:
        print("No valid combination within the budget was found.")
    else:
        for action in best_combination:
            print(f"{action[0]} — Cost: {action[1]:.2f} €, Profit: {action[3]:.2f} €")
        total_cost = sum(action[1] for action in best_combination)
        print(f"\nTotal cost = {total_cost:.2f} €")
        print(f"Total profit after 2 years = {best_profit:.2f} €")


if __name__ == "__main__":
    main()
