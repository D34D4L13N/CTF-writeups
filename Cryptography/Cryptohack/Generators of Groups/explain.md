**The Problem (in Simple Words):**
You are working in a finite field — that's just a set of numbers from 0 to p-1, where p is a prime number (in this case, p = 28151).

**You're being asked:**
Find the smallest number g (greater than 1) such that:
When you raise g to different powers, like g^1, g^2, g^3, ..., g^(p-2), and take the result modulo p, you get all the numbers from 1 to p-1 in some order.
That kind of special number g is called a primitive root or generator of the field 𝔽ₚ.

**What Does a Primitive Root Do?**
et’s say p = 7. Then p - 1 = 6. We want to find a number g such that:
```python
g^1 mod 7
g^2 mod 7
g^3 mod 7
g^4 mod 7
g^5 mod 7
g^6 mod 7 == 1 (always true)```
And all the results of g^1 to g^5 mod 7 should give us: 1, 2, 3, 4, 5, 6 (in some order). If that happens, then g is a primitive root.

**How Do We Test If g is a Primitive Root?**
Compute phi = p - 1 = 28150.
Factor phi (find its prime factors).
For each factor q, check:
if g^(phi / q) mod p == 1:
    g is NOT a primitive root
If it’s not equal to 1 for all factors q, then g is a primitive root.
