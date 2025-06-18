#!/usr/bin/env python3
"""
Starter-Skript für HIS mit Kommandozeilen-UI.
Nutzen Sie das Menü, um vordefinierte Datensätze zu senden
oder manuell Einträge hinzuzufügen.
"""
import sys
from scripts.his_cli import HisCli
from middleware.utils.logger import logger


def main():
    try:
        cli = HisCli()
        cli.main_menu()
    except KeyboardInterrupt:
        logger.info("Programm unterbrochen, Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
