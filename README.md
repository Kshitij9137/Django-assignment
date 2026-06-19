# Accuknox Django Assignment

This Django project covers two topics:
1. **Django Signals** – Q1, Q2, Q3 with working proofs
2. **Custom Classes in Python** – Rectangle class

---

## Project Structure

```
accuknox_assignment/
├── accuknox_assignment/       # Project config
│   ├── settings.py
│   └── urls.py
├── signals_demo/              # Topic 1: Django Signals
│   ├── models.py              # UserProfile model
│   ├── signals.py             # Signal handlers (proofs for Q1, Q2, Q3)
│   ├── views.py               # Demo views
│   └── urls.py
├── custom_classes/            # Topic 2: Custom Classes
│   ├── rectangle.py           # Rectangle class implementation
│   └── views.py               # Demo view
└── manage.py
```

---

## Setup

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

---

## Topic 1 – Django Signals

### Q1: Are Django signals synchronous or asynchronous?

**Answer: Synchronous.**

Django signals are executed synchronously by default. When `send()` is called (or a model is saved), every connected receiver runs to completion *before* control returns to the caller.

**Proof endpoint:** `GET /signals/q1/`

The signal handler sleeps for 1 second. The view measures elapsed time – it will always be ≥ 1s, proving the caller blocked waiting for the handler. If signals were async, elapsed time would be ~0ms.

**Key code in `signals_demo/signals.py`:**
```python
@receiver(post_save, sender=UserProfile)
def q1_synchronous_proof(sender, instance, created, **kwargs):
    if created:
        print("Signal handler sleeping 1 second...")
        time.sleep(1)   # Caller is BLOCKED during this sleep
        print("Signal handler done.")
```

---

### Q2: Do Django signals run in the same thread as the caller?

**Answer: Yes, same thread.**

The signal handler executes in the exact same OS thread as the code that triggered the signal.

**Proof endpoint:** `GET /signals/q2/`

Both the view and the signal handler print `threading.get_ident()`. The two values are always identical.

**Key code in `signals_demo/signals.py`:**
```python
@receiver(post_save, sender=UserProfile)
def q2_same_thread_proof(sender, instance, created, **kwargs):
    if created:
        print(f"Thread ID in handler : {threading.get_ident()}")
        # This matches the thread ID printed in the caller view
```

---

### Q3: Do Django signals run in the same database transaction as the caller?

**Answer: Yes, same transaction.**

By default, signal handlers participate in the same database transaction as their caller. If the caller is inside `transaction.atomic()`, the handler is too – meaning a rollback in either place rolls back both.

**Proof endpoint:** `GET /signals/q3/`

The handler checks `connection.in_atomic_block` (True when inside a transaction). The rollback demo shows that a record saved inside `atomic()` doesn't persist if an exception is raised after it.

**Key code in `signals_demo/signals.py`:**
```python
@receiver(post_save, sender=UserProfile)
def q3_same_transaction_proof(sender, instance, created, **kwargs):
    if created:
        # True when caller is inside transaction.atomic()
        print(f"in_atomic_block = {connection.in_atomic_block}")
```

---

## Topic 2 – Custom Classes in Python

### Rectangle Class

Located at `custom_classes/rectangle.py`.

**Requirements met:**
1. Initialized with `length: int` and `width: int`
2. Instance is iterable (`__iter__` implemented)
3. Iteration yields `{'length': VALUE}` first, then `{'width': VALUE}`

**Implementation:**
```python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}
```

**Usage:**
```python
rect = Rectangle(10, 5)
for item in rect:
    print(item)
# {'length': 10}
# {'width': 5}
```

**Demo endpoint:** `GET /custom/rectangle/?length=10&width=5`

---

## API Endpoints Summary

| Endpoint | Description |
|---|---|
| `/signals/q1/` | Proves signals are synchronous (1s sleep demo) |
| `/signals/q2/` | Proves signals run in same thread (thread ID match) |
| `/signals/q3/` | Proves signals share same DB transaction (atomic rollback) |
| `/custom/rectangle/?length=10&width=5` | Demonstrates Rectangle iteration |
