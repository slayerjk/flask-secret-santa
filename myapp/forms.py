from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length 

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class WishlistForm(Form):
    wishlist_text =TextAreaField('Your Wishlist',validators=[DataRequired(), Length(max=200)])

class RunLotteryForm(Form):
    run_lottery = BooleanField('Run Lottery?', validators=[DataRequired()])

class ClearLotteryTableForm(Form):
    clear_lottery_table = BooleanField('Clear Lottery Table?', validators=[DataRequired()])