# dnd_firefly

Programmatically Drag and Drop Files into Firefly Viewer

## Overview

`dnd_firefly` is a command-line tool that allows you to programmatically upload local files to the [Firefly Viewer](https://irsa.ipac.caltech.edu/irsaviewer/) (IRSA Viewer tool) by simulating a drag-and-drop action. This tool is particularly useful for automating data uploads and integrating with scripts or workflows that interact with the Firefly Viewer.

## Features

- **Automate File Uploads:** Upload files to the Firefly Viewer without manual intervention.
- **Simulate Drag-and-Drop:** Programmatically simulate the drag-and-drop action to upload files.
- **Easy Integration:** Integrate seamlessly with existing data processing pipelines or scripts.

## Installation

You can install `dnd_firefly` directly from PyPI using `pip`:

```bash
pip install dnd_firefly
```

**Note:** `dnd_firefly` requires Python **3.11** or higher.

## Requirements

- **Python 3.11+**
- **Google Chrome Browser:** Ensure that the latest version of Chrome is installed on your system.

## How It Works

The tool uses **Selenium WebDriver** to automate a Chrome browser session. It opens the Firefly Viewer and simulates the drag-and-drop action to upload your specified file.

**Selenium Manager:** Starting from Selenium 4.6.0, Selenium includes Selenium Manager, which automatically manages the browser driver required for automation. If you have Chrome installed, Selenium will handle the rest.

## Usage

The `dnd_firefly` tool accepts one argument: the path to the local file you want to upload to the Firefly Viewer.

### Command-Line Usage

```bash
dnd_firefly /path/to/your/file.tbl
```

**Replace** `/path/to/your/file.tbl` with the actual path to your local file.

### Example

To upload a file named `WISE-allwise_p3as_psd-Cone_100asec.tbl` located in your `Downloads` folder, run:

```bash
dnd_firefly ~/Downloads/WISE-allwise_p3as_psd-Cone_100asec.tbl
```

## Troubleshooting

- **Selenium Exceptions:** If you encounter errors related to Selenium WebDriver, ensure that you have the latest version of Chrome installed and that your Selenium version is up to date.
- **Internet Access:** Selenium Manager requires internet access to download the appropriate WebDriver. If you're in an environment with restricted internet access, you may need to manually set up the WebDriver. Refer to the [Selenium documentation](https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/selenium_manager/) for more details.
- **File Path Issues:** Ensure that the file path you provide is correct and that the file exists.

## Advanced Usage (Optional)

If you need to use a different browser or have specific requirements, you can manually set up the WebDriver.

### Manual WebDriver Setup

1. **Download ChromeDriver:**
   - Visit the [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads) page.
   - Download the version that matches your installed Chrome browser version.

2. **Install ChromeDriver:**
   - Place the `chromedriver` executable in a directory that's in your system's `PATH`, or specify its location in the code.

**Note:** Manual setup is only necessary if Selenium Manager is unable to manage the WebDriver automatically.

## Contributing

Contributions are welcome! Please visit the [GitHub repository](https://github.com/ejoliet/firefly-vscode-extension.git) to report issues or submit pull requests.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Author

**Emmanuel Joliet**

- Email: [ejoliet@caltech.edu](mailto:ejoliet@caltech.edu)
- Affiliation: Caltech/IPAC