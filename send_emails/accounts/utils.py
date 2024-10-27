from django.core.mail import get_connection

def get_user_email_connection(email, password):
    print(email, password)
    return get_connection(
        host="smtp.gmail.com",
        port=587,
        username=email,
        password=password,
        use_tls=True
    )
