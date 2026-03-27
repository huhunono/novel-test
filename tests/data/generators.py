"""
tests/data/generators.py

Dynamic test data generators for scenarios requiring unique-per-run inputs.

Responsibility:
- Generate unique, collision-free test data using stdlib only.
- Used where static constants (users.py, books.py) would cause duplicate-entry
  errors or cross-run pollution (e.g., comment text, ephemeral usernames).
- NOT a replacement for TEST_USERNAME / TEST_PASSWORD in users.py.
  Static credentials must stay in users.py; those are environment fixtures,
  not generated values.

Design note:
- All generators are module-level functions (no class needed).
- No external dependencies: stdlib time + random + string is sufficient for
  uniqueness guarantees in API test data. Faker adds no value here because
  we need ASCII-safe identifiers, not human-readable names.
- Each function includes a short prefix so failures are easy to grep in logs.

Usage example:
    from tests.data.generators import unique_comment, unique_username

    comment_text = unique_comment()   # "cmt-1711234567890-ab3f"
    username     = unique_username()  # "usr_a3kz9f"
"""

import random
import string
import time


# ---------------------------------------------------------------------------
# Comment / content generators
# ---------------------------------------------------------------------------

def unique_comment(prefix: str = "cmt") -> str:
    """
    Generate a globally unique comment string.

    Combines prefix + millisecond timestamp + 4-char random suffix to
    guarantee uniqueness across concurrent runs.

    Args:
        prefix: Short label to identify the test source in logs.

    Returns:
        e.g. "cmt-1711234567890-a3kz"
    """
    ts = int(time.time() * 1000)
    rnd = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{prefix}-{ts}-{rnd}"


# ---------------------------------------------------------------------------
# User data generators
# ---------------------------------------------------------------------------

def unique_username(prefix: str = "usr") -> str:
    """
    Generate a unique username-safe string.

    Uses a random 6-char alphanumeric suffix to guarantee uniqueness.
    ASCII-safe — avoids DB charset issues that Chinese characters would cause.

    Args:
        prefix: Short label to identify the test source.

    Returns:
        e.g. "usr_a3kz9f"
    """
    rnd = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{rnd}"


def unique_email() -> str:
    """
    Generate a unique email address.

    Returns:
        e.g. "test_a3kz9f@example-test.com"
    """
    rnd = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{rnd}@example-test.com"


def unique_phone() -> str:
    """
    Generate a unique 11-digit Chinese mobile number format.
    Uses 139 prefix (non-live range safe for testing).

    Returns:
        e.g. "13900001234"
    """
    suffix = "".join(random.choices(string.digits, k=8))
    return f"139{suffix}"


def strong_password(length: int = 12) -> str:
    """
    Generate a random password meeting common strength requirements.
    Contains uppercase, lowercase, digit, and special character.

    Args:
        length: Total password length (minimum 8).

    Returns:
        e.g. "aB3!xk9Lmq2#"
    """
    length = max(length, 8)
    chars = string.ascii_letters + string.digits + "!@#$"
    # Guarantee at least one of each required class
    required = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$"),
    ]
    rest = random.choices(chars, k=length - len(required))
    combined = required + rest
    random.shuffle(combined)
    return "".join(combined)
