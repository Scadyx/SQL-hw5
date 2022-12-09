from statistics import median
from fastapi import FastAPI
import uvicorn
from collections import Counter
import asyncio
from concurrent.futures import ThreadPoolExecutor
import httpx

app = FastAPI()


async def parser(url: str = 'http://app:8000/users'):
    async with httpx.AsyncClient() as client:
        responses = await client.get(url)
    return responses.json()




async def run_thread_pool(method, args):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, method, args)


class Worker:

    def __init__(self, data):
        self._data = data

    def medians(self, data):
        result = []
        for user in data:
            print(user)
            if user[0]['age'] is not None:
                result.append(user[0]['age'])
        print(result)

        return {'median': median(result)}

    def age_range(self, data):
        minmax = []
        for user in data:
            if 'age' in user[0]:
                if user[0]['age'] is not None:
                    if user[0]['age'] >= '20' and user[0]['age'] <= '30':
                        minmax.append(user)
            else:
                continue
        return minmax

    def unique_names(self, data):
        names = []
        for user in data:
            if user[0]['name'] is not None:
                names.append(user[0]['name'])
        res = Counter(names)
        return res


@app.get('/median')
async def run_median():
    data = await parser()
    worker = Worker(data)
    return await run_thread_pool(worker.medians, data)


@app.get('/age_range')
async def run_age_range():
    data = await parser()
    worker = Worker(data)
    return await run_thread_pool(worker.age_range, data)


@app.get('/unique_names_histogram')
async def run_unique_names_histogram():
    data = await parser()
    worker = Worker(data)
    return await run_thread_pool(worker.unique_names, data)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
