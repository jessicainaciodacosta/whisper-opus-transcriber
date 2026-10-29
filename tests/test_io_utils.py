"""Basic tests for I/O utilities."""

from pathlib import Path
import tempfile

from modules.io_utils import ensure_dir, write_text, consolidate_texts

def test_ensure_and_write():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        p = tmp / "sub" / "file.txt"
        ensure_dir(p.parent)
        write_text(p, "hello")
        assert p.exists()
        assert p.read_text(encoding="utf-8") == "hello"


def test_consolidate():
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out.txt"
        texts = [("a.txt", "content A"), ("b.txt", "content B")]
        consolidate_texts(texts, out)
        content = out.read_text(encoding="utf-8")
        assert "--- a.txt ---" in content
        assert "content A" in content
        assert "--- b.txt ---" in content