import unittest
from pathlib import Path
from pipeline.run_pipeline import process_file


class PipelineTest(unittest.TestCase):
    def test_process_file(self):
        sample = Path('importTranscript/sample.txt')
        sample.write_text('test transcript')
        html_path = process_file(sample, 'Test')
        self.assertTrue(html_path.exists())
        html_path.unlink()


if __name__ == '__main__':
    unittest.main()
