import jupyter_events

def test_cli_version(script_runner):
    ret = script_runner.run('jupyter-events', '--version')
    assert ret.success
    assert ret.stdout.strip() == f"jupyter-events, version {jupyter_events.__version__}"
