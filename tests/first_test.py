import page_analyzer


def test_nothing():
    assert page_analyzer.app


def test_for_test():
    assert page_analyzer.for_test() is True
