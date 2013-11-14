import re

smilie_html_format = '<i class="fe fe-emo-%s"></i>'
smilies_regexes = dict(map(lambda x: (x[1], smilie_html_format % x[1]),
        [(':-?(D|d)', 'laugh'),           # :D, :-D, :-d, :d
        (':-?\)', 'happy'),               # :), :-)
        (';-?(\)|d|D)', 'wink'),          # ;), ;-), ;-D, ;D, ;d, ;-d
        (':-?(P|p)', 'tongue'),           # :P, :-P, :p, :-p
        ('(o|O|0)_(o|O|0)', 'surprised'), # o_O
        (':-?\(', 'unhappy'),             # :-(, :(
        ('(xD|XD|\*g\*)', 'grin'),        # xD, XD, *g*
        ('(:-?\|)', 'displeased'),        # :-|, :|
        ]))
