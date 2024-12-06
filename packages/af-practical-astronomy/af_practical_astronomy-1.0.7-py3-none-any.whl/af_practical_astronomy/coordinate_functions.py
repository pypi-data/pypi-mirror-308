import math
import time_functions
import utils
from astronomy_types import Date, DecimalTime, Time, FullDate, Longitude, Degrees, DecimalDegrees, RightAscension, HourAngle, EquatorialCoordinates, EquatorialCoordinatesHourAngle, HorizontalCoordinates, Latitude, Altitude, Azimuth, EclipticCoordinates, Declination, Obliquity, GalacticCoordinates, GeographicCoordinates, Epoch


def degrees_to_decimal_degrees(degrees: Degrees) -> DecimalDegrees:
  angle, minutes, seconds = degrees
  unsigned_degrees = utils.time_to_decimal_time(Time((abs(angle), abs(minutes), abs(seconds))))
  decimal_degrees = -unsigned_degrees if angle < 0 or minutes < 0 or seconds < 0 else unsigned_degrees 

  return decimal_degrees

def decimal_degrees_to_degrees(decimal_degree: DecimalDegrees) -> Degrees:
    hour, minutes, seconds = utils.decimal_time_to_time(decimal_degree)
    signed_degrees = -1 * hour if decimal_degree < 0 else hour
  
    return Degrees((signed_degrees, minutes, seconds))

def hours_to_degrees(hours: DecimalTime) -> DecimalDegrees:
  return hours / 15

def degrees_to_hours(degrees: DecimalDegrees) -> DecimalTime:
  return degrees * 15
  
def right_ascension_to_hour_angle(right_ascension: RightAscension, local_date_and_time: FullDate, daylight_savings: int, zone_correction: int, longitude: Longitude) -> HourAngle:
  """H = LST - a"""
  utc = time_functions.local_civil_to_universal_time(local_date_and_time, daylight_savings, zone_correction)
  gst = time_functions.universal_to_greenwich_sidereal_time(utc)
  local_sidereal_time = time_functions.greenwich_sidereal_to_local_sidereal_time(gst, longitude)
  lst_dec = utils.time_to_decimal_time(local_sidereal_time)
  ra_decimal = degrees_to_decimal_degrees(Degrees(right_ascension))
  hour_angle = lst_dec - ra_decimal

  if hour_angle < 0:
    hour_angle += 24
  
  return HourAngle(Time(decimal_degrees_to_degrees(hour_angle)))

def hour_angle_to_right_ascension(hour_angle: HourAngle, full_date: FullDate, daylight_savings: int, zone_correction: int, longitude: Longitude) -> RightAscension:
  utc = time_functions.local_civil_to_universal_time(full_date,daylight_savings,zone_correction)
  gst = time_functions.universal_to_greenwich_sidereal_time(utc)
  lst = time_functions.greenwich_sidereal_to_local_sidereal_time(gst, longitude)
  lst_dec = degrees_to_decimal_degrees(Degrees(lst))
  ha_decimal = degrees_to_decimal_degrees(Degrees(hour_angle))
  right_ascension = lst_dec - ha_decimal

  if right_ascension < 0:
    right_ascension += 24

  return RightAscension(Time(decimal_degrees_to_degrees(right_ascension)))

