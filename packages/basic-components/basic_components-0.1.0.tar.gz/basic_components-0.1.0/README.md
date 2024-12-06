# basic-components

Re-usable server-side components based on shadcn/ui.
Built with JinjaX, Alpine.js, and Tailwind CSS, with support for htmx.

## Installation & Usage

### Quick Start with `uvx`

You can use the CLI directly without installing the package:

```bash
# Add components
uvx --from basic-components components add button
```

You will also need to configure your project to load components into the `jinjax.Catalog` and add a global `cn` function
to the Jinja environment. See [utilities](docs/content/docs/utilities.md)

### Package Installation Options

Install only the utility functions for JinjaX and tailwind:

```bash
# With utility functions
pip install basic-components[utils]
```

### Installation Groups

- `utils`: Utility functions for JinjaX setup and `cn()` tailwind class helper
- `docs`: Runs the docs site
- `dev`: Development tools for contributing
- `full`: All features included

## Documentation

Visit [https://components.basicmachines.co](https://components.basicmachines.co) to view the documentation.

## Contributing

Please read the [contributing guide](https://components.basicmachines.co/docs/contribution).

## License

Licensed under the [MIT license](https://github.com/shadcn/ui/blob/main/LICENSE.md).

## Components

19/48

- [x] accordion
- [x] alert
- [x] alert-dialog -- example cancel/action
- [ ] aspect-ratio
- [ ] avatar
- [x] badge
- [ ] breadcrumb
- [x] button
- [ ] calendar
- [x] card
- [ ] carousel
- [ ] chart
- [x] checkbox
- [ ] collapsible
- [ ] command
- [ ] context-menu
- [x] dialog -- examples
- [ ] drawer
- [x] dropdown-menu
- [x] form
- [ ] hover-card
- [ ] input-otp
- [x] input
- [x] label
- [x] link
- [ ] menubar
- [ ] navigation-menu
- [ ] pagination
- [x] popover
- [ ] progress
- [x] radio-group
- [ ] resizable
- [ ] scroll-area
- [x] select
- [ ] separator
- [x] sheet
- [ ] sidebar
- [ ] skeleton
- [ ] slider
- [ ] sonner
- [ ] switch
- [x] table
- [ ] tabs
- [x] textarea
- [x] toast
- [ ] toaster
- [ ] toggle-group
- [ ] toggle
- [ ] tooltip

Extended
- [ ] Prose - https://docs.astro.build/en/recipes/tailwind-rendered-markdown/#recipe