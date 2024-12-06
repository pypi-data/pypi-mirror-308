# corallium

Shared functionality for the calcipy-ecosystem.

## Installation

1. `poetry add corallium`

1. Take advantage of the logger or other common functionality

    ```sh
    form corallium.log import LOGGER

    LOGGER.info('Hello!')
    ```

## Usage

<!-- < TODO: Show an example (screenshots, terminal recording, etc.) >

- **log**: TBD
- **pretty_process**: TBD
- **shell**: TBD
- **file_helpers**: TBD
- **tomllib**: This is a lightweight wrapper to backport `tomli` in place of `tomllib` until we can use Python >3.11. Use with `from corallium.tomllib import tomllib`
- **dot_dict**: has one function `ddict`, which is a light-weight wrapper around whatever is the most [maintained dotted-dictionary package in Python](https://pypi.org/search/?q=dot+accessible+dictionary&o=). Dotted dictionaries can sometimes improve code readability, but they aren't a one-size fits all solution. Sometimes `attr.s` or `dataclass` are more appropriate.
    - The benefit of this wrapper is a stable interface that can be replaced with better internal implementations, such [Bunch](https://pypi.org/project/bunch/), [Chunk](https://pypi.org/project/chunk/), [Munch](https://pypi.org/project/munch/), [flexible-dotdict](https://pypi.org/project/flexible-dotdict/), [classy-json](https://pypi.org/project/classy-json/), and now [Python-Box](https://pypi.org/project/python-box/)
 -->

For more example code, see the [scripts] directory or the [tests].

## Project Status

See the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].

## Contributing

We welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:

- [DEVELOPER_GUIDE]
- [STYLE_GUIDE]

## Code of Conduct

We follow the [Contributor Covenant Code of Conduct][contributor-covenant].

### Open Source Status

We try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/corallium)

## Responsible Disclosure

If you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).

## License

[LICENSE]

[changelog]: https://corallium.kyleking.me/docs/CHANGELOG
[code_tag_summary]: https://corallium.kyleking.me/docs/CODE_TAG_SUMMARY
[contributor-covenant]: https://www.contributor-covenant.org
[developer_guide]: https://corallium.kyleking.me/docs/DEVELOPER_GUIDE
[license]: https://github.com/kyleking/corallium/blob/main/LICENSE
[scripts]: https://github.com/kyleking/corallium/blob/main/scripts
[style_guide]: https://corallium.kyleking.me/docs/STYLE_GUIDE
[tests]: https://github.com/kyleking/corallium/blob/main/tests
