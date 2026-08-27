#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LS AudioPlayer - Um Winamp moderno e acessível
================================================================

IMPORTANTE - motor de áudio:
    Arquivos locais são tocados pelo Windows Media Foundation, já
    embutido no Windows 10/11, através do binding oficial da
    Microsoft para Python: o pacote "winrt" (pywinrt).

    Streams/rádios são tocados pela BASS (www.un4seen.com), uma DLL
    de áudio (não é um programa separado - sem instalador, sem ícone,
    sem processo próprio, só um arquivo .dll ao lado do programa).
    O motor do Windows tinha dificuldade com a negociação HTTPS de
    vários servidores Icecast (cortava no início da reprodução); a
    BASS resolve isso de forma confiável. Se a pasta "bass" com as
    DLLs não for encontrada, o programa cai automaticamente de volta
    para o motor do Windows nas rádios, sem travar.

    BASS é gratuita para uso não-comercial/individual - encaixa no
    LS AudioPlayer, que é distribuído gratuitamente. Se um dia isso
    virar algo comercial, confira www.un4seen.com para licenciamento.

    Único caso de exceção pro motor do Windows (arquivos locais):
    Windows em edição "N"/"KN" (comuns na Europa) vem sem o pacote de
    codecs por remoção legal de fábrica. Nesse caso o próprio Windows
    orienta a instalar o "Media Feature Pack", um recurso opcional
    gratuito da Microsoft - não é um player externo.

Requisitos (instalar antes de rodar):
    pip install winrt-runtime winrt-Windows.Foundation ^
        winrt-Windows.Media.Playback winrt-Windows.Media.Core ^
        winrt-Windows.Storage wxPython mutagen
    (opcional, para fala extra além do NVDA/leitor de tela)
    pip install accessible_output2

    Também precisa da pasta "bass" (com bass.dll e os decodificadores
    bass_aac.dll, bassflac.dll, bassopus.dll, basswma.dll) na mesma
    pasta deste script - já vem pronta, não precisa instalar nada à
    parte pra isso. MP3 é nativo da BASS, não depende de nenhum deles.

Este script roda apenas em Windows.

Interface:
    A janela principal é minimalista de propósito: sem lista de
    reprodução visível, sem barra de volume na tela. Tudo é
    controlado por atalhos de teclado e pelos menus (Alt para
    navegar). O que está tocando aparece no TÍTULO da janela (lido
    pelo Alt+Tab e por comandos de revisão do leitor de tela), sem
    interromper o que você estiver fazendo com anúncios de voz
    automáticos a cada troca de faixa.

Atalhos (funcionam com o foco em qualquer lugar da janela):
    Espaço          -> Play / Pausa
    B               -> Próxima faixa (ou próxima rádio favorita)
    Z               -> Faixa anterior (ou rádio favorita anterior)
    R               -> Liga/desliga repetição da playlist (fica salvo)
    S               -> Liga/desliga modo aleatório (fica salvo)
    X               -> Primeira faixa da lista / reinicia a rádio
    Seta cima       -> Aumenta volume
    Seta baixo      -> Diminui volume
    Seta direita    -> Avança
    Seta esquerda   -> Retrocede
    Home            -> Volta ao início da faixa atual
    End             -> Vai para o fim da faixa atual
    Ctrl+End        -> Vai para a última faixa da lista
    Ctrl+O          -> Abrir arquivo(s)
    Ctrl+D          -> Abrir pasta
    Ctrl+P          -> Ver pastas favoritas (Enter toca)
    Ctrl+Shift+P    -> Cadastrar pasta favorita
    Ctrl+U          -> Abrir stream por URL (rádio/https)
    Ctrl+L          -> Ver/gerenciar lista de reprodução (Enter toca)
    Ctrl+Del        -> Remover a faixa atual da lista
    Ctrl+F          -> Ver rádios favoritas
    Ctrl+Shift+F    -> Adicionar rádio atual aos favoritos
    Ctrl+E          -> Equalizador e efeitos
    Ctrl+S          -> Para a reprodução
    F1              -> Lista de atalhos de teclado
    Alt+F4          -> Sair
    Esc             -> Sair (opcional, desligado por padrão -
                        ative em Preferências)

    Todos esses comandos também estão nos menus (Arquivo,
    Reprodução, Lista, Favoritos, Ajuda).

Modo rádio:
    Ao tocar uma rádio favorita, B e Z passam a trocar de favorita
    (como num radinho), em vez de navegar a lista de reprodução -
    até você tocar outra coisa (arquivo, pasta ou URL avulsa).

Equalizador e efeitos:
    Ctrl+E abre o equalizador (graves, médios e agudos, de -15 a
    +15 dB) e os efeitos opcionais (eco, reverberação, compressor,
    coro, flanger). Funciona tanto em músicas quanto em rádios, e a
    configuração fica salva. Usa efeitos DirectX 8 já embutidos na
    própria bass.dll - não precisa de nada extra.

Plugins VST:
    Ctrl+E > Gerenciar plugins VST permite carregar um plugin VST 2.x
    (ex.: processadores de "loudness"/broadcast), com os parâmetros do
    próprio plugin aparecendo pra ajustar. Vale só para músicas/
    arquivos locais - rádios nunca passam pelos plugins VST (o
    equalizador e os efeitos embutidos continuam valendo pros dois).
    Precisa do arquivo bass_vst.dll na pasta "bass" - se não estiver
    presente, essa opção simplesmente não aparece, sem quebrar nada.
    Usa a BASS_VST (LGPL, gratuita) - crédito no menu Ajuda > Sobre.

Motor de áudio dos arquivos locais:
    Arquivos locais também são tocados pela BASS (pra terem
    equalizador e efeitos). Se a bass.dll não estiver disponível,
    o programa cai automaticamente pro motor do Windows, que toca
    normalmente mas sem equalizador.

Título da janela:
    Segue o padrão do Winamp: "Artista - Música - LS AudioPlayer".

Metadados:
    - Arquivos locais: lidos direto do arquivo (tags ID3/FLAC/OGG)
      usando a biblioteca "mutagen".
    - Streams/rádios: lidos ao vivo via metadados ICY, com
      reconexões curtas e espaçadas (evita competir por banda com
      a conexão de áudio de verdade). O texto é decodificado
      tentando UTF-8 primeiro e caindo para Latin-1 automaticamente
      quando a rádio manda metadado em codificação antiga (comum em
      rádios brasileiras), o que evita perder acentos.

Menu de contexto e player padrão do Windows:
    A partir da versão 1.0.0, esse registro é feito pelo instalador
    (LSAudioPlayer_Setup.exe), com duas caixinhas opcionais durante a
    instalação - não precisa mais fazer isso de dentro do programa.
    Se você rodar o LS AudioPlayer.exe avulso (sem usar o instalador)
    e quiser esse registro, use o script separado
    registrar_menu_contexto.py.

Favoritos (rádios/streams):
    Ctrl+Shift+F adiciona a rádio/stream tocando agora aos favoritos.
    Ctrl+F abre a lista de favoritos (tocar, renomear, reordenar,
    remover). Salvos em %APPDATA%\\LS AudioPlayer\\radios_LSAudioPlayer.json,
    e o menu Favoritos permite exportar/importar essa lista em
    .json, pra backup ou pra levar a outro computador.

Pastas favoritas (músicas):
    Ctrl+Shift+P cadastra uma pasta na lista de favoritas. Ctrl+P
    abre essa lista - Enter toca a pasta selecionada, Delete remove.
    O que fica guardado é o CAMINHO das pastas, não a lista de
    arquivos - então músicas novas colocadas nelas aparecem sozinhas
    na próxima vez que forem abertas.

Quando uma faixa não toca:
    Se o Windows Media Foundation não conseguir abrir ou decodificar
    um arquivo (corrompido, formato não suportado, etc.), o
    LS AudioPlayer agora mostra o motivo na barra de status e pula
    automaticamente para a próxima faixa, em vez de ficar em
    silêncio sem explicação.

Playlists M3U / PLS:
    Arquivo > Abrir lista de reprodução (Ctrl+Shift+L) lê arquivos
    .m3u, .m3u8 e .pls e carrega todas as faixas/streams de dentro
    deles. Lista > Salvar lista como M3U exporta a lista atual.
    Também é possível clicar com o botão direito num arquivo .m3u/.pls
    no Explorer e usar "Reproduzir com LS AudioPlayer" (depois de
    registrado pelo menu Ajuda), que carrega e toca a lista inteira.
"""

import os
import re
import io
import sys
import json
import time
import ctypes
import random
import socket
import asyncio
import threading
import urllib.request
from datetime import timedelta
from pathlib import Path

import wx

if sys.platform != "win32":
    print("Este player usa o Windows Media Foundation e só funciona no Windows.")
    sys.exit(1)

import winreg

try:
    from winrt.windows.media.playback import MediaPlayer, MediaPlaybackState
    from winrt.windows.media.core import MediaSource
    from winrt.windows.foundation import Uri
    from winrt.windows.storage import StorageFile
except ImportError:
    print("ERRO: bibliotecas 'winrt-*' não encontradas.")
    print("Instale com:")
    print("  pip install winrt-runtime winrt-Windows.Foundation "
          "winrt-Windows.Media.Playback winrt-Windows.Media.Core "
          "winrt-Windows.Storage")
    sys.exit(1)

try:
    import mutagen
    _HAS_MUTAGEN = True
except ImportError:
    _HAS_MUTAGEN = False


# --- Recursos visuais (ícone do programa e capa padrão) --------------------
ICON_FILE = "ls_audioplayer.ico"
DEFAULT_COVER_FILE = "default_cover.png"
COVER_SIZE = 200  # pixels, quadrado


def _resource_path(filename):
    """Mesma lógica de _bass_base_dir: ao lado do .py em desenvolvimento,
    ou dentro do pacote do PyInstaller quando rodando como .exe."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


def extract_embedded_cover_bytes(path):
    """Tenta extrair a capa/arte de álbum embutida num arquivo de áudio
    local (ID3 APIC para MP3, tag de imagem nativa para FLAC/OGG/etc).
    Devolve os bytes da imagem, ou None se não encontrar/não conseguir."""
    if not _HAS_MUTAGEN:
        return None
    try:
        audio = mutagen.File(path)
        if audio is None:
            return None
        pictures = getattr(audio, "pictures", None)
        if pictures:
            return pictures[0].data
        tags = getattr(audio, "tags", None)
        if tags is not None:
            for key in list(tags.keys()):
                if key.startswith("APIC"):
                    return bytes(tags[key].data)
    except Exception:
        pass
    return None

# --- Saída de fala opcional (accessible_output2) ---------------------------
try:
    from accessible_output2.outputs.auto import Auto as _AO_Auto
    _speaker = _AO_Auto()

    def speak(text):
        try:
            _speaker.speak(text, interrupt=True)
        except Exception:
            pass
except Exception:
    def speak(text):
        pass


APP_TITLE = "LS AudioPlayer"
APP_VERSION = "1.0.0"
SEEK_STEP = timedelta(seconds=5)      # valor padrão inicial (configurável nas Preferências)
VOLUME_STEP = 0.01                     # valor padrão inicial (configurável nas Preferências)
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"}
PLAYLIST_EXTENSIONS = {".m3u", ".m3u8", ".pls"}
# A leitura de metadado ICY roda numa conexão totalmente independente
# do áudio (que agora é entregue pela BASS via proxy local) - não há
# mais risco de concorrência entre as duas, então o atraso pode ser
# bem curto. Ajustável em Preferências.
ICY_INITIAL_DELAY = 3        # segundos antes da 1a leitura de metadado ICY
ICY_RECONNECT_INTERVAL = 20  # segundos entre leituras curtas de metadado ICY
STREAM_PLAY_DELAY_MS = 0     # espera antes de mandar tocar um stream (0 =
                              # toca imediatamente, igual VLC/Winamp/navegador)

# Códigos oficiais do enum Windows.Media.Playback.MediaPlayerError
# (confirmados na documentação da Microsoft), traduzidos para texto
# compreensível - o campo "error_message" do Windows costuma vir
# vazio, então não dá para confiar só nele.
MEDIA_ERROR_MESSAGES = {
    0: "motivo desconhecido",
    1: "a reprodução foi abortada",
    2: "erro de rede (stream inacessível ou conexão caiu)",
    3: "erro ao decodificar o arquivo - formato ou codec não suportado, "
       "ou o arquivo está corrompido/incompleto",
    4: "esse tipo de arquivo não é suportado pelo Windows",
}

# Pasta de dados do usuário (favoritos e configurações) - fica no
# perfil, não na pasta do programa, pra funcionar mesmo com o .exe
# numa pasta somente-leitura.
FAVORITES_DIR = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")), "LS AudioPlayer"
)
FAVORITES_FILE = os.path.join(FAVORITES_DIR, "radios_LSAudioPlayer.json")
SETTINGS_FILE = os.path.join(FAVORITES_DIR, "config.json")


def load_settings():
    settings = {
        "volume_step": VOLUME_STEP,
        "seek_step_seconds": int(SEEK_STEP.total_seconds()),
        "stream_play_delay_ms": STREAM_PLAY_DELAY_MS,
        "icy_initial_delay_seconds": ICY_INITIAL_DELAY,
        "allow_multiple_instances": False,
        "enable_argv_log": False,
        "repeat_mode": False,
        "shuffle_mode": False,
        "eq_gains": {"eq_bass": 0.0, "eq_vocal": 0.0, "eq_treble": 0.0},
        "active_effects": [],
        "vst_plugins": [],
        "favorite_folders": [],
        "volume_level": 0.8,
        "close_on_escape": False,
    }
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            for key in settings:
                if key in data:
                    settings[key] = data[key]
    except Exception:
        pass
    return settings


