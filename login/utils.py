from django_otp.oath import TOTP
from django_otp.util import random_hex
import time


class TOTPVerification:

    def __init__(self):
        self.key = random_hex(20)
        self.last_verified_counter = -1
        self.token_validity_period = 60
        self.totp = None

    def totp_obj(self):
        totp = TOTP(key=self.key,
                    step=self.token_validity_period)
        totp.time = time.time()
        return totp

    def generate_token(self):
        self.totp = self.totp_obj()
        token = str(self.totp.token()).zfill(6)
        return token

    def verify_token(self, token):
        try:
            token = int(token)
        except ValueError:
            return False
        # totp = self.totp_obj()
        if ((self.totp.t() > self.last_verified_counter) and
                (self.totp.verify(token, tolerance=0))):
            self.last_verified_counter = self.totp.t()
            return True
        return False
