"""
Auth: Nate Koike
Date: 23 October 2020
Desc: a simple input validator for page indexing
"""

# return a t/f value as well as an index position into the document
def validate(uin, length):
    # try to typecast the input to an integer
    try:
        uin_i = int(uin)

        # make sure the input is a valid page
        if uin_i < 1:
            return False, -1

        # make sure the input is within the bounds of the document
        if uin_i > length:
            return False, -1

        # this input is valid (also return the index)
        return True, uin_i - 1

    # this input is not valid
    except:
        return False, -1