def save_settings(settings):
    try:
        os.makedirs(FAVORITES_DIR, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def load_favorites():
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def save_favorites(favorites):
    try:
        os.makedirs(FAVORITES_DIR, exist_ok=True)
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def _decode_icy_text(raw_bytes):
    """Decodifica texto de metadado ICY. Tenta UTF-8 primeiro (padrão
    moderno); se não for válido, cai para Latin-1, que é o que várias
    rádios (principalmente as mais antigas/brasileiras) ainda usam.
    Isso evita perder acentos como 'ç' e derrubar as letras seguintes."""
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1", errors="replace")


def _decode_playlist_file_bytes(raw_bytes):
    """Mesma lógica do _decode_icy_text (UTF-8 com reserva pra
    Latin-1), só que também cuida do BOM UTF-8 no início do arquivo.
    Necessária porque vários geradores de M3U/PLS (Windows Media
    Player, ferramentas antigas) salvam em Latin-1/ANSI em vez de
    UTF-8 - ler assumindo UTF-8 com errors='ignore' descartava
    silenciosamente qualquer acento sem aviso nenhum."""
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        raw_bytes = raw_bytes[3:]
    return _decode_icy_text(raw_bytes)


def _delete_reg_key_recursive(root, path):
    try:
        key = winreg.OpenKey(root, path, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        return
    with key:
        while True:
            try:
                sub = winreg.EnumKey(key, 0)
            except OSError:
                break
            _delete_reg_key_recursive(root, f"{path}\\{sub}")
    winreg.DeleteKey(root, path)


async def _async_get_storage_file(path):
    return await StorageFile.get_file_from_path_async(path)


def get_local_media_source(path):
    """Abre um arquivo local, tentando três formas em sequência, da
    mais confiável pra mais compatível:

    1. StorageFile com o caminho normal - evita problemas de
       codificação com nomes acentuados ('ç', 'ã'), que faziam o
       Windows Media Foundation recusar arquivos válidos.
    2. StorageFile com o prefixo de caminho estendido (\\\\?\\) do
       Windows - contorna o limite clássico de 260 caracteres
       (MAX_PATH), comum em pastas com nomes longos (ex.: downloads
       organizados em pastas tipo "LANÇAMENTOS GOSPEL DA SEMANA
       PASSADA", onde caminho + nome do arquivo passam do limite).
    3. URI file:/// tradicional, como último recurso.

    Se todas falharem, relança o último erro, pra quem chamou poder
    mostrar o motivo real em vez de falhar em silêncio."""
    abs_path = os.path.abspath(path)
    candidates = [abs_path]
    if not abs_path.startswith("\\\\?\\"):
        candidates.append("\\\\?\\" + abs_path)

    last_exception = None
    for candidate in candidates:
        try:
            storage_file = asyncio.run(_async_get_storage_file(candidate))
            return MediaSource.create_from_storage_file(storage_file)
        except Exception as e:
            last_exception = e
            continue

    try:
        uri = Uri(Path(path).as_uri())
        return MediaSource.create_from_uri(uri)
    except Exception as e:
        last_exception = e

    raise RuntimeError(str(last_exception))


def resolve_stream_url(url, timeout=6):
    """Segue redirecionamentos HTTP manualmente (com o urllib do
    Python, que já lida com isso de forma madura) e devolve a URL
    final do stream de áudio. Links curtos de rádio (tipo
    tgaurl.com.br) costumam redirecionar pra um servidor
    Icecast/Shoutcast real, às vezes numa porta não padrão - e o
    Windows Media Foundation pode não lidar bem com esse
    redirecionamento sozinho (reabrindo a conexão repetidamente).
    Resolvendo antes, entregamos a URL final direto pro Windows, que
    nunca precisa lidar com o redirect.

    Se a resolução falhar por qualquer motivo, devolve a URL original
    sem erro - o pior caso é o comportamento de antes, não uma
    quebra nova."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "LSAudioPlayer/1.0", "Icy-MetaData": "0"}
        )
        resp = urllib.request.urlopen(req, timeout=timeout)
        final_url = resp.geturl()
        resp.close()
        return final_url or url
    except Exception:
        return url


# ============================================================================
# Motor de streaming via BASS (un4seen.com) - contorna a negociação
# HTTPS/Icecast do Windows Media Foundation, que causava cortes no
# início da reprodução de várias rádios (MP3 e AAC).
#
# Técnica: nunca deixamos a BASS (nem o Windows) falar HTTPS
# diretamente com o servidor da rádio. Em vez disso, o LS AudioPlayer
# mesmo conecta na rádio (com o urllib do Python, que já lida bem com
# esse tipo de servidor) e serve os bytes crus localmente em HTTP
# simples (127.0.0.1). A BASS só enxerga essa conexão local, sem
# nenhuma negociação HTTPS/TLS pra atrapalhar. É a mesma técnica usada
# por addons de leitor de tela para tocar rádios sem cortes.
#
# BASS é gratuita para uso não-comercial (www.un4seen.com) - o
# LS AudioPlayer é distribuído gratuitamente, então se encaixa nisso.
# ============================================================================
BASS_CONFIG_BUFFER = 0
BASS_CONFIG_NET_TIMEOUT = 11
BASS_CONFIG_NET_BUFFER = 12
BASS_CONFIG_NET_PREBUF = 15
BASS_CONFIG_NET_PLAYLIST = 21
BASS_CONFIG_NET_READTIMEOUT = 37
BASS_ATTRIB_VOL = 2
BASS_UNICODE = 0x80000000   # caminhos de arquivo com acentos
BASS_POS_BYTE = 0
BASS_TAG_META = 5

# ============================================================================
# Plugins VST (efeitos avançados, ex.: TB_Broadcast_v3.dll) via BASS_VST
# ============================================================================
# BASS_VST é um complemento separado da BASS (não vem junto), que faz a
# BASS "hospedar" plugins VST 2.x - permitindo usar qualquer plugin VST
# de efeito no LS AudioPlayer, com os mesmos canais já usados pelo
# equalizador. Se o arquivo bass_vst.dll não estiver presente, esse
# recurso simplesmente não aparece - o resto do programa continua igual.
#
# Licença da BASS_VST: LGPL, gratuita - com duas exigências: não cobrar
# por esse recurso, e dar o crédito "BASS_VST by Bjoern Petersen for
# Silverjuke.net" (esse aviso está no diálogo Sobre do programa).


class BASS_VST_PARAM_INFO(ctypes.Structure):
    """Estrutura oficial da BASS_VST (bass_vst.h), copiada campo a campo -
    o tamanho e o alinhamento foram conferidos batendo exatamente com o
    cabeçalho original antes de usar isso pra valer."""
    _fields_ = [
        ("name", ctypes.c_char * 16),
        ("unit", ctypes.c_char * 16),
        ("display", ctypes.c_char * 16),
        ("defaultValue", ctypes.c_float),
    ]


class BASS_VST_INFO(ctypes.Structure):
    _fields_ = [
        ("channelHandle", ctypes.c_uint32),
        ("uniqueID", ctypes.c_uint32),
        ("effectName", ctypes.c_char * 80),
        ("effectVersion", ctypes.c_uint32),
        ("effectVstVersion", ctypes.c_uint32),
        ("hostVstVersion", ctypes.c_uint32),
        ("productName", ctypes.c_char * 80),
        ("vendorName", ctypes.c_char * 80),
        ("vendorVersion", ctypes.c_uint32),
        ("chansIn", ctypes.c_uint32),
        ("chansOut", ctypes.c_uint32),
        ("initialDelay", ctypes.c_uint32),
        ("hasEditor", ctypes.c_uint32),
        ("editorWidth", ctypes.c_uint32),
        ("editorHeight", ctypes.c_uint32),
        ("aeffect", ctypes.c_void_p),
        ("isInstrument", ctypes.c_uint32),
        ("dspHandle", ctypes.c_uint32),
    ]


def load_bass_vst_dll(bass_dll):
    """Carrega a BASS_VST, se o arquivo existir. Devolve None (sem erro
    fatal) se não conseguir - nesse caso, o recurso de plugin VST some
    da interface, mas nada mais quebra."""
    if bass_dll is None:
        return None
    base = os.path.join(_bass_base_dir(), "bass")
    vst_path = os.path.join(base, "bass_vst.dll")
    if not os.path.exists(vst_path):
        return None

    try:
        dll = ctypes.WinDLL(vst_path)
        dll.BASS_VST_ChannelSetDSP.argtypes = [
            ctypes.c_uint32, ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_int
        ]
        dll.BASS_VST_ChannelSetDSP.restype = ctypes.c_uint32
        dll.BASS_VST_ChannelRemoveDSP.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        dll.BASS_VST_ChannelRemoveDSP.restype = ctypes.c_int
        dll.BASS_VST_GetInfo.argtypes = [ctypes.c_uint32, ctypes.POINTER(BASS_VST_INFO)]
        dll.BASS_VST_GetInfo.restype = ctypes.c_int
        dll.BASS_VST_GetParamCount.argtypes = [ctypes.c_uint32]
        dll.BASS_VST_GetParamCount.restype = ctypes.c_int
        dll.BASS_VST_GetParamInfo.argtypes = [
            ctypes.c_uint32, ctypes.c_int, ctypes.POINTER(BASS_VST_PARAM_INFO)
        ]
        dll.BASS_VST_GetParamInfo.restype = ctypes.c_int
        dll.BASS_VST_GetParam.argtypes = [ctypes.c_uint32, ctypes.c_int]
        dll.BASS_VST_GetParam.restype = ctypes.c_float
        dll.BASS_VST_SetParam.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_float]
        dll.BASS_VST_SetParam.restype = ctypes.c_int
        dll.BASS_VST_SetBypass.argtypes = [ctypes.c_uint32, ctypes.c_int]
        dll.BASS_VST_SetBypass.restype = ctypes.c_int
        dll.BASS_VST_GetBypass.argtypes = [ctypes.c_uint32]
        dll.BASS_VST_GetBypass.restype = ctypes.c_int
        return dll
    except Exception:
        return None


# Efeitos de áudio (DirectX 8, já embutidos na própria bass.dll - não
# precisa de nenhuma DLL extra).
BASS_FX_DX8_CHORUS = 0
BASS_FX_DX8_COMPRESSOR = 1
BASS_FX_DX8_ECHO = 3
BASS_FX_DX8_FLANGER = 4
BASS_FX_DX8_PARAMEQ = 7
BASS_FX_DX8_REVERB = 8

# Efeitos liga/desliga (usam os parâmetros padrão do DirectX, que já
# soam bem). Deixados de fora: distorção e gargle - são efeitos de
# deformação intencional (guitarra/voz robótica), não fazem sentido
# num player de música.
AUDIO_EFFECTS = [
    ("echo", "Eco", BASS_FX_DX8_ECHO),
    ("reverb", "Reverberação (ambiente)", BASS_FX_DX8_REVERB),
    ("compressor", "Compressor (equilibra volume)", BASS_FX_DX8_COMPRESSOR),
    ("chorus", "Coro", BASS_FX_DX8_CHORUS),
    ("flanger", "Flanger", BASS_FX_DX8_FLANGER),
]

# Bandas de equalização: nome interno -> (rótulo, frequência central Hz,
# largura de banda em semitons). O ganho é ajustável pelo usuário.
EQ_BANDS = [
    ("eq_bass",   "Graves",  100.0,  18.0),
    ("eq_vocal",  "Médios",  2500.0, 18.0),
    ("eq_treble", "Agudos",  8000.0, 18.0),
]


class BASS_DX8_PARAMEQ(ctypes.Structure):
    _fields_ = [
        ("fCenter", ctypes.c_float),
        ("fBandwidth", ctypes.c_float),
        ("fGain", ctypes.c_float),
    ]
BASS_STREAM_BLOCK = 0x100000
BASS_ACTIVE_STOPPED = 0
BASS_ACTIVE_PLAYING = 1
BASS_ACTIVE_STALLED = 2
BASS_ACTIVE_PAUSED = 3


def _bass_base_dir():
    """Pasta onde procurar a subpasta 'bass' com as DLLs - ao lado do
    .py em modo desenvolvimento, ou dentro do pacote do PyInstaller
    quando rodando como .exe."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _app_dir():
    """Pasta real onde o programa está instalado (ao lado do .exe de
    verdade, ou do .py em desenvolvimento) - diferente de
    _bass_base_dir(), que aponta pra pasta temporária de extração do
    PyInstaller (recriada do zero a cada execução). Usada pra coisas
    que precisam ser permanentes e visíveis pro usuário, como a pasta
    de plugins VST."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_plugins_dir():
    """Pasta 'plugins', ao lado do programa de verdade, onde o usuário
    guarda os próprios plugins VST (.dll). Cria a pasta se ainda não
    existir."""
    path = os.path.join(_app_dir(), "plugins")
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass
    return path


def load_bass_dll():
    """Carrega e inicializa a BASS. Devolve None (sem erro fatal) se
    não conseguir - nesse caso, as rádios voltam a usar o motor do
    Windows como antes, em vez de travar o programa."""
    base = os.path.join(_bass_base_dir(), "bass")
    bass_path = os.path.join(base, "bass.dll")
    if not os.path.exists(bass_path):
        return None

    try:
        dll = ctypes.WinDLL(bass_path)

        dll.BASS_Init.argtypes = [ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32,
                                   ctypes.c_void_p, ctypes.c_void_p]
        dll.BASS_Init.restype = ctypes.c_int
        dll.BASS_SetConfig.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        dll.BASS_SetConfig.restype = ctypes.c_int
        dll.BASS_StreamCreateURL.argtypes = [ctypes.c_char_p, ctypes.c_uint32,
                                              ctypes.c_uint32, ctypes.c_void_p,
                                              ctypes.c_void_p]
        dll.BASS_StreamCreateURL.restype = ctypes.c_uint32
        dll.BASS_ChannelPlay.argtypes = [ctypes.c_uint32, ctypes.c_int]
        dll.BASS_ChannelPlay.restype = ctypes.c_int
        dll.BASS_ChannelPause.argtypes = [ctypes.c_uint32]
        dll.BASS_ChannelPause.restype = ctypes.c_int
        dll.BASS_ChannelStop.argtypes = [ctypes.c_uint32]
        dll.BASS_ChannelStop.restype = ctypes.c_int
        dll.BASS_ChannelIsActive.argtypes = [ctypes.c_uint32]
        dll.BASS_ChannelIsActive.restype = ctypes.c_uint32
        dll.BASS_ChannelSetAttribute.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_float]
        dll.BASS_ChannelSetAttribute.restype = ctypes.c_int
        dll.BASS_StreamFree.argtypes = [ctypes.c_uint32]
        dll.BASS_StreamFree.restype = ctypes.c_int
        dll.BASS_ErrorGetCode.restype = ctypes.c_int
        dll.BASS_Free.restype = ctypes.c_int
        dll.BASS_PluginLoad.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        dll.BASS_PluginLoad.restype = ctypes.c_uint32
        dll.BASS_ChannelGetTags.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        dll.BASS_ChannelGetTags.restype = ctypes.c_char_p
        dll.BASS_ChannelSetFX.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int]
        dll.BASS_ChannelSetFX.restype = ctypes.c_uint32
        dll.BASS_ChannelRemoveFX.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        dll.BASS_ChannelRemoveFX.restype = ctypes.c_int
        dll.BASS_FXSetParameters.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
        dll.BASS_FXSetParameters.restype = ctypes.c_int
        # Arquivos locais tocados pela BASS (pra ter equalizador/efeitos
        # neles também, não só nas rádios)
        dll.BASS_StreamCreateFile.argtypes = [ctypes.c_int, ctypes.c_void_p,
                                               ctypes.c_uint64, ctypes.c_uint64,
                                               ctypes.c_uint32]
        dll.BASS_StreamCreateFile.restype = ctypes.c_uint32
        dll.BASS_ChannelGetLength.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        dll.BASS_ChannelGetLength.restype = ctypes.c_uint64
        dll.BASS_ChannelGetPosition.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        dll.BASS_ChannelGetPosition.restype = ctypes.c_uint64
        dll.BASS_ChannelSetPosition.argtypes = [ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint32]
        dll.BASS_ChannelSetPosition.restype = ctypes.c_int
        dll.BASS_ChannelBytes2Seconds.argtypes = [ctypes.c_uint32, ctypes.c_uint64]
        dll.BASS_ChannelBytes2Seconds.restype = ctypes.c_double
        dll.BASS_ChannelSeconds2Bytes.argtypes = [ctypes.c_uint32, ctypes.c_double]
        dll.BASS_ChannelSeconds2Bytes.restype = ctypes.c_uint64

        if not dll.BASS_Init(-1, 44100, 0, None, None):
            return None

        # Configuração conservadora, priorizando estabilidade em vez de
        # velocidade de início: um buffer de rede maior (8s) dá margem
        # contra soluços de conexão, e um pré-carregamento de 75% antes
        # de começar a tocar evita ficar reiniciando/engasgando toda
        # hora logo no começo (era 0% = toca imediato, sem margem
        # nenhuma, o que causava cortes curtos e frequentes).
        #
        # Importante: o buffer de rede (NET_BUFFER) só é mantido
        # continuamente durante a reprodução quando o stream é aberto
        # com a flag BASS_STREAM_BLOCK - por isso ela volta a ser usada
        # lá na hora de abrir o stream. Sem ela, esse buffer maior só
        # valia pro pré-carregamento inicial, não pro resto da música -
        # o que explicava os pequenos pulos constantes depois do início.
        #
        # Também aumenta o buffer de reprodução/saída de áudio (padrão
        # 500ms), dando mais margem contra pequenas variações de tempo
        # do nosso próprio proxy em Python.
        #
        # Valores reduzidos em relação à rodada anterior: a causa real
        # dos cliques era o metadado ICY sendo mal interpretado como
        # áudio (já corrigido, repassando icy-metaint pro proxy), não
        # falta de buffer - então dá pra afrouxar um pouco e ganhar
        # velocidade de início, mantendo uma margem de segurança
        # ainda bem maior que o padrão original da BASS.
        dll.BASS_SetConfig(BASS_CONFIG_BUFFER, 2000)
        dll.BASS_SetConfig(BASS_CONFIG_NET_BUFFER, 6000)
        dll.BASS_SetConfig(BASS_CONFIG_NET_PREBUF, 30)
        dll.BASS_SetConfig(BASS_CONFIG_NET_PLAYLIST, 1)
        dll.BASS_SetConfig(BASS_CONFIG_NET_TIMEOUT, 12000)
        dll.BASS_SetConfig(BASS_CONFIG_NET_READTIMEOUT, 12000)

        # Plugins de decodificação extra (AAC, FLAC, Opus, WMA) - cada
        # um é opcional; se um arquivo não existir, a BASS continua
        # funcionando normalmente pros formatos que já tem (MP3 é
        # nativo, não precisa de plugin nenhum).
        for plugin_name in ("bass_aac.dll", "bassflac.dll", "bassopus.dll", "basswma.dll"):
            plugin_path = os.path.join(base, plugin_name)
            if os.path.exists(plugin_path):
                try:
                    dll.BASS_PluginLoad(plugin_path.encode("utf-8"), 0)
                except Exception:
                    pass

        return dll
    except Exception:
        return None


class LocalIcecastProxy:
    """Conecta numa rádio remota (HTTPS/Icecast) usando o urllib do
    Python e repassa os bytes crus recebidos por uma conexão HTTP
    local simples (127.0.0.1). A BASS (ou qualquer motor de áudio)
    então só precisa falar com esse endereço local, sem nunca lidar
    com a negociação HTTPS/TLS do servidor remoto diretamente.

    Repassa também o cabeçalho icy-metaint pro cliente local (a BASS),
    pra ela mesma saber separar os blocos de metadado (nome da música)
    intercalados no meio do áudio - sem isso, esses blocos de texto
    eram encaminhados junto com o áudio sem aviso nenhum, e a BASS
    podia tentar decodificar um pedacinho de texto como se fosse
    áudio, causando cliques."""

    def __init__(self, remote_url):
        self.remote_url = remote_url
        self.port = None
        self.content_type = "audio/mpeg"
        self.icy_name = None
        self.icy_metaint = None
        self._remote_resp = None
        self._server_socket = None
        self._stop_event = threading.Event()

    def start(self, timeout=15):
        """Conecta no servidor remoto (bloqueia até responder ou
        desistir) e abre o servidor local. Deve ser chamado numa
        thread separada da interface."""
        req = urllib.request.Request(
            self.remote_url,
            headers={
                "User-Agent": "LS AudioPlayer/1.0",
                "Icy-MetaData": "1",
                "Accept": "*/*",
            },
        )
        self._remote_resp = urllib.request.urlopen(req, timeout=timeout)
        self.content_type = self._remote_resp.headers.get("content-type", "audio/mpeg")
        self.icy_name = self._remote_resp.headers.get("icy-name")
        self.icy_metaint = self._remote_resp.headers.get("icy-metaint")

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("127.0.0.1", 0))
        self._server_socket.listen(5)
        self.port = self._server_socket.getsockname()[1]

        threading.Thread(target=self._accept_loop, daemon=True).start()
        return f"http://127.0.0.1:{self.port}/stream"

    def _accept_loop(self):
        """Fica pronto pra atender conexões indefinidamente - se o player
        (BASS) reconectar no proxy local por qualquer motivo (soluço,
        lógica interna de retry, etc.), essa reconexão é atendida na
        hora, sem precisar reabrir a conexão de internet com a rádio de
        verdade (essa fica aberta o tempo todo, por trás). Antes, o
        proxy desligava sozinho depois de atender uma vez, e qualquer
        tentativa de reconexão da BASS caía no vazio - isso muito
        provavelmente era a causa dos cortes curtos e repetidos."""
        try:
            self._server_socket.settimeout(1.0)
            while not self._stop_event.is_set():
                try:
                    client, _addr = self._server_socket.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                # Atende cada conexão numa thread própria, pra já voltar
                # a aceitar novas conexões imediatamente, sem esperar
                # essa terminar.
                threading.Thread(
                    target=self._handle_client, args=(client,), daemon=True
                ).start()
        except Exception:
            pass

    def _handle_client(self, client):
        try:
            client.settimeout(5)
            try:
                client.recv(4096)  # descarta a requisição HTTP recebida
            except Exception:
                pass

            headers = f"HTTP/1.0 200 OK\r\nContent-Type: {self.content_type}\r\n"
            if self.icy_metaint:
                # Essencial: avisa a BASS onde os blocos de metadado
                # estão intercalados, pra ela separar corretamente em
                # vez de tentar decodificar texto como áudio.
                headers += f"icy-metaint: {self.icy_metaint}\r\n"
            headers += "Connection: close\r\n\r\n"
            client.sendall(headers.encode("utf-8"))

            client.settimeout(None)
            while not self._stop_event.is_set():
                chunk = self._remote_resp.read(32768)
                if not chunk:
                    break
                client.sendall(chunk)
        except Exception:
            pass
        finally:
            try:
                client.close()
            except Exception:
                pass

    def stop(self):
        self._stop_event.set()
        if self._remote_resp is not None:
            try:
                self._remote_resp.close()
            except Exception:
                pass
        if self._server_socket is not None:
            try:
                self._server_socket.close()
            except Exception:
                pass


def _resolve_playlist_entry(entry_path, base_dir):
    """Resolve uma entrada de playlist M3U/PLS: mantém URLs como estão,
    e resolve caminhos relativos em relação à pasta do arquivo de
    playlist (comportamento padrão desses formatos)."""
    entry_path = entry_path.strip()
    if entry_path.startswith("http://") or entry_path.startswith("https://"):
        return entry_path
    entry_path = entry_path.replace("/", os.sep).replace("\\", os.sep)
    if not os.path.isabs(entry_path):
        entry_path = os.path.normpath(os.path.join(base_dir, entry_path))
    return entry_path


def _parse_m3u(path):
    """Lê M3U/M3U8: uma entrada por linha, ignorando comentários (#)
    exceto #EXTINF, que só traz um título opcional (não usamos aqui,
    os metadados reais vêm do próprio arquivo/stream ao tocar)."""
    entries = []
    base_dir = os.path.dirname(path)
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except Exception:
        return entries

    text = _decode_playlist_file_bytes(raw)
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(_resolve_playlist_entry(line, base_dir))
    return entries


def _parse_pls(path):
    """Lê PLS (formato INI: File1=, File2=, ...)."""
    entries = []
    base_dir = os.path.dirname(path)
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except Exception:
        return entries

    text = _decode_playlist_file_bytes(raw)
    lines = text.splitlines()

    file_map = {}
    for line in lines:
        line = line.strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        match = re.match(r"File(\d+)$", key.strip(), re.IGNORECASE)
        if match and value.strip():
            file_map[int(match.group(1))] = value.strip()

    for idx in sorted(file_map):
        entries.append(_resolve_playlist_entry(file_map[idx], base_dir))
    return entries


def parse_playlist_file(path):
    """Lê um arquivo de playlist M3U/M3U8/PLS e retorna a lista de
    caminhos/URLs, prontos para tocar."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pls":
        return _parse_pls(path)
    return _parse_m3u(path)


def write_m3u(path, entries):
    """Salva a lista de reprodução atual como um arquivo M3U simples."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for entry in entries:
                f.write(entry + "\n")
        return True
    except Exception:
        return False


# ============================================================================
# Leitor de metadados ICY (rádios / streams ao vivo)
# ============================================================================
class IcyMetadataReader(threading.Thread):
    """
    Lê metadados 'tocando agora' do stream via protocolo ICY, com
    conexões CURTAS e espaçadas no tempo (abre, lê um ciclo de
    metadado, fecha, espera). Isso evita manter uma segunda conexão
    de áudio full-time competindo por banda com a conexão real de
    reprodução. Também espera alguns segundos antes da primeira
    leitura, para não brigar por banda logo no início crítico do
    buffer de áudio.

    on_meta_change é chamado como on_meta_change(kind, text), onde
    kind é 'station' (nome da rádio) ou 'title' (música atual).
    """

    def __init__(self, url, on_meta_change, initial_delay=None):
        super().__init__(daemon=True)
        self.url = url
        self.on_meta_change = on_meta_change
        self.initial_delay = ICY_INITIAL_DELAY if initial_delay is None else initial_delay
        self._stop_event = threading.Event()
        self._last_title = None
        self._last_station = None

    def stop(self):
        self._stop_event.set()

    def run(self):
        if self._stop_event.wait(self.initial_delay):
            return
        while not self._stop_event.is_set():
            try:
                self._fetch_once()
            except Exception:
                pass
            self._stop_event.wait(ICY_RECONNECT_INTERVAL)

    def _fetch_once(self):
        req = urllib.request.Request(
            self.url,
            headers={"Icy-MetaData": "1", "User-Agent": "LSAudioPlayer/1.0"},
        )
        resp = urllib.request.urlopen(req, timeout=8)
        try:
            icy_name = resp.headers.get("icy-name")
            if icy_name and icy_name != self._last_station and not self._stop_event.is_set():
                self._last_station = icy_name
                wx.CallAfter(self.on_meta_change, "station", icy_name)

            metaint = resp.headers.get("icy-metaint")
            if not metaint:
                return
            metaint = int(metaint)

            self._read_exact(resp, metaint)
            if self._stop_event.is_set():
                return

            length_byte = self._read_exact(resp, 1)
            if not length_byte:
                return
            meta_length = length_byte[0] * 16
            if meta_length == 0:
                return

            meta_bytes = self._read_exact(resp, meta_length)
            if not meta_bytes:
                return

            text = _decode_icy_text(meta_bytes)
            match = re.search(r"StreamTitle='([^']*)'", text)
            if match:
                title = match.group(1).strip()
                if title and title != self._last_title and not self._stop_event.is_set():
                    self._last_title = title
                    wx.CallAfter(self.on_meta_change, "title", title)
        except (socket.timeout, ConnectionError, OSError):
            return
        finally:
            try:
                resp.close()
            except Exception:
                pass

    @staticmethod
    def _read_exact(resp, n):
        data = b""
        while len(data) < n:
            chunk = resp.read(n - len(data))
            if not chunk:
                break
            data += chunk
        return data


# ============================================================================
# Diálogo de gerenciamento da lista de reprodução (sob demanda)
# ============================================================================
class PlaylistDialog(wx.Dialog):
    def __init__(self, parent, frame):
        super().__init__(parent, title="Lista de reprodução",
                          size=(440, 380),
                          style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.frame = frame
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.listbox = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.listbox.SetName("Itens da lista de reprodução")
        self._refresh()
        if 0 <= frame.current_index < self.listbox.GetCount():
            self.listbox.SetSelection(frame.current_index)
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self._on_play)
        # EVT_CHAR_HOOK no diálogo inteiro, não EVT_KEY_DOWN só na lista -
        # é a mesma técnica usada nos atalhos da janela principal, porque
        # o Enter em wx.ListBox nativo nem sempre chega como tecla normal.
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 8)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_play = wx.Button(panel, label="&Tocar")
        btn_remove = wx.Button(panel, label="&Remover (Del)")
        btn_close = wx.Button(panel, wx.ID_CLOSE, "&Fechar")
        btn_play.Bind(wx.EVT_BUTTON, self._on_play)
        btn_remove.Bind(wx.EVT_BUTTON, self._on_remove)
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        btn_sizer.Add(btn_play, 0, wx.ALL, 4)
        btn_sizer.Add(btn_remove, 0, wx.ALL, 4)
        btn_sizer.Add(btn_close, 0, wx.ALL, 4)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CLOSE)
        self.listbox.SetFocus()

    def _refresh(self):
        self.listbox.Clear()
        for p in self.frame.playlist:
            is_stream = p.startswith("http://") or p.startswith("https://")
            self.listbox.Append(p if is_stream else os.path.basename(p))

    def _on_key(self, event):
        # So intercepta Enter/Delete quando o foco esta na lista, senao
        # atrapalharia botoes (ex.: Enter no botao "Fechar" deve fechar,
        # nao tocar a faixa).
        if wx.Window.FindFocus() is not self.listbox:
            event.Skip()
            return
        code = event.GetKeyCode()
        if code == wx.WXK_DELETE:
            self._on_remove(event)
        elif code in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._on_play(event)
        else:
            event.Skip()

    def _on_play(self, event):
        idx = self.listbox.GetSelection()
        if idx != wx.NOT_FOUND:
            self.frame._play_index(idx)
            self.EndModal(wx.ID_OK)

    def _on_remove(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        was_playing = (idx == self.frame.current_index)
        del self.frame.playlist[idx]
        if was_playing:
            self.frame._stop()
            self.frame.current_index = -1
        elif idx < self.frame.current_index:
            self.frame.current_index -= 1
        self._refresh()
        if self.listbox.GetCount() > 0:
            self.listbox.SetSelection(min(idx, self.listbox.GetCount() - 1))


# ============================================================================
# Diálogo de rádios favoritas
# ============================================================================
class FavoritesDialog(wx.Dialog):
    def __init__(self, parent, frame):
        super().__init__(parent, title="Rádios favoritas",
                          size=(560, 380),
                          style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.frame = frame
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.listbox = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.listbox.SetName("Rádios favoritas")
        self._refresh()
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self._on_play)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 8)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_play = wx.Button(panel, label="&Tocar")
        btn_rename = wx.Button(panel, label="&Renomear")
        btn_up = wx.Button(panel, label="Mover pra &cima (Ctrl+↑)")
        btn_down = wx.Button(panel, label="Mover pra &baixo (Ctrl+↓)")
        btn_remove = wx.Button(panel, label="Remo&ver (Del)")
        btn_close = wx.Button(panel, wx.ID_CLOSE, "&Fechar")
        btn_play.Bind(wx.EVT_BUTTON, self._on_play)
        btn_rename.Bind(wx.EVT_BUTTON, self._on_rename)
        btn_up.Bind(wx.EVT_BUTTON, lambda e: self._move_selected(-1))
        btn_down.Bind(wx.EVT_BUTTON, lambda e: self._move_selected(1))
        btn_remove.Bind(wx.EVT_BUTTON, self._on_remove)
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        for b in (btn_play, btn_rename, btn_up, btn_down, btn_remove, btn_close):
            btn_sizer.Add(b, 0, wx.ALL, 4)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CLOSE)
        self.listbox.SetFocus()

    def _refresh(self):
        self.listbox.Clear()
        for fav in self.frame.favorites:
            self.listbox.Append(fav.get("name") or fav.get("url", "?"))

    def _on_key(self, event):
        # So intercepta Enter/Delete/mover quando o foco esta na lista,
        # senao atrapalharia botoes (ex.: Enter no botao "Fechar" deve
        # fechar, nao tocar a faixa).
        if wx.Window.FindFocus() is not self.listbox:
            event.Skip()
            return
        code = event.GetKeyCode()
        if code == wx.WXK_DELETE:
            self._on_remove(event)
        elif code in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._on_play(event)
        elif code == wx.WXK_UP and event.ControlDown():
            self._move_selected(-1)
        elif code == wx.WXK_DOWN and event.ControlDown():
            self._move_selected(1)
        else:
            event.Skip()

    def _on_play(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        self.frame._play_favorite_by_index(idx)
        self.EndModal(wx.ID_OK)

    def _on_rename(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        fav = self.frame.favorites[idx]
        dlg = wx.TextEntryDialog(self, "Novo nome:", "Renomear favorito", fav.get("name", ""))
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if new_name:
                fav["name"] = new_name
                save_favorites(self.frame.favorites)
                self._refresh()
                self.listbox.SetSelection(idx)
        dlg.Destroy()

    def _on_remove(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        del self.frame.favorites[idx]
        save_favorites(self.frame.favorites)
        self._refresh()
        if self.listbox.GetCount() > 0:
            self.listbox.SetSelection(min(idx, self.listbox.GetCount() - 1))

    def _move_selected(self, direction):
        """Move o favorito selecionado uma posição pra cima (-1) ou
        pra baixo (+1) na lista, e salva a nova ordem."""
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(self.frame.favorites):
            return  # já está no topo/fim, nada a fazer
        favs = self.frame.favorites
        favs[idx], favs[new_idx] = favs[new_idx], favs[idx]
        save_favorites(favs)
        self._refresh()
        self.listbox.SetSelection(new_idx)


# ============================================================================
# Diálogo de pastas favoritas
# ============================================================================
class FavoriteFoldersDialog(wx.Dialog):
    def __init__(self, parent, frame):
        super().__init__(
            parent, title="Pastas favoritas", size=(560, 380),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.frame = frame
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.listbox = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.listbox.SetName("Pastas favoritas")
        self._refresh()
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self._on_play)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 8)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_play = wx.Button(panel, label="&Tocar")
        btn_add = wx.Button(panel, label="&Adicionar...")
        btn_remove = wx.Button(panel, label="Remo&ver (Del)")
        btn_close = wx.Button(panel, wx.ID_CLOSE, "&Fechar")
        btn_play.Bind(wx.EVT_BUTTON, self._on_play)
        btn_add.Bind(wx.EVT_BUTTON, self._on_add)
        btn_remove.Bind(wx.EVT_BUTTON, self._on_remove)
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        for b in (btn_play, btn_add, btn_remove, btn_close):
            btn_sizer.Add(b, 0, wx.ALL, 4)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CLOSE)
        self.listbox.SetFocus()
        if self.listbox.GetCount() > 0:
            self.listbox.SetSelection(0)

    def _refresh(self):
        self.listbox.Clear()
        for path in self.frame.favorite_folders:
            nome = os.path.basename(path.rstrip("\\/")) or path
            self.listbox.Append(f"{nome}  ({path})")

    def _on_key(self, event):
        if wx.Window.FindFocus() is not self.listbox:
            event.Skip()
            return
        code = event.GetKeyCode()
        if code == wx.WXK_DELETE:
            self._on_remove(event)
        elif code in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self._on_play(event)
        else:
            event.Skip()

    def _on_play(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        folder = self.frame.favorite_folders[idx]
        self.EndModal(wx.ID_OK)
        self.frame._load_folder_and_play(folder)

    def _on_add(self, event):
        with wx.DirDialog(
            self, "Escolha a pasta para cadastrar", style=wx.DD_DEFAULT_STYLE
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            folder = dlg.GetPath()

        if folder in self.frame.favorite_folders:
            speak("Essa pasta já está cadastrada.")
            return

        self.frame.favorite_folders.append(folder)
        self.frame._save_favorite_folders()
        self._refresh()
        self.listbox.SetSelection(len(self.frame.favorite_folders) - 1)

    def _on_remove(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            return
        del self.frame.favorite_folders[idx]
        self.frame._save_favorite_folders()
        self._refresh()
        if self.listbox.GetCount() > 0:
            self.listbox.SetSelection(min(idx, self.listbox.GetCount() - 1))


# ============================================================================
# Diálogo de plugins VST - lista com marcar/desmarcar, Configurar e
# Remover, no estilo de programas de automação de rádio (ex.: RadioBoss)
# ============================================================================
class VstPluginsDialog(wx.Dialog):
    def __init__(self, parent, frame):
        super().__init__(
            parent, title="Plugins VST", size=(520, 420),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.frame = frame
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        intro = wx.StaticText(
            panel,
            label=(
                "Marque ou desmarque pra ligar/desligar cada plugin. "
                "Vale só para músicas/arquivos locais - rádios nunca "
                "passam pelos plugins VST."
            ),
        )
        intro.Wrap(460)
        sizer.Add(intro, 0, wx.ALL, 10)

        self.listbox = wx.CheckListBox(panel)
        self.listbox.SetName("Plugins VST carregados")
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 10)
        self._refresh_list()
        self.listbox.Bind(wx.EVT_CHECKLISTBOX, self._on_check)

        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        btn_add = wx.Button(panel, label="&Adicionar...")
        btn_config = wx.Button(panel, label="&Configurar...")
        btn_remove = wx.Button(panel, label="&Remover")
        btn_open_folder = wx.Button(panel, label="Abrir &pasta de plugins")
        btn_add.Bind(wx.EVT_BUTTON, self._on_add)
        btn_config.Bind(wx.EVT_BUTTON, self._on_configure)
        btn_remove.Bind(wx.EVT_BUTTON, self._on_remove)
        btn_open_folder.Bind(wx.EVT_BUTTON, self._on_open_folder)
        for b in (btn_add, btn_config, btn_remove, btn_open_folder):
            btn_row.Add(b, 0, wx.ALL, 4)
        sizer.Add(btn_row, 0, wx.ALIGN_CENTER)

        hint = wx.StaticText(
            panel,
            label=(
                "Cada plugin tem sua própria licença - o LS AudioPlayer "
                "só sabe hospedá-los, não vem com nenhum incluído."
            ),
        )
        hint.Wrap(460)
        sizer.Add(hint, 0, wx.ALL, 10)

        btn_close = wx.Button(panel, wx.ID_CLOSE, "&Fechar")
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        sizer.Add(btn_close, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CLOSE)
        self.listbox.SetFocus()

    def _refresh_list(self):
        self.listbox.Clear()
        for plugin in self.frame.vst_plugins:
            nome = os.path.basename(plugin.get("path", "?"))
            self.listbox.Append(nome)
        for i, plugin in enumerate(self.frame.vst_plugins):
            self.listbox.Check(i, plugin.get("enabled", True))

    def _on_check(self, event):
        idx = event.GetInt()
        self.frame.vst_plugins[idx]["enabled"] = self.listbox.IsChecked(idx)
        self.frame._apply_vst_to_current_stream()
        self.frame._save_vst_settings()

    def _on_add(self, event):
        plugins_dir = get_plugins_dir()
        try:
            arquivos = sorted(
                f for f in os.listdir(plugins_dir) if f.lower().endswith(".dll")
            )
        except Exception:
            arquivos = []

        ja_adicionados = {os.path.basename(p.get("path", "")) for p in self.frame.vst_plugins}
        arquivos = [f for f in arquivos if f not in ja_adicionados]

        if not arquivos:
            wx.MessageBox(
                "Nenhum plugin novo encontrado na pasta \"plugins\".\n\n"
                "Copie o .dll do plugin pra lá primeiro (botão \"Abrir "
                "pasta de plugins\").",
                "Nenhum plugin encontrado", wx.OK | wx.ICON_INFORMATION
            )
            return

        escolhido = wx.GetSingleChoice(
            "Escolha um plugin pra adicionar:", "Adicionar plugin VST",
            arquivos, parent=self
        )
        if not escolhido:
            return

        vst_path = os.path.join(plugins_dir, escolhido)
        self.frame.vst_plugins.append({"path": vst_path, "enabled": True, "params": {}})
        self.frame._apply_vst_to_current_stream()
        self.frame._save_vst_settings()
        self._refresh_list()

        idx_novo = len(self.frame.vst_plugins) - 1
        carregou = (idx_novo < len(self.frame.vst_handles)
                    and self.frame.vst_handles[idx_novo])
        if carregou:
            speak(f"Plugin adicionado: {escolhido}")
        else:
            speak(
                f"{escolhido} adicionado, mas não carregou agora "
                f"(toque uma faixa primeiro, ou não é um VST válido)."
            )

    def _on_configure(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            speak("Selecione um plugin da lista primeiro.")
            return
        dlg = VstParamsDialog(self, self.frame, idx)
        dlg.ShowModal()
        dlg.Destroy()

    def _on_remove(self, event):
        idx = self.listbox.GetSelection()
        if idx == wx.NOT_FOUND:
            speak("Selecione um plugin da lista primeiro.")
            return
        del self.frame.vst_plugins[idx]
        self.frame._apply_vst_to_current_stream()
        self.frame._save_vst_settings()
        self._refresh_list()

    def _on_open_folder(self, event):
        try:
            os.startfile(get_plugins_dir())
        except Exception as e:
            wx.MessageBox(f"Não foi possível abrir a pasta:\n{e}", "Erro", wx.OK | wx.ICON_ERROR)


class VstParamsDialog(wx.Dialog):
    """Parâmetros de UM plugin específico - separado da lista principal
    de propósito, pra não lotar a mesma tela."""

    def __init__(self, parent, frame, plugin_index):
        plugin = frame.vst_plugins[plugin_index]
        nome = os.path.basename(plugin.get("path", "?"))
        super().__init__(
            parent, title=f"Configurar: {nome}", size=(420, 440),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.frame = frame
        self.plugin_index = plugin_index
        self.param_spins = {}
        self._save_timer = None

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        handle = (frame.vst_handles[plugin_index]
                  if plugin_index < len(frame.vst_handles) else 0)

        if not handle or frame.vst_dll is None:
            msg = (
                "Esse plugin não está carregado agora - toque uma faixa "
                "primeiro, ou confira se ele está marcado na lista."
            )
            lbl = wx.StaticText(panel, label=msg)
            lbl.Wrap(380)
            sizer.Add(lbl, 0, wx.ALL, 14)
        else:
            count = frame.vst_dll.BASS_VST_GetParamCount(handle)
            if count == 0:
                lbl = wx.StaticText(panel, label="Esse plugin não tem parâmetros ajustáveis.")
                sizer.Add(lbl, 0, wx.ALL, 14)
            else:
                grid = wx.FlexGridSizer(count, 2, 8, 10)
                grid.AddGrowableCol(1)
                for i in range(count):
                    info = BASS_VST_PARAM_INFO()
                    frame.vst_dll.BASS_VST_GetParamInfo(handle, i, ctypes.byref(info))
                    nome_p = info.name.decode("utf-8", errors="replace").strip("\x00") or f"Parâmetro {i + 1}"
                    unidade = info.unit.decode("utf-8", errors="replace").strip("\x00")
                    valor_atual = frame.vst_dll.BASS_VST_GetParam(handle, i)

                    rotulo = f"{nome_p} ({unidade}):" if unidade else f"{nome_p}:"
                    lbl = wx.StaticText(panel, label=rotulo)
                    spin = wx.SpinCtrl(panel, min=0, max=100,
                                        initial=int(round(valor_atual * 100)))
                    spin.SetName(f"{nome_p}, de 0 a 100")
                    spin.Bind(wx.EVT_SPINCTRL, lambda e, idx=i: self._on_param_change(idx))
                    self.param_spins[i] = spin
                    grid.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
                    grid.Add(spin, 0, wx.EXPAND)
                sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 14)

        btn_close = wx.Button(panel, wx.ID_CLOSE, "&Fechar")
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        sizer.Add(btn_close, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CLOSE)

    def _on_param_change(self, idx):
        """Aplica na hora (pro usuário ouvir o efeito), mas ADIA a
        gravação em disco (com um pequeno atraso que reinicia a cada
        mudança nova) - sem isso, mexer rápido nos controles disparava
        uma gravação de arquivo a cada tick e travava o programa."""
        value01 = self.param_spins[idx].GetValue() / 100.0

        handle = (self.frame.vst_handles[self.plugin_index]
                  if self.plugin_index < len(self.frame.vst_handles) else 0)
        if self.frame.vst_dll is not None and handle:
            try:
                self.frame.vst_dll.BASS_VST_SetParam(handle, idx, value01)
            except Exception:
                pass

        plugin = self.frame.vst_plugins[self.plugin_index]
        plugin.setdefault("params", {})[str(idx)] = value01

        if self._save_timer is not None:
            self._save_timer.Stop()
        self._save_timer = wx.CallLater(400, self.frame._save_vst_settings)


# ============================================================================
# Diálogo do equalizador
# ============================================================================
class EqualizerDialog(wx.Dialog):
    def __init__(self, parent, frame):
        super().__init__(
            parent, title="Equalizador e efeitos", size=(520, 680),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.frame = frame
        self.vst_param_spins = {}

        outer_panel = wx.Panel(self)
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        scroller = wx.ScrolledWindow(outer_panel, style=wx.VSCROLL)
        scroller.SetScrollRate(0, 12)
        panel = scroller
        sizer = wx.BoxSizer(wx.VERTICAL)

        intro = wx.StaticText(
            panel,
            label=(
                "Ajuste o som ao seu gosto. Vale tanto para músicas "
                "quanto para rádios. As mudanças são aplicadas na hora "
                "e ficam salvas."
            ),
        )
        intro.Wrap(440)
        sizer.Add(intro, 0, wx.ALL, 14)

        eq_label = wx.StaticText(panel, label="Equalizador (0 = som original):")
        sizer.Add(eq_label, 0, wx.LEFT | wx.BOTTOM, 12)

        # Usa SpinCtrl (campo numérico com setas) em vez de wx.Slider:
        # o leitor de tela lê o rótulo desses campos de forma
        # confiável, o que não acontecia com os controles deslizantes.
        # É o mesmo tipo de controle usado nas Preferências.
        grid = wx.FlexGridSizer(len(EQ_BANDS), 2, 8, 10)
        grid.AddGrowableCol(1)
        self.sliders = {}
        for name, label, _center, _bandwidth in EQ_BANDS:
            lbl = wx.StaticText(panel, label=f"{label}, em decibéis:")
            spin = wx.SpinCtrl(
                panel, min=-15, max=15,
                initial=int(round(frame.eq_gains.get(name, 0.0))),
            )
            spin.SetName(f"{label}, em decibéis")
            spin.SetToolTip(
                f"{label}: negativo diminui, positivo aumenta, 0 é o som original."
            )
            spin.Bind(wx.EVT_SPINCTRL, lambda e, n=name: self._on_slider(n))
            self.sliders[name] = spin
            grid.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
            grid.Add(spin, 0, wx.EXPAND)
        sizer.Add(grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 10)

        fx_label = wx.StaticText(panel, label="Efeitos:")
        sizer.Add(fx_label, 0, wx.LEFT | wx.BOTTOM, 12)

        self.effect_boxes = {}
        for name, label, _fx_type in AUDIO_EFFECTS:
            chk = wx.CheckBox(panel, label=label)
            chk.SetValue(name in frame.active_effects)
            chk.Bind(wx.EVT_CHECKBOX, lambda e, n=name: self._on_effect(n))
            self.effect_boxes[name] = chk
            sizer.Add(chk, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        # --- Plugins VST (opcional) ---
        if self.frame.vst_dll is not None:
            sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 10)
            btn_manage_vst = wx.Button(panel, label="&Gerenciar plugins VST...")
            btn_manage_vst.Bind(wx.EVT_BUTTON, self._on_manage_vst)
            sizer.Add(btn_manage_vst, 0, wx.LEFT | wx.ALL, 8)

        panel.SetSizer(sizer)
        scroller.FitInside()
        outer_sizer.Add(scroller, 1, wx.EXPAND)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_reset = wx.Button(outer_panel, label="&Zerar tudo")
        btn_close = wx.Button(outer_panel, wx.ID_CLOSE, "&Fechar")
        btn_reset.Bind(wx.EVT_BUTTON, self._on_reset)
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        btn_sizer.Add(btn_reset, 0, wx.ALL, 4)
        btn_sizer.Add(btn_close, 0, wx.ALL, 4)
        outer_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        outer_panel.SetSizer(outer_sizer)
        self.SetEscapeId(wx.ID_CLOSE)

    def _save_and_apply(self):
        self.frame._apply_eq_to_current_stream()
        self.frame.settings["eq_gains"] = dict(self.frame.eq_gains)
        self.frame.settings["active_effects"] = sorted(self.frame.active_effects)
        save_settings(self.frame.settings)

    def _on_slider(self, name):
        """Aplica a mudança na hora, pro usuário ouvir o efeito
        enquanto arrasta, e salva a preferência."""
        value = float(self.sliders[name].GetValue())
        self.frame.eq_gains[name] = value
        self._save_and_apply()
        # Anuncia qual banda mudou e pra quanto - garante que dá pra
        # saber o que se está ajustando mesmo se o leitor de tela não
        # ler o rótulo do controle deslizante.
        label = next((lb for n, lb, _c, _b in EQ_BANDS if n == name), name)
        self.frame.SetStatusText(f"{label}: {int(value):+d} dB")

    def _on_effect(self, name):
        if self.effect_boxes[name].GetValue():
            self.frame.active_effects.add(name)
        else:
            self.frame.active_effects.discard(name)
        self._save_and_apply()

    # ------------------------------------------------------------------
    # Plugins VST
    # ------------------------------------------------------------------
    def _on_manage_vst(self, event):
        dlg = VstPluginsDialog(self, self.frame)
        dlg.ShowModal()
        dlg.Destroy()
        # Ao voltar, atualiza o rótulo caso algo tenha mudado enquanto
        # a tela de plugins estava aberta.

    def _on_reset(self, event):
        for name, slider in self.sliders.items():
            slider.SetValue(0)
            self.frame.eq_gains[name] = 0.0
        for name, chk in self.effect_boxes.items():
            chk.SetValue(False)
        self.frame.active_effects.clear()
        self._save_and_apply()


# ============================================================================
# Diálogo de atalhos de teclado (lista navegável, não um MessageBox)
# ============================================================================
class ShortcutsDialog(wx.Dialog):
    """Mostra os atalhos numa lista de verdade (tecla + ação em
    colunas), navegável com as setas e lida linha por linha pelo
    leitor de tela - bem melhor que um MessageBox, que só lê o texto
    inteiro de uma vez com um único botão OK."""

    SHORTCUTS = [
        ("F1", "Mostrar esta lista de atalhos"),
        ("Espaço", "Tocar/Pausar"),
        ("B", "Próxima faixa (ou próxima rádio favorita)"),
        ("Z", "Faixa anterior (ou rádio favorita anterior)"),
        ("Ctrl+S", "Parar"),
        ("Seta para cima", "Aumentar volume"),
        ("Seta para baixo", "Diminuir volume"),
        ("Seta para a direita", "Avançar na faixa"),
        ("Seta para a esquerda", "Retroceder na faixa"),
        ("Home", "Voltar ao início da faixa atual"),
        ("End", "Ir para o fim da faixa atual"),
        ("X", "Ir para a primeira faixa da lista / reiniciar a rádio"),
        ("Ctrl+End", "Ir para a última faixa da lista"),
        ("R", "Liga/desliga repetir a lista (fica salvo)"),
        ("S", "Liga/desliga modo aleatório (fica salvo)"),
        ("Ctrl+O", "Abrir arquivo(s)"),
        ("Ctrl+D", "Abrir pasta"),
        ("Ctrl+P", "Ver pastas favoritas (Enter toca)"),
        ("Ctrl+Shift+P", "Cadastrar pasta favorita"),
        ("Ctrl+U", "Abrir rádio por URL"),
        ("Ctrl+Shift+L", "Abrir lista de reprodução (.m3u/.pls)"),
        ("Ctrl+L", "Ver lista de reprodução (Enter toca)"),
        ("Ctrl+Del", "Remover a faixa atual da lista"),
        ("Ctrl+F", "Ver rádios favoritas"),
        ("Ctrl+Shift+F", "Adicionar rádio atual aos favoritos"),
        ("Ctrl+E", "Equalizador e efeitos"),
        ("Alt", "Abrir os menus"),
        ("Alt+F4", "Sair"),
        ("Esc", "Sair (opcional - ative em Arquivo > Preferências)"),
    ]

    def __init__(self, parent):
        super().__init__(
            parent, title="Atalhos de teclado",
            size=(560, 480),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        intro = wx.StaticText(
            panel,
            label="Use as setas para percorrer a lista. Esc fecha esta janela."
        )
        sizer.Add(intro, 0, wx.ALL, 10)

        self.list_ctrl = wx.ListCtrl(
            panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL
        )
        self.list_ctrl.SetName("Lista de atalhos de teclado")
        self.list_ctrl.InsertColumn(0, "Tecla", width=170)
        self.list_ctrl.InsertColumn(1, "Ação", width=340)

        for tecla, acao in self.SHORTCUTS:
            idx = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), tecla)
            self.list_ctrl.SetItem(idx, 1, acao)

        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        btn_close = wx.Button(panel, wx.ID_CLOSE, "&Fechar")
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
        sizer.Add(btn_close, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CLOSE)

        if self.list_ctrl.GetItemCount() > 0:
            self.list_ctrl.Select(0)
            self.list_ctrl.Focus(0)
        self.list_ctrl.SetFocus()


# ============================================================================
# Diálogo de preferências
# ============================================================================
class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, frame):
        super().__init__(parent, title="Preferências", size=(420, 420))
        self.frame = frame
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(3, 2, 10, 10)
        grid.AddGrowableCol(1)

        grid.Add(
            wx.StaticText(panel, label="Passo de volume (seta cima/baixo), em %:"),
            0, wx.ALIGN_CENTER_VERTICAL
        )
        self.spin_volume = wx.SpinCtrl(
            panel, min=1, max=25, initial=max(1, int(round(frame.volume_step * 100)))
        )
        grid.Add(self.spin_volume, 0, wx.EXPAND)

        grid.Add(
            wx.StaticText(panel, label="Passo de avanço/retrocesso (segundos):"),
            0, wx.ALIGN_CENTER_VERTICAL
        )
        self.spin_seek = wx.SpinCtrl(
            panel, min=1, max=60, initial=max(1, int(frame.seek_step.total_seconds()))
        )
        grid.Add(self.spin_seek, 0, wx.EXPAND)

        grid.Add(
            wx.StaticText(panel, label="Atraso antes de tocar streams (segundos, 0=imediato):"),
            0, wx.ALIGN_CENTER_VERTICAL
        )
        self.spin_stream_delay = wx.SpinCtrl(
            panel, min=0, max=15,
            initial=max(0, int(round(frame.stream_play_delay_ms / 1000)))
        )
        grid.Add(self.spin_stream_delay, 0, wx.EXPAND)

        sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 14)

        self.chk_allow_multiple = wx.CheckBox(
            panel, label="Permitir mais de uma instância do programa"
        )
        self.chk_allow_multiple.SetValue(
            bool(frame.settings.get("allow_multiple_instances", False))
        )
        sizer.Add(self.chk_allow_multiple, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        restart_hint = wx.StaticText(
            panel, label="(essa opção só tem efeito na próxima vez que abrir o programa)"
        )
        sizer.Add(restart_hint, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        self.chk_argv_log = wx.CheckBox(
            panel,
            label="Registrar argumentos de inicialização em log (diagnóstico)"
        )
        self.chk_argv_log.SetValue(
            bool(frame.settings.get("enable_argv_log", False))
        )
        sizer.Add(self.chk_argv_log, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 4)

        argv_log_hint = wx.StaticText(
            panel,
            label=(
                "Útil só se outro programa (ex.: leitor de tela) abrir o "
                "LS AudioPlayer de um jeito estranho - o log fica em "
                "Ajuda > Abrir pasta de dados. Também só vale a partir "
                "da próxima vez que abrir o programa."
            ),
        )
        argv_log_hint.Wrap(380)
        sizer.Add(argv_log_hint, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        self.chk_close_on_escape = wx.CheckBox(
            panel, label="Tecla Esc também fecha o programa (além de Alt+F4)"
        )
        self.chk_close_on_escape.SetValue(
            bool(frame.settings.get("close_on_escape", False))
        )
        sizer.Add(self.chk_close_on_escape, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        btn_sizer = wx.StdDialogButtonSizer()
        btn_ok = wx.Button(panel, wx.ID_OK, "&Salvar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "&Cancelar")
        btn_sizer.AddButton(btn_ok)
        btn_sizer.AddButton(btn_cancel)
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer)
        self.SetEscapeId(wx.ID_CANCEL)
        btn_ok.SetDefault()
        btn_ok.Bind(wx.EVT_BUTTON, self._on_ok)
        self.spin_volume.SetFocus()

    def _on_ok(self, event):
        self.frame.volume_step = self.spin_volume.GetValue() / 100.0
        self.frame.seek_step = timedelta(seconds=self.spin_seek.GetValue())
        self.frame.stream_play_delay_ms = self.spin_stream_delay.GetValue() * 1000
        self.frame.close_on_escape = self.chk_close_on_escape.GetValue()
        # Atualiza em vez de substituir o dicionário inteiro - assim não
        # apaga outras configurações (repetir/aleatório, etc.) que não
        # aparecem nesta tela.
        self.frame.settings.update({
            "volume_step": self.frame.volume_step,
            "seek_step_seconds": int(self.frame.seek_step.total_seconds()),
            "stream_play_delay_ms": self.frame.stream_play_delay_ms,
            "allow_multiple_instances": self.chk_allow_multiple.GetValue(),
            "enable_argv_log": self.chk_argv_log.GetValue(),
            "close_on_escape": self.frame.close_on_escape,
        })
        save_settings(self.frame.settings)
        self.EndModal(wx.ID_OK)


# ============================================================================
# Janela principal
# ============================================================================
class LSAudioPlayerFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=APP_TITLE, size=(480, 220))

        self.player = MediaPlayer()
        self.player.auto_play = False
        # Prioriza juntar buffer suficiente em vez de tocar com a menor
        # latência possível - RealTimePlayback=True é feito pra chamadas
        # de vídeo ao vivo e sacrifica estabilidade por velocidade, que é
        # exatamente o oposto do que queremos pra rádio via internet.
        try:
            self.player.real_time_playback = False
        except Exception:
            pass
        self.player.add_media_ended(self._on_media_ended)
        self.player.add_media_failed(self._on_media_failed)
        try:
            self.player.playback_session.add_buffering_started(self._on_buffering_started)
            self.player.playback_session.add_buffering_ended(self._on_buffering_ended)
        except Exception:
            pass

        # Motor de streaming via BASS (rádios/streams). Arquivos locais
        # continuam pelo motor do Windows (self.player) acima - só
        # streaming muda de motor, porque era ali que cortava.
        self.bass_dll = load_bass_dll()
        self.bass_stream_handle = 0
        self.icecast_proxy = None
        self._bass_stream_started_at = 0.0
        self._bass_last_meta_title = None

        # Plugins VST (efeito avançado, opcional) - some da interface
        # sozinho se bass_vst.dll não estiver presente. Uma lista, não
        # um só - dá pra usar vários plugins encadeados, cada um
        # podendo ser ligado/desligado independente.
        self.vst_dll = load_bass_vst_dll(self.bass_dll)
        self.vst_handles = []  # handles ativos, mesmo índice de vst_plugins

        self.settings = load_settings()

        saved_vst_list = self.settings.get("vst_plugins")
        if not isinstance(saved_vst_list, list):
            saved_vst_list = []
        self.vst_plugins = []
        for item in saved_vst_list:
            if isinstance(item, dict) and item.get("path"):
                self.vst_plugins.append({
                    "path": item["path"],
                    "enabled": bool(item.get("enabled", True)),
                    "params": dict(item.get("params") or {}),
                })

        self.volume_level = float(self.settings.get("volume_level", 0.8))
        self.volume_level = max(0.0, min(1.0, self.volume_level))
        self.player.volume = self.volume_level

        self._stream_play_timer = None

        self.playlist = []
        self.current_index = -1
        self.is_stream = False
        self.icy_reader = None
        self.last_meta_string = None
        self.stream_station_name = None
        self.favorites = load_favorites()
        self.current_favorite_index = None  # não-None quando "no rádio" (B/Z trocam de favorita)

        self.volume_step = float(self.settings.get("volume_step", VOLUME_STEP))
        self.seek_step = timedelta(seconds=int(self.settings.get("seek_step_seconds", int(SEEK_STEP.total_seconds()))))
        self.stream_play_delay_ms = int(self.settings.get("stream_play_delay_ms", STREAM_PLAY_DELAY_MS))
        self.icy_initial_delay = int(self.settings.get("icy_initial_delay_seconds", ICY_INITIAL_DELAY))
        self.close_on_escape = bool(self.settings.get("close_on_escape", False))
        # Pastas favoritas: guardamos os CAMINHOS, não as listas de
        # arquivos - assim, músicas novas colocadas nelas aparecem
        # automaticamente na próxima vez que forem abertas.
        saved_folders = self.settings.get("favorite_folders")
        self.favorite_folders = [p for p in saved_folders if p] if isinstance(saved_folders, list) else []
        # Repetir/aleatório ficam gravados até o usuário mudar de novo
        self.repeat_mode = bool(self.settings.get("repeat_mode", False))
        self.shuffle_mode = bool(self.settings.get("shuffle_mode", False))
        # Equalizador: ganho em dB por banda (-15 a +15), 0 = neutro
        saved_eq = self.settings.get("eq_gains") or {}
        self.eq_gains = {
            name: float(saved_eq.get(name, 0.0)) for name, _, _, _ in EQ_BANDS
        }
        self._eq_fx_handles = {}
        # Efeitos liga/desliga (eco, reverb, etc.)
        saved_effects = self.settings.get("active_effects") or []
        valid_effect_names = {name for name, _, _ in AUDIO_EFFECTS}
        self.active_effects = {n for n in saved_effects if n in valid_effect_names}
        self._effect_fx_handles = {}
        # Ordem embaralhada do modo aleatório (tipo baralho): percorre
        # todas as faixas antes de repetir qualquer uma.
        self._shuffle_order = []
        self._shuffle_position = -1

        self._build_ui()
        self._build_menu()
        self.item_repeat.Check(self.repeat_mode)
        self.item_shuffle.Check(self.shuffle_mode)
        self._bind_shortcuts()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)
        self.timer.Start(500)

        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.CreateStatusBar()
        self.SetStatusText("Pronto. Ctrl+O para abrir arquivos, Ctrl+U para abrir uma rádio/stream.")

        if not _HAS_MUTAGEN:
            self.SetStatusText(
                "Aviso: instale 'mutagen' (pip install mutagen) para ver "
                "metadados de arquivos locais."
            )

        if self.bass_dll is None:
            self.SetStatusText(
                "Aviso: bass.dll não encontrada - rádios vão usar o motor "
                "do Windows (pode engasgar no início em algumas rádios)."
            )

        self.Centre()
        self.Show()

    # ------------------------------------------------------------------
    # Construção da interface - minimalista de propósito
    # ------------------------------------------------------------------
    def _build_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.cover_bitmap = wx.StaticBitmap(panel, size=(COVER_SIZE, COVER_SIZE))
        self.cover_bitmap.SetName("Capa do álbum")
        sizer.Add(self.cover_bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        panel.SetSizer(sizer)
        self.panel = panel
        self._set_cover_image(None)

        icon_path = _resource_path(ICON_FILE)
        if os.path.exists(icon_path):
            try:
                self.SetIcon(wx.Icon(icon_path, wx.BITMAP_TYPE_ICO))
            except Exception:
                pass

    def _set_cover_image(self, image_bytes):
        """Mostra a capa/arte de álbum embutida no arquivo (se tiver),
        ou a imagem padrão (placeholder) quando não houver - usada em
        streams/rádios, que não trazem capa, e em arquivos sem arte
        embutida."""
        try:
            img = None
            if image_bytes:
                img = wx.Image(io.BytesIO(image_bytes), wx.BITMAP_TYPE_ANY)
                if not img.IsOk():
                    img = None
            if img is None:
                cover_path = _resource_path(DEFAULT_COVER_FILE)
                if os.path.exists(cover_path):
                    img = wx.Image(cover_path, wx.BITMAP_TYPE_ANY)
            if img is None or not img.IsOk():
                return
            img = img.Scale(COVER_SIZE, COVER_SIZE, wx.IMAGE_QUALITY_HIGH)
            self.cover_bitmap.SetBitmap(wx.Bitmap(img))
            self.panel.Layout()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Menus
    # ------------------------------------------------------------------
    def _build_menu(self):
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        item_open_files = file_menu.Append(wx.ID_ANY, "Abrir &arquivo(s)...\tCtrl+O")
        item_open_folder = file_menu.Append(wx.ID_ANY, "Abrir pa&sta...\tCtrl+D")
        item_open_url = file_menu.Append(wx.ID_ANY, "Abrir &URL/Stream...\tCtrl+U")
        item_open_playlist = file_menu.Append(
            wx.ID_ANY, "Abrir &lista de reprodução (m3u/pls)...\tCtrl+Shift+L"
        )
        file_menu.AppendSeparator()
        item_fav_folders = file_menu.Append(
            wx.ID_ANY, "Pastas &favoritas...\tCtrl+P"
        )
        item_fav_folder_add = file_menu.Append(
            wx.ID_ANY, "Cadastrar pasta favorita...\tCtrl+Shift+P"
        )
        file_menu.AppendSeparator()
        item_prefs = file_menu.Append(wx.ID_PREFERENCES, "&Preferências...")
        file_menu.AppendSeparator()
        item_exit = file_menu.Append(wx.ID_EXIT, "Sai&r\tAlt+F4")

        playback_menu = wx.Menu()
        item_play = playback_menu.Append(wx.ID_ANY, "Tocar/Pausar (Espaço)")
        item_next = playback_menu.Append(wx.ID_ANY, "Próxima faixa (B)")
        item_prev = playback_menu.Append(wx.ID_ANY, "Faixa anterior (Z)")
        item_stop = playback_menu.Append(wx.ID_ANY, "&Parar\tCtrl+S")
        playback_menu.AppendSeparator()
        self.item_repeat = playback_menu.AppendCheckItem(wx.ID_ANY, "&Repetir playlist (R)")
        self.item_shuffle = playback_menu.AppendCheckItem(wx.ID_ANY, "Modo &aleatório (S)")
        playback_menu.AppendSeparator()
        item_vol_up = playback_menu.Append(wx.ID_ANY, "Aumentar volume (seta cima)")
        item_vol_down = playback_menu.Append(wx.ID_ANY, "Diminuir volume (seta baixo)")
        item_seek_fwd = playback_menu.Append(wx.ID_ANY, "Avançar (seta direita)")
        item_seek_back = playback_menu.Append(wx.ID_ANY, "Retroceder (seta esquerda)")
        item_seek_start = playback_menu.Append(wx.ID_ANY, "Voltar ao início da faixa (Home)")
        item_seek_end = playback_menu.Append(wx.ID_ANY, "Ir para o fim da faixa (End)")
        playback_menu.AppendSeparator()
        item_equalizer = playback_menu.Append(wx.ID_ANY, "&Equalizador e efeitos...\tCtrl+E")

        list_menu = wx.Menu()
        item_view_playlist = list_menu.Append(wx.ID_ANY, "&Ver lista de reprodução (Enter toca)...\tCtrl+L")
        item_first_track = list_menu.Append(wx.ID_ANY, "Ir para &primeira faixa (X)")
        item_last_track = list_menu.Append(wx.ID_ANY, "Ir para últi&ma faixa\tCtrl+End")
        item_remove_current = list_menu.Append(wx.ID_ANY, "Remover faixa &atual\tCtrl+Del")
        item_clear = list_menu.Append(wx.ID_ANY, "&Limpar lista")
        item_save_playlist = list_menu.Append(wx.ID_ANY, "&Salvar lista como M3U...")

        favorites_menu = wx.Menu()
        item_fav_add = favorites_menu.Append(
            wx.ID_ANY, "&Adicionar rádio atual aos favoritos\tCtrl+Shift+F"
        )
        item_fav_show = favorites_menu.Append(wx.ID_ANY, "&Ver favoritos...\tCtrl+F")
        favorites_menu.AppendSeparator()
        item_fav_export = favorites_menu.Append(wx.ID_ANY, "&Exportar favoritos...")
        item_fav_import = favorites_menu.Append(wx.ID_ANY, "&Importar favoritos...")

        help_menu = wx.Menu()
        item_shortcuts = help_menu.Append(wx.ID_ANY, "&Atalhos de teclado\tF1")
        help_menu.AppendSeparator()
        item_open_data_folder = help_menu.Append(
            wx.ID_ANY, "Abrir &pasta de dados (favoritos, configurações, log)"
        )
        help_menu.AppendSeparator()
        item_about = help_menu.Append(wx.ID_ABOUT, "&Sobre o LS AudioPlayer")

        menubar.Append(file_menu, "&Arquivo")
        menubar.Append(playback_menu, "&Reprodução")
        menubar.Append(list_menu, "&Lista")
        menubar.Append(favorites_menu, "&Favoritos")
        menubar.Append(help_menu, "Aj&uda")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, lambda e: self._open_files(), item_open_files)
        self.Bind(wx.EVT_MENU, lambda e: self._open_folder(), item_open_folder)
        self.Bind(wx.EVT_MENU, lambda e: self._open_url(), item_open_url)
        self.Bind(wx.EVT_MENU, lambda e: self._open_playlist_file(), item_open_playlist)
        self.Bind(wx.EVT_MENU, lambda e: self._show_favorite_folders(), item_fav_folders)
        self.Bind(wx.EVT_MENU, lambda e: self._add_favorite_folder(), item_fav_folder_add)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), item_exit)

        self.Bind(wx.EVT_MENU, lambda e: self._toggle_play(), item_play)
        self.Bind(wx.EVT_MENU, lambda e: self._next_track(manual=True), item_next)
        self.Bind(wx.EVT_MENU, lambda e: self._prev_track(), item_prev)
        self.Bind(wx.EVT_MENU, lambda e: self._stop(), item_stop)
        self.Bind(wx.EVT_MENU, self._on_menu_toggle_repeat, self.item_repeat)
        self.Bind(wx.EVT_MENU, self._on_menu_toggle_shuffle, self.item_shuffle)
        self.Bind(wx.EVT_MENU, lambda e: self._change_volume(self.volume_step), item_vol_up)
        self.Bind(wx.EVT_MENU, lambda e: self._change_volume(-self.volume_step), item_vol_down)
        self.Bind(wx.EVT_MENU, lambda e: self._seek(self.seek_step), item_seek_fwd)
        self.Bind(wx.EVT_MENU, lambda e: self._seek(-self.seek_step), item_seek_back)
        self.Bind(wx.EVT_MENU, lambda e: self._seek_to_start(), item_seek_start)
        self.Bind(wx.EVT_MENU, lambda e: self._seek_to_end(), item_seek_end)
        self.Bind(wx.EVT_MENU, lambda e: self._show_equalizer(), item_equalizer)
        self.Bind(wx.EVT_MENU, lambda e: self._show_preferences(), item_prefs)

        self.Bind(wx.EVT_MENU, lambda e: self._show_playlist_dialog(), item_view_playlist)
        self.Bind(wx.EVT_MENU, lambda e: self._go_to_first_track(), item_first_track)
        self.Bind(wx.EVT_MENU, lambda e: self._go_to_last_track(), item_last_track)
        self.Bind(wx.EVT_MENU, lambda e: self._remove_current_track(), item_remove_current)
        self.Bind(wx.EVT_MENU, lambda e: self._clear_playlist(), item_clear)
        self.Bind(wx.EVT_MENU, lambda e: self._save_playlist_as_m3u(), item_save_playlist)

        self.Bind(wx.EVT_MENU, lambda e: self._add_current_to_favorites(), item_fav_add)
        self.Bind(wx.EVT_MENU, lambda e: self._show_favorites(), item_fav_show)
        self.Bind(wx.EVT_MENU, lambda e: self._export_favorites(), item_fav_export)
        self.Bind(wx.EVT_MENU, lambda e: self._import_favorites(), item_fav_import)

        self.Bind(wx.EVT_MENU, lambda e: self._show_shortcuts(), item_shortcuts)
        self.Bind(wx.EVT_MENU, lambda e: self._open_data_folder(), item_open_data_folder)
        self.Bind(wx.EVT_MENU, lambda e: self._show_about(), item_about)

    # ------------------------------------------------------------------
    # Atalhos globais de teclado (apenas os que não são acelerador de menu)
    # ------------------------------------------------------------------
    def _bind_shortcuts(self):
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key_down)

    def _on_key_down(self, event):
        focus = wx.Window.FindFocus()
        if isinstance(focus, wx.TextCtrl):
            event.Skip()
            return

        keycode = event.GetKeyCode()
        ctrl = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()
        plain = not ctrl and not alt

        if keycode == wx.WXK_F1 and plain:
            self._show_shortcuts()
            return
        if keycode == wx.WXK_SPACE and plain:
            self._toggle_play()
            return
        if keycode == wx.WXK_ESCAPE and plain and self.close_on_escape:
            self.Close()
            return
        if keycode == ord('B') and plain:
            self._next_track(manual=True)
            return
        if keycode == ord('Z') and plain:
            self._prev_track()
            return
        if keycode == ord('R') and plain and not shift:
            self._toggle_repeat_via_key()
            return
        if keycode == ord('S') and plain and not shift:
            self._toggle_shuffle_via_key()
            return
        if keycode == ord('X') and plain and not shift:
            self._go_to_first_track()
            return
        if keycode == wx.WXK_UP and plain:
            self._change_volume(self.volume_step)
            return
        if keycode == wx.WXK_DOWN and plain:
            self._change_volume(-self.volume_step)
            return
        if keycode == wx.WXK_RIGHT and plain:
            self._seek(self.seek_step)
            return
        if keycode == wx.WXK_LEFT and plain:
            self._seek(-self.seek_step)
            return
        if keycode == wx.WXK_HOME and plain:
            self._seek_to_start()
            return
        if keycode == wx.WXK_END and plain:
            self._seek_to_end()
            return

        event.Skip()

    # ------------------------------------------------------------------
    # Repetição / aleatório
    # ------------------------------------------------------------------
    def _toggle_repeat_via_key(self):
        self.repeat_mode = not self.repeat_mode
        self.item_repeat.Check(self.repeat_mode)
        self._save_toggle_setting("repeat_mode", self.repeat_mode)
        self._announce_repeat()

    def _on_menu_toggle_repeat(self, event):
        self.repeat_mode = event.IsChecked()
        self._save_toggle_setting("repeat_mode", self.repeat_mode)
        self._announce_repeat()

    def _announce_repeat(self):
        msg = "Repetir playlist: ativado." if self.repeat_mode else "Repetir playlist: desativado."
        self.SetStatusText(msg)
        speak(msg)

    def _toggle_shuffle_via_key(self):
        self.shuffle_mode = not self.shuffle_mode
        self.item_shuffle.Check(self.shuffle_mode)
        self._save_toggle_setting("shuffle_mode", self.shuffle_mode)
        if self.shuffle_mode:
            self._rebuild_shuffle_order()
        self._announce_shuffle()

    def _on_menu_toggle_shuffle(self, event):
        self.shuffle_mode = event.IsChecked()
        self._save_toggle_setting("shuffle_mode", self.shuffle_mode)
        if self.shuffle_mode:
            self._rebuild_shuffle_order()
        self._announce_shuffle()

    def _save_toggle_setting(self, key, value):
        """Grava repeat_mode/shuffle_mode nas configurações do usuário,
        pra ficarem do jeito que ele deixou até mudar de novo."""
        self.settings[key] = value
        save_settings(self.settings)

    def _announce_shuffle(self):
        msg = "Modo aleatório: ativado." if self.shuffle_mode else "Modo aleatório: desativado."
        self.SetStatusText(msg)
        speak(msg)

    # ------------------------------------------------------------------
    # Abrir arquivos / pasta / URL
    # ------------------------------------------------------------------
    def _clear_playlist_if_switching_kind(self, new_is_stream):
        """Rádios e músicas são coisas de naturezas diferentes e não
        devem se misturar na mesma lista de reprodução. Ao abrir algo
        de um tipo diferente do que está na lista, esvazia a lista
        antes - assim, por exemplo, abrir uma pasta de músicas remove
        a rádio que estava ali, e vice-versa."""
        if not self.playlist:
            return
        current_kind_is_stream = any(
            p.startswith("http://") or p.startswith("https://")
            for p in self.playlist
        )
        if current_kind_is_stream != new_is_stream:
            self.playlist = []
            self.current_index = -1
            self.current_favorite_index = None

    def _open_files(self):
        wildcard = ("Arquivos de áudio (*.mp3;*.wav;*.ogg;*.flac;*.m4a)|"
                    "*.mp3;*.wav;*.ogg;*.flac;*.m4a|Todos os arquivos (*.*)|*.*")
        with wx.FileDialog(
            self, "Escolha um ou mais arquivos de áudio",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            paths = dlg.GetPaths()

        if not paths:
            return

        self._clear_playlist_if_switching_kind(new_is_stream=False)
        start_index = len(self.playlist)
        self.playlist.extend(paths)

        self.SetStatusText(f"{len(paths)} arquivo(s) adicionado(s) à lista.")
        self._play_from(start_index)

    def _open_folder(self):
        with wx.DirDialog(
            self, "Escolha uma pasta com arquivos de áudio",
            style=wx.DD_DEFAULT_STYLE
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            folder = dlg.GetPath()

        self._load_folder_and_play(folder)

    def _load_folder_and_play(self, folder):
        """Varre a pasta (e subpastas) e toca o que encontrar. Separado
        de _open_folder pra ser reaproveitado pela pasta favorita."""
        if not os.path.isdir(folder):
            msg = f"A pasta não existe mais: {folder}"
            self.SetStatusText(msg)
            speak("Essa pasta não existe mais.")
            return

        found = []
        for root, _dirs, files in os.walk(folder):
            for f in files:
                if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS:
                    found.append(os.path.join(root, f))

        if not found:
            msg = "Nenhum arquivo de áudio encontrado nessa pasta."
            self.SetStatusText(msg)
            speak(msg)
            return

        found.sort()

        self._clear_playlist_if_switching_kind(new_is_stream=False)
        start_index = len(self.playlist)
        self.playlist.extend(found)

        msg = f"{len(found)} arquivo(s) adicionado(s) da pasta \"{os.path.basename(folder)}\"."
        self.SetStatusText(msg)
        speak(msg)
        self._play_from(start_index)

    # ------------------------------------------------------------------
    # Pastas favoritas
    # ------------------------------------------------------------------
    def _show_favorite_folders(self):
        """Ctrl+P: lista as pastas favoritas cadastradas pra escolher e
        tocar. Guardamos o CAMINHO, não a lista de arquivos - músicas
        novas colocadas nelas aparecem sozinhas."""
        if not self.favorite_folders:
            speak("Nenhuma pasta favorita cadastrada. Use Ctrl+Shift+P.")
            self.SetStatusText("Nenhuma pasta favorita cadastrada. Use Ctrl+Shift+P para cadastrar.")
            return
        dlg = FavoriteFoldersDialog(self, self)
        dlg.ShowModal()
        dlg.Destroy()

    def _add_favorite_folder(self):
        """Ctrl+Shift+P: cadastra uma pasta nova na lista de favoritas."""
        with wx.DirDialog(
            self, "Escolha a pasta para cadastrar", style=wx.DD_DEFAULT_STYLE
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            folder = dlg.GetPath()

        if folder in self.favorite_folders:
            speak("Essa pasta já está cadastrada.")
            return

        self.favorite_folders.append(folder)
        self._save_favorite_folders()

    def _save_favorite_folders(self):
        self.settings["favorite_folders"] = list(self.favorite_folders)
        save_settings(self.settings)

    def _open_url(self):
        dlg = wx.TextEntryDialog(
            self, "Digite a URL do stream (http/https):", "Abrir stream"
        )
        if dlg.ShowModal() == wx.ID_OK:
            url = dlg.GetValue().strip()
            if url:
                self._clear_playlist_if_switching_kind(new_is_stream=True)
                self.playlist.append(url)
                idx = len(self.playlist) - 1
                self._play_index(idx)
        dlg.Destroy()

    def _open_playlist_file(self):
        wildcard = (
            "Listas de reprodução (*.m3u;*.m3u8;*.pls)|*.m3u;*.m3u8;*.pls|"
            "Todos os arquivos (*.*)|*.*"
        )
        with wx.FileDialog(
            self, "Escolha uma lista de reprodução",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()

        self._load_playlist_file_and_play(path)

    def _load_playlist_file_and_play(self, path):
        entries = parse_playlist_file(path)
        if not entries:
            msg = "Não encontrei nenhuma faixa válida nessa lista."
            self.SetStatusText(msg)
            speak(msg)
            return

        # Um .m3u/.pls pode conter rádios ou músicas - usa o primeiro
        # item pra decidir a natureza da lista que está entrando.
        first_is_stream = entries[0].startswith("http://") or entries[0].startswith("https://")
        self._clear_playlist_if_switching_kind(new_is_stream=first_is_stream)

        start_index = len(self.playlist)
        self.playlist.extend(entries)
        msg = f"{len(entries)} item(ns) adicionado(s) da lista \"{os.path.basename(path)}\"."
        self.SetStatusText(msg)
        speak(msg)
        self._play_from(start_index)

    def _save_playlist_as_m3u(self):
        if not self.playlist:
            speak("Lista vazia.")
            return
        with wx.FileDialog(
            self, "Salvar lista como M3U",
            wildcard="M3U (*.m3u)|*.m3u",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()

        if not path.lower().endswith(".m3u"):
            path += ".m3u"

        if write_m3u(path, self.playlist):
            msg = f"Lista salva em {os.path.basename(path)}."
            self.SetStatusText(msg)
            speak(msg)
        else:
            wx.MessageBox("Não foi possível salvar a lista.", "Erro", wx.OK | wx.ICON_ERROR)

    def open_path_and_play(self, path):
        """Usado ao abrir um arquivo passado por linha de comando
        (ex.: clique em 'Reproduzir com LS AudioPlayer' no Explorer). Detecta
        automaticamente arquivos de playlist (m3u/pls) e carrega todos
        os itens, em vez de tentar tocar o arquivo de lista como áudio."""
        path = os.path.abspath(path)
        if os.path.splitext(path)[1].lower() in PLAYLIST_EXTENSIONS:
            self._load_playlist_file_and_play(path)
            return
        self._clear_playlist_if_switching_kind(new_is_stream=False)
        start_index = len(self.playlist)
        self.playlist.append(path)
        self._play_index(start_index)

    def open_folder_and_play(self, folder_path):
        """Usado ao abrir uma PASTA passada por linha de comando (ex.:
        clique em 'Reproduzir pasta com LS AudioPlayer' no Explorer). Toca
        o álbum inteiro em ordem alfabética, incluindo subpastas."""
        found = []
        for root, _dirs, files in os.walk(folder_path):
            for f in files:
                if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS:
                    found.append(os.path.join(root, f))

        if not found:
            self.SetStatusText("Nenhum arquivo de áudio encontrado nessa pasta.")
            speak("Nenhum arquivo de áudio encontrado nessa pasta.")
            return

        found.sort()
        self._clear_playlist_if_switching_kind(new_is_stream=False)
        start_index = len(self.playlist)
        self.playlist.extend(found)
        self._play_from(start_index)

    # ------------------------------------------------------------------
    # Gerenciamento da lista (sob demanda, via diálogo)
    # ------------------------------------------------------------------
    def _show_playlist_dialog(self):
        if not self.playlist:
            speak("Lista vazia.")
            self.SetStatusText("Lista vazia.")
            return
        dlg = PlaylistDialog(self, self)
        dlg.ShowModal()
        dlg.Destroy()

    def _remove_current_track(self):
        if self.current_index == -1 or not self.playlist:
            speak("Nenhuma faixa tocando.")
            return
        path = self.playlist[self.current_index]
        name = path if (path.startswith("http://") or path.startswith("https://")) else os.path.basename(path)
        del self.playlist[self.current_index]
        self._stop()
        self.current_index = -1
        msg = f"Removido: {name}"
        self.SetStatusText(msg)
        speak(msg)

    def _clear_playlist(self):
        self._stop()
        self.playlist = []
        self.current_index = -1
        self.last_meta_string = None
        self.SetTitle(APP_TITLE)
        self._set_cover_image(None)
        msg = "Lista de reprodução limpa."
        self.SetStatusText(msg)
        speak(msg)

    # ------------------------------------------------------------------
    # Favoritos (rádios/streams)
    # ------------------------------------------------------------------
    def _add_current_to_favorites(self):
        if not self.is_stream or self.current_index == -1:
            msg = "Só é possível favoritar uma rádio/stream que estiver tocando."
            self.SetStatusText(msg)
            speak(msg)
            return

        url = self.playlist[self.current_index]
        for fav in self.favorites:
            if fav.get("url") == url:
                msg = "Essa rádio já está nos favoritos."
                self.SetStatusText(msg)
                speak(msg)
                return

        name = self.stream_station_name or url
        self.favorites.append({"name": name, "url": url})
        if save_favorites(self.favorites):
            msg = f"Adicionado aos favoritos: {name}"
        else:
            msg = f"Adicionado aos favoritos: {name} (não consegui salvar no disco)"
        self.SetStatusText(msg)
        speak(msg)

    def _show_favorites(self):
        if not self.favorites:
            speak("Nenhuma rádio favoritada ainda.")
            self.SetStatusText("Nenhuma rádio favoritada ainda.")
            return
        dlg = FavoritesDialog(self, self)
        dlg.ShowModal()
        dlg.Destroy()

    def _play_favorite_by_index(self, idx):
        """Toca a favorita de índice idx (com volta ao início/fim da
        lista), e entra em 'modo rádio': B/Z passam a trocar de
        favorita em vez de navegar a playlist normal, até o usuário
        tocar outra coisa (arquivo, pasta, URL avulsa, etc.)."""
        if not self.favorites:
            speak("Nenhuma rádio favoritada ainda.")
            return
        idx = idx % len(self.favorites)
        fav = self.favorites[idx]
        self._clear_playlist_if_switching_kind(new_is_stream=True)
        start_index = len(self.playlist)
        self.playlist.append(fav["url"])
        self._play_index(start_index)
        self.current_favorite_index = idx

    def _export_favorites(self):
        """Salva os favoritos num arquivo .json, pra fazer backup ou
        levar pra outro computador."""
        if not self.favorites:
            msg = "Nenhuma rádio favoritada para exportar."
            self.SetStatusText(msg)
            speak(msg)
            return

        with wx.FileDialog(
            self, "Exportar favoritos",
            defaultFile="radios_LSAudioPlayer.json",
            wildcard="Favoritos do LS AudioPlayer (*.json)|*.json",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()

        if not path.lower().endswith(".json"):
            path += ".json"

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            wx.MessageBox(f"Não foi possível exportar:\n{e}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        msg = f"{len(self.favorites)} favorito(s) exportado(s) para {os.path.basename(path)}."
        self.SetStatusText(msg)
        speak(msg)

    def _import_favorites(self):
        """Carrega favoritos de um arquivo .json exportado antes. Deixa
        o usuário escolher entre juntar com os atuais ou substituir
        tudo, e ignora duplicatas (mesma URL) ao juntar."""
        with wx.FileDialog(
            self, "Importar favoritos",
            wildcard="Favoritos do LS AudioPlayer (*.json)|*.json|Todos os arquivos (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            wx.MessageBox(f"Não foi possível ler o arquivo:\n{e}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        # Aceita só o formato esperado: lista de objetos com url
        if not isinstance(data, list):
            wx.MessageBox(
                "Esse arquivo não parece ser uma lista de favoritos do "
                "LS AudioPlayer.", "Erro", wx.OK | wx.ICON_ERROR
            )
            return

        imported = []
        for item in data:
            if isinstance(item, dict) and item.get("url"):
                imported.append({
                    "name": item.get("name") or item["url"],
                    "url": item["url"],
                })

        if not imported:
            wx.MessageBox(
                "Nenhum favorito válido encontrado nesse arquivo.",
                "Aviso", wx.OK | wx.ICON_WARNING
            )
            return

        if self.favorites:
            choice = wx.MessageBox(
                f"Foram encontrados {len(imported)} favorito(s) no arquivo.\n\n"
                f"Sim: juntar com os {len(self.favorites)} favoritos atuais "
                f"(ignorando repetidos)\n"
                f"Não: substituir todos os favoritos atuais",
                "Importar favoritos",
                wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION
            )
            if choice == wx.CANCEL:
                return
            merge = (choice == wx.YES)
        else:
            merge = True

        if merge:
            existing_urls = {f.get("url") for f in self.favorites}
            added = 0
            for item in imported:
                if item["url"] not in existing_urls:
                    self.favorites.append(item)
                    existing_urls.add(item["url"])
                    added += 1
            msg = f"{added} novo(s) favorito(s) importado(s)."
        else:
            self.favorites = imported
            msg = f"{len(imported)} favorito(s) importado(s) (lista substituída)."

        save_favorites(self.favorites)
        self.current_favorite_index = None
        self.SetStatusText(msg)
        speak(msg)

    # ------------------------------------------------------------------
    # Preferências
    # ------------------------------------------------------------------
    def _show_preferences(self):
        dlg = PreferencesDialog(self, self)
        dlg.ShowModal()
        dlg.Destroy()

    # ------------------------------------------------------------------
    # Controle de reprodução
    # ------------------------------------------------------------------
    def _play_index(self, index):
        if not (0 <= index < len(self.playlist)):
            return

        # Sai do "modo rádio" (B/Z trocando favoritas) sempre que tocar
        # qualquer outra coisa - quem entra de volta nesse modo é só
        # _play_favorite_by_index, que reafirma isso logo em seguida.
        self.current_favorite_index = None

        self._stop_icy_reader()
        self._stop_bass_stream()
        if self._stream_play_timer is not None:
            self._stream_play_timer.Stop()
            self._stream_play_timer = None

        # Pausa qualquer coisa que esteja tocando no motor do Windows -
        # sem isso, trocar de um arquivo local (que usa esse motor)
        # pra uma rádio via BASS deixava os dois tocando ao mesmo tempo,
        # um por cima do outro.
        try:
            self.player.pause()
        except Exception:
            pass

        path = self.playlist[index]
        self.is_stream = path.startswith("http://") or path.startswith("https://")

        self.current_index = index
        name = os.path.basename(path) if not self.is_stream else path
        self.last_meta_string = None
        self.stream_station_name = None

        if self.is_stream:
            self._set_now_playing(name, "Conectando ao stream...")
            self.SetStatusText(f"Conectando: {name}")
            self._set_cover_image(None)  # rádios não têm capa embutida
            threading.Thread(
                target=self._start_stream_playback,
                args=(path, index),
                daemon=True,
            ).start()
        else:
            self._play_local_file(path, name)

    def _play_local_file(self, path, name):
        """Toca um arquivo local. Prefere a BASS (que permite
        equalizador e efeitos); se ela não estiver disponível, ou não
        conseguir abrir o arquivo, cai pro motor do Windows como antes."""
        self._load_local_metadata(path, fallback_name=name)

        if self.bass_dll is not None:
            # BASS_UNICODE: essencial pra caminhos com acentos
            # ("LANÇAMENTOS", "Vitória") funcionarem corretamente.
            try:
                stream = self.bass_dll.BASS_StreamCreateFile(
                    0, ctypes.c_wchar_p(path), 0, 0, BASS_UNICODE
                )
            except Exception:
                stream = 0

            if stream:
                self.bass_stream_handle = stream
                self._bass_stream_started_at = time.time()
                self.bass_dll.BASS_ChannelSetAttribute(
                    stream, BASS_ATTRIB_VOL, ctypes.c_float(self.volume_level)
                )
                self._apply_eq_to_current_stream()
                self._apply_vst_to_current_stream()
                self.bass_dll.BASS_ChannelPlay(stream, False)
                return

        # Reserva: motor do Windows (sem equalizador/efeitos, mas
        # garante que o arquivo toca de algum jeito).
        try:
            source = get_local_media_source(path)
        except Exception as e:
            msg = f'Não foi possível abrir "{name}": {e}'
            self.SetStatusText(msg)
            speak(f"Não foi possível abrir {name}.")
            # Pula pra próxima faixa automaticamente, pra um único
            # arquivo com problema não travar a reprodução do
            # resto da pasta.
            wx.CallAfter(self._advance_after_track_end)
            return
        self.player.source = source
        self.player.volume = self.volume_level
        self.player.play()

    # ------------------------------------------------------------------
    # Streaming via BASS (com o motor do Windows como reserva)
    # ------------------------------------------------------------------
    def _start_stream_playback(self, url, expected_index):
        """Roda numa thread separada. Tenta o caminho novo (proxy local
        + BASS); se a BASS não estiver disponível, o proxy falhar, ou a
        URL for HLS (.m3u8 - um manifesto de texto, não áudio direto;
        o proxy simples não entende esse protocolo), cai pro caminho
        antigo (Windows abrindo a conexão sozinho, que lida melhor com
        HLS nativamente)."""
        is_hls = url.lower().split("?", 1)[0].endswith(".m3u8")

        if self.bass_dll is not None and not is_hls:
            try:
                proxy = LocalIcecastProxy(url)
                local_url = proxy.start()
                wx.CallAfter(self._begin_bass_playback, url, local_url, proxy, expected_index)
                return
            except Exception:
                pass  # cai pro caminho antigo abaixo

        resolved_url = resolve_stream_url(url)
        wx.CallAfter(self._open_resolved_stream_wmf, url, resolved_url, expected_index)

    def _begin_bass_playback(self, original_url, local_url, proxy, expected_index):
        if self.current_index != expected_index or not self.is_stream:
            proxy.stop()
            return

        # BASS_STREAM_BLOCK de volta: é o que faz o BASS_CONFIG_NET_BUFFER
        # (8s) valer continuamente durante a reprodução, não só no
        # pré-carregamento inicial - sem essa flag, o buffer maior não
        # tinha efeito nenhum depois que a música já tinha começado.
        stream = self.bass_dll.BASS_StreamCreateURL(
            local_url.encode("utf-8"), 0, BASS_STREAM_BLOCK, None, None
        )
        if not stream:
            err = self.bass_dll.BASS_ErrorGetCode()
            proxy.stop()
            self.SetStatusText(f"Não foi possível abrir o stream (BASS erro {err}).")
            speak("Não foi possível abrir esse stream.")
            return

        self.icecast_proxy = proxy
        self.bass_stream_handle = stream
        self._bass_stream_started_at = time.time()
        self._bass_last_meta_title = None

        self.bass_dll.BASS_ChannelSetAttribute(stream, BASS_ATTRIB_VOL, ctypes.c_float(self.volume_level))
        self.bass_dll.BASS_ChannelPlay(stream, False)
        self._apply_eq_to_current_stream()
        # Plugins VST só valem pra arquivos locais, nunca pra rádios -
        # de propósito (pedido explícito).

        # Metadados (nome da música) direto de dentro da BASS, que já
        # separa os blocos de metadado do áudio sozinha (via o
        # icy-metaint repassado pelo proxy) - sem precisar de nenhuma
        # conexão extra pra isso. O nome da rádio (icy-name) já veio
        # junto com a resposta do proxy.
        if proxy.icy_name:
            self.stream_station_name = proxy.icy_name
            self._set_now_playing(proxy.icy_name, f"Rádio: {proxy.icy_name}")

    def _stop_bass_stream(self):
        if self.bass_stream_handle:
            try:
                self.bass_dll.BASS_StreamFree(self.bass_stream_handle)
            except Exception:
                pass
            self.bass_stream_handle = 0
        self._eq_fx_handles = {}
        self._effect_fx_handles = {}
        # O DSP do VST é destruído automaticamente junto com o canal -
        # só zera nossas referências, sem precisar chamar RemoveDSP.
        self.vst_handles = [0] * len(self.vst_plugins)
        if self.icecast_proxy is not None:
            self.icecast_proxy.stop()
            self.icecast_proxy = None

    # ------------------------------------------------------------------
    # Equalizador (efeitos DirectX 8 embutidos na BASS)
    # ------------------------------------------------------------------
    def _apply_eq_to_current_stream(self):
        """Aplica/atualiza equalizador e efeitos no stream que está
        tocando pela BASS (rádio ou arquivo local). Bandas com ganho 0
        e efeitos desligados não recebem processamento nenhum, pra não
        mexer no áudio à toa."""
        if not self.bass_stream_handle or self.bass_dll is None:
            return

        # --- Equalizador (graves/médios/agudos) ---
        for name, _label, center, bandwidth in EQ_BANDS:
            gain = self.eq_gains.get(name, 0.0)
            handle = self._eq_fx_handles.get(name)

            if abs(gain) < 0.01:
                # Ganho neutro: remove o efeito se estiver ativo
                if handle:
                    try:
                        self.bass_dll.BASS_ChannelRemoveFX(self.bass_stream_handle, handle)
                    except Exception:
                        pass
                    self._eq_fx_handles.pop(name, None)
                continue

            if not handle:
                try:
                    handle = self.bass_dll.BASS_ChannelSetFX(
                        self.bass_stream_handle, BASS_FX_DX8_PARAMEQ, 0
                    )
                except Exception:
                    continue
                if not handle:
                    continue
                self._eq_fx_handles[name] = handle

            params = BASS_DX8_PARAMEQ(float(center), float(bandwidth), float(gain))
            try:
                self.bass_dll.BASS_FXSetParameters(handle, ctypes.byref(params))
            except Exception:
                pass

        # --- Efeitos liga/desliga (eco, reverb, compressor, etc.) ---
        for name, _label, fx_type in AUDIO_EFFECTS:
            handle = self._effect_fx_handles.get(name)
            should_be_on = name in self.active_effects

            if not should_be_on:
                if handle:
                    try:
                        self.bass_dll.BASS_ChannelRemoveFX(self.bass_stream_handle, handle)
                    except Exception:
                        pass
                    self._effect_fx_handles.pop(name, None)
                continue

            if not handle:
                try:
                    handle = self.bass_dll.BASS_ChannelSetFX(
                        self.bass_stream_handle, fx_type, 0
                    )
                except Exception:
                    continue
                if handle:
                    # Sem BASS_FXSetParameters: os padrões do DirectX
                    # já soam bem pra esses efeitos.
                    self._effect_fx_handles[name] = handle

    def _apply_vst_to_current_stream(self):
        """(Re)carrega os plugins VST configurados (os marcados como
        ligados) no stream atual da BASS e reaplica os parâmetros
        salvos de cada um.

        IMPORTANTE: plugins VST valem SÓ para arquivos locais, nunca
        para rádios (cada rádio já tem o próprio processamento). Essa
        regra fica aqui dentro de propósito, e não em quem chama - a
        função é chamada de vários lugares (início de faixa, marcar/
        desmarcar, adicionar, remover), e proteger só alguns deles
        deixava brecha pra aplicar numa rádio sem querer.

        Sempre remove as instâncias anteriores primeiro - sem isso,
        chamar esse método mais de uma vez (ex.: usuário adiciona um
        segundo plugin) empilhava cópias do mesmo plugin tocando ao
        mesmo tempo, sem nunca tirar as antigas."""
        if self.vst_dll is not None and self.bass_stream_handle:
            for old_handle in self.vst_handles:
                if old_handle:
                    try:
                        self.vst_dll.BASS_VST_ChannelRemoveDSP(
                            self.bass_stream_handle, old_handle
                        )
                    except Exception:
                        pass

        self.vst_handles = [0] * len(self.vst_plugins)
        if not self.bass_stream_handle or self.vst_dll is None:
            return
        if self.is_stream:
            # Rádio tocando: sai aqui, depois de já ter removido
            # qualquer plugin que estivesse ativo.
            return

        for i, plugin in enumerate(self.vst_plugins):
            if not plugin.get("enabled", True):
                continue
            path = plugin.get("path", "")
            if not path or not os.path.exists(path):
                continue

            try:
                handle = self.vst_dll.BASS_VST_ChannelSetDSP(
                    self.bass_stream_handle, path, BASS_UNICODE, 0
                )
            except Exception:
                handle = 0
            if not handle:
                continue

            self.vst_handles[i] = handle
            try:
                count = self.vst_dll.BASS_VST_GetParamCount(handle)
                params = plugin.get("params") or {}
                for pidx in range(count):
                    key = str(pidx)
                    if key in params:
                        self.vst_dll.BASS_VST_SetParam(handle, pidx, float(params[key]))
            except Exception:
                pass

    def _save_vst_settings(self):
        self.settings["vst_plugins"] = [
            {
                "path": p.get("path", ""),
                "enabled": bool(p.get("enabled", True)),
                "params": dict(p.get("params") or {}),
            }
            for p in self.vst_plugins
        ]
        save_settings(self.settings)

    def _show_equalizer(self):
        dlg = EqualizerDialog(self, self)
        dlg.ShowModal()
        dlg.Destroy()

    def _open_resolved_stream_wmf(self, original_url, resolved_url, expected_index):
        """Caminho de reserva: Windows abrindo a conexão HTTPS sozinho,
        usado só quando a BASS não está disponível."""
        if self.current_index != expected_index or not self.is_stream:
            return
        try:
            source = MediaSource.create_from_uri(Uri(resolved_url))
        except Exception:
            try:
                source = MediaSource.create_from_uri(Uri(original_url))
            except Exception:
                self.SetStatusText("Não foi possível abrir esse stream.")
                speak("Não foi possível abrir esse stream.")
                return

        try:
            self.player.pause()
        except Exception:
            pass

        self.player.source = source
        self.player.volume = self.volume_level

        self.icy_reader = IcyMetadataReader(
            resolved_url, self._on_icy_meta, initial_delay=self.icy_initial_delay
        )
        self.icy_reader.start()

        if self.stream_play_delay_ms > 0:
            self._stream_play_timer = wx.CallLater(
                self.stream_play_delay_ms, self._begin_stream_playback, expected_index
            )
        else:
            self.player.play()

    def _begin_stream_playback(self, expected_index):
        self._stream_play_timer = None
        # Confere se o usuário não pulou pra outra faixa durante a espera
        if self.current_index == expected_index and self.is_stream:
            self.player.play()

    def _on_buffering_started(self, sender, args):
        wx.CallAfter(self._handle_buffering_started)

    def _handle_buffering_started(self):
        if self.is_stream:
            self.SetStatusText("Bufferizando...")

    def _on_buffering_ended(self, sender, args):
        wx.CallAfter(self._handle_buffering_ended)

    def _handle_buffering_ended(self):
        if self.is_stream and self.current_index != -1:
            self.SetStatusText("Reproduzindo.")

    def _on_media_failed(self, sender, args):
        # Evento do WinRT chega em outra thread; repassa pra thread da UI
        wx.CallAfter(self._handle_media_failed, args)

    @staticmethod
    def _describe_media_error(args):
        """Traduz o erro do Windows Media Foundation para texto
        compreensível, usando o código numérico oficial do erro (mais
        confiável) e complementando com error_message quando disponível
        (esse campo costuma vir vazio na maioria dos casos)."""
        code = None
        try:
            code = int(args.error)
        except Exception:
            pass

        if code is not None:
            description = MEDIA_ERROR_MESSAGES.get(code, f"código de erro {code}")
        else:
            description = "motivo desconhecido"

        try:
            extra = args.error_message
        except Exception:
            extra = None
        if extra:
            description += f" ({extra})"

        return description

    @staticmethod
    def _diagnose_local_file(path):
        """Usa o mutagen para investigar tecnicamente um arquivo que o
        Windows recusou tocar (formato, layer do MP3, taxa de
        amostragem, etc). Isso ajuda a distinguir 'arquivo corrompido'
        de 'formato realmente incomum' - informação que o próprio
        Windows não entrega."""
        if not _HAS_MUTAGEN:
            return None
        try:
            audio = mutagen.File(path)
        except Exception as e:
            return f"o mutagen também não conseguiu ler o arquivo ({e}) - provavelmente corrompido ou incompleto"

        if audio is None:
            return ("o mutagen não reconheceu nenhum formato de áudio nesse "
                    "arquivo - provavelmente corrompido, incompleto, ou não é "
                    "realmente um arquivo de áudio apesar da extensão")

        info = audio.info
        parts = [type(audio).__name__]
        for attr, label, fmt in (
            ("version", "MPEG", lambda v: f"v{v}"),
            ("layer", "layer", lambda v: f"layer {v}"),
            ("bitrate", "taxa", lambda v: f"{v // 1000}kbps"),
            ("sample_rate", "amostragem", lambda v: f"{v}Hz"),
            ("channels", "canais", lambda v: f"{v}ch"),
            ("mode", "modo", lambda v: str(v)),
        ):
            value = getattr(info, attr, None)
            if value is not None:
                try:
                    parts.append(fmt(value))
                except Exception:
                    parts.append(f"{label}={value}")

        return ", ".join(str(p) for p in parts)

    def _handle_media_failed(self, args):
        """Chamado quando o Windows Media Foundation não consegue abrir
        ou decodificar a faixa atual (arquivo corrompido, codec não
        suportado, arquivo inacessível, etc). Mostra E FALA o motivo
        real em vez de ficar em silêncio, tenta diagnosticar tecnicamente
        o arquivo, e pula pra próxima faixa pra não travar a playlist."""
        if not (0 <= self.current_index < len(self.playlist)):
            return

        path = self.playlist[self.current_index]
        name = os.path.basename(path) if not self.is_stream else path
        reason = self._describe_media_error(args)

        msg = f'Falha ao reproduzir "{name}": {reason}'
        speech = f"Não foi possível reproduzir {name}. {reason}."

        if not self.is_stream:
            diagnosis = self._diagnose_local_file(path)
            if diagnosis:
                msg += f" | Diagnóstico técnico: {diagnosis}"
                speech += f" Diagnóstico técnico: {diagnosis}."

        self.SetStatusText(msg)
        speak(speech)

        # Pula automaticamente pra não travar a lista, respeitando
        # repetição/aleatório como se a faixa tivesse terminado.
        self._advance_after_track_end()

    def _load_local_metadata(self, path, fallback_name):
        if not _HAS_MUTAGEN:
            self._set_now_playing(fallback_name, fallback_name)
            self._set_cover_image(None)
            return
        try:
            audio = mutagen.File(path, easy=True)
            title = artist = album = None
            if audio is not None and audio.tags:
                title = (audio.tags.get("title") or [None])[0]
                artist = (audio.tags.get("artist") or [None])[0]
                album = (audio.tags.get("album") or [None])[0]
        except Exception:
            title = artist = album = None

        if artist and title:
            titlebar = f"{artist} - {title}"
        elif title:
            titlebar = title
        else:
            titlebar = fallback_name

        label_parts = [titlebar] if (artist or title) else [fallback_name]
        if album:
            label_parts.append(f"Álbum: {album}")
        label = " | ".join(label_parts)

        self._set_now_playing(titlebar, label)
        self._set_cover_image(extract_embedded_cover_bytes(path))

    def _on_icy_meta(self, kind, text):
        if kind == "station":
            self.stream_station_name = text
            self._set_now_playing(text, f"Rádio: {text}")
        else:  # "title"
            station = self.stream_station_name
            label = text + (f" | Rádio: {station}" if station else "")
            self._set_now_playing(text, label)

    def _set_now_playing(self, titlebar_text, label_text):
        """Atualiza o TÍTULO da janela (padrão Winamp: 'conteúdo -
        LS AudioPlayer', lido pelo Alt+Tab / revisão do leitor de tela) e a
        barra de status. Não fala em voz alta automaticamente - só o
        que o usuário pede diretamente (play/pausa/volume/etc.) é
        anunciado por voz."""
        self.SetTitle(f"{titlebar_text} - {APP_TITLE}")
        if label_text != self.last_meta_string:
            self.last_meta_string = label_text
            self.SetStatusText(label_text)

    def _stop_icy_reader(self):
        if self.icy_reader is not None:
            self.icy_reader.stop()
            self.icy_reader = None

    def _toggle_play(self):
        if self.current_index == -1:
            if self.playlist:
                self._play_index(0)
            else:
                speak("Nenhuma faixa na lista.")
            return

        if self.bass_stream_handle:
            state = self.bass_dll.BASS_ChannelIsActive(self.bass_stream_handle)
            if state == BASS_ACTIVE_PLAYING:
                self.bass_dll.BASS_ChannelPause(self.bass_stream_handle)
                self.SetStatusText("Pausado.")
                speak("Pausado")
            else:
                self.bass_dll.BASS_ChannelPlay(self.bass_stream_handle, False)
                self.SetStatusText("Reproduzindo.")
                speak("Reproduzindo")
            return

        state = self.player.playback_session.playback_state
        if state == MediaPlaybackState.PLAYING:
            self.player.pause()
            self.SetStatusText("Pausado.")
            speak("Pausado")
        else:
            self.player.play()
            self.SetStatusText("Reproduzindo.")
            speak("Reproduzindo")

    def _stop(self):
        self._stop_icy_reader()
        self._stop_bass_stream()
        if self._stream_play_timer is not None:
            self._stream_play_timer.Stop()
            self._stream_play_timer = None
        self.player.pause()
        try:
            self.player.playback_session.position = timedelta(0)
        except Exception:
            pass
        self.SetStatusText("Parado.")
        speak("Parado")

    def _rebuild_shuffle_order(self):
        """Embaralha a lista inteira de uma vez (tipo embaralhar um
        baralho), em vez de sortear uma faixa qualquer a cada troca.
        Assim todas as músicas tocam antes de qualquer uma repetir, e
        a ordem é diferente a cada volta - o sorteio individual antigo
        repetia faixas e parecia ter sequência."""
        self._shuffle_order = list(range(len(self.playlist)))
        random.shuffle(self._shuffle_order)
        # Evita começar a nova volta repetindo a faixa que acabou de
        # tocar (embaralhar de novo pode deixá-la em primeiro).
        if (len(self._shuffle_order) > 1
                and self._shuffle_order[0] == self.current_index):
            self._shuffle_order.append(self._shuffle_order.pop(0))
        self._shuffle_position = -1

    def _next_shuffled_index(self):
        """Devolve a próxima faixa da ordem embaralhada, reembaralhando
        quando a volta termina."""
        if len(self._shuffle_order) != len(self.playlist):
            self._rebuild_shuffle_order()

        self._shuffle_position += 1
        if self._shuffle_position >= len(self._shuffle_order):
            self._rebuild_shuffle_order()
            self._shuffle_position = 0
            speak("Reembaralhando a lista.")

        return self._shuffle_order[self._shuffle_position]

    def _play_from(self, start_index):
        """Começa a tocar a partir de start_index - mas se o modo
        aleatório estiver ligado, sorteia a primeira faixa em vez de
        pegar sempre a primeira da lista (que, ordenada por nome,
        acabava sendo sempre a mesma música)."""
        if self.shuffle_mode and len(self.playlist) > 1:
            self._rebuild_shuffle_order()
            self._play_index(self._next_shuffled_index())
            return
        self._play_index(start_index)

    def _next_track(self, manual=False):
        if self.current_favorite_index is not None and self.is_stream:
            self._play_favorite_by_index(self.current_favorite_index + 1)
            return

        if not self.playlist:
            speak("Lista vazia.")
            return

        if self.shuffle_mode and len(self.playlist) > 1:
            next_idx = self._next_shuffled_index()
        else:
            next_idx = self.current_index + 1
            if next_idx >= len(self.playlist):
                speak("Reiniciando a lista.")
                next_idx = 0

        self._play_index(next_idx)

    def _prev_track(self):
        if self.current_favorite_index is not None and self.is_stream:
            self._play_favorite_by_index(self.current_favorite_index - 1)
            return

        if not self.playlist:
            speak("Lista vazia.")
            return
        prev_idx = self.current_index - 1
        if prev_idx < 0:
            speak("Início da lista.")
            prev_idx = len(self.playlist) - 1
        self._play_index(prev_idx)

    def _go_to_first_track(self):
        # Se estiver ouvindo uma rádio, "X" reinicia a conexão dela
        # (útil quando a transmissão trava ou fica ruim) em vez de
        # pular pra primeira faixa da lista.
        if self.is_stream and self.current_index != -1:
            msg = "Reconectando à rádio..."
            self.SetStatusText(msg)
            speak(msg)
            fav_idx = self.current_favorite_index
            self._play_index(self.current_index)
            if fav_idx is not None:
                self.current_favorite_index = fav_idx
            return

        if not self.playlist:
            speak("Lista vazia.")
            return
        self._play_index(0)

    def _go_to_last_track(self):
        if not self.playlist:
            speak("Lista vazia.")
            return
        self._play_index(len(self.playlist) - 1)

    def _on_media_ended(self, sender, args):
        wx.CallAfter(self._advance_after_track_end)

    def _advance_after_track_end(self):
        if self.current_favorite_index is not None and self.is_stream:
            self._next_track()
            return
        if not self.playlist:
            return
        if self.shuffle_mode:
            self._next_track()
            return
        is_last = self.current_index >= len(self.playlist) - 1
        if is_last and not self.repeat_mode:
            self._stop()
            msg = "Fim da lista."
            self.SetStatusText(msg)
            speak(msg)
            return
        self._next_track()

    # ------------------------------------------------------------------
    # Volume e navegação (seek)
    # ------------------------------------------------------------------
    def _change_volume(self, delta):
        new_vol = max(0.0, min(1.0, self.volume_level + delta))
        self.volume_level = new_vol
        if self.bass_stream_handle:
            self.bass_dll.BASS_ChannelSetAttribute(
                self.bass_stream_handle, BASS_ATTRIB_VOL, ctypes.c_float(new_vol)
            )
        else:
            self.player.volume = new_vol
        msg = f"Volume: {int(round(new_vol * 100))}%"
        self.SetStatusText(msg)

    def _seek(self, delta):
        if self.is_stream:
            speak("Não é possível avançar/retroceder em um stream ao vivo.")
            return

        # Arquivo local tocando pela BASS
        if self.bass_stream_handle:
            try:
                length_bytes = self.bass_dll.BASS_ChannelGetLength(
                    self.bass_stream_handle, BASS_POS_BYTE)
                pos_bytes = self.bass_dll.BASS_ChannelGetPosition(
                    self.bass_stream_handle, BASS_POS_BYTE)
                total = self.bass_dll.BASS_ChannelBytes2Seconds(
                    self.bass_stream_handle, length_bytes)
                current = self.bass_dll.BASS_ChannelBytes2Seconds(
                    self.bass_stream_handle, pos_bytes)
            except Exception:
                return
            if total <= 0:
                return
            new_seconds = max(0.0, min(total, current + delta.total_seconds()))
            try:
                new_bytes = self.bass_dll.BASS_ChannelSeconds2Bytes(
                    self.bass_stream_handle, new_seconds)
                self.bass_dll.BASS_ChannelSetPosition(
                    self.bass_stream_handle, new_bytes, BASS_POS_BYTE)
            except Exception:
                return
            secs = int(new_seconds)
            self.SetStatusText(f"Posição: {secs // 60}:{secs % 60:02d}")
            return

        session = self.player.playback_session
        try:
            duration = session.natural_duration
            current = session.position
        except Exception:
            return
        if duration is None or duration.total_seconds() <= 0:
            return
        new_pos = current + delta
        new_pos = max(timedelta(0), min(duration, new_pos))
        session.position = new_pos
        secs = int(new_pos.total_seconds())
        msg = f"Posição: {secs // 60}:{secs % 60:02d}"
        self.SetStatusText(msg)

    def _seek_to_start(self):
        if self.is_stream:
            speak("Não é possível reiniciar um stream ao vivo.")
            return
        if self.current_index == -1:
            speak("Nenhuma faixa tocando.")
            return

        if self.bass_stream_handle:
            try:
                self.bass_dll.BASS_ChannelSetPosition(
                    self.bass_stream_handle, 0, BASS_POS_BYTE)
            except Exception:
                return
        else:
            try:
                self.player.playback_session.position = timedelta(0)
            except Exception:
                return

        msg = "Início da faixa."
        self.SetStatusText(msg)
        speak(msg)

    def _seek_to_end(self):
        if self.is_stream:
            speak("Não é possível pular pro fim de um stream ao vivo.")
            return
        if self.current_index == -1:
            speak("Nenhuma faixa tocando.")
            return

        # Fica 1 segundo antes do fim de verdade, pra não disparar
        # "faixa terminou" imediatamente ao chegar lá.
        margin = timedelta(seconds=1)

        if self.bass_stream_handle:
            try:
                length_bytes = self.bass_dll.BASS_ChannelGetLength(
                    self.bass_stream_handle, BASS_POS_BYTE)
                total = self.bass_dll.BASS_ChannelBytes2Seconds(
                    self.bass_stream_handle, length_bytes)
            except Exception:
                return
            if total <= 0:
                return
            new_seconds = max(0.0, total - margin.total_seconds())
            try:
                new_bytes = self.bass_dll.BASS_ChannelSeconds2Bytes(
                    self.bass_stream_handle, new_seconds)
                self.bass_dll.BASS_ChannelSetPosition(
                    self.bass_stream_handle, new_bytes, BASS_POS_BYTE)
            except Exception:
                return
        else:
            try:
                duration = self.player.playback_session.natural_duration
            except Exception:
                return
            if duration is None or duration.total_seconds() <= 0:
                return
            new_pos = max(timedelta(0), duration - margin)
            try:
                self.player.playback_session.position = new_pos
            except Exception:
                return

        msg = "Fim da faixa."
        self.SetStatusText(msg)
        speak(msg)

    # ------------------------------------------------------------------
    # Timer de atualização da barra de status (tempo decorrido)
    # ------------------------------------------------------------------
    def _on_timer(self, event):
        if self.current_index == -1:
            return

        if self.is_stream:
            self._poll_bass_status()
            return

        # Arquivo local tocando pela BASS
        if self.bass_stream_handle:
            try:
                state = self.bass_dll.BASS_ChannelIsActive(self.bass_stream_handle)
                if state == BASS_ACTIVE_STOPPED:
                    # Faixa terminou: avança sozinho pra próxima
                    if time.time() - self._bass_stream_started_at > 1:
                        self._stop_bass_stream()
                        wx.CallAfter(self._advance_after_track_end)
                    return
                if state != BASS_ACTIVE_PLAYING:
                    return
                length_bytes = self.bass_dll.BASS_ChannelGetLength(
                    self.bass_stream_handle, BASS_POS_BYTE)
                pos_bytes = self.bass_dll.BASS_ChannelGetPosition(
                    self.bass_stream_handle, BASS_POS_BYTE)
                total = self.bass_dll.BASS_ChannelBytes2Seconds(
                    self.bass_stream_handle, length_bytes)
                current = self.bass_dll.BASS_ChannelBytes2Seconds(
                    self.bass_stream_handle, pos_bytes)
            except Exception:
                return
            if total > 0:
                cur_s, tot_s = int(current), int(total)
                name = os.path.basename(self.playlist[self.current_index])
                self.SetStatusText(
                    f"{name} - {cur_s // 60}:{cur_s % 60:02d} / {tot_s // 60}:{tot_s % 60:02d}"
                )
            return

        try:
            session = self.player.playback_session
            if session.playback_state != MediaPlaybackState.PLAYING:
                return
            duration = session.natural_duration
            current = session.position
        except Exception:
            return

        if duration and duration.total_seconds() > 0:
            cur_s = int(current.total_seconds())
            tot_s = int(duration.total_seconds())
            name = os.path.basename(self.playlist[self.current_index])
            self.SetStatusText(
                f"{name} - {cur_s // 60}:{cur_s % 60:02d} / {tot_s // 60}:{tot_s % 60:02d}"
            )

    def _poll_bass_status(self):
        """Acompanha o estado do stream tocado via BASS: mostra
        'Bufferizando...' quando ela está rebufferizando, avança pra
        próxima faixa se a conexão cair sozinha (ex.: rádio saiu do ar),
        e atualiza o nome da música lendo o metadado direto da BASS
        (sem nenhuma conexão extra - ela já separa isso sozinha)."""
        if not self.bass_stream_handle:
            return
        try:
            state = self.bass_dll.BASS_ChannelIsActive(self.bass_stream_handle)
        except Exception:
            return

        if state == BASS_ACTIVE_STALLED:
            self.SetStatusText("Bufferizando...")
        elif state == BASS_ACTIVE_STOPPED:
            # Só considera "caiu de verdade" depois de alguns segundos
            # desde que começou - evita falso positivo bem no início,
            # antes do primeiro áudio realmente chegar.
            if time.time() - self._bass_stream_started_at > 5:
                self._stop_bass_stream()
                wx.CallAfter(self._advance_after_track_end)
                return

        try:
            raw = self.bass_dll.BASS_ChannelGetTags(self.bass_stream_handle, BASS_TAG_META)
        except Exception:
            raw = None
        if raw:
            text = _decode_icy_text(raw)
            match = re.search(r"StreamTitle='([^']*)'", text)
            if match:
                title = match.group(1).strip()
                if title and title != self._bass_last_meta_title:
                    self._bass_last_meta_title = title
                    station = self.stream_station_name
                    label = title + (f" | Rádio: {station}" if station else "")
                    self._set_now_playing(title, label)

    # ------------------------------------------------------------------
    # Diálogos de ajuda
    # ------------------------------------------------------------------
    def _show_shortcuts(self):
        dlg = ShortcutsDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def _open_data_folder(self):
        """Abre no Explorer a pasta onde ficam os favoritos, as
        configurações e o log de diagnóstico (argv_debug.log) -
        útil pra achar rápido esses arquivos quando precisar."""
        try:
            os.makedirs(FAVORITES_DIR, exist_ok=True)
            os.startfile(FAVORITES_DIR)
        except Exception as e:
            wx.MessageBox(
                f"Não foi possível abrir a pasta:\n{FAVORITES_DIR}\n\n{e}",
                "Erro", wx.OK | wx.ICON_ERROR
            )

    def _show_about(self):
        text = (
            f"{APP_TITLE}\n"
            f"Versão {APP_VERSION}\n\n"
            "Um player de áudio acessível, no estilo Winamp clássico: "
            "rádios pela internet sem cortes, equalizador e efeitos, "
            "suporte a plugins VST, metadados ao vivo e atalhos de "
            "teclado diretos.\n\n"
            "Motor de áudio: BASS (www.un4seen.com), gratuita para uso "
            "não-comercial.\n"
            "Suporte a plugins VST: BASS_VST by Bjoern Petersen for "
            "Silverjuke.net - VST PlugIn Technology by Steinberg Media "
            "Technologies GmbH."
        )
        wx.MessageBox(text, f"Sobre o {APP_TITLE}", wx.OK | wx.ICON_INFORMATION)

    def _on_close(self, event):
        # Guarda o volume atual, pra abrir na mesma altura da última vez.
        # Também força salvar os plugins VST agora - o ajuste de
        # parâmetros espera meio segundo de silêncio antes de gravar
        # (pra não travar mexendo rápido), e se o programa fechar antes
        # desse meio segundo passar, essa gravação agendada nunca roda.
        # Isso garante que o último estado sempre seja salvo de verdade.
        try:
            self.settings["volume_level"] = self.volume_level
            save_settings(self.settings)
            self._save_vst_settings()
        except Exception:
            pass

        self.timer.Stop()
        self._stop_icy_reader()
        self._stop_bass_stream()
        if self.bass_dll is not None:
            try:
                self.bass_dll.BASS_Free()
            except Exception:
                pass
        if self._stream_play_timer is not None:
            self._stream_play_timer.Stop()
            self._stream_play_timer = None
        try:
            self.player.pause()
            self.player.close()
        except Exception:
            pass
        self.Destroy()


SINGLE_INSTANCE_MUTEX_NAME = "Global\\LSAudioPlayer_SingleInstance_Mutex"
ERROR_ALREADY_EXISTS = 183


def acquire_single_instance_lock():
    """Cria um mutex nomeado do Windows. Se já existir (outra instância
    já está rodando), devolve already_running=True - nesse caso, o
    handle ainda é criado (aponta pro mutex existente) e deve ser
    fechado sem soltar o programa (a instância já rodando é quem
    "possui" o mutex de verdade)."""
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, SINGLE_INSTANCE_MUTEX_NAME)
    last_error = ctypes.windll.kernel32.GetLastError()
    already_running = (last_error == ERROR_ALREADY_EXISTS)
    return mutex, already_running


class LSAudioPlayerApp(wx.App):
    def OnInit(self):
        frame = LSAudioPlayerFrame()
        self.SetTopWindow(frame)
        return True


def log_argv_diagnostic(argv):
    """Grava os argumentos de linha de comando recebidos (repr() bruto,
    revelando caracteres estranhos/mal codificados) num arquivo de log
    persistente - útil pra diagnosticar problemas de codificação quando
    outro programa (ex.: DOSVOX) abre o LS AudioPlayer passando um
    caminho de arquivo/pasta como argumento. Sem isso, mensagens de
    erro na tela passam rápido demais pra copiar."""
    try:
        os.makedirs(FAVORITES_DIR, exist_ok=True)
        log_path = os.path.join(FAVORITES_DIR, "argv_debug.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(f"Quantidade de argumentos recebidos: {len(argv)}\n")
            for i, arg in enumerate(argv):
                f.write(f"argv[{i}] = {arg!r}\n")
        # Mantém o log num tamanho razoável, sem crescer pra sempre
        if os.path.getsize(log_path) > 200_000:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(content[-100_000:])
    except Exception:
        pass


if __name__ == "__main__":
    # Verifica se já tem outra instância rodando (a menos que o usuário
    # tenha marcado "Permitir mais de uma instância" nas Preferências).
    # Precisamos ler essa configuração diretamente do disco aqui, antes
    # de criar a janela - por isso não passa pelo self.settings normal.
    _startup_settings = load_settings()
    _allow_multiple = bool(_startup_settings.get("allow_multiple_instances", False))

    if bool(_startup_settings.get("enable_argv_log", False)):
        log_argv_diagnostic(sys.argv)

    _mutex_handle = None
    if not _allow_multiple:
        _mutex_handle, _already_running = acquire_single_instance_lock()
        if _already_running:
            try:
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "O LS AudioPlayer já está aberto.\n\n"
                    "Verifique a barra de tarefas, ou ative \"Permitir mais "
                    "de uma instância\" nas Preferências se quiser abrir "
                    "várias janelas.",
                    "LS AudioPlayer",
                    0x40,  # MB_ICONINFORMATION
                )
            except Exception:
                pass
            sys.exit(0)

    app = LSAudioPlayerApp(False)

    # Suporte a "Reproduzir com LS AudioPlayer" no menu de contexto do
    # Windows: quando o Windows chama o programa passando o caminho
    # do arquivo como argumento, tocamos ele imediatamente.
    if len(sys.argv) > 1:
        path_arg = sys.argv[1]
        frame = app.GetTopWindow()
        if os.path.isdir(path_arg):
            wx.CallAfter(frame.open_folder_and_play, path_arg)
        else:
            wx.CallAfter(frame.open_path_and_play, path_arg)

    app.MainLoop()

    if _mutex_handle:
        try:
            ctypes.windll.kernel32.CloseHandle(_mutex_handle)
        except Exception:
            pass
