import unittest
import coordinate_functions
from astronomy_types import FullDate, Date, Time, HorizontalCoordinates, Degrees, EquatorialCoordinates, HourAngle, RightAscension, EclipticCoordinates, Declination, EquatorialCoordinatesHourAngle, Altitude, Azimuth, GeographicCoordinates, GalacticCoordinates


class CoordinateTestMethods(unittest.TestCase):

  def test_decimal_degrees_to_degrees_minutes_seconds(self):
    msg = 'test_decimal_degrees_to_degrees_minutes_seconds fail'

    self.assertEqual(coordinate_functions.decimal_degrees_to_degrees(182.52416666666667), (182,31,27), msg)

  def test_degrees_minutes_seconds_to_decimal_degrees(self):
    msg = 'test_decimal_degrees_to_degrees_minutes_seconds fail'

    degrees = Degrees((182,31,27))

    self.assertEqual(coordinate_functions.degrees_to_decimal_degrees(degrees), (182.52416666666667), msg)

  def test_right_ascension_to_hour_angle(self):
    msg = 'test_right_ascension_to_hour_angle fail'

    full_date = FullDate((Date((1980,4,22)),Time((14,36,51.67))))

    self.assertEqual(coordinate_functions.right_ascension_to_hour_angle(RightAscension(Time((18,32,21))),full_date,0,-4,-64), (9, 52, 23.66), msg)

  def test_hour_angle_to_right_ascension(self):
    msg = 'test_hour_angle_to_right_ascension fail'

    full_date = FullDate((Date((1980,4,22,)),Time((14,36,51.67))))

    self.assertEqual(coordinate_functions.hour_angle_to_right_ascension(HourAngle(Time((9,52,23.66))),full_date,0,-4,-64), (18, 32, 21.0), msg)

  def test_equatorial_to_horizon_coordinates(self):
    msg = 'test_equatorial_to_horizon_coordinates fail'
    
    coordinates = EquatorialCoordinatesHourAngle((Declination(Degrees((23,13,10))),HourAngle(Time((5,51,44)))))

    self.assertEqual(coordinate_functions.equatorial_to_horizon_coordinates(coordinates,52), ((19,20,3.64), (283,16,15.7)), msg)

  def test_horizon_to_equatorial_coordinates(self):
    msg = 'test_horizon_to_equatorial_coordinates fail'

    coordinates = HorizontalCoordinates((Altitude(Degrees((19,20,3.64))), Azimuth(Degrees((283,16,15.76)))))

    self.assertEqual(coordinate_functions.horizon_to_equatorial_coordinates(coordinates,52), ((23,13,10.04), (5,51,44.0)), msg)

  def test_mean_obliquity_ecliptic(self):
    msg = 'test_mean_obliquity_ecliptic fail'

    self.assertEqual(coordinate_functions.mean_obliquity_ecliptic(Date((2009, 7, 6))), 23.438055312466062, msg)

  def test_ecliptic_to_equatorial_coordinates(self):
    msg = 'test_ecliptic_to_equatorial_coordinates fail'

    coordinates = EclipticCoordinates((Degrees((4,52,31)), Degrees((139,41,10))))
    date = Date((2009,7,6))

    self.assertEqual(coordinate_functions.ecliptic_to_equatorial_coordinates(coordinates,date), ((19,32,8.52), (9,34,53.4)), msg)

  def test_equatorial_to_ecliptic_coordinates(self):
    msg = 'test_equatorial_to_ecliptic_coordinates fail'

    coordinates = EquatorialCoordinates((Declination(Degrees((19,32,8.52))), RightAscension(Time((9,34,53.4)))))

    self.assertEqual(coordinate_functions.equatorial_to_ecliptic_coordinates(coordinates,Date((2009,7,6))), ((4,52,30.99), (139,41,10.25)), msg)

  def test_equatorial_to_galactic_coordinates(self):
    msg = 'test_equatorial_to_galactic_coordinates fail'

    coordinates = EquatorialCoordinates((Declination(Degrees((10,3,11))), RightAscension(Time((10,21,0)))))

    self.assertEqual(coordinate_functions.equatorial_to_galactic_coordinates(coordinates), ((51,7,20.16), (232,14,52.38)), msg)

  def test_galactic_to_equatorial_coordinates(self):
    msg = 'test_galactic_to_equatorial_coordinates fail'

    coordinates = GalacticCoordinates((Degrees((51,7,20.16)), Degrees((232, 14, 52.38))))

    self.assertEqual(coordinate_functions.galactic_to_equatorial_coordinates(coordinates), ((10,3,11.0), (10,21,0)), msg)
    
  def test_angle_difference(self): 
    msg = "test_angle_difference fail"

    coordinates1 = EquatorialCoordinates((Declination(Degrees((-8,13,30))), RightAscension(Time((5,13,31.7))))) 
    coordinates2 = EquatorialCoordinates((Declination(Degrees((-16,41,11))), RightAscension(Time((6,44,13.4)))))

    self.assertEqual(coordinate_functions.angle_difference(coordinates1, coordinates2), ((23, 40, 25.86)), msg)

  def test_rising_and_setting(self): 
    msg = "test_rising_and_setting fail"

    coordinates = EquatorialCoordinates((Declination(Degrees((21,42,0))), RightAscension(Time((23,39,20))))) 
    location = GeographicCoordinates((30, 64))
    greenwich_date = Date((2010, 8, 24))

    self.assertEqual(coordinate_functions.rising_and_setting(coordinates, location, greenwich_date, 0.5667), ((True, (14, 16, 18.018333000000002), (4, 10, 1.1783329999999999), 64.3623480385112, 295.6376519614888)), msg)

  def test_precession_low_precision(self): 
    msg = "test_precession_low_precision fail"

    coordinates = EquatorialCoordinates((Declination(Degrees((14,23,25))), RightAscension(Time((9,10,43))))) 
    original_epoch = 2433282.423
    new_epoch = 2444025.5

    self.assertEqual(coordinate_functions.precession_low_precision(coordinates, original_epoch, new_epoch), ((14, 16, 9.12), (9, 12, 20.18)), msg)

  def test_nutation_from_date(self): 
    msg = "test_nutation_from_date fail"

    self.assertEqual(coordinate_functions.nutation_from_date(Date((1988,9,1))), (0.0015258083552917808, 0.0025671004471993584), msg)