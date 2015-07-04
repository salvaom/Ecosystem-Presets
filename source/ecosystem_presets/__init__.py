from main import PresetExtension


def register(ecosystem):
    run_extension = PresetExtension()
    ecosystem.register_extension(run_extension)
