# -*- mode: python -*-

block_cipher = None


a = Analysis(['watermarker.py'],
             pathex=['C:\\Users\\Stephen\\Scripts\\pdfwatermarker'],
             binaries=[],
             datas=[('pdfwatermarker/watermark/lib/font', 'font'), ('pdfwatermarker/watermark/lib/img', 'img')],
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
          name='watermarker',
          icon='pdfwatermarker/watermark/lib/icon/icon.ico',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
