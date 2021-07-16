from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


# 使用wtforms做参数校验
class SearchForm(Form):
    # DataRequired 不能为空，必须传入
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
