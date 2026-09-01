# Histórico de versões

## 1.0.8

### Correção importante

- Velocidade e tom mudando juntos, mesmo escolhendo "só velocidade"
  ou "só tom": causado pela `bass_fx.dll` ficando de fora do
  empacotamento em alguns builds. Corrigido no script de build (aviso
  específico por DLL que falta) e adicionado aviso na própria
  abertura do programa quando isso acontece

### Novidades

- Preferências: opção "Abrir a última playlist ao iniciar" (ligada
  por padrão)
- Ctrl+J (pular para um tempo) vem com o campo já preenchido com o
  tempo atual da faixa
- Tecla Home de volta (volta ao início da faixa), convivendo com o X
- Janela abre maximizada por padrão

### Ajustes

- Removida a tecla barra (/) de resetar velocidade/tom - não
  respondia em algumas instalações com Windows 11 (continua no menu
  Reprodução)
- Texto confuso sobre o log de diagnóstico, nas Preferências, foi
  simplificado

## 1.0.7

### Velocidade e tom

- Três modos escolhidos nas Preferências: Tom, Velocidade ou Os dois
  juntos (estilo fita/vinil)
- Corrigido: trocar de modo podia deixar resíduo do modo anterior
  misturado (ex.: mudar de "tom" pra "velocidade" sem zerar o tom)

### Normalizador de volume

- Recalibrado depois de relato de estouro/clipping - ataque bem mais
  rápido, pra pegar picos antes que estourem
- 5 intensidades: Muito leve, Leve, Médio, Forte e Muito forte
- Nunca mais aplica em rádio (só em arquivos/músicas locais) - cada
  rádio já vem processada do lado de quem transmite

### Outros

- Removidos os presets prontos do equalizador (Pop/Rock/etc.) - não
  soaram bem com só 3 bandas
- Opção pra permitir volume acima de 100% (desligada por padrão, com
  aviso de risco de distorção)
- Título da janela mostra a posição da faixa na lista (ex.: "12 -
  Nome da Música")
- Equalizador e efeitos embutidos também passaram a valer só pra
  músicas locais, nunca pra rádio
- Manual reescrito, sincronizado com os atalhos reais do programa

## 1.0.6

Sem registro detalhado do que mudou nesta versão especificamente.

## 1.0.5

### Ajustes

- Fades (transições suaves) aumentados mais um pouco, tanto na troca
  de faixa quanto no avançar/retroceder dentro da música

## 1.0.4

### Verificação de atualizações

- O programa confere sozinho, discretamente, se existe uma versão
  nova no GitHub ao abrir - avisa com link de download, nunca baixa
  nem instala nada sozinho
- Opção de não perguntar de novo sobre uma versão específica

## 1.0.3

### Novidades

- Tecla J: pula direto pra um arquivo específico da lista de
  reprodução (substituiu o Alt+E)
- O programa lembra a última playlist/rádio tocada - abre pronta pra
  continuar com X ou Espaço

### Correções

- Abrir uma pasta nova enquanto outra ainda tocava estava somando as
  músicas das duas na mesma lista, em vez de substituir

## 1.0.2

### Novidades

- Numpad 3 avança 10 faixas de uma vez, Numpad 1 volta 10
- Modo portátil: guarda favoritos e configurações na própria pasta do
  programa (Ajuda → Modo portátil), pra levar num pendrive

## 1.0.1

### Atalhos no esquema do Winamp clássico

- X toca, C pausa, V para (Shift+V com fade, Ctrl+V ao fim da faixa),
  B/Z navegam, R/S repetir e aleatório
- L abre arquivo, Shift+L abre pasta, Ctrl+L abre URL

### Velocidade de reprodução

- Ajuste de 0,50x a 2,00x preservando o tom original (via bass_fx),
  com aviso claro quando essa DLL não está disponível
- Transições suaves (fade) ao trocar de faixa e ao avançar/retroceder

### Correções

- Capa de álbum em formato incomum não gera mais uma janela de aviso
  do sistema
- Extremos da lista (início/fim) agora respeitam o "repetir"
  desligado, inclusive no modo aleatório

## 1.0.0

Primeira versão pública.

### Reprodução

- Toca MP3, WAV, OGG, FLAC, M4A, AAC e WMA
- Rádios pela internet (Icecast, Shoutcast e HLS), sem cortes
- Listas de reprodução `.m3u`, `.m3u8` e `.pls` — abre e salva
- Modo aleatório que percorre todas as faixas antes de repetir,
  incluindo a primeira
- Repetir e aleatório ficam salvos entre sessões
- Volume salvo ao fechar
- Avanço automático para a próxima faixa quando uma falha

### Rádios favoritas

- Cadastro com nome próprio, reordenável
- B e Z trocam entre as favoritas, como num radinho
- Exportar e importar em `.json`
- Nome da música ao vivo (metadados ICY)

### Pastas favoritas

- Cadastro de várias pastas
- Guarda o caminho, não a lista: músicas novas aparecem sozinhas

### Áudio

- Equalizador de três bandas (graves, médios, agudos)
- Efeitos: eco, reverberação, compressor, coro e flanger
- Suporte a plugins VST 2.x, com vários simultâneos
- Todos os ajustes ficam salvos

### Acessibilidade

- Uso completo por teclado
- Testado com NVDA
- Lista de atalhos navegável em F1
- Interface enxuta, sem avisos desnecessários
- Capa do álbum extraída dos arquivos

### Integração com o Windows

- Instalador com opções de menu de contexto e player padrão
- Instância única (configurável)
- Ferramenta para limpar entradas antigas do registro

### Notas técnicas

- Rádios tocam via BASS através de um proxy HTTP local, contornando
  problemas de negociação HTTPS do Windows Media Foundation com
  servidores Icecast
- Arquivos locais também tocam pela BASS, para ter equalizador e
  efeitos; se a `bass.dll` faltar, volta ao motor do Windows
- Leitura de `.m3u`/`.pls` aceita UTF-8 e Latin-1, preservando acentos
  em arquivos salvos por ferramentas antigas
- Caminhos longos e com acentos tratados corretamente
