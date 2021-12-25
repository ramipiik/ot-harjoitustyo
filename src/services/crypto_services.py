from repositories.crypto_repository import read_crypto_ids


def get_crypto_ids():
    """
    Service for fetching crypto-id's

    Returns:
        list: all crypto ids
    """
    crypto_ids = read_crypto_ids()
    return crypto_ids
