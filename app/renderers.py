"""
This file contains the custom renderers for Quillts
"""
from misaka import HtmlRenderer, SmartyPants
import jinja2
import re

class JinjaPreprocessor(object):
    def preprocess(self, text):
        """
        Preprocess the text looking for Jinja templates
        """
        return jinja2.Template(text).render()

class WikiPreprocessor(object):
    def preprocess(self, text):
        """
        Convert [[linkname]] to [linkname](/link/)
        """
        p = re.compile('\[\[([^\]]+)\]\]')
        
class QuilltRenderer(HtmlRenderer, SmartyPants, JinjaPreprocessor):
    pass