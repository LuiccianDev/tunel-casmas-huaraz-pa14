# Scripts de Pruebas y Modelos Experimentales NATM

Este directorio contiene modelos experimentales y simulaciones de ingeniería subterránea para el túnel PA14:

- **`prueba_convergencia_natm.py`**: Simulación de curvas de convergencia-confinamiento y soporte elasto-plástico según el método NATM.
- **`prueba_voladura_natm_secciones.py`**: Modelado matemático de excavación por secciones divididas (Calota superior y Destroza inferior) con desglose de áreas y mallas de perforación.

Ambos modelos cuentan con verificación automatizada en la suite oficial mediante [`tests/test_pruebas_natm.py`](../../tests/test_pruebas_natm.py).
