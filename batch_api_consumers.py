
from caching import KeyValuePairCachedObject
# from google_apis import ClasifyTextGoogleApi
import wget

from progress import Progress
from caching import *


import threading
import time
import abc

__all__ = ['BatchVideoDowloader', 'BatchTextTagsClasifier']


class AbsBatchConsumer(abc.ABC):

    @abc.abstractmethod
    def __init__(self,*args,**kwargs):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    @property
    @abc.abstractmethod
    def _cache_manager_prx(self):
        pass

    @property
    @abc.abstractmethod
    def api_proxy(self):
        pass

class BaseBatchConsumer(AbsBatchConsumer):
    
    def __init__(self, subs_list, cache_path_location, **kwargs):

        self._operants_list = list(subs_list)
        self._cache_path_location = cache_path_location

        self._forwarded_kwargs = kwargs.pop('fwd_kwargs', {})
    
        self._num_threads = kwargs.pop('num_threads', 1)

        self._responce = []

        self._verbose = kwargs.pop('verbose', True)

    @property
    def responce(self):
        return self._responce


    def execute(self):
        if self._num_threads > 1:
            self._execute_multithread()
        else:
            self._execute()

    def _execute_multithread(self):

        cache_prx = self._cache_manager_prx 
        cache_loc = self._cache_path_location

        threads = []
        
        # helping funcions
        num_completed_threads = lambda thrds: len([ True for t in thrds if not t.isAlive()]) 


        prg = Progress(len(self._operants_list), name = self.__class__.__name__)        
        with cache_prx(path=cache_loc) as cache: # manage context

            for operant in self._operants_list: # launch threads loop

                thrd = threading.Thread(target = self._job,
                                        args = [cache, operant]
                                        )
                thrd.start()
                
                while threading.active_count() > self._num_threads: # limit num threads

                    prg.progress(num_completed_threads(threads))
            
                    time.sleep(0.25)
 
                threads += [thrd]

            while threading.active_count() > 1: # wait for the last thread
                prg.progress(num_completed_threads(threads))
                time.sleep(0.25)
            prg.progress(num_completed_threads(threads))
                

    def _execute(self):

        cache_prx = self._cache_manager_prx 
        cache_loc = self._cache_path_location

        with cache_prx(path=cache_loc) as cache:

            for operant in self._operants_list:

                self._job(cache, operant)


    def _job(self, cache, operant):
                
        args = (operant, self.api_proxy, cache)
        kwargs = { 'verbose': self._verbose }
                  
        if self._forwarded_kwargs:
            
            kwargs.update( {'func_args': self._forwarded_kwargs})

        try:
            cached_obj_inst = KeyValuePairCachedObject(*args, **kwargs )
        except Exception as err:
            msg = 'Cannot instantiate "KeyValuePairCachedObject" with args %s and kwargs %s.'\
                  ' Perhaps args[0] is not uploaded in google storage.'%(args,kwargs)
            raise RuntimeError(msg) from err
                    
        self._responce += [cached_obj_inst.value]


# class BatchTextTagsClasifier(BaseBatchConsumer):

#     _api_instance = ClasifyTextGoogleApi()
   
#     @property
#     def _cache_manager_prx(self):
#         return TextClassificationCacheManager
    
#     @property
#     def api_proxy(self):
#         return self._api_instance.consume


class BatchVideoDowloader(BaseBatchConsumer):
    
    @property
    def _cache_manager_prx(self):
        return VideoCacheManager
    
    @property
    def api_proxy(self):
        return wget.download
