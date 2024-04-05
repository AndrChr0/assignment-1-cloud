#  Simple script to test testing in Python

def add_two_numbers(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


if __name__ == "__main__":
    first_number = float(input("Enter the first number: "))
    second_number = float(input("Enter the second number: "))
    sum = add_two_numbers(first_number, second_number)
    print(f"The sum of {first_number} and {second_number} is {sum}.")
