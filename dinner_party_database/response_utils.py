class ResponseUtils:
    @staticmethod
    def response_sentiment(response):
        if "know" in response.lower() or "idk" in response.lower():
            return 0
        if "yes" in response.lower():
            return 1
        if "no" in response.lower():
            return -1
