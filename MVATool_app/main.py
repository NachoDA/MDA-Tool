# MVATool

import sys
from Controllers.MainWindowController import MainWindowController

__author__ = 'Ignacio Díaz Arellano'

if __name__ == '__main__':
    controller = MainWindowController()
    sys.exit(controller.run())

# Projects, Data, Examine, Models, Analysis, "Draw"
# Centrado en gestión, visualización y análisis de datos.
# - Gestión:        # TODO: importación de distintos modelos
                    # TODO: tratamiento adecuando de más datos
# - Visualización:  # TODO: sección "Examine" con opciones que no tiene otro software
                    # TODO: Todos los gráficos de Analysis
                    # TODO: ¿Definición de paletas de colores?
                    # TODO: Sección "Draw"
                    # TODO: Representación en tablas "avanzada", no "bruta"
# - Análisis:       # TODO: Modelos estadísticos avanzados para la exploración de procesos multivariantes

# Desvinculación del modelo de su dataset (cómo se organizan y pre procesan los datos)
# para permitir su uso en varios modelos y poder compararlos