import random
import string

def generate_password(length=12, safe_characters=None):
    if safe_characters is None:
        # Define a default set of safe characters (excluding sensitive ones)
        safe_characters = string.ascii_letters + string.digits + "!@$%"

    # Make sure we have at least one character from each category
    required_characters = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@$%,")
    ]

    # Generate the rest of the password
    remaining_length = length - len(required_characters)
    random_characters = [random.choice(safe_characters) for _ in range(remaining_length)]

    # Combine required and random characters, then shuffle them
    password_characters = required_characters + random_characters
    random.shuffle(password_characters)

    # Convert the list of characters into a string
    password = ''.join(password_characters)

    return password

# Example usage:
password = generate_password()
print("Generated Password:", password)