# cyber_ops/yap.py

def yap(*args, **kwargs):
    """
    Custom Print Statement
    For my Codes
    With more Custom Options
    """
    prefix = "[CYBER-OPS]"
    message = " ".join(str(arg) for arg in args)
    formatted_message = f"{prefix} {message}"
    print(formatted_message, **kwargs)