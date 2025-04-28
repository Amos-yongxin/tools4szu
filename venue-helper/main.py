import logging
import time

from apis import postBook
from settings import courses,delay, counts
logger = logging.getLogger(__name__)

# 使用示例
if __name__ == '__main__':
    for _ in range(counts):
        for course in courses:
            try:
                logger.info(f"开始预约: {course}")
                postBook(**course)
                time.sleep(delay / 1000)  # 延迟时间
            except Exception as e:
                logger.error(f"预约失败: {course}, 错误信息: {e}")

