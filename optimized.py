"""
Optimized algorithm to find the best combination of stock actions within a budget.
"""

import csv
import os

BUDGET_EUROS = 500.0


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

            if cost <= 0:
                continue

            profit_percent = float(row["Bénéfice (après 2 ans)"].replace("%", ""))
            profit_euros = cost * profit_percent / 100
            actions.append((name, cost, profit_percent, profit_euros))
    return actions


def choose_dataset(folder="Data"):
    """
    List CSV files in the folder and ask the user to choose one.
    Returns the full path of the selected file.
    """
    csv_files = [f for f in os.listdir(folder) if f.lower().endswith(".csv")]

    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier.")
        return None

    print("Fichiers disponibles :")
    for i, filename in enumerate(csv_files, start=1):
        print(f"  {i}. {filename}")

    choice = input("\nEntrez le numéro du fichier à utiliser : ")

    try:
        file_index = int(choice) - 1
        if 0 <= file_index < len(csv_files):
            return os.path.join(folder, csv_files[file_index])
        else:
            print("Numéro invalide.")
            return None
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return None


def compute_best_portfolio(actions, budget_euro):
    """
    Compute the best combination of actions to maximize profit without exceeding budget.
    Uses dynamic programming to efficiently find the optimal selection.

    Args:
        actions: list of (name, cost_euro, percent, profit_euro)
        budget_euro: budget in euros

    Returns:
        (best_profit_euro, best_combination_list)
    """
    # Convert euros -> cents to use integer indices in DP
    capacity = int(round(budget_euro * 100))

    n = len(actions)
    costs = [int(round(action[1] * 100)) for action in actions]  # costs in cents (integers)
    profits = [action[3] for action in actions]  # profits in euros (floats)

    # Initialize a list to store the best profit for each budget from 0 to capacity (all set to 0 initially)
    dp = [0.0] * (capacity + 1)

    # Initialize a list to track which action (index) was last used to reach each budget.
    # -1 means no action has been used yet for that budget.
    last_item = [-1] * (capacity + 1)

    # Initialize a list to track the previous budget for each current budget when an action is taken.
    # This helps reconstruct the combination of actions that led to the best profit.
    prev_budget = [-1] * (capacity + 1)

    # Process each item once
    for i in range(n):
        cost_i = costs[i]
        profit_i = profits[i]
        # Go through budgets from max to min to avoid using the same action multiple times
        if cost_i <= 0 or cost_i > capacity:
            # item cannot be taken at any capacity, skip
            continue
        for budget in range(capacity, cost_i - 1, -1):
            candidate = dp[budget - cost_i] + profit_i
            if candidate > dp[budget]:
                dp[budget] = candidate
                last_item[budget] = i
                prev_budget[budget] = budget - cost_i

    # Find best profit and its budget index
    best_budget = max(range(capacity + 1), key=lambda x: dp[x])
    best_profit = dp[best_budget]

    # Reconstruct chosen items by walking back from best_budget
    chosen_indices = []
    budget = best_budget
    while budget > 0 and last_item[budget] != -1:
        i = last_item[budget]
        chosen_indices.append(i)
        budget = prev_budget[budget]

    chosen_indices.reverse()

    best_combination = [actions[i] for i in chosen_indices]

    return best_profit, best_combination


def main():
    """
    Main entry point of the program.
    - Load actions from CSV
    - Find the best combination
    - Print the best result
    """
    filepath = choose_dataset()
    if not filepath:
        return

    actions = load_actions(filepath)

    best_profit, best_combination = compute_best_portfolio(actions, BUDGET_EUROS)

    print("\nBest combination of stocks found:")
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
