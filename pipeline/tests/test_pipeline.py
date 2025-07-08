"""Basic end-to-end pipeline test."""

from pathlib import Path

from pipeline.run_pipeline import process_file


def test_process_file(tmp_path: Path, monkeypatch):
    input_file = tmp_path / "sample.txt"
    input_file.write_text("hello world")

    class DummyClient:
        def chat(self, messages):
            return "summary\ndetails"

    monkeypatch.setattr("pipeline.run_pipeline.LLMClient", lambda: DummyClient())
    html = process_file(input_file, title="Test")
    assert "<h1>summary</h1>" in html
