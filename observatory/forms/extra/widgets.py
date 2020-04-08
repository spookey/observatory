from jinja2 import Markup
from wtforms.widgets import SubmitInput

from observatory.start.environment import ICON

# pylint: disable=too-few-public-methods


class SubmitIconInput(SubmitInput):
    def __init__(self, *args, icon, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon

    @property
    def ri_icon(self):
        icon = ICON.get(self.icon, ICON['__fallback'])
        return f'ri-{icon}-line'

    def __call__(self, field, **kwargs):
        mkup = super().__call__(field, **kwargs)
        return Markup(f'''
{mkup.replace('<input ', '<button ')}
  <span class="icon">
    <i class="{self.ri_icon}" aria-hidden="true"></i>
  </span>
  <span>{field.label.text}</span>
</button>
        '''.strip())
