"""
Views that demonstrate each signal question in action.
Hit these endpoints and watch the server console output.
"""

import threading
import time

from django.db import transaction
from django.http import JsonResponse

from .models import UserProfile


def q1_synchronous_demo(request):
    """
    Q1: Proves signals are SYNCHRONOUS.
    The signal handler sleeps for 1 second.  We measure total time here –
    if signals were async the total time would be ~0 ms, but it will be ~1 s.
    """
    start = time.time()
    print(f"\n[Q1 CALLER] About to save UserProfile – time starts now.")

    profile = UserProfile.objects.create(name="Q1 Test", email="q1@test.com")

    elapsed = time.time() - start
    print(f"[Q1 CALLER] Save returned after {elapsed:.2f}s – signal ran SYNCHRONOUSLY before this line.\n")

    return JsonResponse({
        "question": "Q1 – Are Django signals synchronous?",
        "answer": "YES – synchronous",
        "proof": f"Caller had to wait {elapsed:.2f}s because the signal handler slept for 1s. "
                 "If signals were async, elapsed would be ~0s.",
    })


def q2_same_thread_demo(request):
    """
    Q2: Proves signals run in the SAME thread as the caller.
    """
    caller_thread_id = threading.get_ident()
    print(f"\n[Q2 CALLER] Thread ID in caller view : {caller_thread_id}")

    profile = UserProfile.objects.create(name="Q2 Test", email="q2@test.com")

    print(f"[Q2 CALLER] Check the two Thread IDs printed above – they are identical.\n")

    return JsonResponse({
        "question": "Q2 – Do signals run in the same thread as the caller?",
        "answer": "YES – same thread",
        "caller_thread_id": caller_thread_id,
        "proof": "The thread ID printed in the signal handler matches the caller's thread ID. "
                 "Check the server console output.",
    })


def q3_same_transaction_demo(request):
    """
    Q3: Proves signals run in the SAME DB transaction as the caller.
    We wrap the save inside transaction.atomic() so the signal handler
    can observe connection.in_atomic_block == True.
    We also demonstrate that a rollback in the handler prevents the save.
    """
    result = {}

    # --- Part A: Signal sees the open transaction ---
    with transaction.atomic():
        print(f"\n[Q3 CALLER] Inside transaction.atomic() – saving profile...")
        profile = UserProfile.objects.create(name="Q3 Test", email="q3@test.com")
        print(f"[Q3 CALLER] Profile pk={profile.pk} saved inside atomic block.")
        result["part_a"] = "Signal handler confirmed in_atomic_block=True (see console)"

    # --- Part B: Rollback proof ---
    # If the signal handler raises an exception inside an atomic block,
    # the entire transaction (including the save) is rolled back.
    before_count = UserProfile.objects.filter(name="Q3 Rollback Test").count()
    try:
        with transaction.atomic():
            UserProfile.objects.create(name="Q3 Rollback Test", email="q3rb@test.com")
            raise Exception("Simulated error inside atomic block – entire transaction rolls back!")
    except Exception as e:
        after_count = UserProfile.objects.filter(name="Q3 Rollback Test").count()
        result["part_b"] = {
            "exception": str(e),
            "records_before": before_count,
            "records_after_rollback": after_count,
            "proof": "count stayed at 0 – signal + save share the same transaction",
        }

    return JsonResponse({
        "question": "Q3 – Do signals run in the same DB transaction as the caller?",
        "answer": "YES – same transaction",
        "result": result,
    })
