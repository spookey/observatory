from flask import render_template_string
from wtforms.widgets import HTMLString, html_params
from wtforms.widgets.core import escape_html


class SubmitButtonInput:
    input_type = 'submit'

    def __init__(self, icon=None, classreplace_kw=None):
        self.icon = icon
        self.classreplace_kw = classreplace_kw

    def render_icon(self):
        if self.icon is None:
            return ''

        return render_template_string('''
{% from '_macros/elem.html' import text_icon %}{{ text_icon(icon) }}
        '''.strip(), icon=self.icon)

    def replace_class(self, **kwargs):
        if self.classreplace_kw is None:
            return kwargs

        class_ = ' '.join((
            kwargs.setdefault('class', ''),
            kwargs.setdefault('class_', ''),
            kwargs.setdefault('class__', '')
        )).strip()
        del kwargs['class']
        del kwargs['class__']

        for orig, repl in self.classreplace_kw.items():
            class_ = class_.replace(orig, repl)
        kwargs['class_'] = class_.strip()

        return kwargs

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        kwargs = self.replace_class(**kwargs)

        return HTMLString('''
<button {params}>{icon}<span>{text}</span></button>
        '''.strip().format(
            params=html_params(name=field.name, **kwargs),
            icon=self.render_icon(),
            text=escape_html(field.label.text),
        ))
