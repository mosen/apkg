from typing import List, Tuple
from xml.etree import ElementTree as etree
from enum import Enum


class PackageAuthorization(Enum):
    Nothing = 'none'
    Root = 'root'


class PackagePostInstallAction(Enum):
    Logout = 'logout'
    Restart = 'restart'
    Shutdown = 'shutdown'


class PackageBundle(etree.Element):

    def __init__(self, tag, attrib=None, **kwargs):
        super(PackageBundle, self).__init__('bundle', attrib=attrib, **kwargs)

    @classmethod
    def create(cls, id=None, path=None, identifier=None, version=None, short_version=None):
        bundle = cls()
        bundle.set('CFBundleIdentifier', identifier)
        bundle.set('CFBundleVersion', version)
        bundle.set('CFBundleShortVersionString', short_version)
        bundle.set('id', id)
        bundle.set('path', path)

        return bundle


class PackageInfo(etree.Element):

    def __init__(self, tag, attrib=None, **kwargs):
        super(PackageInfo, self).__init__('pkg-info', attrib=attrib, **kwargs)

    @classmethod
    def create(cls):
        p = cls('pkg-info', attrib={
            'format-version': 2,
            'generator-version': 'apkg-0.1',
        })

        _ = etree.SubElement(p, 'payload', {
            'installKBytes': 0, 'numberOfFiles': 0})
        
        return p

    @property
    def overwrite_permissions(self) -> str:
        return self.get('overwrite-permissions')

    @overwrite_permissions.setter
    def overwrite_permissions(self, value: bool):
        self.set('overwrite-permissions', 'true' if value else 'false')

    @property
    def relocatable(self) -> bool:
        return self.get('relocatable') == 'true'

    @relocatable.setter
    def relocatable(self, value: bool):
        self.set('relocatable', 'true' if value else 'false')

    @property
    def identifier(self) -> str:
        return self.get('identifier')

    @identifier.setter
    def identifier(self, value: str):
        self.set('identifier', value)

    @property
    def postinstall_action(self) -> PackagePostInstallAction:
        return PackagePostInstallAction(self.get('postinstall-action'))

    @postinstall_action.setter
    def postinstall_action(self, value: PackagePostInstallAction):
        self.set('postinstall-action', value.value)

    @property
    def version(self) -> str:
        return self.get('version')

    @version.setter
    def version(self, value: str):
        self.set('version', value)

    @property
    def auth(self) -> PackageAuthorization:
        return PackageAuthorization(self.get('auth'))

    @auth.setter
    def auth(self, value: PackageAuthorization):
        self.set('auth', value.value)

    @property
    def install_location(self) -> str:
        return self.get('install-location')

    @install_location.setter
    def install_location(self, value: str):
        self.set('install-location', value)

    #  Scripts
    def preinstalls(self) -> List[Tuple[str, str]]:
        return self.findall('scripts/preinstall')
    
    def postinstalls(self) -> List[Tuple[str, str]]:
        return self.findall('scripts/postinstall')

