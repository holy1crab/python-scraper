import re


from scraper.spiders.avito import get_id_from_details_url


def test_detail_url_id():

    expected = 888310214

    url = '/perm/predlozheniya_uslug/gruzoperevozki_dostavka_vyvoz_musora_gazel_do_6m_888310214'

    item_id = get_id_from_details_url(url)

    assert item_id == expected
