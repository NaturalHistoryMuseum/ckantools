# !/usr/bin/env python
# encoding: utf-8

from functools import wraps

from ckan.plugins import toolkit


def auth(proxy=None, keymapping=None, anon=False):
    def wrapper(function):
        function.is_auth = True
        if anon:
            function = toolkit.auth_allow_anonymous_access(function)

        @wraps(function)
        def wrapped(context, data_dict):
            if proxy:
                check(proxy, context, data_dict, keymapping)
            return function(context, data_dict)

        return wrapped

    return wrapper


def check(proxy, context, data_dict, keymapping=None):
    '''
    Check that the current user has the given access in the given context. The resource id is
    extracted from the data dict and therefore must be present.

    :param proxy: the name of the other auth function to check
    :param context: the context dict
    :param data_dict: the data dict
    :param keymapping: a dict of data_dict key to auth function key, e.g. if the proxied function requires 'id' but the
                       data_dict contains that value as 'resource_id'
    :return: a dict containing a "success" key with a boolean value indicating whether the current
             user has the required access. If the user does not then an additional "msg" key is
             returned in this dict which contains a user-friendly message.
    '''
    data_dict_copy = data_dict.copy() if data_dict else {}
    keymapping = keymapping or {}
    for k, v in keymapping.items():
        if k is None:
            del data_dict_copy[v]
        else:
            data_dict_copy[v] = data_dict_copy[k]

    user = context.get('user')
    authorized = toolkit.check_access(proxy, context, data_dict_copy)

    if authorized:
        return {'success': True}
    else:
        return {
            'success': False,
            'msg': toolkit._(f'User {user} not authorised to perform this action.')
        }


def is_auth(function):
    '''
    Determines whether the given function is an auth function or not. This is simply based on the existance
    of the is_auth attribute which is set in the decorator above.

    :param function: the function to check
    :return: True if the function is an auth function, False if not
    '''
    return getattr(function, 'is_auth', False)
