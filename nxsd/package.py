import nxsd
import shutil

from nxsd import util
from pathlib import Path


class NXSDPackage(object):

    def __init__(self, name, build_directory, output_filename):
        self.name = name
        self.build_directory = build_directory
        self.output_filename = output_filename

        self.components = []

    def build_components(self):
        self._cleanup_build_directory()
        
        all_builds_successful = True

        for component_module in self.components:
            component = component_module.get_component()
            if component.has_all_dependencies():
                nxsd.logger.info('Building {name} {version}...'.format(
                name=component.name, version=component.version_string))
                component.install(self.build_directory)
            else:
                all_builds_successful = False
                nxsd.logger.info('Unable to build {name} {version}!'.format(
                name=component.name, version=component.version_string))

        if all_builds_successful:
            output_path = Path(self.output_filename)
            shutil.make_archive(output_path.stem, 'zip',
                                root_dir=self.build_directory)

        return all_builds_successful

    def clean(self):
        self._cleanup_build_directory()

        for component_module in self.components:
            component = component_module.get_component()
            nxsd.logger.info('Cleaning {name} {version}...'.format(
                name=component.name, version=component.version_string))
            component.clean()

        util.delete_if_exists(Path(self.output_filename))

    def _cleanup_build_directory(self):
        build_dir = Path(self.build_directory)
        if build_dir.exists():
            shutil.rmtree(build_dir)
