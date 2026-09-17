def test_mvp_runner_import():
    from app.runtime.mvp_runner import MVPRunner
    runner = MVPRunner()
    result = runner.run("system test")
    assert result["status"] == "ready"
