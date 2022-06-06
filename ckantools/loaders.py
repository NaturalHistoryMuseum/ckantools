# !/usr/bin/env python
# encoding: utf-8

import inspect

from ckantools.decorators.actions import is_action, wrap_action_function


def create_actions(*modules):
    '''
    Finds action functions in the given modules and returns an action dict (action name -> action
    function). Actions are found by finding all functions in each module that meet the is_action
    function criteria (see the is_action function in this module).

    :param modules: the modules to search through
    :return: an actions dict
    '''
    actions = {}

    for module in modules:
        # actions must be functions and pass the is_action function's tests
        functions = inspect.getmembers(module, lambda f: inspect.isfunction(f) and is_action(f))
        for function_name, function in functions:
            actions[function_name] = wrap_action_function(function_name, function)

    return actions
