# LS AudioPlayer — Manual do usuário

**Versão 1.0.8**

Um player de áudio feito para ser usado inteiro pelo teclado, com foco
em acessibilidade. Toca suas músicas e rádios da internet, com
equalizador, normalizador, controle de velocidade/tom e suporte a
plugins VST.

---

## Como usar, em resumo

O LS AudioPlayer não precisa de mouse. A janela é limpa de propósito:
o que está tocando aparece no **título da janela** (que o leitor de
tela anuncia no Alt+Tab) e na barra de status, embaixo.

Você pode fazer tudo de dois jeitos: pelas **teclas de atalho** (mais
rápido) ou pelos **menus** (pressione Alt para abrir). A qualquer
momento, **F1** mostra a lista completa de atalhos numa tela
navegável (Esc fecha).

---

## Teclas de atalho

### Controlar a reprodução

| Tecla | O que faz |
|---|---|
| **X** | Toca / volta ao início do arquivo. Em rádio, reconecta |
| **C** ou **Espaço** | Pausa ou continua |
| **V** | Para |
| **Shift+V** | Para com o som sumindo aos poucos |
| **Ctrl+V** | Para quando a faixa atual terminar |
| **B** | Próxima faixa (ou próxima rádio favorita) |
| **Z** | Faixa anterior (ou rádio favorita anterior) |
| **Numpad 3** | Avança 10 faixas de uma vez |
| **Numpad 1** | Volta 10 faixas de uma vez |
| **Ctrl+Z** | Vai para a primeira faixa da lista |
| **Ctrl+B** | Vai para a última faixa da lista |
| **Seta para cima** | Aumenta o volume |
| **Seta para baixo** | Diminui o volume |
| **Seta para a direita** | Avança na música |
| **Seta para a esquerda** | Retrocede na música |
| **Home** | Volta ao início da faixa atual |
| **End** | Vai para o fim da faixa atual |
| **Ctrl+J** | Pula para um tempo específico - o campo já vem preenchido com o tempo atual da faixa |

### Velocidade e tom

| Tecla | O que faz |
|---|---|
| **Ponto** | Aumenta velocidade ou tom |
| **Vírgula** | Diminui velocidade ou tom |

Não tem tecla direta pra "voltar ao normal" (a barra `/` foi retirada
— não respondia em algumas máquinas com Windows 11). Pra isso, use o
menu **Reprodução → Voltar ao normal**.

O que "ponto"/"vírgula" ajustam — **Tom**, **Velocidade** ou **Os
dois juntos** (estilo fita/vinil) — se escolhe em **Arquivo →
Preferências**. "Só velocidade" e "só tom" precisam do arquivo
`bass_fx.dll` presente; sem ele, o programa avisa e usa "os dois
juntos" como reserva.

### Abrir músicas e rádios

| Tecla | O que faz |
|---|---|
| **L** | Abrir um ou mais arquivos |
| **Shift+L** | Abrir uma pasta inteira (incluindo subpastas) |
| **Ctrl+L** | Abrir uma rádio pela URL |
| **Ctrl+Shift+L** | Abrir uma lista pronta (arquivos .m3u ou .pls) |
| **J** | Ver a lista de reprodução / pular para um arquivo |
| **Ctrl+P** | Ver suas pastas favoritas de músicas |
| **Ctrl+Shift+P** | Cadastrar uma pasta favorita |

> Abrir uma pasta nova **substitui** a lista atual, nunca soma com o
> que já estava tocando.

### Pastas favoritas

Cadastre as pastas que você mais ouve: **Ctrl+Shift+P** adiciona uma
pasta à lista. Depois, **Ctrl+P** abre a lista — **Enter** toca a
pasta selecionada e **Delete** remove da lista.

O programa guarda o **caminho** das pastas, não a lista de músicas —
ou seja, se você colocar músicas novas nelas depois, elas aparecem
automaticamente da próxima vez, sem precisar refazer nada.

### Modos de reprodução

| Tecla | O que faz |
|---|---|
| **R** | Liga/desliga repetir a lista |
| **S** | Liga/desliga o modo aleatório |

Esses dois modos **ficam salvos**: se você fechar o programa com o
aleatório ligado, ele continua ligado da próxima vez. Com "repetir"
desligado, a lista **para** nos extremos (início/fim) em vez de dar a
volta sozinha — vale também no modo aleatório.

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
| **J** | Abre a lista do que está tocando |
| **Ctrl+B** | Vai para a última faixa |
| **Ctrl+Del** | Remove a faixa atual da lista |

Na lista, **Enter** toca o item selecionado.

### Equalizador, efeitos e normalizador

| Tecla | O que faz |
|---|---|
| **Ctrl+E** | Abre o equalizador, os efeitos e o normalizador |

**Importante:** tudo nessa tela — equalizador, efeitos e
normalizador — vale **só para músicas/arquivos locais**. Rádios
nunca passam por aqui, porque cada uma já vem processada do lado de
quem transmite; empilhar processamento nosso por cima soa estranho em
algumas delas.

