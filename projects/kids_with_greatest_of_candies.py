def kidmaxcandies(candies,extracandies):
    max_candies=max(candies)
    result =[]
    for i in candies:
        result.append(i+extracandies >= max_candies)
    return result
candies=[2,3,5,1,3]
extracandies=3
a=kidmaxcandies(candies,extracandies)
print(a)
