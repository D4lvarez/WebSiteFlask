from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from WebSite.models import Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

# Rutas de aplicación y de usuario

@main.route('/home')
@login_required
def home():
    posts = Post.query.all()

    if current_user.is_authenticated:

        page = request.args.get('page', 1, type=int)

        return render_template('home.html', posts=posts)
        
    else:

        return redirect(url_for('users.login'))
