import logging
import json
log = logging.getLogger(__name__)


class SlackAttachment(object):

    def __init__(self,
                 color="",
                 fallback="",
                 text="",
                 mrkdwn_in=None):
        self.color = color
        self.fallback = fallback
        self.text = text
        if mrkdwn_in is None:
            self.mrkdwn_in = []
        else:
            self.mrkdwn_in = mrkdwn_in

    def load(self, attachment_dict):
        self.color = attachment_dict.get('color', self.color)
        self.fallback = attachment_dict.get('fallback', self.fallback)
        self.text = attachment_dict.get('text', self.text)
        self.mrkdwn_in = attachment_dict.get('mrkdwn_in', self.mrkdwn_in)

    def __str__(self):
        return_dict = {}
        for element in ['color',
                        'fallback',
                        'text',
                        'mrkdwn_in']:
            return_dict.update({element: getattr(self, element)})
        return "[%s]" % json.dumps(return_dict)

    def __eq__(self, other):
        for element in ['color',
                        'fallback',
                        'text',
                        'mrkdwn_in']:
            if not getattr(self, element) == getattr(other, element):
                log.debug("Element %s is different" % element)
                log.debug("%s != %s" % (getattr(self, element),
                                        getattr(other, element)))
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)