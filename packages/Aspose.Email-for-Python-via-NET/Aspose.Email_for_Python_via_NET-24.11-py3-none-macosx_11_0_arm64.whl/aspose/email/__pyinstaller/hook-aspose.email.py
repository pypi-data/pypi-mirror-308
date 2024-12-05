from PyInstaller.utils.hooks import get_package_paths
import os.path

(_, root) = get_package_paths('aspose')

datas = [(os.path.join(root, 'assemblies', 'email'), os.path.join('aspose', 'assemblies', 'email'))]

hiddenimports = [ 'aspose', 'aspose.pyreflection', 'aspose.pygc', 'aspose.pycore' ]

