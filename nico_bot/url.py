import re


def is_valid_nico_video_url_regex(url):
    # Regular expression for a simple URL validation
    url_pattern = re.compile(r'^https?://www.nicovideo.jp/watch/sm\S+$', re.IGNORECASE)
    return bool(re.match(url_pattern, url))
