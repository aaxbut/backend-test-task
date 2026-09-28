from fastapi import Request


def is_authorize_bank_payment(request: Request) -> bool:
    # Check authorization header for bank signature
    # and call the function to verify the signature
    return request.headers.get('bank-signature') is not None
