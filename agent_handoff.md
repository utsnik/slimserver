# Agent Handoff Document: SqueezeOS Firmware Development

This document serves as a comprehensive summary of the recent development work to build, patch, and deploy SqueezeOS V9 firmware for the Squeezebox Radio (`baby`). It contains all necessary credentials, paths, and context for another AI agent to resume this project seamlessly.

---

## 🏗 Infrastructure & Credentials

### 1. Build Server (Compilation Environment)
- **IP Address:** `10.1.4.164`
- **Username:** `utking`
- **SSH Key Path (Local):** `C:\Users\Igland\.ssh\oracle_key`
- **Docker Image:** `ghcr.io/utsnik/squeezeos_builder:v9` (This container represents the fully patched, modernized build environment).
- **Build Workspace:** `/home/utking/squeezeos-build/`
- **Build Scripts (Local):** Located in `c:\Users\Igland\Antigravity\Lyrion media server\` (e.g., Python scripts heavily used to remote-execute patches and trigger builds).
- **Primary Build Trigger:** `.\trigger_build_robust.bat` (Local script wrapping SSH bitbake commands).

### 2. Lyrion Media Server (LMS) Server (Deployment Target)
- **IP Address:** `10.1.1.200`
- **Username:** `utking`
- **Password:** `Oxford18.`
- **Firmware Updates Directory:** `/var/lib/squeezeboxserver/cache/updates/`
- **Note on Deployment:** Locally compiled firmware must use a `custom.` prefix (e.g., `custom.baby.bin` and `custom.baby.version`) inside this directory to be recognized by LMS and offered to the radio as an OTA update.

### 3. Squeezebox Radio (Target Device)
- **IP Address:** `10.1.1.60`
- **Machine Codename:** `baby`

---

## 🛠 Project Status & Completed Work

### 1. Codebase Baseline
The repository was successfully migrated away from the legacy `public/7.8` branch. We are now working off **Ralph Irving's `public/9.0` community branch**, heavily modified for performance and modern compilation. Changes were committed and pushed to the remote `feature/radio-performance` branch.

### 2. Major Bug Fixes & Resolutions
The Yocto/Bitbake environment required significant surgical patching to compile on modern host OS environments and GCC toolchains:
- **`perl-native`:** Failed to link math/real-time libraries (`-lm -lrt`). Fixed by injecting these directly into `config.sh` before regenerating `Makefile.SH`.
- **`openssl`:** Failed to locate headers (`stdio.h`). Fixed by re-creating critical `usr/include` symlinks directly in the cross-compilation sysroot staging area.
- **`alsa-utils`:** Linker error due to missing standalone `libtinfo`. Fixed via surgical `sed` replacement during the `do_configure` stage.
- **`opkg-native`:** Failed due to strict GCC warnings. Fixed by appending `--disable-werror` and `-Wno-error`.
- **`squeezecenter`:** Resiliency patches added to `squeezecenter_svn.bb` to cleanly ignore missing/deleted default plugins (like Amazon) instead of aborting the build.
- **Environmental Staging:** Recovered from severe bitbake `tmp` directory corruption by manually rebuilding `/usr/bin`, `/usr/lib`, and staging targets.

### 3. Performance Optimizations ("Snappiness Patch")
Adapted a legacy v7.8 UI optimization patch for the V9 architecture (where UI definitions were migrated from C to Lua).
- **UI Transition Speed:** Modified `share/jive/ui/Window.lua` to decrease `HORIZONTAL_PUSH_TRANSITION_DURATION` from 500ms to 200ms.
- **Memory Management:** Added explicit `collectgarbage("collect")` hooks before heavy UI drawing operations.
- **Frame Rate:** Hardcoded `JIVE_FRAME_RATE` to 30fps in `src/ui/jive.h`.
- **Compiler Flags:** Added `-O2 -pipe -fomit-frame-pointer` targeting `arm926ejs` architecture in Yocto machine tune files.

### 4. Firmware Generation Pipeline
Successfully generated `baby_9.0.2_r17111.bin` and its accompanying `.version` checksum string. Automated deployment scripts (`deploy_firmware.py` and `rename_lms_custom.py`) were written to tunnel files from the build server straight to the LMS update cache.

---

## 🚀 V9.1 Roadmap & Next Steps

When resuming this objective, the immediate goal is to pivot from simply achieving *build stability* to exploring *architectural enhancements* (V9.1 Firmware).

**Priority Initiatives:**
1. **Native `squeezelite` Playback Engine:**
   - Uncomment the `IMAGE_INSTALL += "squeezelite"` line in `meta-squeezeos/conf/machine/baby.conf`.
   - Compile `squeezelite` specifically for `armv5te`.
   - Script the transition of `squeezeplay` to act purely as a headless remote UI, routing raw `squeezelite` audio output directly to the ALSA backend.
2. **Further Performance Enhancements:**
   - Explore compiling the core with aggressive GCC vectorization flags (`-ftree-vectorize`).
   - Profile kernel 2.6.26 boot times and strip unnecessary boot drivers.
   - Adjust Real-Time (RT) thread priority scheduling explicitly favoring the ALSA playback stream over Lua Jive rendering.
3. **WPA3 Assessment:**
   - Given the strict proprietary limitations of the Atheros AR6002 Wi-Fi architecture, investigate ethernet bridging or kernel module hacks for "SAE Transition Mode" compatibility.
