import pytest

import os
from beni import bcrypto, bfile, bpath, bzip
from beni.bqiniu import QiniuBucket
from beni.btype import Null

_SECRET = 'x6oIvhJbHM9pilQUx7JNVii6tu4nnBRqc/VADjgyJj8tgxj2xdbLijAigL2pKmxuUe54nngHYKOG+TppaNKW/zsAzoZ+nkLu83n+/Ih3m5NWQTQW2rXVArcnXoUwMLuqdgi4ZrAFbXI5CMb0pFgxWQlOnKVvIUEHROEM2T5g4wTMZVN1hq8XX7uGwQh5lG1/HpYncmLwts4npny42BAjSbzMijY7YVYfInYEi7bGELGnztHVHPqLkfF6SbRXhtV0xdWqbfmBL7PbyokWBpEsv60='
_bucket: QiniuBucket = Null
_PREFIX = 'test/'


def _getBucket():
    global _bucket
    _bucket = _bucket or QiniuBucket(**bcrypto.decryptJson(_SECRET, os.environ['PYTEST_PASSWORD']))
    return _bucket


@pytest.mark.order()
@pytest.mark.asyncio
async def test_clearAll():
    fileList, _ = await _getBucket().getFileList(_PREFIX, 999999)
    if fileList:
        keyList = [x.key for x in fileList]
        await _getBucket().deleteFiles(*keyList)


@pytest.mark.order()
@pytest.mark.asyncio
async def test_uploadBytes():
    url = await _getBucket().uploadBytes(_PREFIX + 'data.bytes', b'hello world')
    assert url


@pytest.mark.order()
@pytest.mark.asyncio
async def test_uploadStr():
    url = await _getBucket().uploadStr(_PREFIX + 'data.txt', 'hello world')
    assert url


@pytest.mark.order()
@pytest.mark.asyncio
async def test_uploadJson():
    url = await _getBucket().uploadJson(_PREFIX + 'data.json', {'hello': 'world'})
    assert url


@pytest.mark.order()
@pytest.mark.asyncio
async def test_getPrivateBytes():
    data = await _getBucket().getPrivateBytes(_PREFIX + 'data.bytes')
    assert data == b'hello world'


@pytest.mark.order()
@pytest.mark.asyncio
async def test_getPrivateStr():
    data = await _getBucket().getPrivateStr(_PREFIX + 'data.txt')
    assert data == 'hello world'


@pytest.mark.order()
@pytest.mark.asyncio
async def test_getPrivateJson():
    data = await _getBucket().getPrivateJson(_PREFIX + 'data.json')
    assert data == {'hello': 'world'}


@pytest.mark.order()
@pytest.mark.asyncio
async def test_uploadFile():
    with bpath.useTempFile() as file:
        await bfile.writeText(file, 'hello world')
        url = await _getBucket().uploadFile(_PREFIX + 'file.txt', file)
        assert url


@pytest.mark.order()
@pytest.mark.asyncio
async def test_getPrivateFileUrl():
    url = _getBucket().getPrivateFileUrl(_PREFIX + 'file.txt')
    assert url


@pytest.mark.order()
@pytest.mark.asyncio
async def test_downloadPrivateFile():
    with bpath.useTempFile() as file:
        await _getBucket().downloadPrivateFile(_PREFIX + 'file.txt', file)
        assert await bfile.readText(file) == 'hello world'


@pytest.mark.order()
@pytest.mark.asyncio
async def test_downloadPrivateFileUnzip():
    with bpath.useTempPath() as uploadPath, bpath.useTempPath() as downloadPath:
        uploadFile = uploadPath / 'upload.txt'
        uploadZipFile = uploadPath / 'upload.zip'
        await bfile.writeText(uploadFile, 'hello world')
        bzip.zipFile(uploadZipFile, uploadFile)
        await _getBucket().uploadFile(_PREFIX + 'upload.zip', uploadZipFile)
        await _getBucket().downloadPrivateFileUnzip(_PREFIX + 'upload.zip', downloadPath)
        outputFile = downloadPath / 'upload.txt'
        assert await bfile.readText(outputFile) == 'hello world'


@pytest.mark.order()
@pytest.mark.asyncio
async def test_downloadPrivateFileSevenUnzip():
    with bpath.useTempPath() as uploadPath, bpath.useTempPath() as downloadPath:
        uploadFile = uploadPath / 'upload.txt'
        uploadZipFile = uploadPath / 'upload.7z'
        await bfile.writeText(uploadFile, 'hello world')
        await bzip.sevenZip(uploadZipFile, uploadFile)
        await _getBucket().uploadFile(_PREFIX + 'upload.7z', uploadZipFile)
        await _getBucket().downloadPrivateFileSevenUnzip(_PREFIX + 'upload.7z', downloadPath)
        outputFile = downloadPath / 'upload.txt'
        assert await bfile.readText(outputFile) == 'hello world'


@pytest.mark.order()
@pytest.mark.asyncio
async def test_getFileListByMarker():
    fileList, makert = await _getBucket().getFileList(_PREFIX, 2)
    assert len(fileList) == 2
    assert makert
    fileList, _ = await _getBucket().getFileListByMarker(makert, 2)
    assert len(fileList) == 2


@pytest.mark.order()
@pytest.mark.asyncio
async def test_deleteFiles():
    result = await _getBucket().deleteFiles(
        _PREFIX + 'upload.zip',
        _PREFIX + 'upload.7z',
    )
    assert not result


@pytest.mark.order()
@pytest.mark.asyncio
async def test_hashFile():
    with bpath.useTempFile() as file:
        await bfile.writeText(file, 'hello world')
        hash = await _getBucket().hashFile(file)
        assert hash


@pytest.mark.order()
@pytest.mark.asyncio
async def test_getFileStatus():
    result = await _getBucket().getFileStatus(_PREFIX + 'file.txt')
    assert result


@pytest.mark.order()
@pytest.mark.asyncio
async def test_move():
    url = await _getBucket().move(_PREFIX + 'file.txt', _PREFIX + 'file2.txt')
    assert url


@pytest.mark.order()
@pytest.mark.asyncio
async def test_copy():
    url = await _getBucket().copy(_PREFIX + 'file2.txt', _PREFIX + 'file3.txt')
    assert url
