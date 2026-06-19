"""
Topic: Custom Classes in Python

Requirements:
1. Rectangle(length: int, width: int)
2. Instances must be iterable
3. Iteration yields {'length': VALUE} then {'width': VALUE}
"""


class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        # Yield length first, then width – exactly as the spec says
        yield {'length': self.length}
        yield {'width': self.width}
