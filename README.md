# webrecorder-tests

QA tests for webrecorder player **(WORK IN PROGRESS)**

## Installation
Requires python 3.6

```
$ pip install -r requirements.txt
```
## Tests
Each test in the test suite has three parts:
1. A manifest file (`.yml`), found in the `manifests` directory
2. A single JavaScript file (`.js`) containing all the "test functions", found in the `js` directory
3. A Python file containing the actual test, found in the `tests` directory


### Manifest file
The test manifest describes the resources each test requires and has the following structure.

Please note: **all file system paths are expected to be relative to the project root**

`Required` manifest fields:
```yaml
warc-file: "{WARC_PATH}"
description: {DESCRIPTION}
url: "{URL}"
time: {RECORDING_TIME}
javascript: "{JS_FILE}"
tests:
  - {FUNCTION_NAME}
  - ...
```
* **WARC_FILE**: path to the warc file for the test
* **PORT**: port used by webrecorder player (if test requires webrecorder player)  
* **TEST_DESCRIPTION**: brief description of the recorded content  
* **URL**: URL of the recorded content  
* **TIME**: time (YYYYMMDDhhmmss) of the recorded content  
* **JS_FILE**: path to a JavaScript file containing the "tests"  
* **FUNCTION_NAME**: the name of a JavaScript function contained in the tests file `JS_FILE`

`Optional` manifest fields:
```yaml
chrome:
  {KEY}: {VALUE}
  ...
```
The optional chrome field of the manifest files is a dictionary of key value pairs corresponding to arguments used when launching headless chrome.

For more information about these arguments please see puppeteers [documentation](https://github.com/GoogleChrome/puppeteer/blob/v1.5.0/docs/api.md#puppeteerlaunchoptions).

### Test JavaScript
Each test is expected to supply a single JavaScript file containing functions that will be used to determine the results for each part of the test.

A test may supply as many functions as the writer desires but must supply at **least one**.

The functions used in a test may only return a boolean value indicating test success (true) or test failure (false).

Each function is expected to return its results within **30 seconds** otherwise we automatically consider the current test function as a `failure`.

If more time is required by a test please see the `longer tests` or `custom tests` portion of the Python part of the test suite.

Each named function found in the file is evaluated in the context of the `replayed page` once the [load event](https://developer.mozilla.org/en-US/docs/Web/Events/load) has been dispatched and can have the following signatures

```typescript
function name(): boolean

async function name(): boolean

function name(): Promise<boolean>
```

Please note the `typescript` is used only to describe the allowed function signatures and the testing framework expects **vanilla JavaScript**.

### Test Python
The python portion of the testing framework is considered as each tests `entry point` into the testing system.

Each python test must have a name that follows the following convention:
- `test_<name>.py`, where `<name>` is any name describing the test

and must be placed in the `tests` directory of this project.

The contents of each python test file (in the none-advanced case) are expected to have the following form:
```python
from .wrtest import <TestClass>

class Test<MyAwesomeTestName>(<TestClass>):
    manifest = "manifests/<your tests manifest name>"

```
Where the values of `<TestClass>`, `<MyAwesomeTestName>` and `<your tests manifest name>` are supplied by you.

The testing framework provides two classes that all tests only suppling a manifest file are expected to subclass.  
  - PywbTest: runs your test against `pywb`
  - WRPlayerTest: runs your test against `webrecorder player`

For example consider the contents of `test_youtube.py`:
```python
from .wrtest import WRPlayerTest, PywbTest


class TestYouTubePlayer(WRPlayerTest):
    manifest = "manifests/youtube.yml"


class TestYouTubePYWB(PywbTest):
    manifest = "manifests/youtube.yml"

```
The `TestYouTubePlayer` classes will have the "tests" defined in the manifest file run against `webrecorder player` because it subclasses `WRPlayerTest`.

Likewise, `TestYouTubePYWB` will have the "tests" run against `pywb` because it subclassed `PywbTest`.

This is minimal requirement for each python test file. The testing framework takes care of the rest for you :smile:

#### Longer Tests
If your test(s) require more time and you are using the provided test classes, simply add the class variable `test_to` to your test class and set it to a time in **seconds**.

```python
from .wrtest import PywbTest

class TestLongTime(PywbTest):
    manifest = "...."
    test_to = 90

```  

#### Custom Tests
See the contents of `tests/wrtest.py` and the fixture definitions founcd in `conftest.py` for more information about writing tests that to do not conform to the above example.


## Running the tests

1. `./bootstrap.sh`  
to run once: will download from S3 a binary webrecorderplayer and all the warc files listed in the manifest

2. run the tests: ``./run-tests.sh``
runs both `PywbTest` and `WRPlayerTest` tests

To only run either `PywbTest` or `WRPlayerTest` tests using the supplied shell file a environment variable named `TEST` is expected to exist with a value of "pywb" or "player" respectively.
