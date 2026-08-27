#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
limpar_registros.py - Faxina no registro do Windows
=====================================================
Remove entradas antigas e duplicadas do LS AudioPlayer (e da versão
antiga, "LSWPlayer") que ficaram no registro do Windows e continuam
aparecendo em "Abrir com" e "Aplicativos padrão".

Isso acontece porque:
  - A primeira versão do programa se chamava LSWPlayer. Ao renomear
    para LS AudioPlayer, as chaves antigas continuaram lá.
  - O registro pode ter sido feito mais de uma vez (pelo menu Ajuda
    do programa E pelo instalador), criando entradas repetidas.

Este script mexe SOMENTE no registro do seu usuário
(HKEY_CURRENT_USER), nas chaves criadas por estes programas. Não
precisa ser administrador e não afeta nenhum outro programa.

Uso:
    Dê dois cliques em limpar_registros.bat
    (ou rode: python limpar_registros.py)

Depois de limpar, se quiser o LS AudioPlayer de volta no menu de
contexto, use: Ajuda > Adicionar ao menu de contexto do Windows.
"""

import sys

if sys.platform != "win32":
    print("Este script só funciona no Windows.")
    sys.exit(1)

import winreg

# Todos os nomes internos já usados pelo programa, incluindo o antigo
VERB_NAMES = ["LSWPlayer", "LSAudioPlayer"]
PROGIDS = ["LSWPlayer.AudioFile", "LSAudioPlayer.AudioFile"]
CAPABILITY_KEYS = ["Software\\LSWPlayer", "Software\\LSAudioPlayer"]
REGISTERED_APP_NAMES = ["LSWPlayer", "LS AudioPlayer", "LSAudioPlayer"]

EXTENSIONS = [".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma",
              ".m3u", ".m3u8", ".pls"]

# Usado pra reconhecer o programa nas listas do Explorer (item 6), onde
# o nome pode aparecer como "LS AudioPlayer.exe", "LSWPlayer.exe", o
# ProgID, etc. - compara de forma solta (sem espaço, minúsculo).
TARGET_SUBSTRINGS = ["lswplayer", "lsaudioplayer"]


def _normalize(s):
    return s.lower().replace(" ", "")


def _matches_target(text):
    t = _normalize(text)
    return any(alvo in t for alvo in TARGET_SUBSTRINGS)


def delete_key_recursive(root, path):
    """Apaga uma chave do registro e tudo que estiver dentro dela.
    Devolve True se apagou, False se ela não existia."""
    try:
        key = winreg.OpenKey(root, path, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        return False
    except OSError:
        return False

    with key:
        while True:
            try:
                sub = winreg.EnumKey(key, 0)
            except OSError:
                break
            delete_key_recursive(root, f"{path}\\{sub}")

    try:
        winreg.DeleteKey(root, path)
        return True
    except OSError:
        return False


def clean_open_with_list(ext_path):
    """OpenWithList é o histórico de 'Abrir com' do Explorer, guardado
    por extensão - tipo 'a'=vlc.exe, 'b'=LSWPlayer.exe, MRUList=ba.
    NÃO é apagado quando um programa é desinstalado, por isso um
    programa removido ainda aparece na lista."""
    path = f"{ext_path}\\OpenWithList"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_ALL_ACCESS)
    except OSError:
        return 0

    count = 0
    to_delete = []
    with key:
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
            except OSError:
                break
            i += 1
            if name.lower() == "mrulist":
                continue
            if isinstance(value, str) and _matches_target(value):
                to_delete.append(name)

        for name in to_delete:
            try:
                winreg.DeleteValue(key, name)
                count += 1
            except OSError:
                pass

        # Atualiza o MRUList removendo as letras que acabamos de apagar,
        # senão o Explorer pode ficar confuso com letras "órfãs".
        if to_delete:
            try:
                mru, _ = winreg.QueryValueEx(key, "MRUList")
                new_mru = "".join(c for c in mru if c not in to_delete)
                winreg.SetValueEx(key, "MRUList", 0, winreg.REG_SZ, new_mru)
            except OSError:
                pass
    return count


def clean_open_with_progids(ext_path):
    """Lista separada de tipos (ProgIDs) associados via 'Abrir com'."""
    path = f"{ext_path}\\OpenWithProgids"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_ALL_ACCESS)
    except OSError:
        return 0

    count = 0
    to_delete = []
    with key:
        i = 0
        while True:
            try:
                name, _value, _ = winreg.EnumValue(key, i)
            except OSError:
                break
            i += 1
            if _matches_target(name):
                to_delete.append(name)

        for name in to_delete:
            try:
                winreg.DeleteValue(key, name)
                count += 1
            except OSError:
                pass
    return count


def clean_user_choice(ext_path):
    """UserChoice é o 'programa padrão atual' daquela extensão. Só
    apaga se for realmente o nosso programa - assim, se você já tiver
    escolhido outro player como padrão para algo, isso não é mexido."""
    path = f"{ext_path}\\UserChoice"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        with key:
            progid, _ = winreg.QueryValueEx(key, "ProgId")
    except OSError:
        return 0

    if not _matches_target(progid):
        return 0

    # Protegida por hash em versões recentes do Windows - apagar
    # costuma funcionar (é só remover uma preferência), mas se falhar
    # não é grave: o Windows só vai pedir pra escolher de novo.
    if delete_key_recursive(winreg.HKEY_CURRENT_USER, path):
        return 1
    return 0


def clean_explorer_file_exts():
    """Limpa o histórico próprio do Explorer (FileExts) - é aqui que
    ficam as entradas 'fantasma' de programas já desinstalados, e é
    onde duplicatas de 'Abrir com'/'Definir padrão' realmente moram.
    Essa área é separada do resto do registro que limpamos acima."""
    base = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts"
    total = 0
    for ext in EXTENSIONS:
        ext_path = f"{base}\\{ext}"
        total += clean_open_with_list(ext_path)
        total += clean_open_with_progids(ext_path)
        total += clean_user_choice(ext_path)
    return total


def main():
    print("=" * 62)
    print(" Faxina no registro - LS AudioPlayer")
    print("=" * 62)
    print()
    print("Isto vai remover TODAS as entradas do LS AudioPlayer (e do")
    print("antigo LSWPlayer) do menu de contexto e da lista de")
    print("aplicativos padrao do Windows.")
    print()
    print("Depois, se quiser, voce pode registrar de novo pelo menu")
    print("Ajuda do programa - dessa vez sem duplicatas.")
    print()
    resposta = input("Deseja continuar? (S/N): ").strip().lower()
    if resposta != "s":
        print("\nCancelado. Nada foi alterado.")
        input("Pressione Enter para sair...")
        return

    print()
    total = 0

    # 1) Menu de contexto em arquivos de audio
    print("--- Menu de contexto (arquivos) ---")
    for verb in VERB_NAMES:
        for ext in EXTENSIONS:
            path = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{verb}"
            if delete_key_recursive(winreg.HKEY_CURRENT_USER, path):
                print(f"  removido: {verb} em {ext}")
                total += 1

    # 2) Menu de contexto em pastas
    print("--- Menu de contexto (pastas) ---")
    for verb in VERB_NAMES:
        path = f"Software\\Classes\\Directory\\shell\\{verb}"
        if delete_key_recursive(winreg.HKEY_CURRENT_USER, path):
            print(f"  removido: {verb} em pastas")
            total += 1

    # 3) ProgIDs (tipo de arquivo registrado pelo programa)
    print("--- Tipos de arquivo registrados ---")
    for progid in PROGIDS:
        path = f"Software\\Classes\\{progid}"
        if delete_key_recursive(winreg.HKEY_CURRENT_USER, path):
            print(f"  removido: {progid}")
            total += 1

    # 4) Capabilities (o que faz aparecer em "Aplicativos padrao")
    print("--- Registro de aplicativo padrao ---")
    for cap in CAPABILITY_KEYS:
        if delete_key_recursive(winreg.HKEY_CURRENT_USER, cap):
            print(f"  removido: {cap}")
            total += 1

    # 5) RegisteredApplications - apaga so os NOSSOS valores,
    #    preservando os de outros programas
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\RegisteredApplications",
            0, winreg.KEY_ALL_ACCESS
        )
        with key:
            for name in REGISTERED_APP_NAMES:
                try:
                    winreg.DeleteValue(key, name)
                    print(f"  removido da lista de aplicativos: {name}")
                    total += 1
                except FileNotFoundError:
                    pass
                except OSError:
                    pass
    except FileNotFoundError:
        pass
    except OSError:
        pass

    # 6) Entradas em "Abrir com" (OpenWithProgids / OpenWithList)
    print("--- Entradas de 'Abrir com' ---")
    for ext in EXTENSIONS:
        for sub in ("OpenWithProgids", "OpenWithList"):
            path = (f"Software\\Classes\\SystemFileAssociations\\{ext}\\{sub}")
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0,
                                      winreg.KEY_ALL_ACCESS)
            except (FileNotFoundError, OSError):
                continue
            with key:
                for progid in PROGIDS + ["LS AudioPlayer.exe", "LSWPlayer.exe",
                                          "LS AudioPlayer_debug.exe"]:
                    try:
                        winreg.DeleteValue(key, progid)
                        print(f"  removido: {progid} de {ext}")
                        total += 1
                    except (FileNotFoundError, OSError):
                        pass

        # Tambem na chave direta da extensao
        path2 = f"Software\\Classes\\{ext}\\OpenWithProgids"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path2, 0,
                                  winreg.KEY_ALL_ACCESS)
        except (FileNotFoundError, OSError):
            continue
        with key:
            for progid in PROGIDS:
                try:
                    winreg.DeleteValue(key, progid)
                    print(f"  removido: {progid} de {ext}")
                    total += 1
                except (FileNotFoundError, OSError):
                    pass

    # 7) O lugar que realmente importa: o histórico próprio do
    #    Explorer (FileExts). É aqui que ficam entradas de programas
    #    já desinstalados, e duplicatas de verdade em "Abrir com" e
    #    "Definir padrão" - separado de tudo que limpamos acima.
    print("--- Histórico do Explorer (a causa mais provável) ---")
    antes = total
    total += clean_explorer_file_exts()
    if total > antes:
        print(f"  {total - antes} entrada(s) removida(s) do histórico do Explorer")
    else:
        print("  nada encontrado aqui")

    print()
    print("=" * 62)
    if total:
        print(f" Pronto! {total} entrada(s) removida(s).")
        print()
        print(" IMPORTANTE: reinicie o Windows Explorer para as mudancas")
        print(" aparecerem. O jeito mais simples e reiniciar o computador,")
        print(" ou abrir o Gerenciador de Tarefas, achar 'Explorer' e")
        print(" clicar em 'Reiniciar'.")
    else:
        print(" Nenhuma entrada encontrada - o registro ja estava limpo.")
    print("=" * 62)
    print()
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
