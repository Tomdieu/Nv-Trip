from datetime import datetime
import re
from django.core.exceptions import ValidationError


def validate_dob(dob):
    if dob > datetime.today().date():
        raise ValidationError(
            "The Date must be <= {}".format(datetime.date.today()))

    return dob


def min_place(plc):
    if int(plc) <= 1:
       raise ValidationError(['The Mininum Place Can only be 1','if it is 1 you can only transport one passenger with it'])
       
    return plc

def check_plc(plc):
    if(int(plc)) < 0:
        raise ValidationError('The Availabe places can not be less than 0!')

    return plc