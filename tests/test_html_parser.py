from  html_parser import parse_table


SAMPLE_TABLE_HTML = """
<html>
<body>
<table>
  <thead>
    <tr><th>Company</th><th>Price</th><th>Change</th></tr>
  </thead>
  <tbody>
    <tr><td>Maroc Telecom</td><td>125.00</td><td>-0.40%</td></tr>
    <tr><td>Attijariwafa</td><td>480.00</td><td>+1.20%</td></tr>
  </tbody>
</table>
</body>
</html>
"""

def test_parse_table_returns_correct_rows():
    result = parse_table(SAMPLE_TABLE_HTML)
    assert len(result) == 2
    assert result == [
        {"Company": "Maroc Telecom", "Price": "125.00", "Change": "-0.40%"},
        {"Company": "Attijariwafa", "Price": "480.00", "Change": "+1.20%"},
    ]


NO_TABLE_HTML = """
<html>
<body>
<p>No data available today.</p>
</body>
</html>
"""


def test_parse_table_returns_empty_list_when_no_table():
    result = parse_table(NO_TABLE_HTML)
    assert result == []



PARTIAL_TABLE_HTML = """
<html>
<body>
<table>
  <thead>
    <tr><th>Company</th><th>Price</th><th>Change</th></tr>
  </thead>
  <tbody>
    <tr><td>BCP</td><td>290.00</td><td>+0.50%</td></tr>
    <tr><td>Incomplete row</td></tr>
  </tbody>
</table>
</body>
</html>
"""


def test_parse_table_skips_incomplete_rows():
    result = parse_table(PARTIAL_TABLE_HTML)

    assert len(result) == 1
    assert result[0]["Company"] == "BCP"