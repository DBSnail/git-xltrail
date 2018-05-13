from io import StringIO
from unittest import TestCase, mock

git_xltrail = __import__("git-xltrail")


class TestLocalInstaller(TestCase):

    @mock.patch('git-xltrail.is_git_repository', return_value=True)
    def test_paths(self, mock_is_git_repository):
        installer = git_xltrail.Installer(mode='local', path='\\path\\to\\repository')
        self.assertEqual(installer.get_git_attributes_path(), '\\path\\to\\repository\\.gitattributes')
        self.assertEqual(installer.get_git_attributes_path(), '\\path\\to\\repository\\.gitattributes')

    @mock.patch('git-xltrail.subprocess.run')
    @mock.patch('git-xltrail.is_git_repository', return_value=True)
    @mock.patch('git-xltrail.os.path.exists', return_value=False)
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_can_install_when_files_do_not_exist(self, mock_file_open, mock_path_exists, mock_is_git_repository, mock_run):
        installer = git_xltrail.Installer(mode='local', path='\\path\\to\\repository')
        installer.install()
        mock_run.assert_called_once_with(['git', 'config', 'diff.xltrail.command', 'git-xltrail-diff.exe'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True)
        mock_file_open.assert_has_calls([
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('*.doc diff=xltrail\n*.docm diff=xltrail\n*.dotmppt diff=xltrail\n*.potm diff=xltrail\n*.ppam diff=xltrail\n*.ppapptm diff=xltrail\n*.ppsm diff=xltrail\n*.xla diff=xltrail\n*.xlam diff=xltrail\n*.xls diff=xltrail\n*.xlsb diff=xltrail\n*.xlsm diff=xltrail\n*.xlsx diff=xltrail\n*.xlt diff=xltrail\n*.xltm diff=xltrail\n*.xltx diff=xltrail'),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitignore', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('~$*.doc\n~$*.docm\n~$*.dotmppt\n~$*.potm\n~$*.ppam\n~$*.ppapptm\n~$*.ppsm\n~$*.xla\n~$*.xlam\n~$*.xls\n~$*.xlsb\n~$*.xlsm\n~$*.xlsx\n~$*.xlt\n~$*.xltm\n~$*.xltx'),
            mock.call().__exit__(None, None, None)
        ])

    @mock.patch('git-xltrail.subprocess.run')
    @mock.patch('git-xltrail.is_git_repository', return_value=True)
    @mock.patch('git-xltrail.os.path.exists', return_value=True)
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='something\n')
    def test_can_install_when_files_exist(self, mock_file_open, mock_path_exists, mock_is_git_repository, mock_run):
        installer = git_xltrail.Installer(mode='local', path='\\path\\to\\repository')
        installer.install()
        mock_run.assert_called_once_with(['git', 'config', 'diff.xltrail.command', 'git-xltrail-diff.exe'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True)
        mock_file_open.assert_has_calls([
            mock.call('\\path\\to\\repository\\.gitattributes', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('*.doc diff=xltrail\n*.docm diff=xltrail\n*.dotmppt diff=xltrail\n*.potm diff=xltrail\n*.ppam diff=xltrail\n*.ppapptm diff=xltrail\n*.ppsm diff=xltrail\n*.xla diff=xltrail\n*.xlam diff=xltrail\n*.xls diff=xltrail\n*.xlsb diff=xltrail\n*.xlsm diff=xltrail\n*.xlsx diff=xltrail\n*.xlt diff=xltrail\n*.xltm diff=xltrail\n*.xltx diff=xltrail\nsomething'),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitignore', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitignore', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('something\n~$*.doc\n~$*.docm\n~$*.dotmppt\n~$*.potm\n~$*.ppam\n~$*.ppapptm\n~$*.ppsm\n~$*.xla\n~$*.xlam\n~$*.xls\n~$*.xlsb\n~$*.xlsm\n~$*.xlsx\n~$*.xlt\n~$*.xltm\n~$*.xltx'),
            mock.call().__exit__(None, None, None)
        ])

    @mock.patch('git-xltrail.subprocess.run')
    @mock.patch('git-xltrail.is_git_repository', return_value=True)
    @mock.patch('git-xltrail.os.path.exists', return_value=False)
    @mock.patch('git-xltrail.os.remove')
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_can_uninstall_when_files_do_not_exist(self, mock_file_open, mock_os_remove,  mock_path_exists, mock_is_git_repository, mock_run):
        installer = git_xltrail.Installer(mode='local', path='\\path\\to\\repository')
        installer.uninstall()
        mock_run.assert_called_once_with(['git', 'config', '--list'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True)
        mock_os_remove.assert_has_calls([])


    @mock.patch('git-xltrail.subprocess.run')
    @mock.patch('git-xltrail.is_git_repository', return_value=True)
    @mock.patch('git-xltrail.os.path.exists', return_value=True)
    @mock.patch('git-xltrail.os.remove')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='something')
    def test_can_uninstall_when_files_exist(self, mock_file_open, mock_os_remove,  mock_path_exists, mock_is_git_repository, mock_run):
        installer = git_xltrail.Installer(mode='local', path='\\path\\to\\repository')
        installer.uninstall()
        mock_run.assert_called_once_with(['git', 'config', '--list'], cwd='\\path\\to\\repository', stderr=-1, stdout=-1, universal_newlines=True)
        self.assertEqual(mock_os_remove.call_count, 0)
        mock_file_open.assert_has_calls([
            mock.call('\\path\\to\\repository\\.gitattributes', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('something'),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'r'),
            mock.call().__enter__(),
            mock.call().read(),
            mock.call().__exit__(None, None, None),
            mock.call('\\path\\to\\repository\\.gitattributes', 'w'),
            mock.call().__enter__(),
            mock.call().writelines('something'),
            mock.call().__exit__(None, None, None)
        ])


class TestGlobalInstaller(TestCase):

    @mock.patch('git-xltrail.subprocess.run')
    @mock.patch('git-xltrail.Installer.get_git_attributes_path')
    @mock.patch('git-xltrail.Installer.get_git_ignore_path')
    def test_global_gitconfig_dir(self, mock_get_git_ignore_path, mock_get_git_attributes_path, mock_run):
        installer = git_xltrail.Installer(mode='global')
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_has_calls([
            mock.call(['git', 'config', '--global', '--list', '--show-origin'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True),
            mock.call(['git', 'config', '--global', '--list'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True)
        ])

    @mock.patch('git-xltrail.subprocess.run')
    @mock.patch('git-xltrail.Installer.get_global_gitconfig_dir')
    @mock.patch('git-xltrail.Installer.get_git_ignore_path')
    def test_global_gitattributes_path(self, mock_get_git_ignore_path, get_global_gitconfig_dir, mock_run):
        installer = git_xltrail.Installer(mode='global')
        self.assertEqual(mock_run.call_count, 1)
        mock_run.assert_called_once_with(['git', 'config', '--global', '--get', 'core.attributesfile'], cwd=None, stderr=-1, stdout=-1, universal_newlines=True)


class TestHelp(TestCase):
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_generic_help(self, mock_stdout):
        command_parser = git_xltrail.CommandParser(['help'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), git_xltrail.HELP_GENERIC + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help_install(self, mock_stdout):
        command_parser = git_xltrail.CommandParser(['help', 'install'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), git_xltrail.HELP_INSTALL + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help_uninstall(self, mock_stdout):
        command_parser = git_xltrail.CommandParser(['help', 'uninstall'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), git_xltrail.HELP_UNINSTALL + '\n')


class CommandParser(TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_version(self, mock_stdout):
        command_parser = git_xltrail.CommandParser(['version'])
        command_parser.execute()
        self.assertEqual(mock_stdout.getvalue(), git_xltrail.GIT_XLTRAIL_VERSION + '\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_env(self, mock_stdout):
        command_parser = git_xltrail.CommandParser(['env'])
        command_parser.execute()
        self.assertTrue(mock_stdout.getvalue())



class TestAddinInstaller(TestCase):

    @mock.patch('git-xltrail.winreg.QueryValue', return_value='Excel.Application.16')
    def test_can_get_excel_version(self, mock_query_value):
        addin_installer = git_xltrail.AddinInstaller()
        self.assertEqual(addin_installer.get_excel_version(), '16.0')

    @mock.patch('git-xltrail.winreg.OpenKey', return_value=mock.Mock())
    @mock.patch('git-xltrail.winreg.QueryValueEx', return_value=('C:\\Program Files (x86)\\Microsoft Office\\Root\\Office16\\', 1))
    def test_can_get_excel_path(self, mock_query_value, mock_open_key):
        addin_installer = git_xltrail.AddinInstaller()
        self.assertEqual(addin_installer.get_excel_path(), 'C:\Program Files (x86)\Microsoft Office\Root\Office16\excel.exe')

    @mock.patch('git-xltrail.AddinInstaller.get_excel_path', return_value='c:\\path\\excel\\excel.exe')
    @mock.patch('git-xltrail.AddinInstaller.get_binary_type', return_value=6)
    def test_can_get_excel_bitness(self, mock_get_binary_type, mock_get_excel_path):
        addin_installer = git_xltrail.AddinInstaller()
        self.assertEqual('x64', addin_installer.get_excel_bitness())
