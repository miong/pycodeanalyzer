import pytest
import builtins
from unittest.mock import patch, mock_open, MagicMock

from pycodeanalyzer.core.analyzer.search import SearchAnalyser

class TestSearchAnalyser:

    def test_seachInFile(self, mocker):
        token = "toto"
        text ="""toto
l1 Abcd
l2 kikou
l3 titi
l4 toto
l5 lksdjfsdhf
l6 ksldjlkdjfsjdf
l7 dsdkjldfjlksdj
l8 lkdjsdlkflsdjs
l9 sldlsjflsdf
l10 msdlkjmdfmkskdf
l11 ldsfiokdsfi TOTO ksldjlkdjfsjdf

l13 lsdfsdfls
l14 sdksdfjsldkjflsdjstoto
l15 dlkjdslfjslkdjlsdjfslf
l16 sdfsdfsfsdzzazed
l17 hghjjkuioluirtqzfvb
l18 sdkjdhfsdfskdfhskd toto"""
        with patch("builtins.open", mock_open(read_data=text)):
            analyzer = SearchAnalyser()
            tokens = analyzer.seachInFile(token, "dir/file.txt")
            expected = [
                            ('dir/file.txt',
                             'toto\n'
                             'l1 Abcd\n'
                             'l2 kikou\n'),
                            ('dir/file.txt',
                             'l1 Abcd\n'
                             'l2 kikou\n'
                             'l3 titi\n'
                             'l4 toto\n'
                             'l5 lksdjfsdhf\n'
                             'l6 ksldjlkdjfsjdf\n'),
                            ('dir/file.txt',
                             'l8 lkdjsdlkflsdjs\n'
                             'l9 sldlsjflsdf\n'
                             'l10 msdlkjmdfmkskdf\n'
                             'l11 ldsfiokdsfi TOTO ksldjlkdjfsjdf\n'
                             '\n'
                             'l13 lsdfsdfls\n'),
                            ('dir/file.txt',
                             'l11 ldsfiokdsfi TOTO ksldjlkdjfsjdf\n'
                             '\n'
                             'l13 lsdfsdfls\n'
                             'l14 sdksdfjsldkjflsdjstoto\n'
                             'l15 dlkjdslfjslkdjlsdjfslf\n'
                             'l16 sdfsdfsfsdzzazed\n'),
                            ('dir/file.txt',
                             'l15 dlkjdslfjslkdjlsdjfslf\n'
                             'l16 sdfsdfsfsdzzazed\n'
                             'l17 hghjjkuioluirtqzfvb\n'
                             'l18 sdkjdhfsdfskdfhskd toto\n'),
                       ]
            assert tokens == expected

    def test_searchInAllFiles(self, mocker):
        text1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Nunc commodo arcu eget pharetra sagittis. Fusce sagittis ligula nulla, eget porta justo porttitor gravida.
Proin id egestas dolor, sit amet aliquam libero. Vivamus ac nisi et eros efficitur sodales.
Nullam imperdiet dui erat, quis vestibulum lacus pretium nec. Morbi gravida odio ac pulvinar volutpat.
Fusce tempus vel ligula ac lacinia. Aliquam a augue turpis. Mauris sit amet maximus erat.
Mauris a erat mauris. Mauris facilisis eleifend massa, non iaculis magna cursus ut.
Proin laoreet nisi nec porttitor varius. In hac habitasse platea dictumst. Proin dictum mauris risus, ac finibus turpis tempor sit amet.
Donec dignissim iaculis facilisis. Curabitur vel ligula turpis.
"""

        text2="""Donec cursus turpis eu justo aliquet accumsan.
Nunc elementum finibus semper.
Integer viverra suscipit urna, ac pretium augue tincidunt dictum. Aenean ullamcorper, quam ac tempor cursus, nisi tellus maximus urna,
a auctor sem elit in augue. Praesent fringilla urna id velit cursus, commodo dignissim est elementum. Nulla consequat sapien nisi, at tristique
libero efficitur sed. Etiam sit amet lacus commodo, rutrum ex et, aliquam nibh. Sed urna tellus, porta eget dictum vel, aliquam at ex.
Sed faucibus nisi et nisl sollicitudin, sit amet pulvinar massa ultricies.
Morbi eget est volutpat, suscipit lorem nec, ullamcorper tortor.
Morbi ut est vel ante accumsan efficitur. Aenean eu semper arcu, non volutpat lorem.
Nunc eleifend sapien ac hendrerit rhoncus.
Morbi ultrices lectus at tellus euismod suscipit. Pellentesque aliquam, erat et iaculis hendrerit,
diam lectus varius ex, sed porttitor risus sem eget ligula.
"""

        text3="""Donec euismod condimentum fermentum.
