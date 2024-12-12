import datetime
def time_stamped_msg(message):
    time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    time = time.split(",")[0]
    time = time.replace(":","_")
    time=time.split(" ")
    err = "-".join(time)
    return "{}-{}".format(message,err)

def maybe_print(flag, message):
    if flag:
        print(message)