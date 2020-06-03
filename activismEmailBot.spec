# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import copy_metadata

block_cipher = None
extra_file = copy_metadata('google-api-python-client')
extra_file.append(('credentials.json','.'))

a = Analysis(['send.py'],
             pathex=['C:\\Users\\eugen\\Documents\\activism-mail-bot', 'C:\\Users\\eugen\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages'],
             binaries=[],
             datas=extra_file,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='activismEmailBot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
