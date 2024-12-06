
# annotated  method, using for lock
def locked(lock=None):
    def real_lock(func):
        def wrapper(self, *args, **kwargs):
            lock_obj = getattr(self, lock)
            # print(f"in locked , {func} {args} {kwargs}")
            with lock_obj:
                o = func(self, *args, **kwargs)
                # print(f"out locked , {func} {args} {kwargs}")
                return o
        return wrapper

    return real_lock
