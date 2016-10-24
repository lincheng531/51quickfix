#!/user/bin/env python
#encoding:utf-8
from django import forms
from django.forms import Widget
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt

class SelectatorWidget(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices={}):
        self.choices = choices
        self.attrs = choices
        super(SelectatorWidget, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None):
        html = ['<script type="text/javascript" src="/static/js/fm.selectator.jquery.js"></script>']
        html.append('<link rel="stylesheet" href="/static/css/fm.selectator.jquery.css" type="text/css" />')
        html.append('<script type="text/javascript">')
        html.append('$(document).ready(function(){')
        html.append('$("#id_'+name+'").selectator({')
        html.append('prefix: "selectator_", ')      
        html.append('height: "30px",')                 
        html.append('useDimmer: false,')                 
        html.append('useSearch: true,') 
        html.append('keepOpen: false, ') 
        html.append('showAllOptionsOnFocus: true, ')   
        html.append('selectFirstOptionOnSearch: true') 
        html.append('});') 
        html.append('})') 
        html.append('</script>') 
        html.append('<div multiple id="id_{}" style="line-height:30px!import">'.format(name))
        for index, choice in enumerate(self.choices):
            che = ''
            if value and str(choice[0]) in value: che = 'checked=checked'
            html.append('<input id="id_{}_{}" multiple="" name="{}" type="checkbox" value="{}" dval="{}" {}>{}'.format(index, name, name, choice[0], choice[1], che, choice[1]))
        html.append('</div>')
        return mark_safe(''.join(html))
