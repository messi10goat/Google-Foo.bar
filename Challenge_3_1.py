def solution(l):
    n = len(l)
    ans=0
    a = []
    if n<3:
        return ans
    i=0
    while i<n:
        a.append(0)
        j=i+1
        while j<n:
            if l[j]%l[i]==0:
                a[i]=a[i]+1
            j=j+1
        i=i+1
    i=0
    while i<n:
        j=i+1
        while j<n:
            if l[j] % l[i]==0:
                ans = ans + a[j]
            j=j+1
        i=i+1
    return ans
