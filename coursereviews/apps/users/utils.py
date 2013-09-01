#We put this file in the users folder but we could put it anywhere we want there

from users.models import ViewCount

def get_view_count(url):
    """ 
    Accepts as its parameter a url string or a model.
    """
    if not isinstance(url, basestring):
        url = url.get_absolute_url() # assume it's a model... not so good

    try:
        return ViewCount.objects.get(url=url).count
    except ViewCount.DoesNotExist:
        return 0
