

class ZillowError(Exception):
    def __init__(self, response):
        super(ZillowError, self).__init__(
            "There was a problem with your request. Status code {}, Content {}".
            format(response.status_code, response.content)
        )
