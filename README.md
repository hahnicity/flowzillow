# flowzillow
A general python Zillow client that in addition to all documented Zillow APIs utilizes 
the undocumented Zillow GetResults API. This API is the same one users utilize on the
web to search for housing in a specific city.

## GetResults
The GetResults API is undocumented, but after a little bit of network sleuthing I was able
to figure out its specifics. Everything is documented in `flowzillow.client.SearchClient`.
Basic usage would look like
    
    from flowzillow.client import SearchClient

    search_client = SearchClient()
    search_client.search((lat1, long1), (lat2, long2))

Where the input tuples are tuples of latitude and longitudinal coordinates for opposite
ends of our search rectangle.

## Documented APIs
Documented APIs can be used using the `ZillowClient` object. Provided a `zws-id` the 
`ZillowClient` will be able to make calls to the Zillow API.

    client = ZillowClient(<zws-id>)
    xml_response = client.get_z_estimate(1002)

The following APIs are currently supported by `flowzillow`

 * GetZestimate
 * GetSearchResults
 * GetChart
 * GetComps
 * GetDeepComps
 * GetDeepSearchResults
 * GetUpdatedPropertyDetails
 * GetDemographics
 * GetRegionChildren
 * GetRegionChart

If more APIs are desired for support feature/pull requests are greatly appreciated.
