import hashlib

m = hashlib.sha256()

m.update((b"\u1F435\u211A\u211A\u211D\u211D\u03BC\u30BC\u2122\uFF38\uFF38\u03C0\u1F648"))

print(m.digest())

