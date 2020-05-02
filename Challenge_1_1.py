def solution(xs):
    a = len(xs)
    
    if a==1:
        return xs[0]
    xs.sort()
    if xs[a-1]==0:
        if xs[0]==0 :
            return 0
        if xs[1]== 0:
            return 0
    ans=1
    neg=0
    i=0
    while i<a and xs[i]<0 :
        ans = ans * xs[i]
        neg=neg+1
        i=i+1
    print(ans, neg)
    if ans < 0:
        ans = ans / xs[neg-1]
    i = a-1;
    while i>=0 and xs[i]>0:
        ans = ans * xs[i]
        i=i-1
    ans = int(ans)
    ans = str(ans)
    return ans
