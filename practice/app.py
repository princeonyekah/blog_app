def my_recursive_function(lst):
    if lst == []:
        return 0
    else:
        v =  lst[0] + my_recursive_function(lst[1:])
        return v

print(my_recursive_function([5,6,8]))