#!/usr/bin/env python3
"""
Multi-Browser Build Pipeline for LiveRebuild by NMstudio
Supports: Cốc Cốc, Google Chrome, Microsoft Edge, Opera, Brave, and Mozilla Firefox.
"""
import json
import os
import shutil
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")

BROWSERS = {
    "coccoc": {
        "name": "LiveRebuild - Cốc Cốc Edition (NMstudio)",
        "theme_id": "coccoc",
        "description": "Biến mọi trang web thành canvas trống và chiêm ngưỡng đàn con trỏ chuột Cốc Cốc tái lập lại giao diện trực tiếp kèm hiệu ứng gõ phím cơ và thước đo tỉ mỉ.",
        "is_chromium": True,
        "zip_name": "liverebuild-coccoc-nmstudio.zip"
    },
    "chrome": {
        "name": "LiveRebuild - Chrome Edition (NMstudio)",
        "theme_id": "chrome",
        "description": "Wipe any page to a blank canvas and watch a swarm of Chrome cursors rebuild it live with typing, drawing, and guides.",
        "is_chromium": True,
        "zip_name": "liverebuild-chrome-nmstudio.zip"
    },
    "edge": {
        "name": "LiveRebuild - Edge Edition (NMstudio)",
        "theme_id": "edge",
        "description": "Wipe any page to a blank canvas and watch a swarm of Microsoft Edge cursors rebuild it live.",
        "is_chromium": True,
        "zip_name": "liverebuild-edge-nmstudio.zip"
    },
    "opera": {
        "name": "LiveRebuild - Opera Edition (NMstudio)",
        "theme_id": "opera",
        "description": "Wipe any page to a blank canvas and watch a swarm of Opera cursors rebuild it live.",
        "is_chromium": True,
        "zip_name": "liverebuild-opera-nmstudio.zip"
    },
    "brave": {
        "name": "LiveRebuild - Brave Edition (NMstudio)",
        "theme_id": "brave",
        "description": "Wipe any page to a blank canvas and watch a swarm of Brave cursors rebuild it live.",
        "is_chromium": True,
        "zip_name": "liverebuild-brave-nmstudio.zip"
    },
    "universal": {
        "name": "LiveRebuild - Universal Chromium (NMstudio)",
        "theme_id": "auto",
        "description": "Tiện ích tái lập trang web trực tiếp với đàn con trỏ thông minh tự nhận diện mọi trình duyệt (Cốc Cốc, Chrome, Edge, Opera, Brave).",
        "is_chromium": True,
        "zip_name": "liverebuild-universal-nmstudio.zip"
    },
    "firefox": {
        "name": "LiveRebuild - Firefox Edition (NMstudio)",
        "theme_id": "firefox",
        "description": "Live swarm cursor webpage rebuilder for Firefox by NMstudio.",
        "is_chromium": False,
        "zip_name": "liverebuild-firefox-nmstudio.zip",
        "xpi_name": "liverebuild-firefox-nmstudio.xpi"
    }
}

def create_zip(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, source_dir)
                zipf.write(filepath, arcname)

def build_all():
    os.makedirs(DIST, exist_ok=True)
    
    # Read base files
    with open(os.path.join(SRC, "swarm.js"), "r", encoding="utf-8") as f:
        base_swarm_code = f.read()

    with open(os.path.join(SRC, "background.js"), "r", encoding="utf-8") as f:
        base_background_code = f.read()

    print("🚀 Starting LiveRebuild by NMstudio Multi-Browser Build Pipeline...\n")

    for key, cfg in BROWSERS.items():
        out_folder = os.path.join(DIST, f"{key}-extension")
        if os.path.exists(out_folder):
            shutil.rmtree(out_folder)
        os.makedirs(out_folder, exist_ok=True)

        # 1. Generate Manifest
        manifest = {
            "manifest_version": 3,
            "name": cfg["name"],
            "version": "1.2.0",
            "author": "NMstudio",
            "description": cfg["description"],
            "action": {
                "default_title": f"{cfg['name']} (Alt+Shift+S)",
                "default_icon": {
                    "16": "icons/icon16.png",
                    "32": "icons/icon32.png",
                    "48": "icons/icon48.png",
                    "128": "icons/icon128.png"
                }
            },
            "icons": {
                "16": "icons/icon16.png",
                "32": "icons/icon32.png",
                "48": "icons/icon48.png",
                "128": "icons/icon128.png"
            },
            "permissions": [
                "activeTab",
                "scripting"
            ],
            "commands": {
                "_execute_action": {
                    "suggested_key": {
                        "default": "Alt+Shift+S",
                        "mac": "Alt+Shift+S"
                    },
                    "description": f"Rebuild this page with {cfg['name']}"
                }
            }
        }

        if cfg["is_chromium"]:
            manifest["background"] = {
                "service_worker": "background.js"
            }
        else:
            manifest["background"] = {
                "scripts": ["background.js"]
            }
            manifest["browser_specific_settings"] = {
                "gecko": {
                    "id": "liverebuild-nmstudio@sabbu.addons",
                    "strict_min_version": "142.0",
                    "data_collection_permissions": {
                        "required": ["none"]
                    }
                }
            }

        with open(os.path.join(out_folder, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        # 2. Write swarm.js with theme lock if specified
        swarm_code = base_swarm_code
        if cfg["theme_id"] != "auto":
            # Force the specific browser theme if specified
            theme_inject = f'window.__swarmBrowserTheme = "{cfg["theme_id"]}";\n'
            swarm_code = theme_inject + swarm_code

        with open(os.path.join(out_folder, "swarm.js"), "w", encoding="utf-8") as f:
            f.write(swarm_code)

        # 3. Write background.js
        with open(os.path.join(out_folder, "background.js"), "w", encoding="utf-8") as f:
            f.write(base_background_code)

        # 4. Copy icons
        shutil.copytree(os.path.join(SRC, "icons"), os.path.join(out_folder, "icons"))

        # 5. Create zip
        zip_path = os.path.join(DIST, cfg["zip_name"])
        create_zip(out_folder, zip_path)

        if "xpi_name" in cfg:
            xpi_path = os.path.join(DIST, cfg["xpi_name"])
            shutil.copy2(zip_path, xpi_path)

        print(f"  ✓ [{key.upper()}] -> {out_folder}")
        print(f"    📦 Archive: {zip_path}")
        if "xpi_name" in cfg:
            print(f"    🦊 XPI: {xpi_path}")

    print("\n🎉 ALL BUILDS COMPLETED SUCCESSFULLY IN dist/ !")

if __name__ == "__main__":
    build_all()
