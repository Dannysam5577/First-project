def cantainsduplicate(nums):
    dup=set()
    for i in nums:
        if i in dup:
            return True
        dup.add(i)
    return False
nums=[1,2,3]
a = cantainsduplicate(nums)
print(a)
