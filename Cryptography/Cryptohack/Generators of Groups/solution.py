from sympy import primefactors

p = 28151
phi = p - 1
factors = primefactors(phi)

def is_primitive_root(g):
    for q in factors:
        if pow(g, phi // q, p) == 1:
            return False
    return True

# Find the smallest primitive root
for g in range(2, p):
    if is_primitive_root(g):
        print(f"The smallest primitive root modulo {p} is {g}")
        break
