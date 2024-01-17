import os
import sys
import asyncio
import aiohttp
from aiohttp import ClientSession
from flask import Flask, request


app = Flask(__name__)


async def download_image(session: ClientSession, url: str, filename: str):
    async with session.get(url) as response:
        if response.status == 200:
            with open(filename, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)


async def download_images(urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            filename = url.split('/')[-1]
            task = asyncio.create_task(download_image(session, url, filename))
            tasks.append(task)
        await asyncio.wait(tasks)


@app.route('/download', methods=['POST'])
def download():
    urls = request.json.get('urls', [])
    if isinstance(urls, list) and len(urls) > 0:
        start_time = time.time()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_images(urls))
        end_time = time.time()
        total_time = end_time - start_time
        return f'Downloaded {len(urls)} images in {total_time} seconds'
    else:
        return 'Invalid request'


if __name__ == '__main__':
    app.run()