import uuid


class RandomHash(object):

        @staticmethod
        def generate(amount=20):
            code = uuid.uuid4().hex[:amount].upper()
            return code
