from atlassian_tea_utils.sql.socrates import sql


def test_socrates():
    """
    Main function to test the Splunk class.
    """

    query = r"SELECT explode(sequence(1, 1000)) as seq;"
    expected = list(range(1, 1001))

    assert [row.seq for row in sql(query)] == expected
