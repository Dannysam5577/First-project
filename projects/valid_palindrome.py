def ispalindrome(string):
    left=0
    right=len(string)-1
    while left < right :
        while left < right and not string[left].isalnum():
            left+=1
        while left < right and not string[right].isalnum():
            right-=1
        if string[left].lower()!=string[right].lower():
            return False
        left+=1
        right-=1
    return True
string="A man, a plan, a canal: Panama"
a = ispalindrome(string)
print(a)

    
