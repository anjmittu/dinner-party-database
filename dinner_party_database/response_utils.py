class ResponseUtils:
    @staticmethod
    def response_sentiment(response):
        if "know" in response.lower() or "idk" in response.lower():
            return 0
        if "yes" in response.lower() or "yee" in response.lower() or "yeah" in response.lower() or "ye" in response.lower():
            return 1
        if "no" in response.lower() or "ne" in response.lower():
            return -1
