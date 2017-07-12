"""Test project on basic multithreading benchmarking"""
import time
from urllib import urlopen
from multiprocessing.dummy import Pool as ThreadPool
# Python3.6 doesn't use urllib2 library for the urlopen function.cd ..
# Instead that library was split in 2 libraries which
# we can import urlopen from.
urls = [
    'http://www.python.org',
    'http://www.python.org/about/',
    'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
    'http://www.python.org/doc/',
    'http://www.python.org/download/',
    'http://www.python.org/getit/',
    'http://www.python.org/community/',
    'https://wiki.python.org/moin/',
    'http://planet.python.org/',
    'https://wiki.python.org/moin/LocalUserGroups',
    'http://www.python.org/psf/',
    'http://docs.python.org/devguide/',
    'http://www.python.org/community/awards/'
]

# # ------ For Loop -------#
results = []
start_time = time.time()
for url in urls:
    result = urlopen(url)
    results.append(result)
print('After {} seconds'.format(time.time() - start_time))
# # ------- VERSUS ------- #


# # ------- 4 Pool ------- #
pool = ThreadPool(4)
start_time = time.time()
results = pool.map(urlopen, urls)
print('After {} seconds'.format(time.time() - start_time))

# # ------- 8 Pool ------- #
pool = ThreadPool(8)
start_time = time.time()
results = pool.map(urlopen, urls)
print('After {} seconds'.format(time.time() - start_time))

# # ------- 13 Pool ------- #
pool = ThreadPool(13)
start_time = time.time()
results = pool.map(urlopen, urls)
print('After {} seconds'.format(time.time() - start_time))
