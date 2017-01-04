from pyramid.view import view_config


from ..models import MyModel

from pyramid.httpexceptions import HTTPFound

from pyramid_gist.security import check_credentials
from pyramid.security import remember, forget
from passlib.apps import custom_app_context as pwd_context


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home_view(request):
    return {}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        query = request.dbsession.query(MyModel)
        user_found = query.filter(MyModel.username == request.matchdict['username']).first()
        if user_found is not None:
            real_password = user_found.hashed_password
            password = password
            if check_credentials(password, real_password):
                auth_head = remember(request, username)
            return HTTPFound(
                location=request.route_url("home"),
                headers=auth_head
            )

    return {}


@view_config(
    route_name='logout',
    renderer='../templates/logout.jinja2',
    permission="logout")
def logout_view(request):
    auth_head = forget(request)
    return HTTPFound(location=request.route_url("home"), headers=auth_head)


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        favorite_food = request.POST["favorite_food"]
        new_user = MyModel(
            username=username,
            hashed_password=pwd_context.hash(password),
            email=email,
            first_name=first_name,
            last_name=last_name,
            favorite_food=favorite_food)
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_gist_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
