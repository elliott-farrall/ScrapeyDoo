import PyInstaller.__main__ as compiler
import os
import glob
import shutil
import platform

def compile():   
    try:
        compiler.run([
            f'src/__init__.py',
            f'--onefile',
            f'--windowed',
            f'--argv-emulation',
            f'--name=ScrapeyDoo_{platform.system()}',
            # f'-i=assets/Scrapey-Doo.ico',
            # f'--add-data=assets/Scrappy-Doo.webp{os.pathsep}assets',
            # f'--hidden-import=babel.numbers',
            f'--noconfirm'
        ])
        print('Done!')
    except KeyError:
        print(f'The platform: {platform.system()} is not supported!')

    for spec_file in glob.glob('*.spec'):
        os.remove(spec_file)
    if os.path.exists('build'):
        shutil.rmtree('build')

if __name__ == '__main__':
    compile()