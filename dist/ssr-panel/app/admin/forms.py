from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,ValidationError
class AddportForm(FlaskForm):
    # port = StringField(label="portnumber",validators=[DataRequired("请输入SSR端口")],
    # port will accept a value from {{form.port}} in portlist.html using add port but.
    port = StringField(label="portafa",validators=[DataRequired()],
        render_kw={"placeholder":"请输入新SSR端口dd","class":"tpl-form-input"}
    )
    # pwd = PasswordField(label='password',validators=[DataRequired('请输入新SSR端口密码')],
    # pwd will accept a value from {{form.pwd}} in portlist.html using add port but
    pwd = PasswordField(label='pwdas',validators=[DataRequired('请输入新SSR端口密码')],
        render_kw={'placeholder':"请输入密码dd","class":"tpl-form-input"
        }
    )

class AdduserForm(FlaskForm):
    name = StringField(label="username",validators=[DataRequired("请输入用户名")],
        render_kw={"placeholder":"请输入用户名","class":"tpl-form-input"}
    )
    pwd = PasswordField(label='password',validators=[DataRequired('请输入密码')],
        render_kw={'placeholder':"请输入密码","class":"tpl-form-input"}
    )
#Login Form
class LoginForm(FlaskForm):
    name = StringField(label="username",validators=[DataRequired("请输入管理员账号")],
        render_kw={"placeholder":"请输入管理员账号"}
    )
    pwd = PasswordField(label='password',validators=[DataRequired('请输入管理员密码')],
        render_kw={'placeholder':"请输入管理员密码"}
    )
class SettingForm(FlaskForm):
    username = StringField(label="username",validators=[DataRequired("请输入管理员账号")],
        render_kw={"class":"tpl-form-input","id":"username"}
    )
    password = StringField(label='password',validators=[DataRequired('请输入管理员密码')],
        render_kw={
            "class":"tpl-form-input",
            "id":"password"
        }
    )
    host = StringField(
        label="username",
        validators=[
            DataRequired("请输入SSR服务器")
        ],
        render_kw={
            "class":"tpl-form-input",
            "id":"host"
        }
    )

