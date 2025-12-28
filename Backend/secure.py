import secrets
print(secrets.token_hex(64))   # 128 characters (512-bit secret)

import secrets
print(secrets.token_urlsafe(32))
