from rfc9290 import encode_problem_details, decode_problem_details

# Build Problem Details as a dictionary
problem_details = {
    "type": "https://example.com/error/validation-error",
    "title": "Validation Error",
    "detail": "Missing required field 'username'.",
    "instance": "/requests/12345",
    "response-code": 400
}

# Encode to CBOR
cbor_encoded = encode_problem_details(problem_details)
print("CBOR Encoded:", cbor_encoded)

# Decode back to dictionary
decoded_details = decode_problem_details(cbor_encoded)
print("Decoded Details:", decoded_details)
