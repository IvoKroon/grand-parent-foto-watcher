import uuid


class RandomHash(object):

        @staticmethod
        def generate():
            code = uuid.uuid4().hex[:20].upper()
            return code
