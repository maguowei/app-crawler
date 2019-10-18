def retry(times=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t = 0
            while t <= times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'Exception: {e}, times: {t}')
                    t += 1
        return wrapper
    return decorator


@retry(times=3)
def test_retry():
    raise Exception


if __name__ == '__main__':
    test_retry()
