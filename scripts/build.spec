# -*- mode: python -*-
a = Analysis(['../src/rtkgers.py'],
             pathex=['../src'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='rtkgers',
          debug=False,
          strip=None,
          upx=True,
          console=True )
