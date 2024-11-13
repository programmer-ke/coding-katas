LOG = None

def open_log(filename):
    global LOG
    LOG = open(filename, "w")

def log(*args):
    print(*args, file=LOG)
