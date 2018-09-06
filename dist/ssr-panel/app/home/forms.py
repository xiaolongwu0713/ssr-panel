from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, validators
from wtforms.validators import DataRequired,ValidationError

class LoginForm(FlaskForm):
    name = StringField(label="username",validators=[DataRequired("input username")],
        render_kw={"placeholder":"your username"}
    )
    pwd = PasswordField(label='password',validators=[DataRequired('input your password')],
        render_kw={'placeholder':"your password"}
    )

class RegForm(FlaskForm):
    name = StringField(label="username",validators=[DataRequired("input username")],
        render_kw={"placeholder":"your username"}
    )
   #pwd = PasswordField(label='password',validators=[DataRequired('input your password'),EqualTo('confirm', message='Password must match')],
    #    render_kw={'placeholder':"your password"}
    #)
    pwd = PasswordField('New Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Password must match')],
    	render_kw={"placeholder":"password"})
    #confirm = PasswordField(label='Repeat password',validators=[DataRequired('confirm password')],
    #    render_kw={'placeholder':"confirm password"}
    #)
    confirm = PasswordField('Repeat password',[validators.DataRequired()],
    	render_kw={"placeholder":"confirm your password"})

class SettingForm(FlaskForm): # reset user password
    password = StringField(label='password',validators=[DataRequired('请输入管理员密码')],
        render_kw={"class":"tpl-form-input","id":"password"}
    )