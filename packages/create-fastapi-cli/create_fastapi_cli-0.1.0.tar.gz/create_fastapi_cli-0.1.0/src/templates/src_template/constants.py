from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

    def is_dev(self):
        return self == self.DEV

    def is_staging(self):
        return self == self.STAGING

    def is_prod(self) -> bool:
        return self == self.PROD
