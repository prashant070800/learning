from concurrent.futures import ThreadPoolExecutor
import time

def task(n:int)-> None:
    print(f"Task : {n} started")
    time.sleep(n)
    print(f"Task : {n} completed")

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task,i) for i in range(5)]
    for futuur in futures:
        print(futuur.result())