This repository is the result of me following my urge to code when I was studying python more thourghly. I do not see any direct use of the code, except maybe for when you develop localy somehting and you would like to avoid uncessesary calls to an expensive a pi, as most cloud platofrms tend to charge you for development runs as well.   

This code implememnts a simple logic for consuming web api sources and chacning the result locally. The concurent batch consumption is handled by the base class BaseBatchConsumer.

In order to consume an api you need to:
- Write a consumer derived class that inherites from the BaseBatchConsumer class under batc_api_consumers.py.
- Write a cache manager class that derives from BaseCacheManager under caching.py.

An example is given in the same file, namely the derived class BatcVideoDownloader which consumers the wget api (you need to pip install the wget package for that example). Also take a look at the VideoCacheManger derived class. In is simple, really... 

Under the general directory a naive message service that includes the calss or function, that triggered the prinout, in the print message can be found. While in the progress.py file the calssic progress display with an rotating cursor is implemented. 

There are also some google api consumer class that are under the experimentation folder, you will need to install special packages from google as well as take care of authentication. In the same directory, there is also a wrapper class around the mssql connector, where the idea is to cache query results for working offline, but never got the time to finish it.
