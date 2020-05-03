def check(num, pegs):
    j = pegs[0]+num
    i=1
    while i<len(pegs):
        if j>pegs[i]-1:
            return True
        j = 2*pegs[i] - j
        i = i+1
        
    return False

def solution(pegs):
    s = len(pegs)
    i=1
    while i<s:
        if pegs[i]==pegs[i-1]:
            a=[-1,-1]
            return a
        i=i+1
    if s%2==0 :
        temp=0
        temp = pegs[s-1]
        i=s-2;
        while i>0:
            if i%2==0:
                temp = temp - (2*pegs[i])
                i = i-1
            else:
                temp = temp + (2*pegs[i])
                i = i-1
                
        temp = temp - pegs[0]
        
        if temp<3:
            a = [-1,-1]
            return a
        q = check((temp*2)/3,pegs)
        if q:
            a = [-1,-1]
            return a
        else:
            if temp % 3==0:
                a = [int((temp/3)*2), 1]
                return a
            else:
                a = [int(2*temp), 3]
                return a
    else :
        temp = pegs[s-1]
        i = s-2
        while i>0:
            if i%2!=0:
                temp = temp - (2*pegs[i])
                i = i-1
            else:
                temp = temp + (2*pegs[i])
                i = i-1
        temp = temp + pegs[0]
        if temp>-1:
            a = [-1,-1]
            return a
        q = check(-2*temp, pegs)
        if q:
            a=[-1,-1]
            return a
        else:
            a = [int(-2*temp), 1]
            return a
        

