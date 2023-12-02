from fastapi import HTTPException, status


class DateFormatException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please use dd-mm-yyyy format.")


class InvalidMutualFundDateException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail='data related to the given date are not available '
                                                                         'for the given scheme code.')

class InvalidSchemeCodeException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid scheme code')


