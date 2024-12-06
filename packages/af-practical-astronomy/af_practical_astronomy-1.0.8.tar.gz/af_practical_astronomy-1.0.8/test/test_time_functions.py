import unittest
import time_functions
from astronomy_types import Date, Time, FullDate

class TimeTestMethods(unittest.TestCase):

  def test_date_of_easter(self):
    msg = 'test_date_of_easter fail'

    self.assertEqual(time_functions.date_of_easter(2009), (2009,4,12), msg)
    self.assertEqual(time_functions.date_of_easter(2010), (2010,4,4), msg)
    self.assertEqual(time_functions.date_of_easter(2024), (2024,3,31), msg)

  def test_date_to_day_number(self):
    msg = 'test_date_to_day_number fail'

    self.assertEqual(time_functions.date_to_day_number(Date((2000,1,1))), 1, msg)
    self.assertEqual(time_functions.date_to_day_number(Date((2000,12,31))), 366, msg)
    self.assertEqual(time_functions.date_to_day_number(Date((1900,12,31))), 365, msg)

  def test_greenwich_to_julian_date(self):
    msg = 'test_greenwich_to_julian_date fail'

    self.assertEqual(time_functions.greenwich_to_julian_date(Date((2009,6,19.75))), 2455002.25, msg)
    self.assertEqual(time_functions.greenwich_to_julian_date(Date((1969,1,5))), 2440226.5, msg)

  def test_julian_date_to_j2000(self):
    msg = 'test_julian_date_to_j2000'

    self.assertEqual(time_functions.julian_date_to_j2000(2440227.54513888889), -11317.454861111008, msg)

  def test_julian_to_greenwich_date(self):
    msg = 'test_julian_to_greenwich_date fail'

    self.assertEqual(time_functions.julian_to_greenwich_date(2455002.25), (2009, 6, 19.75), msg)
    self.assertEqual(time_functions.julian_to_greenwich_date(2440588), (1970, 1, 1.5), msg)

  def test_finding_day_of_week(self):
    msg = 'test_finding_day_of_week fail'

    self.assertEqual(time_functions.finding_day_of_week(2455001.5), "Friday", msg)
    self.assertEqual(time_functions.finding_day_of_week(time_functions.greenwich_to_julian_date(Date((2024,4,7)))), "Sunday", msg)

  def test_hours_minutes_seconds_to_decimal_time(self):
    msg = 'test_hours_minutes_seconds_to_decimal_time fail'

    self.assertEqual(time_functions.hours_minutes_seconds_to_decimal_time(Time((18,31,27))), 18.524166666666666, msg)
    self.assertEqual(time_functions.hours_minutes_seconds_to_decimal_time(Time((18,31,27)),False), 6.524166666666666, msg)
    self.assertEqual(time_functions.hours_minutes_seconds_to_decimal_time(Time((11,31,5)),False), 11.518055555555556, msg)
    self.assertEqual(time_functions.hours_minutes_seconds_to_decimal_time(Time((12,00,00)),False), 12, msg)
    self.assertEqual(time_functions.hours_minutes_seconds_to_decimal_time(Time((12,00,00))), 12, msg)

  def test_decimal_hours_to_hours_minutes_seconds(self):
    msg = 'test_decimal_hours_to_hours_minutes_seconds fail'

    self.assertEqual(time_functions.decimal_hours_to_hours_minutes_seconds(18.52416667), (18, 31, 27), msg)

  def test_local_civil_to_universal_time(self):
    msg = 'test_local_civil_to_universal_time fail'

    lct = FullDate((Date((2013,7,1)),Time((3,37,5))))

    self.assertEqual(time_functions.local_civil_to_universal_time(lct,1,4), ((2013,6,30),(22,37,5.0)), msg)

  def test_universal_to_local_civil_time(self):
    msg = 'test_universal_to_local_civil_time fail'

    utc = FullDate((Date((2013,6,30)), Time((22,37,0))))

    self.assertEqual(time_functions.universal_to_local_civil_time(utc,4,1), ((2013,7,1),(3,37,0)), msg)

  def test_universal_to_greenwich_sidereal_time(self):
    msg = 'test_universal_to_greenwich_sidereal_time fail'

    utc = FullDate((Date((1980,4,22)),Time((14,36,51.67))))

    self.assertEqual(time_functions.universal_to_greenwich_sidereal_time(utc), (4, 40, 5.23), msg)

  def test_greenwich_sidereal_to_universal_time(self):
    msg = 'test_greenwich_sidereal_to_universal_time fail'

    full_date = FullDate((Date((1980,4,22)),Time((4,40,5.23))))

    self.assertEqual(time_functions.greenwich_sidereal_to_universal_time(full_date), ((1980,4,22), (14,36,51.67)), msg)

  def test_greenwich_sidereal_to_local_sidereal_time(self):
    msg = 'test_greenwich_sidereal_to_local_sidereal_time fail'

    self.assertEqual(time_functions.greenwich_sidereal_to_local_sidereal_time(Time((4,40,5.23)),-64), (0, 24, 5.23), msg)

  def test_local_sidereal_to_greenwich_sidereal_time(self):
    msg = 'test_local_sidereal_to_greenwich_sidereal_time fail'
    
    self.assertEqual(time_functions.local_sidereal_to_greenwich_sidereal_time(Time((0,24,5.23)),-64), (4, 40, 5.23), msg)

  def test_year_is_leap(self):
    msg = 'test_year_is_leap fail'

    self.assertEqual(time_functions.year_is_leap(1600), True, msg)
    self.assertEqual(time_functions.year_is_leap(1900), False, msg)
    self.assertEqual(time_functions.year_is_leap(1992), True, msg)
    self.assertEqual(time_functions.year_is_leap(2000), True, msg)
    self.assertEqual(time_functions.year_is_leap(2023), False, msg)
    self.assertEqual(time_functions.year_is_leap(2024), True, msg)
    self.assertEqual(time_functions.year_is_leap(2048), True, msg)