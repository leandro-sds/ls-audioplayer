# LS AudioPlayer — Manual do usuário

**Versão 1.0.0**

Um player de áudio feito para ser usado inteiro pelo teclado, com foco
em acessibilidade. Toca suas músicas e rádios da internet, com
equalizador e efeitos.

---

## Como usar, em resumo

O LS AudioPlayer não precisa de mouse. A janela é limpa de propósito:
o que está tocando aparece no **título da janela** (que o leitor de
tela anuncia no Alt+Tab) e na barra de status, embaixo.

Você pode fazer tudo de dois jeitos: pelas **teclas de atalho** (mais
rápido) ou pelos **menus** (pressione Alt para abrir).

---

## Teclas de atalho

### Controlar a reprodução

| Tecla | O que faz |
|---|---|
| **Espaço** | Toca ou pausa |
| **B** | Próxima faixa (ou próxima rádio favorita) |
| **Z** | Faixa anterior (ou rádio favorita anterior) |
| **Ctrl+S** | Para a reprodução |
| **Seta para cima** | Aumenta o volume |
| **Seta para baixo** | Diminui o volume |
| **Seta para a direita** | Avança na música |
| **Seta para a esquerda** | Retrocede na música |
| **Home** | Volta ao início da música |
| **X** | Vai para a primeira faixa da lista. Se estiver ouvindo rádio, **reconecta** a rádio |

### Abrir músicas e rádios

| Tecla | O que faz |
|---|---|
| **Ctrl+O** | Abrir um ou mais arquivos |
| **Ctrl+D** | Abrir uma pasta inteira (incluindo subpastas) |
| **Ctrl+P** | Ver suas pastas favoritas de músicas |
| **Ctrl+Shift+P** | Cadastrar uma pasta favorita |
| **Ctrl+U** | Abrir uma rádio pela URL |
| **Ctrl+Shift+L** | Abrir uma lista pronta (arquivos .m3u ou .pls) |

### Pastas favoritas

Cadastre as pastas que você mais ouve: **Ctrl+Shift+P** adiciona uma
pasta à lista. Depois, **Ctrl+P** abre a lista — **Enter** toca a
pasta selecionada e **Delete** remove da lista.

O programa guarda o **caminho** das pastas, não a lista de músicas — ou
seja, se você colocar músicas novas nelas depois, elas aparecem
automaticamente da próxima vez, sem precisar refazer nada.

### Modos de reprodução

| Tecla | O que faz |
|---|---|
| **R** | Liga/desliga repetir a lista |
| **S** | Liga/desliga o modo aleatório |

Esses dois modos **ficam salvos**: se você desligar o programa com o
aleatório ligado, ele continua ligado da próxima vez.

O modo aleatório embaralha a lista inteira e toca **todas as músicas
antes de repetir qualquer uma** — e embaralha de novo, numa ordem
diferente, quando termina a volta.

### Rádios favoritas

| Tecla | O que faz |
|---|---|
| **Ctrl+Shift+F** | Adiciona a rádio que está tocando aos favoritos |
| **Ctrl+F** | Abre a lista de rádios favoritas |

Na lista de favoritas, você pode:
- **Enter** — toca a rádio selecionada
- **Delete** — remove da lista
- **Ctrl+Seta para cima / para baixo** — muda a rádio de posição
- Botão **Renomear** — dá um nome mais fácil de achar

**Trocando de rádio como num radinho:** depois de tocar uma favorita,
as teclas **B** e **Z** passam a trocar entre as suas rádios
favoritas, em vez de navegar pela lista de músicas. Volta ao normal
quando você abrir uma música ou pasta.

**Backup:** o menu Favoritos tem **Exportar** e **Importar**, para
guardar suas rádios num arquivo ou levá-las para outro computador.

### Lista de reprodução

| Tecla | O que faz |
|---|---|
| **Ctrl+L** | Abre a lista do que está tocando |
| **Ctrl+End** | Vai para a última faixa |
| **Ctrl+Delete** | Remove a faixa atual da lista |

Na lista, **Enter** toca o item selecionado e **Delete** remove.

