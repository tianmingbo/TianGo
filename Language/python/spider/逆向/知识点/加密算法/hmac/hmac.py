import hashlib
import hmac

key = 'salt'.encode()
text = 'tian'.encode()
mac = hmac.new(key, text, hashlib.sha256)
mac.digest()
mac.hexdigest()
