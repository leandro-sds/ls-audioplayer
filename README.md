# LS AudioPlayer

Um player de áudio acessível para Windows, no estilo Winamp clássico.
Feito para ser usado inteiro pelo teclado, com foco em quem usa leitor
de tela.

**Versão atual: 1.0.0** — [Baixar o instalador](../../releases/latest)

---

## O que ele faz

- **Toca suas músicas** — MP3, WAV, OGG, FLAC, M4A, AAC, WMA
- **Toca rádios da internet** — Icecast, Shoutcast e HLS, sem cortes
- **Rádios favoritas** — cadastre as suas e troque entre elas com B e Z,
  como num radinho
- **Pastas favoritas** — guarda o caminho, não a lista: músicas novas
  aparecem sozinhas
- **Equalizador e efeitos** — graves, médios, agudos, eco,
  reverberação, compressor, coro e flanger
- **Plugins VST** — carregue processadores de áudio externos
- **Listas de reprodução** — abre e salva `.m3u`, `.m3u8` e `.pls`
- **Capa do álbum** — extraída automaticamente do arquivo
- **Nome da música ao vivo** — nas rádios que enviam essa informação

## Acessibilidade

Este é o ponto central do projeto, não um detalhe:

- Tudo funciona pelo teclado — o mouse é opcional
- Testado com **NVDA**
- Sem elementos visuais desnecessários competindo por atenção
- O que está tocando aparece no título da janela (que o leitor de tela
  anuncia no Alt+Tab)
- Listas navegáveis em vez de caixas de mensagem
- Avisos falados só quando informam algo útil, sem falatório
- Pressione **F1** a qualquer momento para ver todos os atalhos

## Atalhos principais

| Tecla | Ação |
|---|---|
| **F1** | Lista completa de atalhos |
| **Espaço** | Tocar / Pausar |
| **B** / **Z** | Próxima / anterior |
| **Setas** | Volume (cima/baixo), avançar/retroceder (lados) |
| **Ctrl+O** | Abrir arquivos |
| **Ctrl+D** | Abrir pasta |
| **Ctrl+P** | Pastas favoritas |
| **Ctrl+U** | Abrir rádio por URL |
| **Ctrl+F** | Rádios favoritas |
| **Ctrl+E** | Equalizador e efeitos |

O [manual completo](MANUAL.md) tem a lista inteira.

---

## Instalação

Baixe o instalador em **[Releases](../../releases/latest)** e execute.

Requisitos: Windows 10 ou 11, 64 bits.

### Sobre alertas de antivírus

Alguns antivírus podem acusar falso positivo. Isso é comum em programas
feitos com Python/PyInstaller — a ferramenta de empacotamento é a mesma
usada por alguns malwares, então os antivírus desconfiam de tudo que ela
gera. Além disso, este programa faz duas coisas que disparam heurísticas:
baixa dados da internet (é como rádio funciona) e integra com leitores de
tela (que por natureza leem o conteúdo de outras janelas).

O código-fonte está inteiro aqui, aberto, para quem quiser verificar.

---

## Rodando a partir do código-fonte

O jeito recomendado de usar é pelo instalador em
[Releases](../../releases/latest). Mas se você quiser rodar direto do
código, para inspecionar ou modificar:

```bash
pip install winrt-runtime winrt-Windows.Foundation ^
    winrt-Windows.Media.Playback winrt-Windows.Media.Core ^
    winrt-Windows.Storage wxPython mutagen accessible_output2

python ls_audioplayer.py
```

Requer Python 3 de 64 bits (as DLLs incluídas são x64).

---

## Estrutura do projeto

```
ls_audioplayer.py          O programa
limpar_registros.py        Limpa entradas antigas do registro do Windows
registrar_menu_contexto.py Integração com o Windows (uso portátil)
ls_audioplayer.ico         Ícone
default_cover.png          Capa padrão
MANUAL.md                  Manual do usuário
bass/                      DLLs do motor de áudio
```

---

## Como funciona por dentro

Vale registrar duas decisões técnicas que custaram trabalho:

**Rádios não passam pelo Windows Media Foundation.** O motor nativo do
Windows tem dificuldade com a negociação HTTPS de vários servidores
Icecast, o que causava cortes constantes no início da reprodução. A
solução: o programa conecta na rádio ele mesmo (em Python) e serve os
bytes para a BASS através de uma conexão HTTP local — a BASS nunca fala
HTTPS com o servidor remoto. Isso eliminou os cortes.

**Arquivos locais tocam pela BASS, não pelo Windows.** Assim ganham
equalizador e efeitos, que o motor do Windows não oferece. Se a
`bass.dll` não estiver presente, o programa volta ao motor do Windows
automaticamente — toca normalmente, só sem equalizador.

---

## Créditos e licenças

**Código do LS AudioPlayer**: [MIT](LICENSE) — use, modifique e
distribua à vontade.

**Motor de áudio**: [BASS](https://www.un4seen.com), da un4seen
developments. Gratuita para uso não-comercial. As DLLs estão incluídas
neste repositório para facilitar; se você for usar em algo comercial,
confira o licenciamento com eles.

**Suporte a VST**: BASS_VST, por Bjoern Petersen para Silverjuke.net
(LGPL). VST PlugIn Technology by Steinberg Media Technologies GmbH.

**Plugins VST não acompanham o programa** — cada um tem sua própria
licença. Coloque os seus na pasta `plugins`.

---

Desenvolvido por Leandro Souza.
