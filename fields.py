#-*- coding: utf-8 -*-

from django import forms
from django.core.validators import ValidationError
from django.db import models
from django.forms import fields
from testing.forms import URLFieldForm


"""
full_url = URLField(default_protocol="http", protocols=["https","ssh","mailto"])
url = URLField()


"""



class URLField(models.Field):
    description = "URL Field"
    __metaclass__ = models.SubfieldBase

    def __init__(self,default_protocol="http",protocols=[], *args, **kwargs):
        kwargs['max_length'] = kwargs.get("max_length",4096)
        self.default_protocol = default_protocol
        if type(protocols) is list:
            self.protocols = protocols
        else:
            raise ValueError("protocols must be a list")
        super(URLField,self).__init__(*args,**kwargs)

    def to_python(self, value):
        if not value:
            return ""
        elif isinstance(value, basestring):
            return value

    def db_type(self,connection):
        return "VARCHAR(%s)" % (self.max_length,) 

    def formfield(self, **kwargs):
        defaults = {'form_class':URLFieldForm}
        defaults['default_protocol'] = self.default_protocol
        defaults['protocols'] = self.protocols
        defaults.update(kwargs)
        return super(URLField,self).formfield(**defaults)
        
    def get_prep_value(self, value):
        if not value:
            return None
        else:
            url_parts = str(value).split("://")
            if len(url_parts) == 1:
                value = "%s://%s" % (self.default_protocol,value)  
                return value                                   
            elif len(url_parts) == 2:                              
                if url_parts[0].lower() in self.protocols or\
                   url_parts[0].lower() == self.default_protocol:
                    if url_parts[1]:
                        return value                                   
                    else:
                        raise forms.ValidationError("Must supply more than just a protocol.")
                else:
                    raise forms.ValidationError("Not a well formatted URL")
            else:
                raise forms.ValidationError("Not a well formatted URL")


class URLFieldForm(fields.CharField):
    """
    docstring
    """
    def __init__(self,*args, **kwargs):
        self.default_protocol=kwargs.pop("default_protocol","http")
        self.protocols = kwargs.pop("protocols",[])
         
        dwargs = {
            'required':False,
            'label':None,
            'blank':True,
            'initial':None,
            'help_text':None,
            'error_messages':None,
            'show_hidden_initial':None,
        }
        for attr in dwargs:
            if attr in kwargs:
                dwargs[attr] = kwargs[attr]

        super(URLFieldForm,self).__init__(*args,**kwargs)

    def clean(self,value):
        if not value:
            return None
        else:
            url_parts = value.split("://")
            if len(url_parts) == 1:
                value = "%s://%s" % (self.default_protocol,value)
                return value
            elif len(url_parts) == 2:
                if url_parts[0].lower() in self.protocols or\
                   url_parts[0].lower() == self.default_protocol:
                    if url_parts[1]:
                        return value
                    else:
                        raise forms.ValidationError("Must supply more than just a protocol.")
                else:
                    acceptable = self.protocols
                    acceptable.insert(0,self.default_protocol)
                    raise forms.ValidationError("Protocol not accepted. (%s) MUST BE %s" % (url_parts[0],acceptable))
            else:
                raise forms.ValidationError("Not acceptable URL")
