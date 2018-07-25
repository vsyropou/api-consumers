This repository implememnts a simple logic for consuming web api sources and cahcning the result locally. The concurent batch consumption is handled by the base class BaseBatchConsumer. The idea is to cach things, such as responces of apis that charge per query, when devoping an application to save time and money. Thus, it is by no means a robust caching engine.

In order to consume an api you need to:
- Write a consumer derived class that inherites from the BaseBatchConsumer class under batc_api_consumers.py.
- Write a cache manager class that derives from BaseCacheManager under caching.py.

An example is given in the same file, namely the derived class BatcVideoDownloader which consumers the wget api (you need to pip install the wget package for that example). Also take a look at the VideoCacheManger derived class. In is simple, really ...

There are also some google api consumer class that are under the experimentation folder, you will need to install special packages from google as well as take care of authentication. In the same directory, there is also a wrapper class around the mssql connector, where the idea is to cache query results for working offline, but never got the time to finish it.