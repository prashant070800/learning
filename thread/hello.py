import threading
from abc import ABC, abstractmethod
import time
# Base class inheriting from both Thread and ABC
class BaseClass(threading.Thread, ABC):

    def __init__(self,fun):
        super().__init__()
        self.some_condition = True
        self.fun = fun

    def run(self):
        self.fun.append(25)
        if self.some_condition:
            # Trigger the event or print something
            print("Condition met in BaseClass!")

# Extended class inheriting from BaseClass
class ExtendedClass(BaseClass):

    def __init__(self,fun):
        super().__init__(fun)

   
# Where you create the object
def main():
    fun = [1]
    obj = ExtendedClass(fun)  # Create the object
    obj.start()  # Start the thread (this will call the run method)
    time.sleep(1)
    print(fun)
if __name__ == "__main__":
    main()
