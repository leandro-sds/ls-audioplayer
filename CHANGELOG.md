# Histórico de versões

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
