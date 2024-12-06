from datetime import datetime

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

def get_current_datetime() -> str:
    """
    Get the current date and time.

    Returns:
    str: The current date and time in the format YYYY-MM-DD HH:MM:SS.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def days_between_dates(date1: str, date2: str) -> int:
    """
    Calculate the number of days between two dates.

    Parameters:
    date1 (str): The first date in the format YYYY-MM-DD.
    date2 (str): The second date in the format YYYY-MM-DD.

    Returns:
    int: The number of days between date1 and date2.
    """
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def reverse_string(s: str) -> str:
    """
    Reverse a given string.

    Parameters:
    s (str): The string to be reversed.

    Returns:
    str: The reversed string.
    """
    return s[::-1]

def decimal_to_binary(n: int) -> str:
    """
    Convert a decimal number to its binary representation.

    Parameters:
    n (int): The decimal number to convert.

    Returns:
    str: The binary representation of the decimal number as a string.
    """
    return bin(n)[2:]