#!/usr/bin/python

from simplegeneric import generic

def is_placeholder(obj):
    """True iff. obj is a placeholder
    >>> is_placeholder('abc')
    False

    >>> is_placeholder('?abc')
    True
    """
    return isinstance(obj, str) and obj.startswith("?")

def tmatch(template, value):
    """

    """
    if is_placeholder(template):
        return True, {template : value}
    else:
        return _sub_tmatch(template, value)


def tmatched(template, value):
    a, b = tmatch(template, value)
    return a

#def binding_match(template, value, env):
#    def clean(a):
#        return a.strip("?")
#    a, b = tmatch(template, value)


#    if a:


#        import inspect
#        stack = inspect.stack()
#        st_caller = stack[1]

#        loc = st_caller[0].f_locals
#        for k, v in b.items():
#            env[clean(k)] = v

#        print loc
#    return a

@generic
def _sub_tmatch(template, value):
    if type(template) == type(value):
        return tmatch(tuple(template), tuple(value))
    else:
        return False, {}


@_sub_tmatch.when_type(int, float, str)
def tmatch_builtin(template, value):
    if is_placeholder(template):
        return True, {template : value}
    else:
        return template == value, {}

@_sub_tmatch.when_type(tuple)
def tmatch_tuple(template, value):
    b = True
    d = {}

    if len(template) != len(value):
        return False, d

    for t, v in zip(template, value):
        rv, rd = tmatch(t,v)

        if not rv:
            return False, {}
        else:
            d.update(rd)

    return b, d

@_sub_tmatch.when_type(list)
def tmatch_list(template, value):
    def is_tail_marker(v):
        return isinstance(v, str) and v.startswith("|")

    d = {}
    capture = False

    for pos, t in enumerate(template):
        v = value[pos]

        if is_tail_marker(t):
            d[t] = value[pos:]
            break
        else:
            rv, rd = tmatch(t,v)

            if not rv:
                return False, {}
            else:
                d.update(rd)

    return True, d

@_sub_tmatch.when_type(dict)
def tmatch_dict(template, value):
    captured = { }

    value = dict( value )

    for t_key, t_value in template.items():
        #assert not (is_placeholder(t_key) and is_placeholder(value) )

        for k, v in value.items():
            a, b = tmatch(t_key, k)
            c, d = tmatch(t_value, v)
            if a and c:
                captured.update(b)
                captured.update(d)
                break
        else:
            return False, {}

        del value[k] # value should not matched again

    return True, captured
