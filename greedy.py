"""
Optimized algorithm to find the best combination of stock actions within a budget.
"""

import csv
import os
import time

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


def greedy_by_ratio(actions, budget):
    """
    Greedy selection of actions based on profit-to-cost ratio.

    Chooses the most profitable actions per euro spent until the budget is used.

    Args:
        actions (list of tuple): (name, cost, percent, profit)
        budget (float): Maximum budget in euros

    Returns:
        tuple: (total_profit, selected_actions)
    """
    actions_sorted = sorted(actions, key=lambda action: action[3] / action[1], reverse=True)

    selected = []
    total_cost = 0
    total_profit = 0

    for action in actions_sorted:
        if total_cost + action[1] <= budget:
            selected.append(action)
            total_cost += action[1]
            total_profit += action[3]

    return total_profit, selected


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

    start_time = time.time()
    best_profit, best_combination = greedy_by_ratio(actions, BUDGET_EUROS)
    end_time = time.time()

    print("\nBest combination of stocks found:")
    if not best_combination:
        print("No valid combination within the budget was found.")
    else:
        for action in best_combination:
            print(f"{action[0]} — Cost: {action[1]:.2f} €, Profit: {action[3]:.2f} €")
        total_cost = sum(action[1] for action in best_combination)
        print(f"\nTotal cost = {total_cost:.2f} €")
        print(f"Total profit after 2 years = {best_profit:.2f} €")

    print(f"\nTemps d'exécution : {end_time - start_time:.4f} secondes")


if __name__ == "__main__":
    main()
