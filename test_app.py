from subprocess import call
from tempfile import NamedTemporaryFile

from hypothesis import settings, note
from hypothesis.stateful import RuleBasedStateMachine, rule
from hypothesis.strategies import sampled_from


def versions():
    """ generates only minor versions available on Docker Hub """
    # TODO: treat as sem-ver version to allow accurate ordering (exercise left to the reader)
    return sampled_from(['3.5', '3.6', '3.7', '3.8'])


class TestPythonVersions(RuleBasedStateMachine):
    @rule(version=versions())
    def try_build_image(self, version):
        with NamedTemporaryFile() as tmp:
            print(f"building in Python version {version} ({tmp.name})")
            contents = f"""FROM python:{version}-alpine
COPY demoapp.py .
RUN python demoapp.py
"""
            tmp.write(contents.encode())
            tmp.flush()
            note(f'Program does not run on Python {version}')
            exit_code = call(f'docker build -f {tmp.name} .'.split(' '))
        assert exit_code == 0


TestPythonVersions.TestCase.settings = settings(deadline=None)

test_python_versions = TestPythonVersions.TestCase
