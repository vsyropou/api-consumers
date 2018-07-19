
from general import MessageService

error = MessageService.error
info  = MessageService.info
warn  = MessageService.warn
debug = MessageService.debug


import hashlib
import json
import os
import sys

__all__ = ['VideoCacheManager', 'TextClassificationCacheManager']

class BaseCacheManager():
    def __init__(self, path=None):
        self._file_path = path
    
    def __enter__(self):
        
        #TODO: check for more rexceptions
        self._cache = {}
        if not os.path.exists(self._file_path):
            
            warn ('No cahce file, named "%s", was found. Will recreate cache file.'%self._file_path)
            
        else:
            info ('Succesfully located cache file: "%s".'%self._file_path)
            self._open_file = open(self._file_path, 'r')

            try:
                self._cache = json.load(self._open_file)
                info('Succefully loaded cache from: "%s"'%self._file_path)
            except json.decoder.JSONDecodeError:
                warn('Cache in "%s" is empty or unserializable. Recreating cache '%self._file_path)
            
        return self._cache

    def __exit__(self,*args):

        info('Finished manipualting cahe: "%s". Writting out.'%self._file_path)
        ## TODO::  It is stupid to rewrite the cache every time.
        ##        Find a better way to update cache, perhaps a local db
        ## TODO::  It is also stupid to check for open file with an exception.
        ##       There must be some way to do this with less risk.
        
        try:
            self._open_file.close()
            os.remove(self._file_path)
        except AttributeError:
            warn('No open file found. Continueing to rewrite cache')
            pass


        serialized_cahe = json.dumps(self._cache)
        
        info('Succeccfully serialied cache: "%s"'%self._file_path)
        with open(self._file_path, 'w+') as out_file:
            out_file.write(serialized_cahe)


class KeyValuePairCachedObject():
    
    def __init__(self, value, value_getter_func, cache, **kwargs):
        
        self._getter_proxy = value_getter_func
        self._cache = cache
        self._value = value

        self._getter_func_args = kwargs.pop('func_args', {})

        self._verbose = kwargs.pop('verbose', True)
        
        self._key = self._get_unique_key(self._value)

        # check if cache has the key
        if self._exists_in_cache(self._key): # retrive cahced object
            
            self._value = self._cache[self._key]

        else: # get and cache object from source

            # print info
            msg = 'Will call getter function "%s".'%(self._getter_proxy.__name__)
            if self._getter_func_args:
                msg +=  'with kwargs: %s'%self._getter_func_args

            if self._verbose:
                info(msg)

            # call source
            self._value = self._getter_proxy(self._value, **self._getter_func_args)
                
            # update cache
            self._update_cache()


    def _exists_in_cache(self, key):
        return self._key in self._cache.keys()

    def _value_getter(self):
        return self._getter_proxy

    def _get_unique_key(self, item):
        # TODO: Check if it is tring
        return hashlib.sha1(item.encode('utf-8')).hexdigest()

    def _update_cache(self):
        self._cache[self._key] = self._value
        if self._verbose:
            print()
            info ('Appended entry to cache: \n {%s : %s}'%(self._key,self._value))
        
    @property
    def value(self):
        return self._value


class VideoCacheManager(BaseCacheManager):
    def __init__(self, *args,**kwargs):
        
        super(VideoCacheManager,self).__init__(*args,**kwargs)

        if not self._file_path:
            self._file_path = './__video_urls_cache__.json'
            warn('Using defalut cache path for subtitle files, "%s" '%self._file_path)


class TextClassificationCacheManager(BaseCacheManager):
    def __init__(self, *args,**kwargs):
        
        super(TextClassificationCacheManager,self).__init__(*args,**kwargs)

        if not self._file_path:
            self._file_path = './__text_calssification_cache__.json'
            warn('Using defalut cache path for subtitle files, "%s" '%self._file_path)


