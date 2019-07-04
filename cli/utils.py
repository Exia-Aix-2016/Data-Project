from PyInquirer import Validator, ValidationError


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


def whenMenu(m):
    return lambda answers: answers['menu'] == m


def toInt(val): return int(val)


def toFloat(val): return float(val)
