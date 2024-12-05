import base64


def str_to_base_64(_str: str) -> str:
    """
    Method that encodes a string into a Base64 string.
    :param _str: string to be encoded
    :return: base64 string
    """
    return base64.b64encode(_str.encode("utf-8")).decode("utf-8").replace("=", "%3D")
