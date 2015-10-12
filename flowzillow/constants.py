try:
	from urlparse import urljoin # python 2
except ImportError:
	from urllib.parse import urljoin # python 3

BASE_URL = "http://zillow.com/"
DAYS = "any"
DS = "all"
HOME_TYPE = 111111
LISTING_TYPE = 111101
P = 1
PF = 1
PMF = 1
RED = 0
RT = 6
SEARCH = "maplist"
SORT = "priced"
SPT = "homes"
STATUS = 111011
SUCCESS_CODE = 200
ZILLOW_WEBSERVICE = urljoin(BASE_URL, "webservice/")
ZOOM_LEVEL = 12
