from typing import List

import os

from pathlib import Path
import shutil

from cli import args
from log import setup_logging

def validate_source_mirror(source: Path, mirror: Path) -> bool:
    commonpath = ''

    if source.anchor == mirror.anchor:
        commonpath = os.path.commonpath([source, mirror])

    if source == mirror or commonpath == source or commonpath == mirror:
        logger.error(msg='ERROR | CIRCULAR REFERENCE')
        return False

    if not source.exists():
        logger.error(msg=f'ERROR | SOURCE PATH NOT FOUND | {source}')
        return False

    if not mirror.exists():
        logger.error(msg=f'ERROR | MIRROR PATH NOT FOUND | {mirror}')
        return False
    
    return True

def contents(path: Path) -> dict[str, list]:
    is_dir = []
    is_file = []

    for content in list(path.glob(pattern='**/*')):
        path_relative_as_posix = content.relative_to(path).as_posix()

        if content.is_dir():
            is_dir.append(path_relative_as_posix)
        else:
            is_file.append(path_relative_as_posix)

    return {'is_dir': is_dir, 'is_file': is_file}

def ignore_dir(contents: dict[str, list], ignore: List[str]) -> dict[str, list]:
    
    # is_dir
    index = 0
    while index < len(contents['is_dir']):
        values = contents['is_dir'][index].split('/')
        if any(_ignore in values for _ignore in ignore):
            contents['is_dir'].pop(index)
            index -= 1

        index += 1

    # is_file
    index = 0
    while index < len(contents['is_file']):
        values = contents['is_file'][index].split('/')[:-1]
        if any(_ignore in values for _ignore in ignore):
            contents['is_file'].pop(index)
            index -= 1

        index += 1

    return contents

def send(contents: dict[str, set]) -> None:
    
    # is_dir
    for content in contents['is_dir']:
        source = source_path / content
        mirror = mirror_path / content

        try:
            logger.info(msg=f'+ {mirror} | DIRECTORY')
            mirror.mkdir(parents=True, exist_ok=True)
            shutil.copystat(source, mirror)
        except Exception as e:
            logger.error(msg=f'\tERROR | {mirror}')
            logger.error(msg=f'\t{e}')
            pass

    # is_file
    for content in contents['is_file']:
        source = source_path / content
        mirror = mirror_path / content

        try:
            logger.info(msg=f'+ {mirror} | FILE')
            source.copy(mirror, preserve_metadata=True)
        except Exception as e:
            logger.error(msg=f'\tERROR | {mirror}')
            logger.error(msg=f'\t{e}')
            pass

def update(contents: dict[str, set]) -> None:

    # is_dir
    for content in contents['is_dir']:
        source = source_path / content
        mirror = mirror_path / content

        try:
            if source.stat().st_mtime_ns != mirror.stat().st_mtime_ns:
                try:
                    logger.info(msg=f'> {mirror} | DIRECTORY')
                    shutil.copystat(source, mirror)
                except Exception as e:
                    logger.error(msg=f'\tERROR | {mirror}')
                    logger.error(msg=f'\t{e}')
                    pass
        except Exception as e:
            logger.error(msg=f'\tERROR | {mirror}')
            logger.error(msg=f'\t{e}')
            pass
            
    # is_file
    for content in contents['is_file']:
        source = source_path / content
        mirror = mirror_path / content

        try:
            if source.stat().st_mtime_ns != mirror.stat().st_mtime_ns:
                try:
                    logger.info(msg=f'> {mirror} | FILE')
                    source.copy(mirror, preserve_metadata=True)
                except Exception as e:
                    logger.error(msg=f'\tERROR | {mirror}')
                    logger.error(msg=f'\t{e}')
                    pass

        except Exception as e:
            logger.error(msg=f'\tERROR | {mirror}')
            logger.error(msg=f'\t{e}')
            pass

def delete(contents: dict[str, set]) -> None:

    # is_file
    for content in contents['is_file']:
        mirror = mirror_path / content

        try:
            logger.info(msg=f'- {mirror} | FILE')
            mirror.unlink(missing_ok=True)
        except Exception as e:
            logger.error(msg=f'\tERROR | {mirror}')
            logger.error(msg=f'\t{e}')
            pass
    
    # is_dir
    for content in contents['is_dir']:
        mirror = mirror_path / content

        try:
            logger.info(msg=f'- {mirror} | DIRECTORY')
            mirror.rmdir()
        except Exception as e:
            logger.error(msg=f'\tERROR | {mirror}')
            logger.error(msg=f'\t{e}')
            pass

def sync_mirror(source: Path, mirror: Path, ignore: List[str]) -> None:

    if not validate_source_mirror(source=source, mirror=mirror):
        return

    content_source = contents(source)
    content_mirror = contents(mirror)

    if ignore:
        content_source = ignore_dir(content_source, ignore)
    
    # UPDATE
    to_update = dict()
    to_update['is_dir'] = set(content_source['is_dir']) & set(content_mirror['is_dir'])
    to_update['is_dir'] = sorted(list(to_update['is_dir'])) # type: ignore
    to_update['is_file'] = set(content_source['is_file']) & set(content_mirror['is_file'])
    update(to_update)

    # SEND
    to_send = dict()
    to_send['is_dir'] = set(content_source['is_dir']) - set(content_mirror['is_dir'])
    to_send['is_dir'] = sorted(list(to_send['is_dir'])) # type: ignore
    to_send['is_file'] = set(content_source['is_file']) - set(content_mirror['is_file'])
    send(to_send)
    
    # DELETE
    to_delete = dict()
    to_delete['is_dir'] = set(content_mirror['is_dir']) - set(content_source['is_dir'])
    to_delete['is_dir'] = sorted(list(to_delete['is_dir']), reverse=True) # type: ignore
    to_delete['is_file'] = set(content_mirror['is_file']) - set(content_source['is_file'])
    delete(to_delete)

logger = setup_logging(logprefix=args.logprefix, verbose=args.verbose)

if args.source and args.mirror:
    source_path = Path(args.source)
    mirror_path = Path(args.mirror)
    
    sync_mirror(source=source_path, mirror=mirror_path, ignore=args.ignore)