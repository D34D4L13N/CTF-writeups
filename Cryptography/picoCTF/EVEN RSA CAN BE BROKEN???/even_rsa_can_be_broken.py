from Crypto.Util.number import inverse, long_to_bytes
from sympy import factorint

# Given values
N = 18857420634248426774854664054335003846621455741244295255652268591079775355883058802572264798003352710899262140176051621427576040768159043041502226623013822
e = 65537
cipher = 16888794051406534213571494826859222666661906485017145360100255007689256358864290173931842965790316512572625757129689581749953467234104434625550563777107837

# Step 1: Factor N
factors = factorint(N)
assert len(factors) == 2, "Expected N to have exactly 2 prime factors"

p, q = list(factors.keys())

# Step 2: Compute φ(N)
phi = (p - 1) * (q - 1)

# Step 3: Compute private key d
d = inverse(e, phi)

# Step 4: Decrypt ciphertext
m = pow(cipher, d, N)

# Step 5: Convert to bytes and print
try:
    flag = long_to_bytes(m).decode()
except:
    flag = long_to_bytes(m)  # fallback if it's not valid utf-8

print("FLAG:", flag)
