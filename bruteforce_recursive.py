"""
Brute-force algorithm to find the best combination of stock actions within a budget.
"""

import csv

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


def explore(actions, index, chosen, total_cost, total_profit):
    """
    Recursively explore all possible combinations of actions.

    Args:
        actions (list): List of all available actions.
        index (int): Current index in the list of actions.
        chosen (list): Current list of selected actions.
        total_cost (float): Current sum of costs.
        total_profit (float): Current sum of profits in euros.

    Returns:
        tuple: (best_profit, best_combination) found in this branch.
    """
    # Base case: we reached the end of the list
    if index == len(actions):
        if total_cost <= BUDGET:
            return total_profit, chosen[:]  # return a copy of chosen
        else:
            return 0, []  # invalid combination

    # Case 1: skip the current action
    profit_skip, combo_skip = explore(actions, index + 1, chosen, total_cost, total_profit)

    # Case 2: take the current action (if budget allows)
    name, cost, profit_percent, profit_euros = actions[index]
    new_cost = total_cost + cost
    new_profit = total_profit + profit_euros

    if new_cost <= BUDGET:
        chosen.append(actions[index])
        profit_take, combo_take = explore(actions, index + 1, chosen, new_cost, new_profit)
        chosen.pop()  # backtrack
    else:
        profit_take, combo_take = 0, []

    # Best option
    if profit_take > profit_skip:
        return profit_take, combo_take
    else:
        return profit_skip, combo_skip


def main():
    """
    Main entry point of the program.
    - Load actions from CSV
    - Explore combinations recursively
    - Print the best result
    """
    actions = load_actions("Data/Actions.csv")

    best_profit, best_combination = explore(actions, 0, [], 0, 0)

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
