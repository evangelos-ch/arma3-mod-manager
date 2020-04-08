from arma3_mod_manager import workshop


def test_get_items():
    URL = "https://steamcommunity.com/sharedfiles/filedetails/?id=1402094102"
    items = workshop.get_items(URL)
    assert len(items) > 0
    for item in items:
        assert "name" in item
        assert "id" in item
