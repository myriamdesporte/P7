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
    Uses 0/1 knapsack to ensure each action is chosen at most once.

    Args:
        actions: list of (name, cost_euro, percent, profit_euro)
        budget_euro: budget in euros

    Returns:
        (best_profit_euro, best_combination_list)
    """
    capacity = int(budget_euro * 100)  # budget in cents
    n = len(actions)
    costs = [int(action[1] * 100) for action in actions]  # costs in cents
    profits = [action[3] for action in actions]            # profits in euros

    # DP table: dp[i][budget] = max profit using first i actions with given budget
    dp = [[0.0] * (capacity + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        cost_i = costs[i - 1]
        profit_i = profits[i - 1]
        for current_budget in range(capacity + 1):
            if cost_i <= current_budget:
                dp[i][current_budget] = max(
                    dp[i - 1][current_budget],
                    dp[i - 1][current_budget - cost_i] + profit_i
                )
            else:
                dp[i][current_budget] = dp[i - 1][current_budget]

    # Reconstruct chosen actions
    chosen_indices = []
    remaining_budget = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining_budget] != dp[i - 1][remaining_budget]:
            chosen_indices.append(i - 1)
            remaining_budget -= costs[i - 1]

    chosen_indices.reverse()
    best_combination = [actions[i] for i in chosen_indices]
    best_profit = sum(a[3] for a in best_combination)

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
