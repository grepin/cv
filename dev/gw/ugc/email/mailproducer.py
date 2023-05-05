from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader


def html_message(
        mail_from: str,
        mail_to: str,
        subject: str,
        template_name: str,
        **kwargs
) -> EmailMessage:
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    output = template.render(kwargs)

    msg.add_alternative(output, subtype='html')

    return msg
