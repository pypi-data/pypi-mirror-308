import random
from .utils import quote_list


def generate_quote():
    """fungsi untuk generate quoote"""
    return random.choice(quote_list)
