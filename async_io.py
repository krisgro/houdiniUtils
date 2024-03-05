import asyncio
from colorama import Fore, Back, Style

async def load_website():
    task = asyncio.create_task(fetch_data())
    print("step 1")
    print("step 2")
    print("step 3")
    print("step 4")
    print(".......")
    return_value = await task
    print(f"sucess in loading.. : {return_value}")

async def fetch_data():
    print("fetching data.....")
    await asyncio.sleep(4)
    return Fore.GREEN + "Data from the web server"

asyncio.run(load_website())