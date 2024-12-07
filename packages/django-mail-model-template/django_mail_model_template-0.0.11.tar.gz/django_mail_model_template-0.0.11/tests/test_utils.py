from django.test import TestCase
from django_mail_model_template.models import MailTemplate
from django_mail_model_template.utils import get_mail_template


class MailTemplateTest(TestCase):
    def test_get_main_template(self):
        MailTemplate.objects.create(
            name="main",
            subject="main subject {{ name }}",
            body="main body {% if name %}{{ name }}{% endif %}",
            html="<p>main html {{ name }}</p>",
        )
        params = {"name": "yamada"}
        result = get_mail_template("main", params)
        self.assertEqual(result["subject"], "main subject yamada")
        self.assertEqual(result["body"], "main body yamada")
        self.assertEqual(result["html"], "<p>main html yamada</p>")
