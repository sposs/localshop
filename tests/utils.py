from io import BytesIO


class NamedStringIO(BytesIO):

    """A StringIO that has a name in it"""

    def __init__(self, *args, **kwargs):
        super(NamedStringIO, self).__init__(*args, **kwargs)
