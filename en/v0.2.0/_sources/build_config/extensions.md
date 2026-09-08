---
title: Extensions & Customization
status: STABLE
---

# Extensions & Customization

## Adding New CMake Modules

1. Create a `.cmake` file in `cmake/modules/`
2. Add it to the module loading list in `telink_default.cmake`

```cmake
# telink_default.cmake
list(APPEND telink_cmake_modules my_module)
```

## Extending West Commands

1. Create a command implementation file in `scripts/west_commands/`
2. Register the command in `scripts/west-commands.yml`

```yaml
# west-commands.yml
west-commands:
  - file: scripts/west_commands/my_command.py
    commands:
      - name: tl-mycmd
        class: MyCommand
        help: my custom command
```

3. Implement the command class:

```python
from west.commands import WestCommand

class MyCommand(WestCommand):
    def __init__(self):
        super().__init__('tl-mycmd', 'my custom command', '...')

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name, help=self.help)
        return parser

    def do_run(self, args, unknown_args):
        print("Hello from my custom command!")
```

## Adding Kconfig Configuration

1. Create or modify a Kconfig file in the appropriate location
2. Integrate into the configuration tree using the `rsource` directive

```kconfig
# Add my_feature/Kconfig
menu "My Feature"

config MY_FEATURE_ENABLED
    bool "Enable my feature"
    default n
    help
        Enable custom feature.

endmenu
```

Then include it in the parent Kconfig:

```kconfig
# Kconfig.build
rsource "my_feature/Kconfig"
```

## Adding New Applications

1. Create an application directory at any location
2. Add `CMakeLists.txt` and source files
3. Build:

```bash
west tl-build /path/to/my_app --board TLSR9528A_EVK
```

### CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.20.0)
find_package(Telink REQUIRED HINTS $ENV{TELINK_BASE})
project(MyApp LANGUAGES C CXX)

file(GLOB C_SOURCES "*.c")
target_sources(Telink PRIVATE ${C_SOURCES})

if(CONFIG_TLK_ALLOW_CPP_WRAPPERS)
    file(GLOB CPP_SOURCES "*.cpp")
    target_sources(Telink PRIVATE ${CPP_SOURCES})
endif()
```

## West Command Behavior Notes

West command availability depends on the current working directory:

- **Inside a West workspace**: Loads UniSDK extension commands (`tl-build`, `tl-boards`, `tl-socs`, etc.)
- **Outside a workspace**: Only shows West built-in commands

West discovers extensions through the following mechanism:
1. Searches upward from the current directory for `.west/config`
2. Loads `west-commands` declarations from `west.yml`
