try:
	from urlparse import urljoin # python 2
except ImportError:
	from urllib.parse import urljoin # python 3

import requests

from flowzillow import constants
from flowzillow.exceptions import ZillowError


def _trim_none_values(dict_):
    new_dict = dict(dict_)
    del_keys = []
    for k, v in new_dict.items():
        if not v:
            del_keys.append(k)
    for key in del_keys:
        del new_dict[key]
    return new_dict


def _validate_response(response):
    if response.status_code != constants.SUCCESS_CODE:
        raise ZillowError(response)


class SearchClient(object):
    def search(self, latlong1, latlong2, **kwargs):
        """
        Search for all home listings in within a set of rectangular geocoordinates. Returns
        a block of JSON with all the search results. Since this is an undocumented API not
        all parameters available to this API are of known purpose

        :param tuple latlong1: Geocoords of the upper left point of the rectangular search box
        :param tuple latlong2: Geocoords of the lower right point of the rectangular search box
        :param **kwargs:
        :param spt: Seems to be "homes" by default
        :param rid: Region ID. A region unique number
        :param days: Number of days on market. Select "any" for any number of days
        :param att: Custom keyword search.
        :param sort: Sort by choice of (days/featured/priced/pricea/lot/built/size/baths/beds/zest/zesta)
        :param zoom: The zoom of the map.
        :param pf: Search for properties in pre-foreclosure (0/1)
        :param pmf: Search for foreclosed properties (0/1)
        :param laundry: In unit laundry (rentals only) (0/1)
        :param parking: On site-parking (rentals only) (0/1)
        :param pets: Accepts pets (rentals only) (0/1)
        :param bd: Bedrooms (number plus) eg input of "1," means 1 bedroom and up
        :param pr: Price (number plus) eg input of 50000 means 50000 and up
        :param ba: Bathrooms (number plus)
        :param sf: Square feet "<min>,<max>". If either min or max not set just leave blank but keep comma
        :param lot: Lot size "<min>,<max>"
        :param yr: Year build "<min>,<max>"
        :param lt: List Type. A 6 digit binary number for filtering by for sale 111111 would mean search for
        all for sale "By Agent", "By Owner", "Foreclosures", "New Homes", "Open Houses Only", "Coming Soon."
        :param status: Status of home. A 6 digit binary number. input of 111011 means search for all houses
        (Set to 1 to search "For Sale"), "Make me move", "Recently Sold", (Next bit seems unused),
        "For Rent", (Set to 1 if you want to search for foreclosure properties)
        :param ht: Home Type. A 6 digit binary number. 111111 means search for "Houses", "Condos",
        "Apartments", "Manufactured", "Lots/Land", "Townhomes"
        :param rt: ?? 6 seems to be default
        :param red: ?? 0 seems to be default
        :param pho: ?? 0 seems to be default
        :param pnd: ?? 0 seems to be default
        :param zso: ?? 0 seems to be default
        :param ds: ?? "all" seems to be default
        :param p: ?? 1 seems to be default
        """
        params = self._make_search_params(latlong1, latlong2, **kwargs)
        response = requests.get(
            urljoin(constants.BASE_URL, "search/GetResults.htm"), params=params
        )
        _validate_response(response)
        return response.json()

    def _make_rect_param(self, latlong1, latlong2):
        geo1 = map(lambda coord: str(coord).replace(".", ""), reversed(list(latlong1)))
        geo2 = map(lambda coord: str(coord).replace(".", ""), reversed(list(latlong2)))
        return ",".join(geo1 + geo2)

    def _make_search_params(self, latlong1, latlong2, **kwargs):
        rect = self._make_rect_param(latlong1, latlong2)
        param_dict = {
            "ht": constants.HOME_TYPE,
            "isMapSearch": False,
            "lt": constants.LISTING_TYPE,
            "rect": rect,
            "red": constants.RED,
            "rt": constants.RT,
            "search": constants.SEARCH,
            "spt": constants.SPT,
            "status": constants.STATUS,
            "zoom": constants.ZOOM_LEVEL,
            "pr": ",",
            "mp": ",",
            "bd": "0,",
            "ba": "0,",
            "sf": "0,",
            "lot": "0,",
            "yr": "0,",
            "pho": "0,",
            "pets": 0,
            "parking": 0,
            "laundry": 0,
            "pnd": 0,
            "zso": 0,
            "days": constants.DAYS,
            "ds": constants.DS,
            "pf": constants.PF,
            "pmf": constants.PMF,
            "p": constants.P,
            "sort": constants.SORT,
        }
        param_dict.update(kwargs)
        return param_dict.items()


