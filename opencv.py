def solution(k):
    a = "2";
    check = True
    i=3
    while len(a)<k+7:
        check=True
        j=2;
        while j<i:
            if i%j==0:
                check = False
                break;
            else:
                j=j+1;
        if check== True:
            a = a + str(i)
        i = i+1
    ans = a[k:k+5]
    return ans