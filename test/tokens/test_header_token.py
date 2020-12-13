from pycourselet import CourseletScanner

from pycourselet.tokens import HeaderToken


def test_strip_right():
    source = '# Test1  Strip '

    token = HeaderToken.parse(source)

    assert token, 'Token not found'
    assert token.level == 1, 'Wrong Level'
    assert token.text == "Test1  Strip", 'Wrong Text'


def test_strip_left():
    source = '#   Test1  Strip '

    token = HeaderToken.parse(source)

    assert token, 'Token not found'
    assert token.level == 1, 'Wrong Level'
    assert token.text == "Test1  Strip", 'Wrong Text'


def test_level_1():
    source = '# Test1'

    token = HeaderToken.parse(source)

    assert token, 'Token not found'
    assert token.level == 1, 'Wrong Level'
    assert token.text == "Test1", 'Wrong Text'


def test_level_2():
    source = '## Test2'

    token = HeaderToken.parse(source)

    assert token, 'Token not found'
    assert token.level == 2, 'Wrong Level'
    assert token.text == "Test2", 'Wrong Text'


def test_level_3():
    source = '### Test3'

    token = HeaderToken.parse(source)

    assert token, 'Token not found'
    assert token.level == 3, 'Wrong Level'
    assert token.text == "Test3", 'Wrong Text'


def test_scan_level_1():
    source = '# Test1'
    scanner = CourseletScanner()

    tree = scanner.scan(source)

    return