Ajuste **graves**, **médios** e **agudos** de -15 a +15 (0 é o som
original), usando as setas do teclado ou digitando o número.

Também há efeitos que você pode ligar e desligar: **eco**,
**reverberação**, **compressor**, **coro** e **flanger**.

**Normalizador de volume:** equilibra faixas altas e baixas (ajuda a
ouvir conversas/trechos baixos sem estourar os altos). Tem 5
intensidades: Muito leve, Leve, Médio, Forte e Muito forte.

Tudo fica salvo automaticamente.

**Plugins VST:** a mesma tela permite carregar um plugin VST 2.x
(efeitos profissionais de terceiros). Coloque seus plugins (arquivos
`.dll`) na pasta **plugins**, ao lado do programa — o botão
correspondente na tela leva direto lá. Também valem só para arquivos
locais. Cada plugin tem sua própria licença; o LS AudioPlayer sabe
hospedá-los, mas não vem com nenhum incluído.

### Outros

| Tecla | O que faz |
|---|---|
| **F1** | Mostra a lista de atalhos de teclado |
| **Alt** | Abre os menus |
| **Alt+F4** | Fecha o programa |
| **Esc** | Fecha o programa (opcional — ative em Preferências) |

---

## Retomando de onde parou

Ao fechar o programa com algo tocando, ele guarda a lista inteira e
qual faixa estava na vez. Na próxima abertura, o nome já aparece no
título — é só apertar **X** ou **Espaço** para continuar direto dali,
sem precisar reabrir a pasta ou a rádio manualmente.

---

## Modo portátil

Em **Ajuda → Modo portátil**, dá para fazer o programa guardar
favoritos e configurações na própria pasta dele, em vez do perfil do
Windows — útil para levar num pendrive. A troca só vale a partir da
próxima vez que abrir o programa.

---

## Verificar atualizações

O programa confere sozinho, discretamente, se existe uma versão mais
nova no GitHub logo depois de abrir — sem interromper nada se não
houver novidade ou se não conseguir verificar. Encontrando algo novo,
pergunta se você quer abrir o navegador para baixar (nunca baixa nem
instala sozinho). Dá para conferir manualmente a qualquer momento em
**Ajuda → Verificar atualizações**.

---

## Preferências

No menu **Arquivo → Preferências**, você pode ajustar:

- **Passo de volume** — de quanto em quanto o volume muda a cada
  toque nas setas.
- **Passo de avanço/retrocesso** — quantos segundos as setas
  laterais pulam.
- **Atraso antes de tocar streams** — normalmente 0 (imediato). Se
  alguma rádio específica engasgar ao iniciar, aumentar isso pode
  ajudar.
- **Permitir mais de uma instância** — por padrão, só uma janela do
  programa abre por vez.
- **Registrar argumentos em log** — só para diagnóstico.
- **Abrir a última playlist ao iniciar** — ligado por padrão; se
  desmarcar, o programa abre limpo, sem carregar a sessão anterior.
- **Esc também fecha o programa** — desligado por padrão.
- **Permitir aumentar o volume acima de 100%** — desligado por
  padrão; acima de 100% o som pode distorcer, dependendo da faixa.
- **O que "ponto"/"vírgula" alteram** — Tom, Velocidade ou Os dois.

---

## Integração com o Windows

O registro de "Reproduzir com LS AudioPlayer" no menu de contexto do
Windows, e o registro como aplicativo padrão, são feitos pelo
**instalador** (duas opções na hora de instalar) — não é preciso (nem
possível) fazer isso de dentro do programa.

---

## Formatos suportados

**Áudio:** MP3, WAV, OGG, FLAC, M4A, AAC, WMA
**Listas:** M3U, M3U8, PLS
**Rádios:** streams por HTTP e HTTPS (Icecast e Shoutcast). Rádios em
HLS (`.m3u8` como fonte ao vivo, ex.: algumas rádios que usam esse
formato de transmissão) tocam pelo motor do Windows em vez da BASS —
funcionam, mas sem equalizador/efeitos/normalizador.

---

## Onde ficam seus dados

Suas rádios favoritas e configurações ficam em:

```
%APPDATA%\LS AudioPlayer\
├── radios_LSAudioPlayer.json   (suas rádios favoritas)
└── config.json                 (suas preferências)
```

(Ou na própria pasta do programa, se o **modo portátil** estiver
ativado.)

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

**A tecla Espaço muda a velocidade ou o tom?**
Não — Espaço (e C) só pausam e continuam a reprodução. Velocidade e
tom se ajustam só com ponto/vírgula, e voltam ao normal pelo menu
Reprodução → Voltar ao normal.

**Posso usar em qualquer computador?**
O LS AudioPlayer funciona no Windows 10 e 11, em versões de 64 bits.

---

## Créditos

Desenvolvido por Leandro Souza.

Motor de áudio: **BASS**, de un4seen developments
(www.un4seen.com) — gratuita para uso não-comercial.

Suporte a velocidade/tom preservados: **BASS_FX**. Suporte a plugins
VST: **BASS_VST**, por Bjoern Petersen para Silverjuke.net (LGPL).

Este programa é distribuído gratuitamente.
