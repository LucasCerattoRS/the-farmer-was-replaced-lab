"""tools/sync_save.py: dry-run não copia; --apply copia NEW e CHANGED; skip e UNMAPPED."""
import json

import pytest

import sync_save


@pytest.fixture
def ambiente(tmp_path, monkeypatch):
    save = tmp_path / "save"
    repo = tmp_path / "repo"
    ferramentas = tmp_path / "tools"
    for p in (save, repo, ferramentas):
        p.mkdir()
    (ferramentas / "sync_map.json").write_text(json.dumps({
        "files": {"novo.py": "farms/novo.py", "mudou.py": "farms/mudou.py", "igual.py": "farms/igual.py"},
        "skip": ["dup.py"],
    }), encoding="utf-8")
    (repo / "farms").mkdir()
    (repo / "farms/mudou.py").write_text("velho", encoding="utf-8")
    (repo / "farms/igual.py").write_text("mesmo", encoding="utf-8")
    for nome, txt in {"novo.py": "n", "mudou.py": "novo", "igual.py": "mesmo",
                      "dup.py": "d", "solto.py": "s"}.items():
        (save / nome).write_text(txt, encoding="utf-8")
    monkeypatch.setattr(sync_save, "REPO", repo)
    monkeypatch.setattr(sync_save, "__file__", str(ferramentas / "sync_save.py"))
    return save, repo


def rodar(monkeypatch, *args):
    monkeypatch.setattr("sys.argv", ["sync_save.py", *args])
    return sync_save.main()


def test_dry_run_relata_e_nao_copia(ambiente, monkeypatch, capsys):
    save, repo = ambiente
    assert rodar(monkeypatch, "--save-dir", str(save)) == 0
    saida = capsys.readouterr().out
    assert "NEW       novo.py -> farms/novo.py" in saida
    assert "CHANGED   mudou.py -> farms/mudou.py" in saida
    assert "UNMAPPED  solto.py" in saida
    assert "dup.py" not in saida
    assert "OK: 1  NEW: 1  CHANGED: 1  UNMAPPED: 1" in saida
    assert not (repo / "farms/novo.py").exists()
    assert (repo / "farms/mudou.py").read_text(encoding="utf-8") == "velho"


def test_apply_copia_novo_e_alterado(ambiente, monkeypatch, capsys):
    save, repo = ambiente
    assert rodar(monkeypatch, "--save-dir", str(save), "--apply") == 0
    assert (repo / "farms/novo.py").read_text(encoding="utf-8") == "n"
    assert (repo / "farms/mudou.py").read_text(encoding="utf-8") == "novo"
    assert not (repo / "farms/dup.py").exists()
    capsys.readouterr()
    rodar(monkeypatch, "--save-dir", str(save))
    assert "OK: 3  NEW: 0  CHANGED: 0" in capsys.readouterr().out


def test_save_dir_inexistente_sai_1(tmp_path, monkeypatch, capsys):
    assert rodar(monkeypatch, "--save-dir", str(tmp_path / "nao-existe")) == 1
    assert "Save dir not found" in capsys.readouterr().err