def equatorial_to_horizon_coordinates(equatorial_coordinates: EquatorialCoordinatesHourAngle, latitude: Latitude) -> HorizontalCoordinates:
  declination, hour_angle = equatorial_coordinates

  if isinstance(latitude, tuple):
        latitude = degrees_to_decimal_degrees(latitude)

  ha_decimal = degrees_to_decimal_degrees(Degrees(hour_angle))
  ha_degrees =  degrees_to_hours(ha_decimal)
  ha_radians = math.radians(ha_degrees)
  declination_decimal = degrees_to_decimal_degrees(declination)
  declination_radians = math.radians(declination_decimal)
  lat_radians = math.radians(latitude)

  sin_a = math.sin(declination_radians) * math.sin(lat_radians) + math.cos(declination_radians) * math.cos(lat_radians) * math.cos(ha_radians)

  altitude_radians = math.asin(sin_a)
  altitude_degrees = math.degrees(altitude_radians)

  y = -math.cos(declination_radians) * math.cos(lat_radians) * math.sin(ha_radians)
  x = math.sin(declination_radians) - math.sin(lat_radians) * sin_a
  azimuth_radians = math.atan2(y, x) # Python takes y as first argument
  azimuth_degrees = math.degrees(azimuth_radians)

  if azimuth_degrees < 0:
    azimuth_degrees += 360 # TODO: b - (360 * math.floor(b/360))

  altitude = Altitude(decimal_degrees_to_degrees(altitude_degrees))
  azimuth = Azimuth(decimal_degrees_to_degrees(azimuth_degrees))

  return HorizontalCoordinates((altitude, azimuth))

def horizon_to_equatorial_coordinates(horizontal_coordinates: HorizontalCoordinates, latitude: Latitude) -> EquatorialCoordinatesHourAngle:
  altitude, azimuth = horizontal_coordinates

  if isinstance(latitude, tuple):
    latitude = degrees_to_decimal_degrees(latitude)

  azimuth_decimal = degrees_to_decimal_degrees(azimuth)
  altitude_decimal = degrees_to_decimal_degrees(altitude)
  azimuth_radians = math.radians(azimuth_decimal)
  altitude_radians = math.radians(altitude_decimal)
  latitude_radians = math.radians(latitude)

  declination_sin = math.sin(altitude_radians) * math.sin(latitude_radians) + math.cos(altitude_radians) * math.cos(latitude_radians) * math.cos(azimuth_radians)

  declination_radians = math.asin(declination_sin)
  declination_degrees_decimal = math.degrees(declination_radians)
  declination = Declination(decimal_degrees_to_degrees(declination_degrees_decimal))

  y = -math.cos(altitude_radians) * math.cos(latitude_radians) * math.sin(azimuth_radians)
  x = math.sin(altitude_radians) - math.sin(latitude_radians) * declination_sin
  a = math.atan2(y, x)
  b = math.degrees(a)
  ha_hours = b - (360 * math.floor(b/360))
  ha = hours_to_degrees(ha_hours)

  hour_angle = HourAngle(Time(decimal_degrees_to_degrees(ha)))

  return EquatorialCoordinatesHourAngle((declination, hour_angle))

def mean_obliquity_ecliptic(greenwich_date: Date) -> Obliquity:
  julianDate = time_functions.greenwich_to_julian_date(greenwich_date)
  j2000 = time_functions.julian_date_to_j2000(julianDate)
  t = j2000 / 36525
  de = (t * (46.815 + t * (0.0006-(t * 0.00181)))) / 3600
  obliquity = 23.439292 - de

  return obliquity 

def ecliptic_to_equatorial_coordinates(ecliptic_coordinates: EclipticCoordinates, greenwich_date: Date) -> EquatorialCoordinates:
  eclat, eclon = ecliptic_coordinates

  if isinstance(eclat, tuple):
    eclat = degrees_to_decimal_degrees(eclat)
  if isinstance(eclon, tuple):
    eclon = degrees_to_decimal_degrees(eclon)

  eclat_decimal = eclat
  eclon_decimal = eclon

  eclon_rad = math.radians(eclon_decimal)
  eclat_rad = math.radians(eclat_decimal)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_date) + 0.001176447533936198 # this value is needed to correct, cannot be applied globally
  obliquity_rad = math.radians(obliquity_deg)
  declination_sin = math.sin(eclat_rad) * math.cos(obliquity_rad) + math.cos(eclat_rad) * math.sin(obliquity_rad) * math.sin(eclon_rad)
  declination_rad = math.asin(declination_sin)
  declination_degrees_decimal = math.degrees(declination_rad)
  declination_deg = Declination(decimal_degrees_to_degrees(declination_degrees_decimal))

  y = math.sin(eclon_rad) * math.cos(obliquity_rad) - math.tan(eclat_rad) * math.sin(obliquity_rad)
  x = math.cos(eclon_rad)
  right_ascension_rad = math.atan2(y,x)
  right_ascension_deg = math.degrees(right_ascension_rad)
  right_ascension_deg_corrected = right_ascension_deg - 360 * math.floor(right_ascension_deg/360)
  right_ascension_degrees =  hours_to_degrees(right_ascension_deg_corrected)

  right_ascension = RightAscension(Time(decimal_degrees_to_degrees(right_ascension_degrees)))

  return EquatorialCoordinates((declination_deg, right_ascension))

