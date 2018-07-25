

from batch_api_consumers import BatchVideoDowloader

resource_list = ['http://ftp.gnu.org/gnu/wget/wget-1.5.3.tar.gz']

batch_vid_dowloader = BatchVideoDowloader(resource_list,
                                          'tmp_cache.json',
                                          fwd_kwargs = {}, # arguments to forward to the underlying api
                                          num_threads = 3,
                                          verbose = True)

batch_vid_dowloader.execute()

