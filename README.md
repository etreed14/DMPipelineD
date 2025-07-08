# 🎯 Meeting Summary Pipeline

**Drop a transcript into `importTranscript/` → get a full investor-style HTML summary.**

### Quickstart:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python -m pipeline.run_pipeline --file Calls/2025/July/08/Din7-8Transcript.txt --title SportsBetting
```

