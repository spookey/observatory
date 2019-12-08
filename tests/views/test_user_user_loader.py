from pytest import mark

from stats.models.user import User
from stats.views.user import user_loader


@mark.usefixtures('session')
class TestUserLoader:

    @staticmethod
    def test_user_loader_no_user():
        assert user_loader(23) is None

    @staticmethod
    def test_user_loader(gen_user):
        user = gen_user()
        assert User.query.all() == [user]

        assert user_loader(user.prime) == user