In aliquet hendrerit bibendum. Mauris eget rhoncus sem.
Aenean non tristique justo.
Phasellus faucibus lobortis lectus non interdum.
Nunc facilisis metus ut sapien lobortis, quis auctor diam feugiat.
Aenean non ipsum a erat ornare ultrices. Duis vitae ante id lorem dignissim rhoncus sit amet in leo.
Fusce ornare augue vitae eros congue laoreet.
Proin fermentum dapibus porttitor.
"""

        text4="""nuNc nisl justo,
convallis imperdiet maximus quis, pharetra eu sem.
Donec congue, dolor non pretium dictum, sem felis tempus metus, sed eleifend lorem sem eget urna.
Curabitur cursus enim eget nisl posuere, ut laoreet felis luctus. Donec eu dui ullamcorper, rhoncus dui in, porta augue.
Sed luctus quam rutrum, euismod diam ut, ultrices justo. Pellentesque tempus rutrum lectus ac sollicitudin. Integer placerat est libero.
Etiam tempus arcu eu semper consectetur. Etiam eget quam efficitur, auctor odio facilisis, viverra risus.
Vestibulum vel augue molestie, condimentum metus id, eleifend leo.
NUNC !
"""

        def get_mock_open_for_files(files):
            def my_open_mock(filename, *args, **kwargs):
                for expected_filename, content in files.items():
                    if filename == expected_filename:
                        return mock_open(read_data=content).return_value
                raise FileNotFoundError('(mock) Unable to open {}'.format(filename))
            return mocker.MagicMock(side_effect=my_open_mock)

        token = "nunC"
        files = {
            "dir/file.txt": text1,
            "dir/file2.txt": text2,
            "file3.txt": text3,
            "dir/file666.txt": text4
        }
        with patch("builtins.open", get_mock_open_for_files(files)):
            analyzer = SearchAnalyser()
            tokens = analyzer.searchInAllFiles(token, files.keys())
            expected = [
                ('dir/file.txt',
                 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n'
                 'Nunc commodo arcu eget pharetra sagittis. Fusce sagittis ligula nulla, eget '
                 'porta justo porttitor gravida.\n'
                 'Proin id egestas dolor, sit amet aliquam libero. Vivamus ac nisi et eros '
                 'efficitur sodales.\n'
                 'Nullam imperdiet dui erat, quis vestibulum lacus pretium nec. Morbi gravida '
                 'odio ac pulvinar volutpat.\n'),
                ('dir/file2.txt',
                 'Donec cursus turpis eu justo aliquet accumsan.\n'
                 'Nunc elementum finibus semper.\n'
                 'Integer viverra suscipit urna, ac pretium augue tincidunt dictum. Aenean '
                 'ullamcorper, quam ac tempor cursus, nisi tellus maximus urna,\n'
                 'a auctor sem elit in augue. Praesent fringilla urna id velit cursus, '
                 'commodo dignissim est elementum. Nulla consequat sapien nisi, at '
                 'tristique\n'),
                ('dir/file2.txt',
                 'Sed faucibus nisi et nisl sollicitudin, sit amet pulvinar massa ultricies.\n'
                 'Morbi eget est volutpat, suscipit lorem nec, ullamcorper tortor.\n'
                 'Morbi ut est vel ante accumsan efficitur. Aenean eu semper arcu, non '
                 'volutpat lorem.\n'
                 'Nunc eleifend sapien ac hendrerit rhoncus.\n'
                 'Morbi ultrices lectus at tellus euismod suscipit. Pellentesque aliquam, '
                 'erat et iaculis hendrerit,\n'
                 'diam lectus varius ex, sed porttitor risus sem eget ligula.\n'),
                ('file3.txt',
                 'In aliquet hendrerit bibendum. Mauris eget rhoncus sem.\n'
                 'Aenean non tristique justo.\n'
                 'Phasellus faucibus lobortis lectus non interdum.\n'
                 'Nunc facilisis metus ut sapien lobortis, quis auctor diam feugiat.\n'
                 'Aenean non ipsum a erat ornare ultrices. Duis vitae ante id lorem dignissim '
                 'rhoncus sit amet in leo.\n'
                 'Fusce ornare augue vitae eros congue laoreet.\n'),
                ('dir/file666.txt',
                 'nuNc nisl justo,\n'
                 'convallis imperdiet maximus quis, pharetra eu sem.\n'
                 'Donec congue, dolor non pretium dictum, sem felis tempus metus, sed '
                 'eleifend lorem sem eget urna.\n'),
                ('dir/file666.txt',
                 'Sed luctus quam rutrum, euismod diam ut, ultrices justo. Pellentesque '
                 'tempus rutrum lectus ac sollicitudin. Integer placerat est libero.\n'
                 'Etiam tempus arcu eu semper consectetur. Etiam eget quam efficitur, auctor '
                 'odio facilisis, viverra risus.\n'
                 'Vestibulum vel augue molestie, condimentum metus id, eleifend leo.\n'
                 'NUNC !\n'),

            ]
            assert tokens == expected
