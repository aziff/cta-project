

def convert_time(str):
    # Split the string by the :
    time = str.split(str=":")
    
    return time[0] * 60 + time[1]
    
