from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"anchor mismatch in {path}: count={count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# 1) Runtime: impedir substituição silenciosa de template já ativo.
path = "ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py"
old = '''    if nome in pio.templates and not substituir:
        raise ThemeError(
            "PLOTLY_TEMPLATE_EXISTS",
            "Já existe um template com esse nome na sessão.",
            field="$.template_name",
            action="Escolha outro nome ou use substituir=True conscientemente.",
        )
    pio.templates[nome] = go.layout.Template(layout=config)
    if ativar:
        pio.templates.default = nome
'''
new = '''    default_atual = pio.templates.default
    templates_ativos = (
        {parte.strip() for parte in default_atual.split("+") if parte.strip()}
        if isinstance(default_atual, str)
        else set()
    )
    if nome in pio.templates and not substituir:
        raise ThemeError(
            "PLOTLY_TEMPLATE_EXISTS",
            "Já existe um template com esse nome na sessão.",
            field="$.template_name",
            action="Escolha outro nome ou use substituir=True conscientemente.",
        )
    if nome in pio.templates and substituir and not ativar and nome in templates_ativos:
        raise ThemeError(
            "PLOTLY_TEMPLATE_ACTIVE",
            "O template solicitado já participa do padrão ativo da sessão.",
            field="$.template_name",
            action="Para substituí-lo, use ativar=True explicitamente ou escolha outro nome.",
        )
    pio.templates[nome] = go.layout.Template(layout=config)
    if ativar:
        pio.templates.default = nome
'''
replace_once(path, old, new)

old = '''    ``nome`` deve usar o namespace ``hub-*``. O nome legado ``caixa`` e templates
    nativos ficam fora desta API. Registrar não ativa por padrão; ``ativar=True``
    é a ação explícita que muda ``pio.templates.default``.
'''
new = '''    ``nome`` deve usar o namespace ``hub-*``. O nome legado ``caixa`` e templates
    nativos ficam fora desta API. Registrar não ativa por padrão; ``ativar=True``
    é a ação explícita que muda ``pio.templates.default``. Substituir um nome que
    já participa do default ativo também exige ``ativar=True`` para não produzir
    mudança global implícita pela troca do objeto registrado.
'''
replace_once(path, old, new)

# 2) Testes: default simples, composto e substituição explicitamente ativada.
path = "tools/tests/test_temas_v03.py"
anchor = '''    def test_opcoes_precisam_booleanas(self):
'''
insert = '''    def test_substituicao_template_ativo_simples_exige_ativacao(self):
        name = "hub-v03-ativo-simples"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            pio.templates.default = name
            with self.assertRaises(ThemeError) as ctx:
                registrar_template_plotly_resolvido(
                    proposta(**{"chart.width_px": 1111}), nome=name, substituir=True
                )
            self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_ACTIVE")
            self.assertEqual(pio.templates[name].layout.width, 321)
            self.assertEqual(pio.templates.default, name)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_substituicao_template_ativo_composto_exige_ativacao(self):
        name = "hub-v03-ativo-composto"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            pio.templates.default = f"plotly+{name}"
            with self.assertRaises(ThemeError) as ctx:
                registrar_template_plotly_resolvido(
                    proposta(**{"chart.width_px": 1111}), nome=name, substituir=True
                )
            self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_ACTIVE")
            self.assertEqual(pio.templates[name].layout.width, 321)
            self.assertIn(name, pio.templates.default.split("+"))
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_substituicao_template_ativo_com_ativacao_explicita(self):
        name = "hub-v03-ativo-explicito"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            pio.templates.default = name
            registrar_template_plotly_resolvido(
                proposta(**{"chart.width_px": 1111}),
                nome=name,
                substituir=True,
                ativar=True,
            )
            self.assertEqual(pio.templates[name].layout.width, 1111)
            self.assertEqual(pio.templates.default, name)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

'''
replace_once(path, anchor, insert + anchor)

# 3) README do objeto: regra operacional visível.
path = "ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md"
old = '''Escolha conscientemente entre aplicação explícita e registro global. Para propostas V03, prefira `aplicar_tema_resolvido`; `registrar_template_plotly_resolvido` exige namespace `hub-*`, recusa colisão por padrão e só ativa o template com `ativar=True`. Para recuperar o padrão da sessão depois de uma experiência de registro, guarde o valor anterior de `pio.templates.default` e restaure-o; não suponha que uma nova célula comece uma sessão vazia.'''
new = '''Escolha conscientemente entre aplicação explícita e registro global. Para propostas V03, prefira `aplicar_tema_resolvido`; `registrar_template_plotly_resolvido` exige namespace `hub-*`, recusa colisão por padrão e só ativa o template com `ativar=True`. `substituir=True` permite trocar um nome já registrado, mas não permite substituir silenciosamente um nome que já participa do default da sessão: nesse caso, a chamada falha e exige também `ativar=True`, pois trocar o objeto ativo já seria uma mudança global. Para recuperar o padrão da sessão depois de uma experiência de registro, guarde o valor anterior de `pio.templates.default` e restaure-o; não suponha que uma nova célula comece uma sessão vazia.'''
replace_once(path, old, new)

