---
title: Development Environment Setup
status: STABLE
---

# Development Environment Setup

This chapter describes how to install and configure the UniSDK development environment. The recommended approach is to use the Telink VS Code Extension, which provides a graphical interface for managing dependencies. Alternatively, you can set up the environment from the command line.

## VS Code Extension (Recommended)

The **Telink Development Tool** VS Code Extension provides a graphical interface for installing dependencies, managing the toolchain, and initializing the workspace with a single click.

### Prerequisites

- **VS Code**: Install the latest version of [Visual Studio Code](https://code.visualstudio.com/).

> If your VS Code version is not the latest, the extension may not work properly or some features may not function as expected.

### Step 1: Install the Telink VS Code Extension

1. Launch VS Code.
2. Click the **Extensions** icon in the left activity bar (or press **Ctrl+Shift+X**).
3. Search for **Telink**.
4. Find **Telink Development Tool** in the results and click **Install**.

![Telink DEVELOPMENT Icon](pics/telink_development_icon.png)

After installation, a **Telink DEVELOPMENT** icon will appear on the left sidebar.

> To facilitate automatic identification of the Unified SDK by subsequent tools, open the Unified SDK folder in VS Code after completing the installation.

### Step 2: Install Dependencies via the Extension

1. Click the **Telink DEVELOPMENT** button in the left sidebar.
2. In the **DEVELOPMENT TOOLS** tree, you will see the required components: **Toolchain**, **West**, **CMake**, and **Ninja**.
3. Install each component:
   - **Toolchain**: Click the toolchain entry and select **Install Toolchain**.
   - **West**: Right-click **West** and select **Install**. We recommend using a Python virtual environment for West.
   - **CMake**: Right-click **CMake** and select **Install**.
   - **Ninja**: Right-click **Ninja** and select **Install**.

![Dependency Installation](pics/dependency_installation.png)
![Dependency Installation Success](pics/dependency_installation_success.png)

Wait for each component to finish installing. A notification appears in the bottom-right corner when installation is complete.

### Step 3: Initialize the West Workspace

1. In the **Telink DEVELOPMENT** view, locate the **West Command** section.
2. Click the **init** button.

![West Init](pics/west_init.png)

3. Check the **OUTPUT** terminal panel. A confirmation message appears when initialization completes successfully.

![West Init Success](pics/west_init_success.png)

### Step 4: Verify the Environment

1. In the **West Command** section, click the **tl-build** button.
2. A linker error is expected because no source directory has been configured yet. This indicates that the toolchain, build system, and West environment are configured correctly.

![Expected Linker Error](pics/expected_linker_error.png)


## CLI Setup (Alternative)

If you prefer to set up the development environment from the command line, refer to the platform-specific guides:

- [Linux Environment Setup](../developing/setup_linux.md)
- [Windows Environment Setup](../developing/setup_windows.md)
- [macOS Environment Setup](../developing/setup_macos.md)

## Next Steps

After completing the environment setup, proceed to [Get and Import the SDK](get_sdk.md).
