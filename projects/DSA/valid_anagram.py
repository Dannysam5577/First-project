def anagram(s,t):
    if len(s) != len(t):
        return False
    count_s={}
    count_t={}
    for char in s:
        count_s[char]=count_s.get(char,0)+1
    for char in t:
        count_t[char]=count_t.get(char,0)+1
    return count_s == count_t
s="danny"
t="yannd"
a=anagram(s,t)
print(a)
