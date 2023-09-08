def test_is_vo():
    from main import is_vo

    assert is_vo("2020:10:10:rijk-verantwoord-2022", "rekenkamer") == True
    assert is_vo("2020:10:10:rijk-verantwoord-2022", "adr") == False

    assert (
        is_vo("2020:10:10:resultaten-verantwoordingsonderzoek-BZK", "rekenkamer")
        == True
    )
    assert (
        is_vo("2020:10:10:staat-van-de-rijksverantwoording-2022", "rekenkamer") == True
    )
    assert (
        is_vo("2020:10:1:staat-van-de-rijksverantwoording-2022", "rekenkamer") == True
    )
