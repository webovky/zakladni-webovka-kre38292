from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = b'\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0'b'\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0'


@app.route("/")
def index():
    return render_template("base.html.j2", a=12, b=3.14)

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        else:
            flash(
                f"Počkej, počkej hrdino, pro zobrazení této stránky ({request.path}) je nutné se přihlásit!",
                "err",
            )
            return redirect(url_for("login", next=request.path))
    wrapper.__name__=f.__name__
    wrapper.__doc=f.__doc__
    return wrapper

@app.route("/mcu/", methods=["GET"])
@login_required
def mcu():
    try:
        x = request.args.get("x") 
        y = request.args.get("y")
        soucet = int(x) + int(y)
    except TypeError:
        soucet = None
    except ValueError:
        soucet = "Nedělej si srandu!!!"
    
    slovo = request.args.get('slovo')
    if slovo:
        session['slovo'] = slovo

    return render_template("mcu.html.j2", soucet=soucet)


@app.route("/mcu/", methods=["POST"])
def mcu_post():
    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    print("POST:", jmeno, heslo)

    return redirect(url_for("mcu"))


@app.route("/stanlee/<parametr>")
def stanlee(parametr):
    return render_template("stanlee.html.j2", parametr=parametr)


@app.route("/spoilery/")
def spoilery():
    if "user" in session:
        return render_template("spoilery.html.j2")
    else:
        flash(f"POZOR! Nejsi přihlášen, aby jsis zobrazil ({request.path}) je nutné se přihlásit.","err")
        return redirect(url_for("login",next=request.path))

@app.route("/Login/", methods=("GET",))
def login():
    if request.method == "GET":
        login = request.args.get("nick")
        passwd = request.args.get("pswd")
    return render_template("login.html.j2")

@app.route("/Login/", methods=("POST",))
def login_post():
    login = request.form.get("nick")
    passwd = request.form.get("pswd")
    print(login,passwd)
    next=request.args.get("next")
    if login == "lofas" and passwd == "dingus":
        session["user"]=login
        flash("Vítej na stránce.","pass")
        if next:
            return redirect(next)
    else:
        flash("Přístup zamítnut, bohužel no, zkus to znova.","err")
    if next:
        return redirect(url_for("login"), next=next)
    else:
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.pop("user",None)
    flash("Tak zase někdy.","pass")
    return redirect(url_for("login"))
