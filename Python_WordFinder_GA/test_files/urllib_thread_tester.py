from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
#Python3.6 doesn't use urllib2 library for the urlopen function.
#Instead that library was split in 2 libraries which 
#we can import urlopen from.

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
  # etc.. 
  ]

# Make the Pool of workers
pool = ThreadPool(4)
# Open the urls in their own threads
# and return the results
results = pool.map(urlopen, urls)
#close the pool and wait for the work to finish 
pool.close()
pool.join()
