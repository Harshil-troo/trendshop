

def is_seller(user):
    return user.is_authenticated and user.user_types == 'seller'