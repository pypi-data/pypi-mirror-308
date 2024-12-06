import math
from astronomy_types import Year, Date, JulianDate, Epoch, DaysOfWeek, DecimalTime, Time, FullDate, Longitude 
import utils

def date_of_easter(year: Year) -> Date:
  a = year % 19
  b = math.floor(year / 100)
  c = year % 100
  d = math.floor(b / 4)
  e = b % 4
  f = math.floor((b + 8) / 25)
  g = math.floor((b - f - 1) / 3)
  h = ((19 * a) + b - d - g + 15) % 30
  i = math.floor(c / 4)
  k = c % 4
  l = (32 + (2 * e) + (2 * i) - h - k) % 7
  m = math.floor((a + (11 * h) + (22 * l)) / 451)
  n = math.floor((h + l - (7 * m) + 114) / 31)
  p = (h + l - (7 * m) + 114) % 31
  day = p + 1
  month = n

  return Date((year, month, day))

def date_to_day_number(date: Date) -> int:
  year, month, day = date
  if month > 2:
    j = math.floor((month + 1) * 30.6)

    if (year_is_leap(year)):
      k = j - 62
    else:
      k = j - 63

    return int(k + day)
  
  else:
    if (year_is_leap(year)):
      d = (month - 1) * 62
    else:
      d = (month - 1) * 63
    f = math.floor(d / 2)

    return int(f + day)   
  
def year_is_leap(year: Year) -> bool:
  year_divisable_by_4 = year % 4 == 0
  year_divisable_by_100 = year % 100 == 0
  year_divisable_by_400 = year % 400 == 0
  
  if((year_divisable_by_4 and year_divisable_by_100 and year_divisable_by_400) or (year_divisable_by_4 and not year_divisable_by_100)):
    return True
    
  return False

def greenwich_to_julian_date(date: Date) -> JulianDate:
  year, month, day = date
  if month == 1 or month == 2:
    y = year -1
    m = month + 12
  else:
    y = year
    m = month

  if year > 1582 or year == 1582 and month > 10 or year == 1582 and month == 10 and day > 15:
    a = math.floor(y / 100)
    b = 2 - a + math.floor(a / 4)
  else:
    b = 0
  
  if y < 0:
    c = math.floor((365.25 * y) - 0.75)
  else:
    c = math.floor(365.25 * y)

  d = math.floor(30.6001 * (m + 1))
  jd = b + c + d + day + 1720994.5

  return jd

def julian_to_greenwich_date(julianDate: JulianDate) -> Date:
  jd = julianDate + 0.5
  i = math.floor(jd)
  f = jd - i
  
  if i > 2299160:
    a = math.floor((i - 1867216.25) / 36524.25)
    b = i + a - math.floor(a / 4) + 1
  else:
    b = 1

  c = b + 1524
  d = math.floor((c - 122.1) / 365.25)
  e = math.floor(365.25 * d)
  g = math.floor((c - e) / 30.6001)

  day = c - e + f - math.floor(30.6001 * g)
  month = g - 1 if g < 13.5 else g - 13
  year = d - 4716 if month > 2.5 else d - 4715

  return Date((year, month, day))

def julian_date_to_j2000(julianDate: JulianDate) -> Epoch:
  return julian_date_to_epoch(julianDate, -2451545.0)

def julian_date_to_epoch(julianDate: JulianDate, adjustment: float) -> Epoch:
  return julianDate + adjustment

def finding_day_of_week(julianDate: JulianDate) -> DaysOfWeek:
  julianDay = (julianDate + 1.5) % 7
  dayNumber = math.floor(julianDay)

  days = [DaysOfWeek.Sunday, DaysOfWeek.Monday, DaysOfWeek.Tuesday, DaysOfWeek.Wednesday, DaysOfWeek.Thursday, DaysOfWeek.Friday, DaysOfWeek.Saturday]

  return days[dayNumber]

def hours_minutes_seconds_to_decimal_time(time: Time, twenty_four_hour_clock = True) -> DecimalTime:
  c = utils.time_to_decimal_time(time)

  return c if twenty_four_hour_clock or c <= 12 else c - 12

def decimal_hours_to_hours_minutes_seconds(decimalTime: DecimalTime) -> Time:
  hours, minutes, seconds = utils.decimal_time_to_time(decimalTime)
  hours = hours * -1 if decimalTime < 0 else hours

  return Time((hours, minutes, seconds))

