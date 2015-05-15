# -*- mode: python -*-
# example run cmd: `pyinstaller --additional-hooks-dir=hooks/ Maker-Windows.spec`
import os

def Datafiles(*filenames, **kw):
  def datafile(path, strip_path=False):
    parts = path.split('/')
    path = name = os.path.join(*parts)
    if strip_path:
      name = os.path.basename(path)
    return name, path, 'DATA'

  strip_path = kw.get('strip_path', True)
  return TOC(
    datafile(filename, strip_path=strip_path)
    for filename in filenames
    if os.path.isfile(filename))

docfiles = Datafiles('pic_lrg.gif', 'pr.hex')

a = Analysis(['Maker.py'],
             pathex=['c:\\Users\\IEUser\\Desktop\\Misc_tools\\MakrKT'],
             hiddenimports=['intelhex', 'datetime', 'struct', 'math', 'crcmod', 'getopt'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
      docfiles,
          name='Maker.exe',
          debug=False,
          strip=None,
          upx=False,
          console=True )
