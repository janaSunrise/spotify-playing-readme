import random
from textwrap import dedent

from memoization import cached


@cached(ttl=60, max_size=128)
def generate_bar(bar_count: int = 75) -> str:
    css_bar = ""
    left = 1

    for i in range(1, bar_count + 1):
        anim = random.randint(300, 600)
        css_bar += dedent(
            f"""
        .bar:nth-child({i}) {{
            left: {left}px;
            animation-duration: {anim}ms;
        }}
        """
        )
        left += 4

    return css_bar
