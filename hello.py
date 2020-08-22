def hello():
    print("Hello, World.")

def event_glob_test(event_stream):
    """Demonstration of how to change a global var from differnet module
    """
    event_stream.add("YOLO")

    