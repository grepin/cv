import smtplib

# charset = 'Content-Type: text/plain; charset=utf-8'
# mime = 'MIME-Version: 1.0'
# body = '"From: welcome@info66.ru", "To: andrey@dyfor.ru", "Subject: welcome test",\
#         mime, charset, "", "Hi this is test"'
mes = """\
From: welcome@info66.ru
To: andrey@dynfor.ru
Subject: Hi there

This message is sent from Python."""
try:
    print("Start sending email")
    smtp = smtplib.SMTP("smtp.yandex.ru", 587)
    smtp.starttls()
# smtp.ehlo()

    smtp.login("welcome@info66.ru", "toelalwwhglkxwif")
    smtp.sendmail("From: welcome@info66.ru", "To: andrey@dynfor.ru", mes)
    print("Welcome email sent to andrey@d.")
except smtplib.SMTPException as err:
    print(f"Welcome email not sent to {err}")
finally:
    smtp.quit()
