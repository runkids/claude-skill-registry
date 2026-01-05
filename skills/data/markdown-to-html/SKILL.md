---
name: markdown-to-html
description: Convierte archivos Markdown a HTML single-file con estilos profesionales corporativos
version: 1.0.0
author: Skiller Project
tags:
  - markdown
  - html
  - conversion
  - documentation
---

# Skill: Markdown to HTML

## Descripción

Esta skill convierte archivos Markdown a documentos HTML single-file (sin dependencias externas de imágenes) con estilos profesionales basados en documentos corporativos.

## Características

- **HTML Single-File**: Todo el contenido (CSS, imágenes) está embebido en un solo archivo HTML
- **Portada profesional**: Título + imagen corporativa + autor/fecha (sin logos adicionales)
- **Tabla de contenidos**: Generada automáticamente (solo niveles H1 y H2)
- **Estilos EXACTOS del ejemplo**: Colores, tipografías y ancho extraídos del PDF de referencia
- **Código con fondo gris**: Bloques de código con fondo `#f5f5f5` para mejor legibilidad
- **Compatible con Google Docs**: El HTML se puede abrir directamente en Google Docs
- **Ancho correcto**: `max-width: 550pt` con padding `50pt` lateral (igual que el ejemplo)

## Uso

### Comando básico

```bash
./scripts/convert.sh documento.md
```

### Opciones disponibles

| Opción | Descripción |
|--------|-------------|
| `-o, --output <file>` | Archivo de salida (por defecto: mismo nombre .html) |
| `--title <titulo>` | Título del documento (por defecto: primer H1 del MD) |
| `--author <autor>` | Autor del documento |
| `--date <fecha>` | Fecha del documento (por defecto: fecha actual) |
| `--no-toc` | No incluir tabla de contenidos |
| `--no-cover` | No incluir portada |
| `-h, --help` | Mostrar ayuda |

### Ejemplos

```bash
# Conversión básica
./scripts/convert.sh mi-documento.md

# Con título y autor personalizados
./scripts/convert.sh documento.md --title "Manual de Usuario" --author "Equipo Dev"

# Sin portada ni TOC (solo contenido)
./scripts/convert.sh documento.md --no-cover --no-toc

# Especificar archivo de salida
./scripts/convert.sh README.md -o documentacion.html
```

## Estilos aplicados

### Títulos (extraídos del PDF de ejemplo)

| Nivel | Tamaño | Color | Peso |
|-------|--------|-------|------|
| H1 | 20pt | #000000 | Normal |
| H2 | 16pt | #222222 | Normal |
| H3 | 14pt | #434343 | Bold |
| H4 | 12pt | #666666 | Normal |
| H5 | 11pt | #666666 | Normal |
| H6 | 11pt (italic) | #666666 | Normal |

### Listas

- **Nivel 1**: Marcador de disco (●)
- **Nivel 2**: Marcador de círculo (○)
- **Nivel 3+**: Sin marcador, texto en negrita

### Código

- Fondo gris (`#f5f5f5`)
- Borde sutil (`#e0e0e0`)
- Fuente monoespaciada (Consolas, Monaco, Courier New)

### Tablas

- Cabecera con fondo azul corporativo (`#3c78d8`)
- Filas alternadas con fondo gris claro
- Bordes en `#cccccc`

## Dependencias

- **pandoc**: Para la conversión de Markdown a HTML
  - macOS: `brew install pandoc`
  - Linux: `apt-get install pandoc`
  - Windows: `choco install pandoc`

## Estructura de archivos

```
markdown-to-html/
├── SKILL.md           # Este archivo
├── scripts/
│   └── convert.sh     # Script de conversión
└── assets/
    └── cover-image.jpg  # Imagen de portada corporativa
```

## Personalización

### Cambiar imagen de portada

Reemplaza el archivo `assets/cover-image.jpg` por tu imagen corporativa.
Formatos soportados: JPG, PNG.

### Modificar estilos

Los estilos CSS están embebidos en el script `convert.sh`. Busca la función `generate_css()` para modificar:
- Colores de títulos (variables `--color-h1` a `--color-h6`)
- Color de fondo de código (`--bg-code`)
- Color de cabeceras de tabla (`--bg-table-header`)
- Tipografías y tamaños

## Compatibilidad con Google Docs

El HTML generado está optimizado para abrirse en Google Docs:

1. Sube el archivo `.html` a Google Drive
2. Haz clic derecho → "Abrir con" → "Google Docs"
3. Los estilos se preservarán automáticamente

**Nota**: Algunas características avanzadas de CSS pueden no renderizarse exactamente igual en Google Docs.

