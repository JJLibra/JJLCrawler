import time
import asyncio

now = lambda: time.time()


# 同步编程
def task1():
    print("Start task 1")
    time.sleep(2)  # 模拟耗时操作
    print("End task 1")


def task2():
    print("Start task 2")
    time.sleep(1)  # 模拟耗时操作
    print("End task 2")


def main():
    start_time = now()
    task1()
    task2()
    print(f'同步编程耗时: {now() - start_time}')


main()


# 异步编程
async def async_task1():
    print("Start task 1")
    await asyncio.sleep(2)  # 模拟耗时操作
    print("End task 1")


async def async_task2():
    print("Start task 2")
    await asyncio.sleep(1)  # 模拟耗时操作
    print("End task 2")


async def main():
    start = now()
    # 并发运行两个任务
    await asyncio.gather(async_task1(), async_task2())
    print(f'异步编程耗时: {now() - start}')


asyncio.run(main())