class ZillowClient(object):
    def __init__(self, zws_id):
        self.zws_id = zws_id

    def _perform_get_request(self, path, params):
        response = requests.get(urljoin(constants.ZILLOW_WEBSERVICE, path),
                                params=_trim_none_values(params).items())
        _validate_response(response)
        return response.content

    def get_z_estimate(self, zpid, rent_z_estimate=None):
        return self._perform_get_request(
            "GetZestimate.htm",
            {"zws-id": self.zws_id, "zpid": zpid, "rentzestimate": rent_z_estimate},
        )

    def get_search_results(self, address, city_state_zip, rent_z_estimate=None):
        return self._perform_get_request(
            "GetSearchResults.htm",
            {"zws-id": self.zws_id,
             "address": address,
             "citystatezip": city_state_zip,
             "rent_z_estimate": rent_z_estimate},
        )

    def get_chart(self, zpid, unit_type, width, height, chart_duration):
        return self._perform_get_request(
            "GetChart.htm",
            {"zws-id": self.zws_id,
             "zpid": zpid,
             "unit-type": unit_type,
             "width": "width",
             "height": height,
             "chartDuration": chart_duration}
        )

    def get_comps(self, zpid, count, rent_z_estimate=None):
        return self._perform_get_request(
            "GetComps.htm",
            {"zws-id": self.zws_id,
             "zpid": zpid,
             "count": count,
             "rentzestimate": rent_z_estimate}
        )

    def get_deep_comps(self, zpid, count, rent_z_estimate=None):
        return self._perform_get_request(
            "GetDeepComps.htm",
            {"zws-id": self.zws_id,
             "zpid": zpid,
             "count": count,
             "rentzestimate": rent_z_estimate}
        )

    def get_deep_search_results(self, address, city_state_zip, rent_z_estimate=None):
        return self._perform_get_request(
            "GetDeepSearchResults.htm",
            {"zws-id": self.zws_id,
             "address": address,
             "citystatezip": city_state_zip,
             "rent_z_estimate": rent_z_estimate}
        )

    def get_updated_property_details(self, zpid):
        return self._perform_get_request(
            "GetUpdatedPropertyDetails.htm",
            {"zws-id": self.zws_id, "zpid": zpid}
        )

    def get_demographics(self, region_id=None, state=None, city=None, neighborhood=None, zipcode=None):
        """
        Get the demographics of a specific city.

        At least rid, state/city,  city/neighborhood, or zipcode is required
        """
        if not region_id and not (state and city) and not (city and neighborhood) and not zipcode:
            raise ValueError("At least rid, state/city,  city/neighborhood, or zipcode is required")
        return self._perform_get_request(
            "GetDemographics.htm",
            {"zws-id": self.zws_id,
             "regionId": region_id,
             "state": state,
             "city": city,
             "neighborhood": neighborhood,
             "zip": zipcode}
        )

    def get_region_children(self, region_id=None, state=None, county=None, city=None, child_type=None):
        """
        Get a list of sub-regions with their relevant information

        At least region_id or state is required
        """
        if not region_id and not state:
            raise ValueError("At least region_id or state is required")
        return self._perform_get_request(
            "GetRegionChildren.htm",
            {"zws-id": self.zws_id,
             "regionId": region_id,
             "state": state,
             "county": county,
             "city": city,
             "childtype": child_type}
        )

    def get_region_chart(self,
                         unit_type,
                         city=None,
                         state=None,
                         neighborhood=None,
                         zipcode=None,
                         width=None,
                         height=None,
                         chart_duration=None):
        return self._perform_get_request(
            "GetRegionChart.htm",
            {"zws-id": self.zws_id,
             "city": city,
             "state": state,
             "neighborhood": neighborhood,
             "zip": zipcode,
             "unit-type": unit_type,
             "width": width,
             "height": height,
             "chartDuration": chart_duration}
        )
