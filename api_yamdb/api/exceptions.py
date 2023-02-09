class PassDataError(Exception):
    def __init__(self, data, *args: object) -> None:
        self.data = data
        super().__init__(*args)