"""Module for verifying DSA signatures."""
import hashlib
def verify_sign(message, sign, p, q, g, y):
    """Function to verify a DSA signature."""
    r, s = sign
    if not (0 < r < q and 0 < s < q): # basic check
        return False

    hash_obj = hashlib.sha1(message.encode()) # hash again
    hash_v = int(hash_obj.hexdigest(), 16)

    w = pow(s, -1, q) # inverted s in power of q
    t1 = (hash_v * w) % q # weighting original value
    t2 = (r * w) % q # now weighting the imprint (kinda)
    valid = ((pow(g, t1, p) * pow(y, t2, p)) % p) % q # crazy formula to check the validity

    return valid == r
