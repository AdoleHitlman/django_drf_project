import re
from rest_framework.exceptions import ValidationError
class DescriptionValidator:
    def __init__(self,field):
        self.field = field

    def __call__(self, value):
        description = dict(value).get(self.field)
        link_pat = r'https?://\S+|www\.\S+'
        youtube_url = r'(?:https?://)?(?:www\.)?youtube\.com'
        links = re.findall(link_pat,description)
        for link in links:
            if not bool(re.match(youtube_url,link)):
                raise ValidationError('You cannot attach links to third-party educational platforms or personal sites')