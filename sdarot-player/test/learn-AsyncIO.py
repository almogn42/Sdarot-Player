# #!/usr/bin/env python3
# # countasync.py
#
# #importing the module
# import asyncio
#
# #Defining the asyncronus function
# async def count():
#     print("One")
#     #making the program Wailt
#     await asyncio.sleep(1)
#     print("Two")
#
# async def main():
#     await asyncio.gather(count(), count(), count())
#
# if __name__ == "__main__":
#     import time
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")
#
#
# print("\n\n\n\n\nNoAsyce")
#
#
#     #importing the module
# import asyncio
# import time
# #Defining the asyncronus function
# def count():
#     print("One")
#     #making the program Wailt
#     time.sleep(1)
#     print("Two")
#
# def main():
#     count()
#     count()
#     count()
#
# if __name__ == "__main__":
#     s = time.perf_counter()
#     main()
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# import asyncio
#
#
# async def counterA():
#     for a in range(15):
#
#         print(f"a is: {a}")
#         await asyncio.sleep(2)
#
#
# async def counterB():
#     for b in range(15):
#         print(f"b is: {b}")
#         await asyncio.sleep(1)
#
# async def runner():
#
#     # await asyncio.sleep(6)
#     # await counterB()
#     asyncio.create_task(counterA())
#     asyncio.create_task(counterB())
#     await asyncio.sleep(5)
#
# asyncio.run(runner())


import asyncio
from os import getcwd,popen

# async def MPV():
#     Player_Command = fr'"C:\Users\almogn\Downloads\mpv-x86_64-20220807-git-9add44b\mpv" "C:\Users\almogn\Videos\Captures\Windows PowerShell 2022-09-06 08-36-57.mp4"'
#     player = popen(Player_Command)
#     print(player.read())
#
# async def counter():
#
#     for a in range(26000123):
#         await asyncio.sleep(0)
#         try:
#             print(a)
#
#         except asyncio.CancelledError as e:
#             print("Stopping the alarm")
#
#
#
# async def runner():
#
#     task1 = asyncio.create_task(counter())
#     await MPV()
#
#     await asyncio.sleep(2)
#     a = task1.cancel()
#     print(a)
    # await task1
from random import random
async def RunIncremental():
    for a in range(10):
        print("inc: " + str(a+1))
        await asyncio.sleep(random()/10)

async def RunDecrimental():
    for a in range(10)[::-1]:
        print("dec: " + str(a+1))
        await asyncio.sleep(random()/10)

async def runner():
    # task1 = asyncio.create_task(RunIncremental())
    # task2 = asyncio.create_task(RunDecrimental())
    await asyncio.gather(RunDecrimental(),RunIncremental())
    print("tasks were finished successfully")
asyncio.run(runner())
