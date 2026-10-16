"""Valida os scripts do repositório contra as assinaturas do stub (farms/lib/__builtins__.py).

Verifica, sem executar o jogo e sem copiar texto dele:
  * chamadas a funções do stub com número de argumentos compatível com a assinatura;
  * membros de Items/Entities/Grounds/Unlocks/Hats/Leaderboards que realmente existem;
  * nomes chamados que não são stub, nem definidos no script, nem builtins permitidos.

Uso (da raiz do repo):  python tools/validar_stub.py [arquivos...]
Sem argumentos, varre farms/ (menos lib/) e jornada/codigo/.
"""

import ast
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUB = os.path.join(RAIZ, "farms", "lib", "__builtins__.py")
ENUMS = {"Items", "Entities", "Grounds", "Unlocks", "Hats", "Leaderboards"}
# métodos de lista/dict/etc. e tipos que o jogo aceita e o stub não declara como função
PERMITIDOS = {"list", "dict", "set", "tuple", "int", "float", "bool", "True", "False", "None"}


def carregar_stub(caminho=STUB):
    arv = ast.parse(open(caminho, encoding="utf-8").read())
    funcs, enums, nomes = {}, {}, set()
    for no in arv.body:
        if isinstance(no, ast.FunctionDef):
            a = no.args
            pos = len(a.posonlyargs) + len(a.args)
            funcs[no.name] = (pos - len(a.defaults), None if a.vararg else pos)
            nomes.add(no.name)
        elif isinstance(no, ast.ClassDef) and no.name in ENUMS:
            enums[no.name] = {
                n.target.id for n in no.body if isinstance(n, ast.AnnAssign)
            }
        elif isinstance(no, ast.Assign):
            nomes.update(t.id for t in no.targets if isinstance(t, ast.Name))
    return funcs, enums, nomes


def definidos(arv):
    d = set()
    for no in ast.walk(arv):
        if isinstance(no, (ast.FunctionDef, ast.ClassDef)):
            d.add(no.name)
        elif isinstance(no, ast.Name) and isinstance(no.ctx, ast.Store):
            d.add(no.id)
        elif isinstance(no, ast.arg):
            d.add(no.arg)
        elif isinstance(no, ast.ExceptHandler) and no.name:
            d.add(no.name)
    return d


def validar_fonte(fonte, nome, stub):
    funcs, enums, nomes = stub
    arv = ast.parse(fonte, nome)
    locais = definidos(arv)
    erros = []
    for no in ast.walk(arv):
        if isinstance(no, ast.Attribute) and isinstance(no.value, ast.Name) \
                and no.value.id in enums and no.attr not in enums[no.value.id]:
            erros.append((no.lineno, f"{no.value.id}.{no.attr} não existe no stub"))
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
            n = no.func.id
            if n in funcs and n not in locais:
                minimo, maximo = funcs[n]
                dado = len(no.args) + len(no.keywords)
                if dado < minimo or (maximo is not None and dado > maximo):
                    esp = f"{minimo}" if minimo == maximo else f"{minimo}..{maximo or '*'}"
                    erros.append((no.lineno, f"{n}() recebe {dado} argumento(s); stub aceita {esp}"))
            elif n not in funcs and n not in locais and n not in nomes and n not in PERMITIDOS:
                erros.append((no.lineno, f"{n}() não é do stub nem foi definido no script"))
    return sorted(erros)


def arquivos_padrao():
    for base in ("farms", os.path.join("jornada", "codigo")):
        for d, _, fs in os.walk(os.path.join(RAIZ, base)):
            if os.path.join("farms", "lib") in d:
                continue
            for f in sorted(fs):
                if f.endswith(".py"):
                    yield os.path.join(d, f)


def main(argv):
    stub = carregar_stub()
    total = 0
    for caminho in argv or arquivos_padrao():
        rel = os.path.relpath(caminho, RAIZ)
        try:
            erros = validar_fonte(open(caminho, encoding="utf-8").read(), rel, stub)
        except SyntaxError as e:
            erros = [(e.lineno or 0, f"sintaxe: {e.msg}")]
        for lin, msg in erros:
            print(f"{rel}:{lin}: {msg}")
        total += len(erros)
    print(f"{total} problema(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
