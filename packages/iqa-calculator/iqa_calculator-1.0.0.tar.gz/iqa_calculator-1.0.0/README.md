# IQA/WQI Calculator

Este pacote fornece uma função `IQA / WQI` para calcular o Índice de Qualidade da Água (IQA).

## Exemplo de uso

```python
from iqa_calculator import IQA

resultado = IQA(
    oxigenio_dissolvido=8.0,
    coliformes_fecais=200,
    ph=7.0,
    dbo=5.0,
    nitrogenio_total=1.0,
    fosforo_total=0.1,
    turbidez=2.0,
    solidos_totais=500,
    altitude=100,
    temperatura=25
)

print(resultado)  # Saída: 0
