from autonomous_core.report_pipeline import ReportPipeline


def test_report_pipeline():
    assert ReportPipeline().build({})["status"] == "completed"
