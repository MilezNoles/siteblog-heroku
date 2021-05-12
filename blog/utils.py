# функции для отправки на почту
def get_mail_subject(nick):
    return f"{nick}, Welcome to my blog"


def get_mail_context(nick, email, password):
    return f"Hello, {nick}!\n" \
           f"Congrats! You have successfully register at our project  !\n" \
           f"Here your register data:\n" \
           f"Login: {nick}\n" \
           f"Email: {email}\n" \
           f"Password: {password}\n"

def normalizer_bd(word):
    """
    заменяет "-" на " "
    и делает все заглавными
     буквами(для единого вида)
    """
    return word.replace("-"," ").title()