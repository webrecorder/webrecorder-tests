# webrecorder-tests

QA tests for webrecorder player **(WORK IN PROGRESS)**

## installation

required: python 3.6, selenium, chromedriver, google chrome (headless)


    pip3 install -r requirements.txt

    # macos 
    brew install chromedriver
    brew cask install google-chrome

## tests manifest

`manifest.yml` describe a list of warc files with the relative selenium tests to run with.  

structure:

    tests:
        {TEST_CLASS}:
        warc-file: {WARC_FILE}
        player_port: "{PORT}"
        recordings:
        - 
            description: {DESCRIPTION}
            url: {URL}
            time: {RECORDING_TIME}
            test: {TEST_FUNC}
        - 

* **TEST_CLASS**: pytest Class Name  
* **WARC_FILE**: warc file (will be downloaded from a s3 bucket)  
* **PORT**: port on which the player will be started  
* **TEST_DESCRIPTION**: brief description of the recorded content  
* **URL**: URL of the recorded content  
* **TIME**: time (YYYYMMDDhhmmss) of the recorded content  


## run

1. `./bootstrap.sh`  
to run once: will download from S3 a binary webrecorderplayer and all the warc files listed in the manifest

2. `export CHROME=/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary`  
set ENV with chrome executable.  

    TODO: if it is a local path run the tests with a local chrome (headless). if it is a SAUCELABS remote driver run the tests remote.

3. run the tests: `pytest -v`

    to evaluate: 
    * [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) to run tests in parallel
    * [pytest-assume](https://github.com/astraw38/pytest-assume) to define multiple asserts per test