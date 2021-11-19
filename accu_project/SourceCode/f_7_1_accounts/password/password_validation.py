from string import ascii_uppercase, ascii_lowercase, digits
from django.core.exceptions import ValidationError


def contain_any(target, condition_list):
    return any([i in target for i in condition_list])

class CustomValidator:
    message = "パスワードは半角英語数字8文字以上で（大小英字、数字）全てを組み合わせて設定してください。"
    def validate(self, password, user=None):
        is_valid = True
        if len(password) < 8:
            is_valid = False
        
        if not all([contain_any(password, ascii_lowercase),
                    contain_any(password, ascii_uppercase),
                    contain_any(password, digits)]):
            is_valid = False

        if not is_valid:
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message