> Rádios e músicas não se misturam: ao abrir uma pasta enquanto ouve
> uma rádio, a rádio sai da lista automaticamente (e vice-versa).

### Equalizador e efeitos

| Tecla | O que faz |
|---|---|
| **Ctrl+E** | Abre o equalizador e os efeitos |

Ajuste **graves**, **médios** e **agudos** de -15 a +15 (0 é o som
original), usando as setas do teclado ou digitando o número.

Também há efeitos que você pode ligar e desligar: **eco**,
**reverberação**, **compressor** (equilibra o volume entre partes
altas e baixas), **coro** e **flanger**.

Tudo vale tanto para músicas quanto para rádios, e fica salvo.

**Plugins VST:** a mesma tela permite carregar um plugin VST 2.x
(efeitos profissionais de terceiros, como processadores de
"loudness"/transmissão). Coloque seus plugins (arquivos `.dll`) na
pasta **plugins**, ao lado do programa - o botão "Abrir pasta de
plugins" leva direto lá. Cada plugin tem sua própria licença; o LS
AudioPlayer sabe hospedá-los, mas não vem com nenhum incluído.

### Outros

| Tecla | O que faz |
|---|---|
| **F1** | Mostra a lista de atalhos de teclado |
| **Alt** | Abre os menus |
| **Alt+F4** | Fecha o programa |

---

## Integração com o Windows

No menu **Ajuda**, você encontra:

- **Adicionar ao menu de contexto do Windows** — permite clicar com o
  botão direito em um arquivo de áudio (ou numa pasta inteira) e
  escolher "Reproduzir com LS AudioPlayer".
- **Registrar como player padrão** — faz o LS AudioPlayer aparecer em
  *Configurações do Windows → Aplicativos → Aplicativos padrão*, para
  você poder defini-lo como o player dos seus arquivos de áudio.
- **Abrir pasta de dados** — abre onde ficam suas rádios favoritas e
  configurações.

Ambos os registros têm a opção de remover, no mesmo menu.

---

## Preferências

No menu **Arquivo → Preferências**, você pode ajustar:

- **Passo de volume** — de quanto em quanto o volume muda a cada
  toque nas setas (padrão: 1%).
- **Passo de avanço/retrocesso** — quantos segundos as setas
  laterais pulam (padrão: 5 segundos).
- **Atraso antes de tocar streams** — normalmente 0 (imediato). Se
  alguma rádio específica engasgar ao iniciar, aumentar isso pode
  ajudar.
- **Permitir mais de uma instância** — por padrão, só uma janela do
  programa abre por vez.
- **Registrar argumentos em log** — só para diagnóstico, caso algum
  outro programa abra o LS AudioPlayer de um jeito estranho.

---

## Formatos suportados

**Áudio:** MP3, WAV, OGG, FLAC, M4A, AAC, WMA
**Listas:** M3U, M3U8, PLS
**Rádios:** streams por HTTP e HTTPS (Icecast, Shoutcast e HLS)

---

## Onde ficam seus dados

Suas rádios favoritas e configurações ficam em:

```
%APPDATA%\LS AudioPlayer\
├── radios_LSAudioPlayer.json   (suas rádios favoritas)
└── config.json                 (suas preferências)
```

Você chega lá rápido pelo menu **Ajuda → Abrir pasta de dados**.

Esses arquivos **não são apagados** quando você atualiza o programa.

---

## Perguntas comuns

**A rádio demora um pouquinho para começar. É normal?**
Sim. O programa carrega um pedaço do áudio antes de começar a tocar,
para não cortar depois. É uma troca proposital: um instante a mais no
início, em troca de uma reprodução estável.

**Uma música da minha pasta não tocou. O que houve?**
O programa avisa o motivo na barra de status e pula para a próxima
automaticamente, sem travar o resto da pasta. Costuma ser arquivo
corrompido ou incompleto.

**Posso usar em qualquer computador?**
O LS AudioPlayer funciona no Windows 10 e 11, em versões de 64 bits.

---

## Créditos

Desenvolvido por Leandro.

Motor de áudio: **BASS**, de un4seen developments
(www.un4seen.com) — gratuita para uso não-comercial.

Este programa é distribuído gratuitamente.
