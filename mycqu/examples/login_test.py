from mycqu.auth import login, NeedCaptcha
from mycqu.course.models.course_timetable import CourseTimetable
from mycqu.mycqu import access_mycqu
from requests import Session

session = Session()
try:
   login(session, "27130525", "bdsc11081bdsc") # 需要登陆
except NeedCaptcha as e: # 需要输入验证码的情况
   with open("captcha.jpg", "wb") as file:
      file.write(e.image)
   print("输入 captcha.jpg 处的验证码并回车: ", end="")
   e.after_captcha(input())
access_mycqu(session)

timetables = CourseTimetable.fetch(session, "201xxxxx")  # 获取学号 201xxxxx 的本学期课表
week = 9
print(f"第 {week} 周的课")
weekdays = ["一", "二", "三", "四", "五", "六", "日"]
for timetable in timetables:
   for start, end in timetable.weeks:
      if start <= week <= end:
            break
   else:
      continue
   if timetable.day_time:
      print(f"科目：{timetable.course.name}, 教室：{timetable.classroom}, "
            f"周{weekdays[timetable.day_time.weekday]} {timetable.day_time.period[0]}~{timetable.day_time.period[1]} 节课")
   elif timetable.whole_week:
      print(f"科目：{timetable.course.name}, 地点: {timetable.classroom}, 全周时间")
   else:
      print(f"科目：{timetable.course.name}, 无明确时间")