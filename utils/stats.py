class ApiStats:
    """
    Basic in-memory API usage statistics.
    """

    total_requests = 0
    successful_requests = 0
    failed_requests = 0
    viewed_deals = {}

    @staticmethod
    def record_request(status_code):
        """
        Track completed API requests by response status code.
        """

        ApiStats.total_requests += 1

        if status_code < 400:
            ApiStats.successful_requests += 1
            return

        ApiStats.failed_requests += 1

    @staticmethod
    def record_deal_view(deal_id):
        """
        Track successful deal views.
        """

        ApiStats.viewed_deals[deal_id] = ApiStats.viewed_deals.get(deal_id, 0) + 1

    @staticmethod
    def remove_deal(deal_id):
        """
        Remove deleted deals from view tracking.
        """

        ApiStats.viewed_deals.pop(deal_id, None)

    @staticmethod
    def get_deal_view_counts():
        """
        Return tracked deal view counts.
        """

        return ApiStats.viewed_deals.copy()

    @staticmethod
    def get_stats():
        """
        Return basic request counters.
        """

        return {
            "total_requests": ApiStats.total_requests,
            "successful_requests": ApiStats.successful_requests,
            "failed_requests": ApiStats.failed_requests,
        }
