import hashlib
PASSWORD = "abcdefg"
encoded=PASSWORD.encode()
result = hashlib.md5(encoded)
print("String : " + PASSWORD)
print("Hash Value : ")
print(result)
print("Hexadecimal equivalent: ",result.hexdigest())