from nico_bot.url import is_valid_nico_video_url_regex


def test_url():
    assert is_valid_nico_video_url_regex("https://www.nicovideo.jp/watch/sm9")
    assert not is_valid_nico_video_url_regex("aaa")
