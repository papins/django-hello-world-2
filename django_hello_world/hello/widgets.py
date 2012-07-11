# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from datetime import datetime


class CalendarWidget(forms.DateInput):
    class Media:
        css = {
            'all': (settings.STATIC_URL +
                    "css/jquery/smoothness/jquery-ui-1.8.21.custom.css",)
        }
        js = (
            settings.STATIC_URL + "js/jquery-1.7.2.min.js",
            settings.STATIC_URL + "js/jquery-ui-1.8.21.custom.min.js",
        )

    def __init__(self, params='', attrs=None):
        self.params = params
        super(CalendarWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(CalendarWidget, self).render(name, value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({changeYear: true, changeMonth: true, yearRange:"1900:%d", %s});
            </script>''' % (name, datetime.now().year, self.params,))
