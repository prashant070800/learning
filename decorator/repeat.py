from functools import wraps

def repeat(n):
    def decorator(func):
        # @wraps(func)
        def wrapperr(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapperr
    return decorator

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args} and {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(x, y):
    return x + y

add(10, y=20)

@repeat(5)
def pp():
    print(10)

pp()