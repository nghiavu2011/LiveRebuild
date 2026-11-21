# Privacy Policy: LiveRebuild by NMstudio

_Last updated: November 2026 (v1.2.0)_

LiveRebuild by NMstudio does not collect, store, sell, or transmit any personal data.

- **Nothing runs until you click.** The extension uses the `activeTab` permission, so it can only touch the tab you clicked the icon on or triggered via shortcut, and only at that moment.
- **Everything stays on your device.** To rebuild a page, the extension reads the page's layout and styles in your browser. For WebGL canvases, playing videos, and embedded frames, it takes one screenshot of the visible tab and crops those regions out. The page snapshot and the screenshot live only in that tab's memory and are discarded when you exit or leave the page.
- **No network requests.** The extension does not contact any external server, use analytics, or load remote code. The only network activity comes from the page's own images and videos, which the browser loads directly while rebuilding.
- **Sound is synthesized, not recorded.** The music and mechanical keyboard sound effects are synthesized in your browser using the native Web Audio API. The extension never uses your microphone.
- **Screen recording stays 100% local.** If you choose to use the "🎥 Quay clip" recording button, video capture is processed locally in your browser via the native `MediaRecorder` API. The recorded `.webm` file is saved directly to your local downloads folder and is never transmitted anywhere.
- **No accounts, cookies, or storage.** Nothing is written to `localStorage`, cookies, or remote databases.

## Permissions

| Permission | Why |
| :--- | :--- |
| `activeTab` | Lets the extension run on the current tab when you click its icon or press its shortcut, and capture regions of that tab. |
| `scripting` | Injects the animation script into that tab and briefly hides non-media elements for the media screenshot. |

## Contact & Issues

Questions or issues: please visit <https://github.com/nghiavu2011/LiveRebuild/issues>.
