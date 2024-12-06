'''
这是一个对处理跑步计时数据的函数
'''
def sanitize(time_string):
    '''
        time_string为你传入的数据的一个单位
    '''
    if '-'in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)
    (mins,secs) = time_string.split(splitter)
    return(mins + '.' + secs)
