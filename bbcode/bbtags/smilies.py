from bbcode import *
from bbcode import settings
import re

smilies_to_class = {
        'lol': 'laugh',
        'smilie': 'happy',
        'wink': 'wink',
        'razz': 'tongue',
        'eek': 'surprised',
        'sad': 'unhappy',
        'grin': 'grin',
        'neutral': 'displeased',
        }

class AlternativeSmilie(SelfClosingTagNode):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'alias'):
            self.alias = self.__class__.__name__.lower()
        SelfClosingTagNode.__init__(self, *args, **kwargs)

    def parse(self):
        class_ = smilies_to_class[self.alias]
        return '<i class="fe fe-emo-%s"></i>' % class_

@register
class LOL(AlternativeSmilie):
    # :D, :-D, :-d, :d
    open_pattern = re.compile(':-?(D|d)')

@register
class  Smilie(AlternativeSmilie):
    # :), :-)
    open_pattern = re.compile(':-?\)')

@register
class Wink(AlternativeSmilie):
    # ;), ;-), ;-D, ;D, ;d, ;-d
    open_pattern = re.compile(';-?(\)|d|D)')

@register
class Razz(AlternativeSmilie):
    # :P, :-P, :p, :-p
    open_pattern = re.compile(':-?(P|p)')

@register
class Eek(AlternativeSmilie):
    # o_O....
    open_pattern = re.compile('(o|O|0)_(o|O|0)')

@register
class Sad(AlternativeSmilie):
    # :-(, :(
    open_pattern = re.compile(':-?\(')

@register
class Crying(AlternativeSmilie):
    # ;_;, :'(, :'-(
    open_pattern = re.compile("(;_;|:'-?\()")

@register
class Grin(AlternativeSmilie):
    # xD, XD, *g*
    open_pattern = re.compile('(xD|XD|\*g\*)')

@register
class Neutral(AlternativeSmilie):
    # :-|, :|
    open_pattern = re.compile('(:-?\|)')
