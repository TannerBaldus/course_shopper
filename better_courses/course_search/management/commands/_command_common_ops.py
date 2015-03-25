__author__ = 'tanner'
import  importlib

def get_func_from_string(function_string):
    """
    Takes a string of the form module.path_to.function and returns the function.
    Useful for getting the the functions from strings in settings.
    Credit to SO user ferrouswheel http://stackoverflow.com/a/19393328
    :param function_string:  a string of the form module.path_to.function
    :return: the function

    """
    mod_name, func_name = function_string.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    return func


    
