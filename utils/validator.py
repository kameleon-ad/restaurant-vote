def auth_login_validator(data: dict):
    errors = {}
    if 'username' not in data:
        errors['username'] = 'Username is required'
    if 'password' not in data:
        errors['password'] = 'Password is required'
    return errors


def create_user_validator(data: dict):
    errors = {}
    if 'username' not in data:
        errors['username'] = 'Username is required'
    if 'password' not in data:
        errors['password'] = 'Password is required'
    if 'email' not in data:
        errors['email'] = 'Email is required'
    return errors
