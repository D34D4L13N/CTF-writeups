## Let’s walk through it manually via netcat:
### Step 1: Connect
- nc socket.cryptohack.org 13371
You’ll get:
- {"p": "...", "g": "...", "A": "..."}
- Send to Bob:

### Step 2: Send p instead of A
Just copy the p value exactly and paste it in as the A:
- {"A": "the_same_value_as_p"}

### Step 3: Receive Bob’s response
You’ll receive:
- {"B": "..."}
- Send to Alice:

### Step 4: Again, send p as Bob’s public key:
- {"B": "the_same_value_as_p"}

### Step 5: Get the encrypted flag
You’ll receive a JSON with:
{
  "iv": "...",
  "encrypted": "..."
}




