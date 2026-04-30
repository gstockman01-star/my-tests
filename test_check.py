def test_math_pass():
    # Этот тест должен пройти (2+2 действительно 4)
    assert 2 + 2 == 4

def test_logic_fail():
    # Этот тест специально упадет, чтобы мы увидели отчет об ошибке
    # Мы проверяем, что слово "QA" есть в строке "Python Developer"
    text = "Python Developer"
    assert "QA" in text
