import re
import subprocess
import tempfile
from pathlib import Path

from synapse_sdk.utils.file import calculate_checksum, download_file
from synapse_sdk.utils.storage import get_storage


def archive(source_path, archive_path):
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    command = f'git ls-files --others --exclude-standard --cached  | zip -q --names-stdin {archive_path}'
    subprocess.run(command, cwd=source_path, shell=True, check=True, stdout=subprocess.DEVNULL)


def download_and_upload(source_url, url):
    storage = get_storage(url)
    with tempfile.TemporaryDirectory() as temp_path:
        file_path = str(download_file(source_url, temp_path))
        checksum = calculate_checksum(file_path, prefix='dev')
        # TODO 중복 체크
        return storage.upload(file_path, f'{checksum}.zip')


def archive_and_upload(source_path, url):
    storage = get_storage(url)
    dist_path = Path(source_path, 'dist')
    archive_path = dist_path / 'archive.zip'

    archive(source_path, archive_path)
    checksum = calculate_checksum(archive_path, prefix='dev')
    checksum_archive_path = dist_path / f'{checksum}.zip'

    if checksum_archive_path.exists():
        # TODO 실제 스토리지 있는지 확인
        return storage.get_url(checksum_archive_path.name)

    archive_path.rename(checksum_archive_path)
    for file_path in dist_path.glob('*.zip'):
        if file_path.name != checksum_archive_path.name:
            file_path.unlink()
    return storage.upload(str(checksum_archive_path), checksum_archive_path.name)


def build_and_upload(source_path, url, virtualenv_path='.venv'):
    storage = get_storage(url)
    dist_path = Path(source_path, 'dist')
    archive_path = dist_path / 'archive.zip'

    archive(source_path, archive_path)
    checksum = calculate_checksum(archive_path, prefix='dev')
    checksum_archive_path = dist_path / f'{checksum}.zip'

    if checksum_archive_path.exists():
        # TODO 실제 스토리지 있는지 확인
        wheel_path = next(dist_path.glob('*.whl'), None)
        return storage.get_url(wheel_path.name)

    # wheel file 빌드 진행
    for file_path in dist_path.glob('*.whl'):
        file_path.unlink()

    print(f'Building {Path(source_path).name}...')
    subprocess.run(
        f'{virtualenv_path}/bin/python -m build --wheel',
        cwd=source_path,
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    wheel_path = next(dist_path.glob('*.whl'), None)

    archive_path.rename(checksum_archive_path)
    for file_path in dist_path.glob('*.zip'):
        if file_path.name != checksum_archive_path.name:
            file_path.unlink()
    return storage.upload(str(wheel_path), wheel_path.name)


def change_whl_version(whl_name, new_version):
    pattern = r'^(?P<distribution>.+?)-(?P<version>[\d\.\w]+(\+[\w\.]+)?)(?P<rest>-.+\.whl)$'
    return re.sub(pattern, rf'\g<distribution>-{new_version}\g<rest>', whl_name)
