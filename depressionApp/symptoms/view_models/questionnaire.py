from django import forms
from ..models import Questionnaire, Question, ResponseOption, UserResponse

class QuestionResponseForm(forms.Form):
    """Form for answering a single question in a questionnaire."""
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[str(question.id)] = forms.ChoiceField(
            label=question.question,
            choices=[(option.value, option.text) for option in question.response_options.all()],
            widget=forms.RadioSelect,
            required=True
        )