def equatorial_to_ecliptic_coordinates(equatorial_coordinates: EquatorialCoordinates, greenwich_date: Date) -> EclipticCoordinates:
  declination, right_ascension = equatorial_coordinates

  right_ascension_degrees = degrees_to_hours(degrees_to_decimal_degrees(Degrees(right_ascension))) 
  declination_deg = degrees_to_decimal_degrees(declination)
  right_ascension_rad = math.radians(right_ascension_degrees)
  declination_rad = math.radians(declination_deg)
  obliquity_deg = mean_obliquity_ecliptic(greenwich_date)
  obliquity_rad = math.radians(obliquity_deg)

  ecliptic_lat_sin = math.sin(declination_rad) * math.cos(obliquity_rad) - math.cos(declination_rad) * math.sin(obliquity_rad) * math.sin(right_ascension_rad) # TODO: common pattern can be extracted to a util

  ecliptic_lat_rad = math.asin(ecliptic_lat_sin) - 1.3284561980173026e-05 # this value is needed to correct, cannot be applied globally TODO investigate
  ecliptic_lat_deg = math.degrees(ecliptic_lat_rad)

  y = math.sin(right_ascension_rad) * math.cos(obliquity_rad) + math.tan(declination_rad) * math.sin(obliquity_rad) # TODO: common pattern can be extracted to a util
  x = math.cos(right_ascension_rad)
  ecliptic_long_rad = math.atan2(y, x)
  ecliptic_long_deg = math.degrees(ecliptic_long_rad)
  ecliptic_long_deg_corrected = ecliptic_long_deg - 360 * math.floor(ecliptic_long_deg / 360) # TODO

  latitude = decimal_degrees_to_degrees(ecliptic_lat_deg)
  longitude = decimal_degrees_to_degrees(ecliptic_long_deg_corrected)

  return EclipticCoordinates((latitude, longitude))

def equatorial_to_galactic_coordinates(equatorial_coordinates: EquatorialCoordinates) -> GalacticCoordinates:
  dec, ra = equatorial_coordinates

  dec_decimal = degrees_to_decimal_degrees(dec)
  ra_decimal = degrees_to_hours(degrees_to_decimal_degrees(Degrees(ra)))
  dec_rad = math.radians(dec_decimal)
  ra_rad = math.radians(ra_decimal)
  b = math.cos(dec_rad) * math.cos(math.radians(27.4)) * math.cos(ra_rad - math.radians(192.25)) + math.sin(dec_rad) * math.sin(math.radians(27.4))
  b_rad = math.asin(b)
  b_deg = math.degrees(b_rad)

  y = math.sin(dec_rad) - b * math.sin(math.radians(27.4))
  x = math.cos(dec_rad) * math.sin(ra_rad - math.radians(192.25)) * math.cos(math.radians(27.4))
  longitude = math.degrees(math.atan2(y,x)) + 33
  longitude_corrected = longitude - 360 * math.floor(longitude/360) # TODO: b - (360 * math.floor(b/360))

  latitude = decimal_degrees_to_degrees(b_deg)
  longitude = decimal_degrees_to_degrees(longitude_corrected)

  return GalacticCoordinates((latitude, longitude))

