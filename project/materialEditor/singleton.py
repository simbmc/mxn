'''
Created on 31.07.2016

@author: mkennert
'''


class Singleton:
    '''
    represents the singleton-pattern. 
    if you want use this, set a annotation @Singleton over your class
    '''
    def __init__(self, decorated):
        self._decorated = decorated
    
    '''
    proofs whether a instance is already exist. 
    yes=> return this instance
    no=> create the first instance a return this
    '''
    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance
    
    '''
    raise a TypError when the user want create a materiallist
    with a other methodname as Instance()
    '''
    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`')
