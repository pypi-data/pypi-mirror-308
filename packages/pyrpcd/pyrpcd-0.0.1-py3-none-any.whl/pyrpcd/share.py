managers = set()


def emit(message):
    global managers
    try:
        for manager in managers:
            manager.publish(message)
    except Exception as e:
        traceback.print_exception(e)