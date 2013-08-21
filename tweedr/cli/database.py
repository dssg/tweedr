import os
import sys
import argparse
import mako.template


def reflect(**kw):
    from tweedr.models import metadata
    schema_filepath = os.path.join(os.path.dirname(metadata.__file__), 'schema.py')
    schema_template_filepath = os.path.join(os.path.dirname(metadata.__file__), 'schema.template')

    template = mako.template.Template(filename=schema_template_filepath)
    metadata.metadata.reflect()
    schema = template.render(metadata=metadata.metadata)

    if kw.get('in_place'):
        with open(schema_filepath, 'w') as out:
            out.write(schema)
    else:
        sys.stdout.write(schema)

    print >> sys.stderr, '\nDone printing schema'


def create(**kw):
    from tweedr.models.schema import metadata
    metadata.create_all()


commands = dict(reflect=reflect, create=create)


def main():
    parser = argparse.ArgumentParser(description='Tweedr database tools')
    parser.add_argument('command', choices=commands, help='Command to run')
    parser.add_argument('--in-place', action='store_true', help='Whether or not to update the schema.py file in place')

    opts = parser.parse_args()
    commands[opts.command](**vars(opts))

if __name__ == '__main__':
    main()
