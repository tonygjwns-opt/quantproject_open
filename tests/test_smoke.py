"""뼈대 확인용 smoke 테스트: 패키지가 설치되어 import 되는지만 검증한다."""

import portoptim


def test_import():
    assert portoptim.__version__ == "0.0.0"
