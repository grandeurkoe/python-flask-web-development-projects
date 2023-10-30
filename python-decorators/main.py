# def add(n1, n2):
#     return n1 + n2
#
#
# def subtract(n1, n2):
#     return n1 - n2
#
#
# def multiply(n1, n2):
#     return n1 * n2
#
#
# def divide(n1, n2):
#     return n1 + n2


# Functions are first-class objects, can be passed around as arguments E.g. int/string/float etc.
# These are what we call higher order functions.
# Here we can pass add, subtract, divide and multiply as arguments to calculate() function.

# def calculate(calc_function, n1, n2):
#     return calc_function(n1, n2)
#
#
# result = calculate(add, 5, 6)


# print(result)


# Nested Functions are functions that can be nested inside other functions.

# def outer_function():
#     print("I'm the outer function.")
#
#     # The nested_function() function will be accessible only inside the outer_function() function.
#     def nested_function():
#         print("I'm the inner nested function.")
#
#     nested_function()
#
#
# outer_function()


# Functions can be returned from other functions.
def outer_function():
    print("I'm the outer function.")

    # The nested_function() function will be accessible only inside the outer_function() function.
    def nested_function():
        print("I'm the inner nested function.")

    # We have to get rid of the parenthesis after nested_function if we wish to return it.
    return nested_function


# inner_function = outer_function()
# inner_function()
# OR
# outer_function()()

# Python Decorator Function
import time


def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        # Do something before calling the function.
        function()
        function()
        # Do something after calling the function.

    return wrapper_function


# Functions with @delay_decorator before them will be delayed by 2 seconds.
# @delay_decorator is what we call Syntactic sugar.
@delay_decorator
def say_hello():
    print("Hello")


@delay_decorator
def say_bye():
    print("Bye")


def say_greeting():
    print("How are you?")


say_hello()
# OR
decorated_function = delay_decorator(say_greeting)
decorated_function()
