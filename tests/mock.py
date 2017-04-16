
uid_counter = 0

def uid():
    global uid_counter
    uid_counter += 1
    return uid_counter
