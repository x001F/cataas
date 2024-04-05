import aiohttp
from aiogram.types import BufferedInputFile, FSInputFile, InputFile
from typing import Tuple, AnyStr, Callable
from functools import wraps
from urllib.parse import quote
import re
from src.config import *
# I will rebuild this. When I rebuild this every :tag from /cattag will work...
# Either on site not every tag work - https://cataas.com/cat/Quintico - exists in api tags but don't work

logger = get_logger('main.api')
urls = {
    'cat': 'https://cataas.com/cat',
    'cattag': 'https://cataas.com/cat/:tag',
    'catgif': 'https://cataas.com/cat/gif',
    'catsays': 'https://cataas.com/cat/says/:text',
    'catgifsays': 'https://cataas.com/cat/gif/says/:text',
    'cattagsays': 'https://cataas.com/cat/:tag/says/:text',
    'catsaysmore': 'https://cataas.com/cat/says/:text?fontSize=:size&fontColor=:color',
    'catgifsaysmore': 'https://cataas.com/cat/gif/says/:text?fontSize=:size&fontColor=:color',
    'cattype': 'https://cataas.com/cat?type=:type',
    'catfilter': 'https://cataas.com/cat?filter=:filter',
    'catfiltercustom': 'https://cataas.com/cat?filter=custom&r=:red&g=:green&b=:blue',
    'catsize': 'https://cataas.com/cat?width=:width&?height=:height',
    'tags': 'https://cataas.com/api/tags',
}


def shield(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> InputFile | tuple | int:
        try:
            result = await func(*args, **kwargs)
        except aiohttp.client_exceptions.ClientOSError as e:
            logger.error(func.__name__, '-', e)
            return FSInputFile(path='other/Error.png')
        except aiohttp.client_exceptions.ClientConnectorError as e:
            logger.error(func.__name__, '-', e)
            return FSInputFile(path='other/Error.png')
        else:
            return result
    return wrapper


@shield
async def _download(url: str) -> InputFile:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_bin = await response.content.read()
            print(response.status)
            if response.status != 200:
                logger.error(f'{url} returned {response.status} code.\nResponse: {image_bin}')
                return FSInputFile(path='src/other/Error.png')
            elif len(image_bin) < 500:
                # Can't find out what incoming bin is (image/text)
                logger.error(f'{url} returned no image')
                return FSInputFile(path='src/other/CatNotFound.png')

            logger.info(f'{url} returned valid image')
            if url[23:26] == 'gif':
                return BufferedInputFile(image_bin, 'kitty.gif')
            return BufferedInputFile(image_bin, 'kitty.png')


async def cat() -> InputFile:
    logger.debug('Downloading cat')
    return await _download(urls['cat'])


async def cat_tag(tag: str) -> InputFile:
    logger.debug(f'Downloading cat with {tag}')
    _url = re.sub(r':tag', quote(tag), urls['cattag'])
    return await _download(_url)


async def cat_gif() -> InputFile:
    logger.debug('Downloading gif cat')
    return await _download(urls['catgif'])


async def cat_says(text: str) -> InputFile:
    logger.debug(f'Downloading cat saying: "{text}"')
    _url = re.sub(r':text', quote(text), urls['catsays'])
    return await _download(_url)


async def cat_tagsays(tag: str, text: str) -> InputFile:
    logger.debug(f'Downloading cat with "{tag}" saying "{text}"')
    _url = re.sub(r':tag', quote(text), urls['cattagsays'])
    _url = re.sub(r':text', quote(text), _url)
    return await _download(_url)


async def cat_says_more(text: str, color: str, size: str) -> InputFile:
    logger.debug(f'Downloading cat saying "{text}" with {size} text and "{color}" text')
    _url = re.sub(r':text', quote(text), urls['catsaysmore'])
    _url = re.sub(r':color', quote(color), _url)
    _url = re.sub(r':size', quote(size), _url)
    return await _download(_url)


async def cat_gif_says(text: str) -> InputFile:
    logger.debug(f'Downloading gif cat saying "{text}"')
    _url = re.sub(r':text', quote(text), urls['catgifsays'])
    return await _download(_url)


async def cat_gif_says_more(text: str, color: str, size: str) -> InputFile:
    logger.debug(f'Downloading gif cat saying "{text}" with {size} text and "{color}" text')
    _url = re.sub(r':text', quote(text), urls['catgifsaysmore'])
    _url = re.sub(r':color', quote(color), _url)
    _url = re.sub(r':size', quote(size), _url)
    return await _download(_url)


async def cat_type(image_type: str) -> InputFile:
    logger.debug(f'Downloading cat with "{image_type}" type')
    _url = re.sub(r':type', quote(image_type), urls['cattype'])
    return await _download(_url)


async def cat_filter(filter: str) -> InputFile:
    logger.debug(f'Downloading cat with {filter} filter')
    _url = re.sub(r':filter', quote(filter), urls['catfilter'])
    return await _download(_url)


async def cat_filter_custom(red: int, green: int, blue: int) -> InputFile:
    logger.debug(f'Downloading cat with {red},{green},{blue} filter')
    _url = re.sub(r':red', quote(str(red)), urls['catfiltercustom'])
    _url = re.sub(r':green', quote(str(green)), _url)
    _url = re.sub(r':blue', quote(str(blue)), _url)
    return await _download(_url)


async def cat_size(height: int, width: int) -> InputFile:
    logger.debug(f'Downloading cat {height}x{width}')
    _url = re.sub(r':height', quote(str(height)), urls['catsize'])
    _url = re.sub(r'width', quote(str(width)), _url)
    return await _download(_url)


async def tags() -> Tuple[AnyStr]:
    logger.debug('Downloading existing tags')
    async with aiohttp.ClientSession() as session:
        async with session.get(urls['tags']) as r:
            return tuple(await r.json())
