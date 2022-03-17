import os
from pathlib import Path
from src import logger

def extract_avatar_url(full_avatar_url: str):
    print(f'\nExtracting avatar url: {full_avatar_url}...')
    try:
        the_url = full_avatar_url.split('/static')[1]
        print(f'Extracted the avatar url: {the_url}...')
        return the_url
    except Exception as ect:
        print(f'Error to extract url [{full_avatar_url}]:', ect)
        return 'default_user.jpg'

def server_name():
    import socket
    return socket.gethostname()

def get_svg_content(url: str, width=24, height=24, classes=''):
    # logger.info(f'\nGetting svg content: {url}...')
    try:
        path = Path(__file__).parent / f'../static/{url}'
        svg = path.resolve().open().read()

        svg = svg.split('<svg ')
        svg = '<svg ' + f'class="{classes}" ' + svg[1]
        
        # remove the 'fill' attributes
        svg = ''.join(svg.split('fill="none"'))
        svg = ''.join(svg.split('fill="#212121"'))

        svg = f'width={width}'.join(svg.split('width="24"'))
        svg = f'height={height}'.join(svg.split('height="24"'))

        # print(svg)
        return svg
    except Exception as ect:
        print(f'Error to extract url [{url}]:', ect)
        return ''
