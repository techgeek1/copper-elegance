#!/usr/bin/env python3
"""Build a .vsix package for the Copper Elegance extension."""

import zipfile
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    with open(os.path.join(SCRIPT_DIR, "package.json")) as f:
        pkg = json.load(f)

    name      = pkg["name"]
    version   = pkg["version"]
    publisher = pkg["publisher"]
    display   = pkg.get("displayName", name)
    desc      = pkg.get("description", "")
    engine    = pkg["engines"]["vscode"]

    content_types = '<?xml version="1.0" encoding="utf-8"?>\n' \
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n' \
        '  <Default Extension=".json" ContentType="application/json"/>\n' \
        '  <Default Extension=".vsixmanifest" ContentType="text/xml"/>\n' \
        '</Types>'

    vsix_manifest = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<PackageManifest Version="2.0.0"'
        ' xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011"'
        ' xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">\n'
        '  <Metadata>\n'
        f'    <Identity Language="en-US" Id="{name}" Version="{version}" Publisher="{publisher}"/>\n'
        f'    <DisplayName>{display}</DisplayName>\n'
        f'    <Description xml:space="preserve">{desc}</Description>\n'
        '    <Tags>theme,color-theme</Tags>\n'
        '    <Categories>Themes</Categories>\n'
        '    <GalleryFlags>Public</GalleryFlags>\n'
        '    <Properties>\n'
        f'      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{engine}"/>\n'
        '      <Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value=""/>\n'
        '      <Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value=""/>\n'
        '      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui"/>\n'
        '      <Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value=""/>\n'
        '    </Properties>\n'
        '  </Metadata>\n'
        '  <Installation>\n'
        '    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>\n'
        '  </Installation>\n'
        '  <Dependencies/>\n'
        '  <Assets>\n'
        '    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/>\n'
        '  </Assets>\n'
        '</PackageManifest>'
    )

    vsix_name = f"{publisher}.{name}-{version}.vsix"
    vsix_path = os.path.join(SCRIPT_DIR, vsix_name)

    with zipfile.ZipFile(vsix_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("extension.vsixmanifest", vsix_manifest)
        zf.write(os.path.join(SCRIPT_DIR, "package.json"), "extension/package.json")

        themes_dir = os.path.join(SCRIPT_DIR, "themes")
        for theme_file in sorted(os.listdir(themes_dir)):
            if theme_file.endswith(".json"):
                zf.write(
                    os.path.join(themes_dir, theme_file),
                    f"extension/themes/{theme_file}",
                )

    size_kb = os.path.getsize(vsix_path) / 1024
    print(f"{vsix_name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    build()
