#!/usr/bin/env python3

import sys
import os
from datetime import datetime

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from gui.main_window import GICApp
from utils.logger import Logger

def main():
    print("=" * 60)
    print("GESTOR INTELIGENTE DE CLIENTES (GIC)")
    print("SolutionTech - Sistema de Gestión de Clientes")
    print("=" * 60)
    
    logger = Logger()
    logger.log("Sistema GIC iniciado", "INFO")
    
    try:
        print("\nIniciando interfaz gráfica...")
        app = GICApp()
        app.run()
        
    except Exception as e:
        logger.log(f"Error en el sistema principal: {str(e)}", "ERROR")
        print(f"Error: {str(e)}")
        return 1
    
    logger.log("Sistema GIC finalizado correctamente", "INFO")
    return 0

if __name__ == "__main__":
    sys.exit(main())