def galactic_to_equatorial_coordinates(galactic_coordinates: GalacticCoordinates) -> EquatorialCoordinates:
  lat, lon = galactic_coordinates

  if isinstance(lat, tuple):
    lat = degrees_to_decimal_degrees(lat)
  if isinstance(lon, tuple):
    lon = degrees_to_decimal_degrees(lon)
  
  lat_dec = lat
  lon_dec = lon

  lat_rad = math.radians(lat_dec)
  lon_rad = math.radians(lon_dec)

  sin_dec = math.cos(lat_rad) * math.cos(math.radians(27.4)) * math.sin(lon_rad - math.radians(33)) + math.sin(lat_rad) * math.sin(math.radians(27.4))
  declination = math.asin(sin_dec)
  declination_degrees_decimal = math.degrees(declination)
  declination_degrees = Declination(decimal_degrees_to_degrees(declination_degrees_decimal))

  y = math.cos(lat_rad) * math.cos(lon_rad - math.radians(33))
  x = math.sin(lat_rad) * math.cos(math.radians(27.4)) - math.cos(lat_rad) * math.sin(math.radians(27.4)) * math.sin(lon_rad - math.radians(33))
  right_ascension = math.degrees(math.atan2(y,x)) + 192.25
  right_ascension_corrected = right_ascension - 360 * math.floor(right_ascension/360)
  right_ascension_hours = decimal_degrees_to_degrees(hours_to_degrees(right_ascension_corrected))
  right_ascension = RightAscension(Time(right_ascension_hours))

  return EquatorialCoordinates((declination_degrees, right_ascension))

def angle_difference(object1_coordinates: EquatorialCoordinates, object2_coordinates: EquatorialCoordinates) -> Degrees:
  declination1, right_ascension1 = object1_coordinates
  decimal_declination1 = degrees_to_decimal_degrees(declination1)
  decimal_right_ascension1 = degrees_to_hours(degrees_to_decimal_degrees(Degrees(right_ascension1)))
  radians_declination1 = math.radians(decimal_declination1)
  radians_right_ascension1 = math.radians(decimal_right_ascension1)
  
  declination2, right_ascension2 = object2_coordinates
  decimal_declination2 = degrees_to_decimal_degrees(declination2)
  decimal_right_ascension2 = degrees_to_hours(degrees_to_decimal_degrees(Degrees(right_ascension2)))
  radians_declination2 = math.radians(decimal_declination2)
  radians_right_ascension2 = math.radians(decimal_right_ascension2)
  
  difference = radians_right_ascension1 - radians_right_ascension2
  cos_d = math.sin(radians_declination1) * math.sin(radians_declination2) + math.cos(radians_declination1) * math.cos(radians_declination2) * math.cos(difference)
  
  rad_d = math.acos(cos_d)
  deg_d = math.degrees(rad_d)

  return decimal_degrees_to_degrees(deg_d)
  