old = '''A paleta categórica não substitui escalas explicitamente definidas em heatmaps nem cores já fixadas nos traces. O registro global afeta outras figuras que usem o padrão da mesma sessão, e não outras sessões independentes. A V03 aplica somente `mode=light`: `dark` e `high_contrast` são válidos no contrato, mas falham fechados no adaptador Plotly até existirem tokens de superfície suficientes para não inventar backgrounds implícitos.'''
new = '''A paleta categórica não substitui escalas explicitamente definidas em heatmaps nem cores já fixadas nos traces. O registro global afeta outras figuras que usem o padrão da mesma sessão, e não outras sessões independentes. Um default Plotly pode ser composto, por exemplo `plotly+hub-alguma-coisa`; a V03 considera cada nome desse composto como ativo e recusa sua substituição com `ativar=False`. A V03 aplica somente `mode=light`: `dark` e `high_contrast` são válidos no contrato, mas falham fechados no adaptador Plotly até existirem tokens de superfície suficientes para não inventar backgrounds implícitos.'''
replace_once(path, old, new)

# 4) Manual central: mesma semântica sem exigir leitura do código.
path = "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
old = '''Mantém a rota legada de configuração/aplicação/registro e acrescenta, na V03, uma rota opt-in que consome `ResolvedTheme` de contexto notebook. `aplicar_tema_resolvido` afeta somente a figura passada; `registrar_template_plotly_resolvido` usa namespace `hub-*` e não muda o default da sessão sem `ativar=True`. Como a rota V03 revalida o tema antes do consumo, ela requer também as dependências declaradas em `hub_snippets/requirements-temas.txt` (`jsonschema` e `referencing`); nenhuma função instala pacotes. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. Dados, eixos e cores explícitas de traces permanecem fora da responsabilidade do adaptador.'''
new = '''Mantém a rota legada de configuração/aplicação/registro e acrescenta, na V03, uma rota opt-in que consome `ResolvedTheme` de contexto notebook. `aplicar_tema_resolvido` afeta somente a figura passada; `registrar_template_plotly_resolvido` usa namespace `hub-*` e não muda o default da sessão sem `ativar=True`. Se o nome a substituir já estiver ativo, sozinho ou dentro de um default composto, `substituir=True` sem `ativar=True` é recusado para impedir mudança global implícita. Como a rota V03 revalida o tema antes do consumo, ela requer também as dependências declaradas em `hub_snippets/requirements-temas.txt` (`jsonschema` e `referencing`); nenhuma função instala pacotes. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. Dados, eixos e cores explícitas de traces permanecem fora da responsabilidade do adaptador.'''
replace_once(path, old, new)

# 5) Documentação da sprint: critério e adversarial explícitos.
path = "docs/sprints/sistema_temas/V03/README.md"
old = '''- `registrar_template_plotly_resolvido(theme, *, nome, ativar=False, substituir=False)` — registra no namespace `hub-*`; só muda o default da sessão com `ativar=True`.'''
new = '''- `registrar_template_plotly_resolvido(theme, *, nome, ativar=False, substituir=False)` — registra no namespace `hub-*`; só muda o default da sessão com `ativar=True` e recusa substituir um nome já ativo quando a ativação não é explícita.'''
replace_once(path, old, new)

path = "docs/sprints/sistema_temas/V03/TESTES.md"
old = '''A suíte cobre compatibilidade das três APIs legadas, equivalência da fixture legada, mapeamento dos tokens configuráveis, preservação de dados/eixos/cores explícitas, rodapé configurado, ausência de efeito global na aplicação por figura, contexto incorreto, modos ainda não suportados, tipo incorreto, fingerprint adulterado, namespace de template, colisão, substituição e ativação explícitas.'''
new = '''A suíte cobre compatibilidade das três APIs legadas, equivalência da fixture legada, mapeamento dos tokens configuráveis, preservação de dados/eixos/cores explícitas, rodapé configurado, ausência de efeito global na aplicação por figura, contexto incorreto, modos ainda não suportados, tipo incorreto, fingerprint adulterado, namespace de template, colisão, substituição e ativação explícitas. Inclui regressões para impedir substituição silenciosa de template já ativo tanto em default simples quanto composto, e confirma que a substituição permanece permitida quando `ativar=True` é solicitado conscientemente.'''
replace_once(path, old, new)

old = '''A guarda precisa rejeitar: dicionário cru em vez de `ResolvedTheme`; contexto `readme`; modo `dark`/`high_contrast` antes da implementação de superfícies; fingerprint inconsistente; nome fora de `hub-*`; colisão sem `substituir=True`; opções não booleanas.'''
new = '''A guarda precisa rejeitar: dicionário cru em vez de `ResolvedTheme`; contexto `readme`; modo `dark`/`high_contrast` antes da implementação de superfícies; fingerprint inconsistente; nome fora de `hub-*`; colisão sem `substituir=True`; substituição de nome que participa do default ativo sem `ativar=True`; opções não booleanas.'''
replace_once(path, old, new)

# 6) Changelog: preservar o quinto achado P2 e a correção.
path = "CHANGELOG.md"
old = '''- (Codex) README do núcleo V02 deixa de afirmar que Plotly ainda não está integrado e passa a registrar a integração opt-in V03 sem sugerir migração automática ou aprovação.'''
new = '''- (Codex) README do núcleo V02 deixa de afirmar que Plotly ainda não está integrado e passa a registrar a integração opt-in V03 sem sugerir migração automática ou aprovação.
- (Codex) Code review P2 final: `registrar_template_plotly_resolvido` recusa substituir um template que já participa do default ativo quando `ativar=False`, inclusive em defaults compostos; regressões cobrem recusa e ativação explícita.'''
replace_once(path, old, new)

print("V03_ACTIVE_TEMPLATE_P2_PATCH_OK")
