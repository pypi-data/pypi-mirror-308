from .models import MailTemplate
from typing import Dict, Any

from django.template import Context, Template


def get_mail_template(name: str, params: Dict[str, Any]) -> Dict[str, str]:
    mail_template = MailTemplate.objects.get(name=name)
    context = Context(params)
    return {
        "name": mail_template.name,
        "subject": Template(mail_template.subject).render(context),
        "body": Template(mail_template.body).render(context),
        "html": Template(mail_template.html).render(context),
    }
