import json
import os
from os import path
import sys

from errors import ConfigurationError, TransformationRuntimeError

class Migration(object):
    @staticmethod
    def load_config(config_file):
        with open(config_file) as json_file:
            return json.loads(json_file.read())

    @staticmethod
    def import_class(class_import_str):
        _module, _class = class_import_str.rsplit('.', 1)
        try:
            return getattr(
                __import__(
                    _module,
                    globals=globals(),
                    locals=locals(),
                    fromlist=[_class],
                    level=0
                ),
                _class
            )
        except ImportError, e:
            print >> sys.stderr, '\t\t{}, skipping'.format(e.message)
            return None
        except AttributeError, e:
            print >> sys.stderr, '\t\t{}, skipping'.format(e.message)
            return None

    @staticmethod
    def normalize_args(args):
        return {key: str(value) if type(value)==unicode else value for key, value in args.items()}

    @staticmethod
    def run(config):

        root_dir = config.get('root', '')
        if not path.exists(root_dir) or not path.isdir(root_dir):
            raise ConfigurationError('Not a valid root directory', 'Please make sure "root" points to a valid path on your system')

        print """------------------------------------
Root dir: {}
------------------------------------""".format(root_dir)

        for pipeline, pipeline_config in config.get('pipelines', {}).items():
            print pipeline
            for date in pipeline_config.get('dates', []):
                for file_config in pipeline_config.get('files', []):
                    filename = file_config.get('filename', '')
                    source_file = path.join(root_dir, pipeline, date, filename)

                    # Does file exist?
                    if not path.exists(source_file) or not path.isfile(source_file):
                        print >> sys.stderr, '\t{}: not found, skipping'.format(filename)
                        continue

                    print '\t{}:'.format(filename)

                    # Instanciating transformations
                    transformations = []
                    for transformation_config in file_config.get('transformations', []):
                        if not transformation_config.has_key('name'):
                            print >> sys.stderr, '\t\tSkipping: Missing transformation name'
                            continue

                        transformation_name = transformation_config.get('name')
                        transformation_class = Migration.import_class('transformations.{}.Transformation'.format(transformation_name))
                        if transformation_class is None:
                            print >> sys.stderr, '\t\t{}, skipping'.format(transformation_name)
                            continue

                        if transformation_config.has_key('config'):
                            transformation = transformation_class(transformation_config.get('config'))
                        else:
                            transformation = transformation_class()

                        transformations.append((transformation_name, transformation))

                        print '\t\t{}: {}'.format(transformation_name, transformation.get_banner().replace('\n', '\n\t\t\t'))

                    reader_config = file_config.get('reader', {})
                    reader_name = reader_config.get('type', 'csv.DictReader')
                    reader_class = Migration.import_class(reader_name)

                    if reader_class is None:
                        print >> sys.stderr, '\t\t{}, skipping'.format(reader_name)
                        continue

                    writer_config = file_config.get('writer', {})
                    writer_name = writer_config.get('type', 'csv.DictWriter')
                    writer_class = Migration.import_class(writer_name)

                    if writer_class is None:
                        print >> sys.stderr, '\t\t{}, skipping'.format(writer_name)
                        continue

                    # Back up input file
                    source_file_items = path.splitext(source_file)
                    tmp_file = '{}{}'.format(source_file_items[0], '.migration')

                    try:
                        os.rename(source_file, tmp_file)
                    except:
                        print >> sys.stderr, '\t\t\tFailed to create backup'
                        continue

                    error = False
                    with open(tmp_file) as file_to_migrate:
                        args = Migration.normalize_args(reader_config.get('args', {}))

                        reader = reader_class(file_to_migrate, **args)

                        with open(source_file, 'w') as new_file:
                            args = Migration.normalize_args(writer_config.get('args', {}))

                            writer = writer_class(new_file, **args)

                            try:
                                Migration.apply_transformations(reader, writer, transformations)
                            except TransformationRuntimeError, e:
                                print >> sys.stderr, '\t\t\tTransformation ({}) error: {}'.format(e.transformation_name, e.message)
                                error = True

                    if error:
                        try:
                            os.rename(tmp_file, source_file)
                        except:
                            print >> sys.stderr, '\t\t\tFailed to delete backup'
                    else:
                        if not config.get('keep_backup', False):
                            try:
                                os.remove(tmp_file)
                            except:
                                print >> sys.stderr, '\t\t\tFailed to delete backup'

    @staticmethod
    def apply_transformations(reader, writer, transformations):
        for transformation_name, transformation in transformations:
            try:
                transformation.before_run(reader, writer)
            except Exception, e:
                raise TransformationRuntimeError(transformation_name, '"before_run" has failed: {}'.format(e.message))

        writer.writeheader()

        for row in reader:
            for transformation_name, transformation in transformations:
                try:
                    transformation.apply(row)
                except Exception, e:
                    raise TransformationRuntimeError(transformation_name, 'Failed to transform "{}": {}'.format(row, e.message))

            try:
                writer.writerow(row)
            except Exception, e:
                raise TransformationRuntimeError(transformation_name, 'Failed to write row "{}": {}'.format(e.message, row))

        for transformation_name, transformation in transformations:
            try:
                transformation.after_run(reader, writer)
            except TransformationRuntimeError, e:
                raise TransformationRuntimeError(transformation_name, '"after_run" has failed: {}'.format(e.message))
