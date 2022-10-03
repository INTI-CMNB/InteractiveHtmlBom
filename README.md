# Interactive HTML BOM plugin for KiCad
## Supports EasyEDA, Eagle and Fusion360

![icon](https://i.imgur.com/js4kDOn.png)

This plugin generates convenient BOM listing with ability to visually correlate
and easily search for components and their placements on the pcb.

This is really useful when hand soldering your prototype and you have to find 50
places where 0.1uF cap should be or which of the SOP8 footprints are for the same
micro. Dynamically highlighting all components in the same group on the rendering
of the pcb makes manually populating the board much easier.

This plugin utilizes Pcbnew python bindings to read pcb data and render
silkscreen, fab layer, footprint pads, text and drawings. Additionally it can
pull data from schematic if you export it through netlist or xml file that
Eeschema can generate from it's internal bom tool. That extra data can be added
as additional columns in the BOM table (for example manufacturer id) or it can be
used to indicate which components should be omitted altogether (dnp field). For
full description of functionality see [wiki](https://github.com/openscopeproject/InteractiveHtmlBom/wiki).

Generated html page is fully self contained, doesn't need internet connection to work
and can be packaged with documentation of your project or hosted anywhere on the web.

[A demo is worth a thousand words.](https://openscopeproject.org/InteractiveHtmlBomDemo/)

## Installation and Usage

Important: when installing this fork to be used with `KiBot` you must be sure the `generate_interactive_bom.py` is in your path.
Or at least that the plug-in is accessible from KiCad (`KiBot` also looks in the KiCad plug-in dirs).
For Debian/Ubuntu systems the simplest way is to install the Debian package provided by this fork, check the [releases section](https://github.com/INTI-CMNB/InteractiveHtmlBom/releases)

See [project wiki](https://github.com/openscopeproject/InteractiveHtmlBom/wiki) for instructions.

## License and credits

Plugin code is licensed under MIT license, see `LICENSE` for more info.

Html page uses [Split.js](https://github.com/nathancahill/Split.js),
[PEP.js](https://github.com/jquery/PEP) and (stripped down)
[lz-string.js](https://github.com/pieroxy/lz-string) libraries that get embedded into
generated bom page.

`units.py` is borrowed from [KiBom](https://github.com/SchrodingersGat/KiBoM)
plugin (MIT license).

`svgpath.py` is heavily based on
[svgpathtools](https://github.com/mathandy/svgpathtools) module (MIT license).
