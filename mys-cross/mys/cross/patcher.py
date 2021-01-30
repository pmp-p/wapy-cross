import os
"""
TARGET = os.environ.get('TARGET') and sysconfig.get_config_var('MULTIARCH')

def create_file(path, data):
    with open(path, 'w') as fout:
        fout.write(data)


def read_template_file(path):
    template = os.path.join(MYS_DIR, 'cli/templates', path)
    if TARGET:
        from mys.cross.patcher import patch
        template = patch(MYS_DIR, 'cli/templates', path, TARGET)

    with open(template) as fin:
        return fin.read()


"""


def patch(MYS_ROOT, template_dir, source, TARGET):
    template = os.path.join(MYS_ROOT, template_dir, source)
    override = f"{template}.{TARGET}"
    if os.path.exists(override):
        print(f" > Cross-compilation : FORCING {override=} for {TARGET=}")
        return override
    print(f" > Cross-compilation : READING {fname=} for {TARGET=}")


