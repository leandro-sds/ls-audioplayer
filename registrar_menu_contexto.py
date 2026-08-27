#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registrar_menu_contexto.py
============================
Adiciona (ou remove) a opção "Reproduzir com LS AudioPlayer" no menu de
contexto do Windows Explorer, para os formatos de áudio suportados
(.mp3, .wav, .ogg, .flac, .m4a, .aac, .wma).

Uso:
    python registrar_menu_contexto.py            -> registra
    python registrar_menu_contexto.py --remover   -> remove

Este script mexe apenas no registro do USUÁRIO ATUAL
(HKEY_CURRENT_USER\\Software\\Classes\\SystemFileAssociations), então
NÃO precisa rodar como administrador e não afeta outras contas do
Windows nem outros programas já associados a esses arquivos.
"""

import os
import sys

if sys.platform != "win32":
    print("Este script só funciona no Windows.")
    sys.exit(1)

import winreg

APP_NAME = "LS AudioPlayer"
VERB_NAME = "LSAudioPlayer"                # nome interno do verbo no registro
VERB_LABEL = "Reproduzir com LS AudioPlayer"  # texto exibido no menu de contexto

AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"]


def find_exe_path():
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base, "dist", f"{APP_NAME}.exe"),
        os.path.join(base, f"{APP_NAME}.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def register(exe_path):
    command = f'"{exe_path}" "%1"'
    for ext in AUDIO_EXTENSIONS:
        key_path = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{VERB_NAME}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, VERB_LABEL)
        cmd_path = key_path + "\\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
        print(f"Registrado para {ext}")

    print()
    print(f'Pronto! Clique com o botao direito num arquivo de audio e procure')
    print(f'"{VERB_LABEL}" no menu de contexto.')


def _delete_key_recursive(root, path):
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
            _delete_key_recursive(root, f"{path}\\{sub}")
    winreg.DeleteKey(root, path)


def unregister():
    for ext in AUDIO_EXTENSIONS:
        key_path = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{VERB_NAME}"
        _delete_key_recursive(winreg.HKEY_CURRENT_USER, key_path)
        print(f"Removido de {ext}")
    print()
    print("Entradas removidas do menu de contexto.")


def main():
    if "--remover" in sys.argv:
        unregister()
        input("\nPressione Enter para sair...")
        return

    exe_path = find_exe_path()
    if not exe_path:
        print(f"ERRO: nao encontrei {APP_NAME}.exe.")
        print("Coloque este script na mesma pasta do executavel.")
        input("\nPressione Enter para sair...")
        sys.exit(1)

    print(f'Registrando "{VERB_LABEL}" usando: {exe_path}')
    print()
    register(exe_path)
    input("\nPressione Enter para sair...")


if __name__ == "__main__":
    main()
