#!/usr/bin/env python
 
def say_hello(who="poscodx"):
    print(f"Hello, {who}!")
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            say_hello(arg)
    else:
        say_hello()