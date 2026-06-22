from itertools import combinations
from collections import defaultdict

def apriori_algorithm(transactions, min_support):
    """
    Finds frequent itemsets using the Apriori Algorithm.
    """
    # Convert transactions to a list of sets for fast subset checking
    transaction_sets = [set(t) for t in transactions]

    # Store the final result: {frozenset({'Item'}): support_count}
    all_frequent_itemsets = {}

    # ---------------------------------------------------------
    # Step 1: Find Frequent 1-Itemsets (L1)
    # ---------------------------------------------------------
    item_counts = defaultdict(int)
    for t in transaction_sets:
        for item in t:
            item_counts[frozenset([item])] += 1

    # Filter out items below the minimum support
    current_l_set = {itemset for itemset, count in item_counts.items() if count >= min_support}

    # Save L1 to our final results
    for itemset in current_l_set:
        all_frequent_itemsets[itemset] = item_counts[itemset]

    # ---------------------------------------------------------
    # Steps 2-6: Generate larger itemsets (L2, L3, ... Lk)
    # ---------------------------------------------------------
    k = 2
    while current_l_set:
        candidates = set()
        l_list = list(current_l_set)

        # Step 2: Generate Candidate Itemsets (Ck)
        for i in range(len(l_list)):
            for j in range(i + 1, len(l_list)):
                # Join two itemsets to create a new set of size k
                union_set = l_list[i] | l_list[j]

                if len(union_set) == k:
                    # Step 3: Prune Candidates
                    # Check if all (k-1) subsets of this new candidate are frequent
                    subsets = [frozenset(x) for x in combinations(union_set, k - 1)]
                    if all(subset in current_l_set for subset in subsets):
                        candidates.add(union_set)

        # Step 4: Count Support for the generated candidates
        candidate_counts = defaultdict(int)
        for t in transaction_sets:
            for candidate in candidates:
                # If the candidate is fully present in the transaction, count it
                if candidate.issubset(t):
                    candidate_counts[candidate] += 1

        # Step 5: Generate Frequent Itemsets
        # Keep only candidates that meet the minimum support
        current_l_set = {candidate for candidate, count in candidate_counts.items() if count >= min_support}

        # Store the current level's frequent itemsets in our final results
        for itemset in current_l_set:
            all_frequent_itemsets[itemset] = candidate_counts[itemset]

        # Increment k to look for larger itemsets on the next loop
        k += 1

    # Step 7: Return Result
    return all_frequent_itemsets


# ==========================================
# Testing with the Provided Example
# ==========================================
if __name__ == "__main__":
    transactions = [
        {"Milk", "Bread"},                           # T1
        {"Milk", "Bread", "Butter"},                 # T2
        {"Milk", "Butter"},                          # T3
        {"Bread", "Butter"},                         # T4
        {"Milk", "Bread"},                           # T5
        {"Milk", "Bread", "Eggs"},                   # T6
        {"Milk", "Butter", "Eggs"},                  # T7
        {"Bread", "Butter", "Eggs"},                 # T8
        {"Milk", "Bread", "Butter", "Eggs"},         # T9
        {"Milk"},                                    # T10
        {"Bread"},                                   # T11
        {"Butter"},                                  # T12
        {"Milk", "Bread", "Jam"},                    # T13
        {"Bread", "Jam"},                            # T14
        {"Milk", "Jam"},                             # T15
        {"Milk", "Bread", "Butter", "Jam"},          # T16
        {"Eggs", "Bread"},                           # T17
        {"Eggs", "Milk"},                            # T18
        {"Eggs", "Butter"},                          # T19
        {"Milk", "Bread", "Eggs", "Butter"},         # T20
        {"Cheese", "Bread"},                         # T21
        {"Cheese", "Milk"},                          # T22
        {"Cheese", "Butter"},                        # T23
        {"Cheese", "Milk", "Bread"},                 # T24
        {"Cheese", "Milk", "Butter"},                # T25
        {"Milk", "Bread", "Cheese", "Butter"},       # T26
        {"Juice", "Bread"},                          # T27
        {"Juice", "Milk"},                           # T28
        {"Juice", "Butter"},                         # T29
        {"Juice", "Milk", "Bread"},                  # T30
        {"Juice", "Milk", "Butter"},                 # T31
        {"Juice", "Milk", "Bread", "Butter"},        # T32
        {"Milk", "Bread", "Eggs", "Cheese"},         # T33
        {"Milk", "Butter", "Cheese"},                # T34
        {"Bread", "Butter", "Jam"},                  # T35
        {"Milk", "Jam", "Eggs"},                     # T36
        {"Bread", "Cheese", "Jam"},                  # T37
        {"Milk", "Bread", "Juice", "Eggs"},          # T38
        {"Milk", "Butter", "Juice", "Cheese"},       # T39
        {"Bread", "Butter", "Eggs", "Cheese"},       # T40
        {"Milk", "Bread", "Butter", "Cheese"},       # T41
        {"Milk", "Bread", "Juice"},                  # T42
        {"Milk", "Eggs", "Cheese"},                  # T43
        {"Bread", "Jam", "Juice"},                   # T44
        {"Milk", "Bread", "Jam", "Cheese"},          # T45
        {"Butter", "Eggs", "Cheese"},                # T46
        {"Milk", "Bread", "Butter", "Eggs", "Jam"},  # T47
        {"Milk", "Cheese", "Juice"},                 # T48
        {"Bread", "Butter", "Juice"},                # T49
        {"Milk", "Bread", "Butter"}                  # T50
    ]

    minimum_support = 4

    print("Running Apriori Algorithm...\n")
    results = apriori_algorithm(transactions, minimum_support)

    print("Final Frequent Itemsets:")
    print("-" * 30)

    # Sort results by size of itemset, then alphabetically for clean output
    sorted_results = sorted(
        results.items(),
        key=lambda x: (len(x[0]), sorted(list(x[0])))
    )

    for itemset, support in sorted_results:
        # Format the set nicely for printing
        formatted_set = "{" + ", ".join(sorted(list(itemset))) + "}"
        print(f"{formatted_set:<25} = {support}")