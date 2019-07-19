
class KeywordToAttr(object):
    __slots__ = ()
    def __init__(self, **kw):
        for k,v in kw.items():
            setattr(self, k, v)

class AttrSerializer(KeywordToAttr):
    __slots__ = ( 'priority', 'chain', 'longDesc',
        'shortDesc', 'predicate', 'transformer' )
