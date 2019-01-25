
PY2 = hasattr(dict, 'iteritems')

def unexpression_adder(appendable):
    def dec(unexpression):
        appendable.append(unexpression.__name__)
        return unexpression

    return appendable, dec

def pairfmt(pair):
    return '{},{}'.format(*pair)

def pairsfmt(pairs):
    return ' '.join(map(pairfmt, pairs))

def attrs_to_xml(dct):
    """Booleans are caught so that they do not convert to "True" and "False."
    So, if you have a subclass of bool that you don't want converted to an
    int, wrap it and delegate __str__() or __format__().
    """
    return ' '.join(['{}="{}"'.format(k, int(v) if
        isinstance(v, bool) else v) for k,v in dct.items()])
