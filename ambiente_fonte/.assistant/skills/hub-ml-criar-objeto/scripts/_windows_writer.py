"""Primitivas do piloto: somente Windows em volume local NTFS.

Handles sem SHARE_DELETE fixam cada ancestral material até fechar o contexto.
CREATE_NEW nunca abre destino existente. Não é transação nem rollback: um
arquivo vazio/parcial pode sobreviver a falha ou encerramento do processo.
"""
from __future__ import annotations

import ctypes
import os
from pathlib import Path


def _api():
    if os.name != "nt":
        raise ValueError("UNSUPPORTED_HOST: piloto demonstrado somente Windows local NTFS")
    from ctypes import wintypes as w
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, w.LPVOID, w.DWORD, w.DWORD, w.HANDLE]
    k.CreateFileW.restype = w.HANDLE
    k.CloseHandle.argtypes = [w.HANDLE]
    k.CloseHandle.restype = w.BOOL
    k.GetFileInformationByHandle.argtypes = [w.HANDLE, w.LPVOID]
    k.GetFileInformationByHandle.restype = w.BOOL
    k.GetDriveTypeW.argtypes = [w.LPCWSTR]
    k.GetDriveTypeW.restype = w.UINT
    k.GetVolumeInformationW.argtypes = [w.LPCWSTR, w.LPWSTR, w.DWORD, w.LPDWORD, w.LPDWORD, w.LPDWORD, w.LPWSTR, w.DWORD]
    k.GetVolumeInformationW.restype = w.BOOL
    return k


def _information(k, handle):
    from ctypes import wintypes as w
    class Info(ctypes.Structure):
        _fields_ = [("attributes", w.DWORD), ("created", w.FILETIME),
                    ("accessed", w.FILETIME), ("modified", w.FILETIME),
                    ("volume", w.DWORD), ("size_hi", w.DWORD), ("size_lo", w.DWORD),
                    ("links", w.DWORD), ("index_hi", w.DWORD), ("index_lo", w.DWORD)]
    info = Info()
    if not k.GetFileInformationByHandle(handle, ctypes.byref(info)):
        raise ctypes.WinError(ctypes.get_last_error())
    return {"volume": info.volume, "file_id": (info.index_hi << 32) | info.index_lo,
            "attributes": info.attributes, "links": info.links}


def _open(k, path, access, share, disposition, flags):
    handle = k.CreateFileW(str(path), access, share, None, disposition, flags, None)
    if handle == ctypes.c_void_p(-1).value:
        error = ctypes.WinError(ctypes.get_last_error())
        error.filename = str(path)
        raise error
    return handle


class PinnedParent:
    """Mantém nomes ancestrais estáveis no Windows NTFS demonstrado.

    Não suporta UNC, reparse points, junctions ou mountpoints; não depende de
    resolve() seguido de open(). Abre cada componente depois de fixar seu pai.
    """
    def __init__(self, root, relative):
        self.root = Path(os.path.abspath(root))
        self.destination = self.root / relative
        self.handles = []
        self.identities = []
        self.created = False
        self.created_identity = None
        self.k = _api()

    def __enter__(self):
        try:
            anchor = self.root.anchor
            if len(anchor) != 3 or anchor[1:] != ":\\" or self.k.GetDriveTypeW(anchor) != 3:
                raise ValueError("UNSUPPORTED_VOLUME: exige drive local fixo")
            fs = ctypes.create_unicode_buffer(64)
            if not self.k.GetVolumeInformationW(anchor, None, 0, None, None, None, fs, len(fs)):
                raise ctypes.WinError(ctypes.get_last_error())
            if fs.value != "NTFS":
                raise ValueError("UNSUPPORTED_FILESYSTEM: exige NTFS")
            paths = [Path(anchor)]
            for part in self.destination.parent.parts[1:]:
                paths.append(paths[-1] / part)
            for path in paths:
                # READ_ATTRIBUTES sozinho não participa da arbitragem de share:
                # o probe nativo permitiu rename da folha. GENERIC_READ inclui
                # LIST_DIRECTORY e torna a ausência de SHARE_DELETE efetiva.
                handle = _open(self.k, path, 0x80000000, 3, 3, 0x02200000)
                self.handles.append(handle)
                info = _information(self.k, handle)
                if not info["attributes"] & 0x10 or info["attributes"] & 0x400:
                    raise ValueError("UNSUPPORTED_TOPOLOGY: ancestral não é diretório real")
                if self.identities and info["volume"] != self.identities[0]["volume"]:
                    raise ValueError("UNSUPPORTED_VOLUME: cadeia entre volumes")
                self.identities.append({"path": str(path), **info})
            if os.path.lexists(self.destination):
                raise FileExistsError("DESTINATION_ALREADY_EXISTS")
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def create(self):
        """Retorna fd binário read/write de arquivo exclusivamente novo."""
        import msvcrt
        handle = _open(self.k, self.destination, 0xC0000000, 0, 1, 0x00200000)
        # Criação já aconteceu, mesmo se a conversão subsequente falhar.
        self.created = True
        try:
            self.created_identity = _information(self.k, handle)
            # Transferência de ownership: fechar fd fecha HANDLE.
            return msvcrt.open_osfhandle(handle, os.O_BINARY | os.O_RDWR)
        except BaseException:
            self.k.CloseHandle(handle)
            raise

    def __exit__(self, *_):
        for handle in reversed(self.handles):
            self.k.CloseHandle(handle)
        self.handles.clear()
