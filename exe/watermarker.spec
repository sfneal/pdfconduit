# -*- mode: python -*-

block_cipher = None


a = Analysis(['watermarker.py'],
             pathex=['C:\\Users\\Stephen\\Scripts\\pdfconduit'],
             binaries=[],
             datas=[
                 ('../pdf/conduit/lib/font', 'font'),
                 ('../pdf/conduit/lib/img', 'img'),
                 ('../pdf/gui/config', 'pdf/gui/config')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Watermarker',
          icon='icon/stamp.ico',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )