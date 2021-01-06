from random import choice

from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.space_drop import (
    SpaceDropCamForm,
    SpaceDropKeymastersForm,
    SpaceDropLinksForm,
    SpaceDropMembershipPlansForm,
    SpaceDropProjectsForm,
)
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


def form_drop(form, *, keys):
    def res():
        pass

    res.form = form
    res.keys = keys

    return res


FORMS = [
    form_drop(
        SpaceDropCamForm,
        keys=['cam'],
    ),
    form_drop(
        SpaceDropKeymastersForm,
        keys=[
            'contact.keymasters.name',
            'contact.keymasters.irc_nick',
            'contact.keymasters.phone',
            'contact.keymasters.email',
            'contact.keymasters.twitter',
            'contact.keymasters.xmpp',
            'contact.keymasters.mastodon',
            'contact.keymasters.matrix',
        ],
    ),
    form_drop(
        SpaceDropProjectsForm,
        keys=['projects'],
    ),
    form_drop(
        SpaceDropLinksForm,
        keys=[
            'links.name',
            'links.description',
            'links.url',
        ],
    ),
    form_drop(
        SpaceDropMembershipPlansForm,
        keys=[
            'membership_plans.name',
            'membership_plans.value',
            'membership_plans.currency',
            'membership_plans.billing_interval',
            'membership_plans.description',
        ],
    ),
]
IDS = [drop.form.__name__ for drop in FORMS]


@mark.usefixtures('session', 'ctx_app')
class TestSpaceDropCommons:
    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_edit_keys(drop):
        assert drop.form.KEYS == drop.keys

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_basic_fields(drop):
        form = drop.form(idx=0)
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_form_idx(drop):
        idx = choice(range(23, 42))
        form = drop.form(idx=idx)
        assert form.idx == idx

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_submit_button(drop):
        idx = choice(range(23, 42))
        form = drop.form(idx=idx)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_delete'
        assert form.submit.widget.classreplace_kw == {
            'is-dark': 'is-danger is-small'
        }

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_invalid(drop):
        form = drop.form(idx=None)
        assert form.validate() is False
        assert form.action() is None

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_empty_action(drop):
        form = drop.form(idx=0)
        assert form.validate() is True
        assert form.action() is None

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_delete(drop):
        idx = choice(range(23, 42))
        elems = [
            Value.set(
                key=f'{SP_API_PREFIX}.{key}',
                idx=idx,
                value=choice(
                    [
                        choice(['test', 'demo']),
                        choice([True, False]),
                        choice(range(23, 42)),
                    ]
                ),
            )
            for key in drop.keys
        ]

        assert Value.query.all() == elems

        form = drop.form(idx=idx, submit=True)
        assert form.validate() is True
        assert form.action()

        assert Value.query.all() == []
