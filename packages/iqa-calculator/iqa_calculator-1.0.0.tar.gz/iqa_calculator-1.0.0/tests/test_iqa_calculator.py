import pytest


from iqa.iqa_calculator import IQA


def test_calc_iqa_default_values():
    # Test with default values for altitude and temperature
    resultado = IQA(
        oxigenio_dissolvido=8.0,
        coliformes_fecais=200,
        ph=7.0,
        dbo=5.0,
        nitrogenio_total=1.0,
        fosforo_total=0.1,
        turbidez=2.0,
        solidos_totais=100
    )
    assert isinstance(resultado, dict), "O resultado deve ser um dicionário"
    assert "iqa" in resultado and "qualidade" in resultado, "O resultado deve conter 'iqa' e 'qualidade'"
    assert resultado["iqa"] >= 0, "O valor do IQA deve ser não-negativo"

def test_calc_iqa_with_altitude_and_temperature():
    # Test with specified altitude and temperature values
    resultado = IQA(
        oxigenio_dissolvido=9.0,
        coliformes_fecais=150,
        ph=6.5,
        dbo=4.0,
        nitrogenio_total=2.0,
        fosforo_total=0.5,
        turbidez=3.0,
        solidos_totais=120,
        altitude=100,
        temperatura=25
    )
    assert isinstance(resultado, dict), "O resultado deve ser um dicionário"
    assert "iqa" in resultado and "qualidade" in resultado, "O resultado deve conter 'iqa' e 'qualidade'"
    assert resultado["iqa"] >= 0, "O valor do IQA deve ser não-negativo"

def test_calc_iqa_extreme_values():
    # Test with extreme values for parameters
    resultado = IQA(
        oxigenio_dissolvido=0.5,
        coliformes_fecais=100000,
        ph=2.0,
        dbo=50.0,
        nitrogenio_total=80.0,
        fosforo_total=10.0,
        turbidez=200,
        solidos_totais=1000,
        altitude=5000,
        temperatura=50
    )
    assert isinstance(resultado, dict), "O resultado deve ser um dicionário"
    assert "iqa" in resultado and "qualidade" in resultado, "O resultado deve conter 'iqa' e 'qualidade'"
    assert resultado["iqa"] >= 0, "O valor do IQA deve ser não-negativo"
