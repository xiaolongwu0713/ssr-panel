from . import home
from flask import render_template,session,template_rendered,url_for,flash,redirect,request
from app import create_app
from app.home.forms import LoginForm,SettingForm,RegForm
import os,json,time
from functools import wraps
import base64, operator
from subprocess import call
def readadmin():
    print(os.getcwd())
    f = open("config/admin.json", encoding='utf-8')
    setting = json.load(f)
    f.close()
    data = {
        "username":setting['username'],
        "password":setting['password'],
        "host":setting['host']
    }
    return data

def getuser():
    f = open("config/user.json", encoding='utf-8')
    setting = json.load(f)
    data = setting["userlist"]
    return data
def getport():
    f = open("/etc/shadowsocks/config.json", encoding='utf-8')
    setting = json.load(f)
    portdata = setting["port_password"]
    return portdata

def usernumber():
    f = open("/etc/shadowsocks/config.json", encoding='utf-8')
    setting = json.load(f)
    number = len(setting["port_password"])
    return number


def availablePort():
    f = open("/etc/shadowsocks/config.json", encoding='utf-8')
    userdata = json.load(f)
    #maxRec = max(userdata['userlist'], key=lambda ssr: ssr['ssr']['port'])
    #maxPort = maxRec['ssr']['port']
    #print (maxPort)
    maxPort = max(userdata['port_password'].items(), key=operator.itemgetter(0))[0]
    return maxPort

def home_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "username" in session and "password" in session:
            return f(*args , **kwargs)
        else:
            flash('请先登录！','error')
            return redirect(url_for('home.login',next = request.url))
    return decorated_function


@home.route('/')
def homepage():
    number = usernumber()
    return render_template("home/home.html", number = number)


@home.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        name = data['name']
        pwd = data['pwd']
        userdata = getuser()
        for user in userdata:
            if name == user['username'] and pwd == user['password']:
                session['username'] = user['username']
                session['password'] = user['password']
                return redirect(url_for('home.index'))
        flash("账号或密码错误","error")
    return render_template("home/login.html",form = form)


@home.route('/register',methods=['GET','POST'])
def register():
    form = RegForm()
    #print(genPort)
    if form.validate_on_submit():
    #if 1:
        #fdata = form.data
        #name = fdata['name']
        #pwd = fdata['pwd']
        userdata = getuser()
        #portdata = getport()
        # for user in userdata:
        #     if name == user['username'] and pwd == user['password']:
        #         session['username'] = user['username']
        #         session['password'] = user['password']
        #         return redirect(url_for('home.index'))
        # flash("账号或密码错误","error")
        genPort = int(availablePort()) + 1  #generate a new port number
        flash('Register completed and an SSR entry is automated generated for you. Enjoy.')
        newuserdata = {
            "username":form.data['name'],
            "password":form.data['pwd'],
            "port":str(genPort)
        }

        userdata.append(newuserdata)

        #newPort = {str(genPort), form.data['pwd']}
        #print(newuserdata)
        #portdata.port_password = newPort
        #print(userdata)
        f = open("/etc/shadowsocks/config.json", encoding='utf-8')
        setting = json.load(f)
        setting['port_password'][genPort]=form.data['pwd']
        data = {
             "userlist":userdata
        }
        print(data)
        print(setting)
        json.dump(data,open("config/user.json" ,"w"),ensure_ascii=False)
        json.dump(setting,open("/etc/shadowsocks/config.json" ,"w"),ensure_ascii=False)
        shutdownsss = '/usr/python/bin/python3.6 /usr/python/bin/ssserver --log-file /home/python/ssr-panel/ss.log --pid-file /home/python/ssr-panel/ss.pid -c /etc/shadowsocks/config.json -d stop'
        startsss = '/usr/python/bin/python3.6 /usr/python/bin/ssserver --log-file /home/python/ssr-panel/ss.log --pid-file /home/python/ssr-panel/ss.pid -c /etc/shadowsocks/config.json -d start'
        #time.sleep(5)
        print("sleep done")
        #return render_template('home/waitforsss.html', string = 'Wait for 5 seconds')
        return render_template('home/afterRegister.html', portnum=genPort) # login after your registration 
        os.system(shutdownsss)
        os.system(startsss)
    else:
        flash(u'Input error, please try again.','error')
        return render_template("home/register.html",form = form)

@home.route('/afterRegister',methods=['GET','POST'])
def afterRegister():
    return render_template('home/afterRegister.html')

@home.route('/list')
@home_login_req
def index():
    userData = getuser()
    admindata = readadmin()
    ssrdata = {}

    for user in userData:
        if user['username'] == session["username"] and user['password'] == session["password"]:
            ssrdata['port'] = user['port']
            ssrdata['method'] = "aes-256-cfb"
            ssrdata['protocol'] = "origin"
            ssrdata['obfs'] = "plain"

    ctx = {
        "ssrdata":ssrdata,
        "host":admindata['host'],
        "qrcode":"error"
    }
    return render_template("home/index.html",**ctx)

@home.route('/setting',methods = ["GET","POST"])
@home_login_req
def setting(): #reset user password
    form = SettingForm()
    ctx = {
        "data":session["password"]
    }
    if form.validate_on_submit():
        data = form.data
        userdata = getuser()
        for user in userdata:
            if user['username'] == session["username"]:
                user["password"] = data["password"]  # update userlist
        taskdata = {
            "userlist":userdata # update userlist
        }
        json.dump(taskdata,open("/etc/shadowsocks/config.json" ,"w"),ensure_ascii=False)
        session.pop("username") #delete user in session dict
        session.pop("password")
        return redirect(url_for('home.login')) # login after you reset your password
    return render_template("home/setting.html",form = form,**ctx)

@home.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username')
    session.pop("password")
    return redirect(url_for('home.login'))