import random
import string


def generate_email_hash():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(55))