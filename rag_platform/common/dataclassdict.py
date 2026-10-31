class DataClassDict:
    def __getitem__(self, key: str):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key) from None
