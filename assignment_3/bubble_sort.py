def bubble(lst):
    swaps = False
    for i in range(len(lst)-1):
        if lst[i+1] < lst[i]:
            tmp = lst[i]
            lst[i] = lst[i+1]
            lst[i+1] = tmp
            swaps = True
    if not swaps:
        return lst
    return bubble(lst)
