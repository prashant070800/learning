import threading
from abc import ABC, abstractmethod

# Base class inheriting from both Thread and ABC
class BaseClass(threading.Thread, ABC):

    def __init__(self, func):
        super().__init__()
        self.some_condition = True
        self.func = func

    def run(self):
        if self.some_condition:
            # Trigger the function and handle the condition
            self.func()
            print("Condition met in BaseClass!")

# Extended class inheriting from BaseClass
class ExtendedClass(BaseClass):

    def __init__(self, func):
        super().__init__(func)


class Hello:
    # Example function to be passed
    def __init__(self) -> None:
        self.l = []
    def example_function(self):
        print("Function executed in the thread!")
        self.l.append(25)
        print(self.l)
        # You can perform any logic here
        # e.g., modifying a shared list, logging, etc.
    def pprint(self):
        print(self.l)
    obj = ExtendedClass(v)  # Pass the function instead of a list
    obj.start()  # Start the thread (this will call the run method)
    obj.join()   # Wait for the thread to finish
    # pprint()

if __name__ == "__main__":
    o = Hello()
