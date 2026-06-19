from django.http import JsonResponse
from .rectangle import Rectangle


def rectangle_demo(request):
    """
    Demonstrates the Rectangle class iteration behaviour.
    """
    length = int(request.GET.get('length', 10))
    width = int(request.GET.get('width', 5))

    rect = Rectangle(length, width)

    # Iterating over the Rectangle instance
    iteration_output = list(rect)

    return JsonResponse({
        "description": "Rectangle class iteration demo",
        "input": {"length": length, "width": width},
        "iteration_output": iteration_output,
        "note": "Iterating yields {'length': VALUE} first, then {'width': VALUE}",
    })
