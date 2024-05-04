import PyInstaller.__main__ as compiler
import os
import glob
import shutil
import platform

def build():   
    try:
        compiler.run([
            f'src/__init__.py',
            f'--onefile',
            f'--windowed',
            f'--argv-emulation',

            f'--name=ScrapeyDoo',
            f'--icon=src/assets/ScrapeyDoo.ico',
            f'--add-data=src/assets{os.pathsep}assets',

            f'--paths=src',
            f'--additional-hooks-dir=src/hooks',
            f'--hidden-import=settings',
            f'--add-data=src/resources{os.pathsep}resources',

            f'--noconfirm'
        ])
        print('Done!')
    except KeyError:
        print(f'The platform: {platform.system()} is not supported!')

    # for spec_file in glob.glob('*.spec'):
    #     os.remove(spec_file)
    if os.path.exists('build'):
        shutil.rmtree('build')

if __name__ == '__main__':
    build()