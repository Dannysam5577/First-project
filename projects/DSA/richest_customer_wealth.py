def maxwealth(accounts):
    max_wealth=0

    for i in accounts:
        wealth=0

        for j in i:
            wealth+=j

        if max_wealth < wealth:
            max_wealth=wealth
    return max_wealth
accounts=[[1,5],[5,7],[4,7]]
rich_amount = maxwealth(accounts)
print(rich_amount)
