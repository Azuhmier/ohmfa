def decorator2(start):
    def decorator1(func):
        def wrapper(*args, **kwargs):
            wrapper.num += 1
            num = args[0] + wrapper.num
            args = [num]
            result = func(*args, **kwargs)
            return result
        wrapper.num = start
        return wrapper
    return decorator1