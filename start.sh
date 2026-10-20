#!/bin/bash
# Astrofyzikální Výzkumné Prostředí - Startovací Skript

echo "======================================"
echo "Astrofyzikální Výzkumné Prostředí"
echo "======================================"
echo ""

# Aktivace virtuálního prostředí
cd /home/dawe/Projects/astro-science
source .venv/bin/activate

echo "✓ Virtuální prostředí aktivováno"
echo "✓ Python: $(python --version)"
echo ""

# Informace o dostupných nástrojích
echo "Dostupné nástroje:"
echo "  - jupyter lab:   Spustit Jupyter Lab"
echo "  - jupyter nb:    Spustit Jupyter Notebook"
echo "  - python:        Python REPL"
echo "  - ds9:          FITS image viewer"
echo "  - julia:        Julia REPL"
echo "  - ~/tools/Stellarium-26.3-qt5-x86_64.AppImage: Stellarium"
echo ""

echo "Pro spuštění Jupyter Lab spusťte:"
echo "  jupyter lab"
echo ""

# Volitelně rovnou spustit Jupyter Lab
if [ "$1" == "lab" ]; then
    echo "Spouštím Jupyter Lab..."
    jupyter lab
elif [ "$1" == "nb" ]; then
    echo "Spouštím Jupyter Notebook..."
    jupyter notebook
else
    echo "Pro automatické spuštění Jupyter Lab použijte:"
    echo "  ./start.sh lab"
    echo ""
    echo "Nebo spusťte ručně:"
    echo "  jupyter lab"
fi
