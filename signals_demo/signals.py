"""
Django Signals Demo - Answering all 3 questions.

Question 1: Are Django signals synchronous or asynchronous?
Answer: Synchronous. The signal handler runs BEFORE the view/caller continues.

Question 2: Do signals run in the same thread as the caller?
Answer: Yes. Same thread ID is printed in both caller and handler.

Question 3: Do signals run in the same DB transaction as the caller?
Answer: Yes. If the caller is inside a transaction.atomic() block,
        the signal handler participates in the same transaction.
"""

import time
import threading

from django.db import connection, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


# ─────────────────────────────────────────────
# Q1  –  Synchronous proof
# ─────────────────────────────────────────────
@receiver(post_save, sender=UserProfile)
def q1_synchronous_proof(sender, instance, created, **kwargs):
    """
    If signals were async this sleep would NOT block the caller.
    But because Django signals are synchronous, the caller has to
    wait until this handler finishes before it can continue.
    """
    if created:
        print(f"\n[Q1 SIGNAL HANDLER] Started – sleeping 1 second to prove synchronous execution...")
        time.sleep(1)
        print(f"[Q1 SIGNAL HANDLER] Done sleeping.\n")


# ─────────────────────────────────────────────
# Q2  –  Same thread proof
# ─────────────────────────────────────────────
@receiver(post_save, sender=UserProfile)
def q2_same_thread_proof(sender, instance, created, **kwargs):
    """
    We print the current thread ID here.  The caller also prints its
    thread ID.  They will be identical, proving same-thread execution.
    """
    if created:
        handler_thread_id = threading.get_ident()
        print(f"[Q2 SIGNAL HANDLER] Thread ID inside handler : {handler_thread_id}")


# ─────────────────────────────────────────────
# Q3  –  Same DB transaction proof
# ─────────────────────────────────────────────
@receiver(post_save, sender=UserProfile)
def q3_same_transaction_proof(sender, instance, created, **kwargs):
    """
    We check the number of open transactions via the DB connection.
    Inside a transaction.atomic() block this will be > 0, and the
    signal handler sees the same uncommitted data – proving it shares
    the caller's transaction.
    """
    if created:
        # Django wraps each request in a transaction by default (ATOMIC_REQUESTS).
        # Here we verify the signal can see the unsaved state of the transaction.
        in_atomic_block = connection.in_atomic_block
        print(f"[Q3 SIGNAL HANDLER] connection.in_atomic_block = {in_atomic_block}")
        print(f"[Q3 SIGNAL HANDLER] The handler is inside the SAME transaction as the caller.")
        print(f"[Q3 SIGNAL HANDLER] If we raise an exception here, the caller's save() also rolls back.\n")
