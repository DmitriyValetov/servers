import time

def decorator(func, argument2):
    def decrated_func(argument1):
        return func(argument1, argument2)
    return decrated_func

def queue_print(data, queue):
    queue.put(data)



def main(timer, data_queue):
    if data_queue:
        print = decorator(queue_print, data_queue)

    for i in range(timer):
        text = "Iteration {}".format(i)
        if data_queue:
            print(text)
            # data_queue.put(text)
        else:
            print(text)
        time.sleep(5)

    data_queue.put("Process ends")
    data_queue.close()

if __name__ == "__main__":
    main(1000000, None)