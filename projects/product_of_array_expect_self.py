def productexpect(nums):
    n = len(nums)
    right = [1]*n
    left = [1]*n
    answer=[1]*n
    for i in range(1,n):
        left[i]=left[i-1]* nums[i-1]
    for i in range(n-2,-1,-1):
        right[i]=right[i+1]*nums[i+1]
    for i in range(n):
        answer[i]=left[i]*right[i]
    return answer
nums=[1,2,3,4]
a=productexpect(nums)
print(a)

                   
                   
