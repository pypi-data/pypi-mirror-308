def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers and return the result.

    Parameters:
    a (int): The first number to add.
    b (int): The second number to add.

    Returns:
    int: The sum of a and b.
    """
    return a + b


def is_even(number: int) -> bool:
    """
    Check if a number is even.

    Parameters:
    number (int): The number to check.

    Returns:
    bool: True if the number is even, False otherwise.
    """
    return number % 2 == 0


def greet_user(name: str) -> str:
    """
    Generate a greeting message for a user.

    Parameters:
    name (str): The name of the user.

    Returns:
    str: A greeting message.
    """
    return f"Hello, {name}!"


def find_max(numbers: list[int]) -> int:
    """
    Find the maximum number in a list of integers.

    Parameters:
    numbers (list[int]): A list of integers.

    Returns:
    int: The maximum integer in the list.
    """
    return max(numbers)


def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given its radius.

    Parameters:
    radius (float): The radius of the circle.

    Returns:
    float: The area of the circle.
    """
    from math import pi
    return pi * radius ** 2
