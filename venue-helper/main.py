import logging
import time

from apis import postBook, getRoom
from settings import courses, delay, counts

logger = logging.getLogger(__name__)

CDWIDs = []

datas = []

if __name__ == '__main__':
    while len(courses):
        course = courses[0]
        if course.get("CDWID", None) is None:
            rooms = getRoom(**{
                "XMDM": course["XMDM"],
                "YYRQ": course["YYRQ"],
                "YYLX": course["YYLX"],
                "KSSJ": course["KYYSJD"].split("-")[0],
                "JSSJ": course["KYYSJD"].split("-")[1],
                "XQDM": course["XQWID"],
            })
            time.sleep(0.2)
            if rooms is None:
                continue
            flag =False
            for room in rooms:
                if not room["disabled"]:
                    flag = True
                    course["CDWID"] = room["WID"]
                    datas.append(course)
            if not flag:
                logger.error(f"没有可预约的场地: {course}")
                print(f"没有可预约的场地: {course}")
                continue

        else:
            datas.append(course)
        courses.pop(0)

    for _ in range(counts):
        for course in datas:
            try:
                logger.info(f"开始预约: {course}")
                postBook(**course)
                time.sleep(delay / 1000)  # 延迟时间
            except Exception as e:
                logger.error(f"预约失败: {e}")