def local_civil_to_universal_time(local_time_and_date: FullDate, daylight_savings_correction = 0, timezone_offset_correction = 0) -> FullDate:
  (local_year, local_month, local_day), (local_hours, local_minutes, local_seconds) = local_time_and_date
  zone_time = local_hours - daylight_savings_correction
  decimal_zone_time = hours_minutes_seconds_to_decimal_time(Time((zone_time, local_minutes, local_seconds)))
  ut = decimal_zone_time - timezone_offset_correction
  greenwich_calendar_day = local_day + (ut / 24)
  jd = greenwich_to_julian_date(Date((local_year, local_month, greenwich_calendar_day)))
  greenwich_year, greenwich_month, greenwich_day = julian_to_greenwich_date(jd)

  utc = decimal_hours_to_hours_minutes_seconds(24 * (greenwich_calendar_day - math.floor(greenwich_calendar_day)))
  date = Date((greenwich_year, greenwich_month, math.floor(greenwich_day)))

  return FullDate((date, utc))

def universal_to_local_civil_time(universal_time_and_date: FullDate, timezone_offset_correction = 0, daylight_savings_correction = 0) -> FullDate:
  greenwich_date, utc = universal_time_and_date
  decimalHours = hours_minutes_seconds_to_decimal_time(utc)
  lct = decimalHours + timezone_offset_correction + daylight_savings_correction
  jd = greenwich_to_julian_date(greenwich_date)
  ljd = jd + (lct / 24)
  local_civil_year, local_civil_month, local_civil_day = julian_to_greenwich_date(ljd)
  integer_day = math.floor(local_civil_day)

  local_date = Date((local_civil_year, local_civil_month, integer_day))
  lct = Time(decimal_hours_to_hours_minutes_seconds((local_civil_day - integer_day) * 24))
  
  return FullDate((local_date, lct))

def universal_to_greenwich_sidereal_time(universal_time_and_date: FullDate) -> Time:
  date, time = universal_time_and_date
  julianDate = greenwich_to_julian_date(date) 
  s = julian_date_to_j2000(julianDate)
  t = s / 36525.0
  t0 = 6.697374558+(2400.051336*t)+(0.000025862*t**2)
  t1 = t0 - (24 * math.floor(t0 / 24))
  ut = hours_minutes_seconds_to_decimal_time(time)
  a = ut * 1.002737909
  gst0 = a + t1

  gst = gst0 - (24 * math.floor(gst0 / 24))

  return decimal_hours_to_hours_minutes_seconds(gst)

def greenwich_sidereal_to_universal_time(greenwich_date_and_sidereal_time: FullDate) -> FullDate:
  greenwich_date, greenwich_sidereal_time  = greenwich_date_and_sidereal_time
  julianDate = greenwich_to_julian_date(greenwich_date) 
  s = julian_date_to_j2000(julianDate)
  t = s / 36525.0
  t0 = 6.697374558+(2400.051336*t)+(0.000025862*t**2)
  t1 = t0 - (24 * math.floor(t0 / 24))
  gst_decimal = hours_minutes_seconds_to_decimal_time(greenwich_sidereal_time)
  a = gst_decimal - t1
  b = a - (24 * math.floor(a / 24))
  ut = b * 0.9972695663

  utc = decimal_hours_to_hours_minutes_seconds(ut)

  return FullDate((greenwich_date, utc))

def greenwich_sidereal_to_local_sidereal_time(greenwich_sidereal_time: Time, longitude: Longitude) -> Time:
  gst_decimal = hours_minutes_seconds_to_decimal_time(greenwich_sidereal_time)
  if isinstance(longitude, tuple):
    longitude = longitude[0]
  offset = longitude / 15
  lst = gst_decimal + offset
  lst1 = lst - (24 * math.floor(lst / 24))

  non_decimal_lst = decimal_hours_to_hours_minutes_seconds(lst1)

  return non_decimal_lst

def local_sidereal_to_greenwich_sidereal_time(local_sidereal_time: Time, longitude: Longitude) -> Time:
  lst_decimal = hours_minutes_seconds_to_decimal_time(local_sidereal_time)
  if isinstance(longitude, tuple):
    longitude = longitude[0]
  offset = longitude / 15
  gst = lst_decimal - offset
  gst1 = gst - (24 * math.floor(gst / 24))

  non_decimal_lst = decimal_hours_to_hours_minutes_seconds(gst1)

  return non_decimal_lst
