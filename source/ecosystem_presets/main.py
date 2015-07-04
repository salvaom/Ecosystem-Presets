#!/bin/python
import os
import json
import sys
import argparse
from ecosystem.ext import EcosystemPlugin


class ApplicationManager(object):
    '''ApplicationManager Class. Basically, it discovers applications and
    various executables. Also launches a software.'''
    def __init__(self, ecosystem):
        self.ecosystem = ecosystem
        self.launcher_path = os.path.split(os.path.dirname(__file__))[0]
        self.apps_path = os.getenv('ECO_PRESET_PATH', '')
        self.presets = {}
        self.discover()

    def get_eco_args(self, preset, extra):
        '''Builds depending on the host OS the proper ecosystem command to be
        executed.

        :param preset: Name of the preset (json) to be loaded.
        :param args: Extra arguments to be passed to the software.
        :type preset: str
        :type args: list

        :return: Command to be executed by python
        :rtype: list
        '''
        dependencies, launcher = map(preset.data.get, ['requires', 'launcher'])
        args = ['run', '--tools']
        args += dependencies
        args += ['--run', launcher]
        args += extra
        return args

    def discover(self):
        '''Looks in the ECORUN_APPS_FOLDER environment variable or (by default)
        in the apps folder in the root directory and populates
        "self.presets" with the presets found.
        '''

        for app_path in self.apps_path.split(os.pathsep):
            for root, dirs, files in os.walk(app_path):
                relative_root = root[len(app_path)+1:]
                jsonfiles = [x for x in files if x.endswith('.json')]
                for jsonfile in jsonfiles:
                    preset = Preset(os.path.join(root, jsonfile))
                    if preset.is_valid():
                        _relative_root = relative_root.split(os.sep)
                        jsonfile = os.path.splitext(jsonfile)[0]
                        preset_name = '/'.join(_relative_root + [jsonfile])
                        preset.name = preset_name
                        self.presets[preset_name] = preset

    def launch(self, preset, extra=[], blocking=False):
        '''Launches an ecosystem instance in the system with a built command
        based on a preset and (optional) extra arguments.

        :param preset: Relative path to JSON file.
        :param args: Extra arguments to be passed to the software.
        :type preset: str
        :type args: list
        '''
        if not preset:
            raise ValueError(
                'Preset must be specified either with --preset or --from_env'
            )
        if preset not in self.presets:
            raise ValueError('Preset "%s" not found' % preset)
        preset = self.presets.get(preset)

        args = self.get_eco_args(preset, extra)
        os.environ['ECO_PRESET'] = str(preset.name)
        self.ecosystem.execute_args(args)


class Preset(object):
    '''From a json file, builds a valid preset.

    :param path: Path to the preset json file.
    :type path: str
    '''
    def __init__(self, path):
        self.path = path
        self.data = {}
        self.setup(path)

    def __repr__(self):
        return '<ecorun.Preset "%s">' % self.name

    def setup(self, path):
        '''Reads the JSON file and populates self.data if valid.
        '''
        with file(path, 'r') as f:
            try:
                data = json.load(f)
            except ValueError:
                msg = 'Json file "%s" is not valid.'
                print msg % path
                return
        if self.preset_is_valid(data):
            self.data = data

    def preset_is_valid(self, preset):
        '''Determines if a preset has the minimum keys to ve valid.

        :param preset: The content of the json file as a dict.
        :type preset: dict

        :return: Wether the preset is valid or not.
        :rtype: bool
        '''
        requires = ['requires', 'launcher']
        return all([x in preset for x in requires])

    def is_valid(self):
        '''Returns if the application is valid by looking at the number of
        valid presets within.

        :return: Wether the application is valid or not.
        :rtype: bool
        '''
        return bool(self.data)


class PresetExtension(EcosystemPlugin):
    name = 'preset'

    def initialize(self, ecosystem):
        self.ecosystem = ecosystem
        self.parser = argparse.ArgumentParser('eco-%s' % self.name)
        exclusive = self.parser.add_mutually_exclusive_group()
        exclusive.add_argument('-l', '--list', action='store_true')
        exclusive.add_argument('-p', '--preset')

    def execute(self, args):
        appmanager = ApplicationManager(self.ecosystem)
        args, extra = self.parser.parse_known_args(args)

        if args.list:
            for key in appmanager.presets.keys():
                sys.stdout.write(key+'\n')
            return

        preset = args.preset or os.getenv('ECO_PRESET')
        if not preset:
            raise RuntimeError('Preset not specified.')
        appmanager.launch(
            preset,
            extra
        )
