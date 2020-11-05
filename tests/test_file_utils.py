import  pytest
import importlib
import codecs
from pathlib import Path
from file_utils import split_by


def test_split_by(tmp_path, capsys):
    with capsys.disabled():
        dzen = codecs.encode(importlib.import_module("this").s, "rot13")
        p = Path(tmp_path).joinpath("dzen.txt")
        p.write_text(data=dzen, encoding='utf-8')
    ret = split_by(p.absolute(), 1)
    # print(p.absolute())
    captured = capsys.readouterr()
    assert captured.out == 'OK\n'
    assert ret == 0
    assert len(list(p.parent.glob("dzen*"))) == 21


