supported_types = [
    'text',
    'image',
    'video',
    'audio',
    'file',
    'template',
]


class Message():
    """
    Base message object
    """

    def __init__(self, type, payload):

        assert type in supported_types, 'That is not a supported type'

        self.type = type
        self.payload = payload

    def to_json(self):
        """Returns json representation of message"""
        data = {}
        # TODO: check types on the payload

        if self.type == 'text':
            data['text'] = self.payload

        else:

            data['attachment'] = {}
            data['attachment']['type'] = self.type

            if self.type == 'template':
                template = self.payload
                data['attachment']['payload'] = template.to_json()
            else:
                data['attachment']['payload'] = {
                    'url': self.payload
                }

        return data


class ReceivedMessage(Message):
    """
    Model to represent reciepts
    """

    def __init__(self, json):

        if 'text' in json['message']:
            self.type = 'text'
            self.text = json['message']['text']

        self.recipient = json['recipient']['id']
        self.sender = json['sender']['id']
        self.time = json['timestamp']

    def to_json(self):
        raise NotImplementedError
