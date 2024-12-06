from atlassian_tea_utils.splunk import Splunk


def test_splunk():
    """
    Main function to test the Splunk class.
    """

    query = {
        "earliest_time": "-1m",
        "latest_time": "now",
        "count": 1100,
        "exec_mode": "oneshot",
        "search": r"| makeresults count=1000 | streamstats count | table count | rename count as seq",
    }
    expected = [{"seq": str(i)} for i in range(1, 1001)]

    connector = Splunk()
    assert list(connector.isearch(query)) == expected
    assert connector.search(query) == expected
