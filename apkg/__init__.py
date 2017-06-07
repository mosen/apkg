from bixar.archive import XarFile


def is_package(path: str) -> bool:
    if not XarFile.is_xarfile(path):
        return False

    xar = XarFile(path=path)
    return 'PackageInfo' in xar

