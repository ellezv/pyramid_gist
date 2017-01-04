import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel
from passlib.apps import custom_app_context as pwd_context

TEST_USERS = [
    {
        "username": "test",
        "hashed_password": "password",
        "email": "test@email.com",
        "first_name": "test first name",
        "last_name": "test last name",
        "favorite_food": "test fav food"
    },
    {
        "username": "test2",
        "hashed_password": "password",
        "email": "test2@email.com",
        "first_name": "test2 first name",
        "last_name": "test2 last name",
        "favorite_food": "test2 fav food"
    }
]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

    for user in TEST_USERS:
        model = MyModel(
            username=user["username"],
            hashed_password=pwd_context.hash(user["hashed_password"]),
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            favorite_food=user["favorite_food"]
        )
        dbsession.add(model)
