from services.auth_service.service import Authentication
# example to autentication with jwt

authentication_service = Authentication()

access_token = authentication_service.encode_payload("algo@example", "sapee")
print(access_token)

data = authentication_service.decode_payload(access_token)
print(data)

# password hashing
password = "minibumer12"
password_hashed = authentication_service.hash_password(password)
print(password_hashed)

# verify password
is_verified = authentication_service.verify_password("minibumer1", password_hashed)
print("IS VERIFIED", is_verified)