def rising_and_setting(target_coordinates: EquatorialCoordinates, observer_coordinates: GeographicCoordinates, greenwich_date: Date, vertical_shift: DecimalDegrees) -> tuple:
  dec, ra = target_coordinates
  decimal_right_ascension = degrees_to_decimal_degrees(Degrees(ra))
  radians_declination = math.radians(degrees_to_decimal_degrees(dec))
  radians_vertical_shift = math.radians(vertical_shift)
  lat, long = observer_coordinates

  if isinstance(lat, tuple):
    lat = degrees_to_decimal_degrees(lat)
    
  radians_geographic_latitude = math.radians(lat)

  cosine_ha = -(math.sin(radians_vertical_shift) + math.sin(radians_geographic_latitude) * math.sin(radians_declination)) / (math.cos(radians_geographic_latitude) * math.cos(radians_declination))
  hours_h = hours_to_degrees(math.degrees(math.acos(cosine_ha)))
  rise_lst = (decimal_right_ascension - hours_h) - 24 * int(((decimal_right_ascension - hours_h))/ 24)
  set_lst = (decimal_right_ascension + hours_h) - 24 * int(((decimal_right_ascension + hours_h))/ 24)

  a = math.degrees(math.acos((math.sin(radians_declination) + math.sin(radians_vertical_shift) * math.sin(radians_geographic_latitude)) / (math.cos(radians_vertical_shift) * math.cos(radians_geographic_latitude))))
  rise_az = a - 360 * int(a / 360)
  set_az = (360 - a) - 360 * int((360 - a)/ 360)

  rise_greenwich_sidereal_time = time_functions.local_sidereal_to_greenwich_sidereal_time(utils.decimal_time_to_time(rise_lst), long)
  rise_full_date = FullDate((greenwich_date, rise_greenwich_sidereal_time))
  set_greenwich_sidereal_time = time_functions.local_sidereal_to_greenwich_sidereal_time(utils.decimal_time_to_time(set_lst), long)
  set_full_date = FullDate((greenwich_date, set_greenwich_sidereal_time))
  _, (r_h, r_m, r_s) = time_functions.greenwich_sidereal_to_universal_time(rise_full_date)
  _, (s_h, s_m, s_s) = time_functions.greenwich_sidereal_to_universal_time(set_full_date)
  rise_time_adjusted = Time((r_h, r_m, r_s + 0.008333))
  set_time_adjusted = Time((s_h, s_m, s_s + 0.008333))

  circumpolar = True if cosine_ha < 1 else False

  return (circumpolar, rise_time_adjusted, set_time_adjusted, rise_az, set_az)

def precession_low_precision(equatorial_coordinates: EquatorialCoordinates, original_epoch: Epoch, new_epoch: Epoch) -> EquatorialCoordinates:
  dec1, ra1 = equatorial_coordinates
  dec1_rad = math.radians(degrees_to_decimal_degrees(dec1))
  ra1_rad = math.radians(degrees_to_hours(degrees_to_decimal_degrees(Degrees(ra1))))
  t_centuries = time_functions.julian_date_to_epoch(original_epoch, -2415020.5) / 36525
  m = 3.07234 + (0.00186 * t_centuries)
  n = 20.0468 - (0.0085 * t_centuries)
  n_years = time_functions.julian_date_to_epoch(new_epoch, -original_epoch)  / 365.25
  s1 = ((m + (n * math.sin(ra1_rad) * math.tan(dec1_rad) / 15)) * n_years) / 3600
  ra2 = degrees_to_decimal_degrees(Degrees(ra1)) + s1
  s2 = (n * math.cos(ra1_rad) * n_years) / 3600
  dec2 = degrees_to_decimal_degrees(dec1) + s2

  return EquatorialCoordinates((Declination(decimal_degrees_to_degrees(dec2)), RightAscension(Time(decimal_degrees_to_degrees(ra2)))))

def nutation_from_date(greenwich_date: Date) -> tuple:
  jd = time_functions.greenwich_to_julian_date(greenwich_date)
  t_centuries = time_functions.julian_date_to_epoch(jd, -2415020) / 36525
  a = 100.0021358 * t_centuries
  l1 = 279.6967 + (0.000303 * t_centuries**2)
  l2 = l1 + 360 * (a - math.floor(a))
  l3 = l2 - 360 * math.floor(l2 / 360)
  l4 = math.radians(l3)
  b = 5.372617 * t_centuries
  n1 = 259.1833 - 360 * (b - math.floor(b))
  n2 = n1 - 360 * (math.floor(n1 / 360))
  n3 = math.radians(n2)
  nutation_longtitude = (-17.2 * math.sin(n3) - 1.3 * math.sin(2 * l4)) / 3600
  nutation_obliquity = (9.2 * math.cos(n3) + 0.5 * math.cos(2 * l4)) / 3600

  return (nutation_longtitude, nutation_obliquity)

# if __name__ == '__main__':
    
#     date1 = 2433282.423

#     print(nutation_from_date(Date((1988,9,1))))