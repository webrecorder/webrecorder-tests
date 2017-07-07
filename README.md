# webrecorder-tests

QA tests for webrecorder player

## required tools
python3, selenium, chromedriver, google chrome (headless)

## tests manifest

`manifest.yml` describe a list of warc files with the relative selenium tests to run with.  

structure:

    tests:
        {{ TEST_ID }}:
        warc-file: {{ WARC_FILE }}
        recordings:
        - 
            description: {{ DESCRIPTION }}
            url: {{ URL }}
            time: {{ RECORDING_TIME }}
            test: {{ TEST_FUNC }}
        - 

**TEST_ID**: test identifier  
**WARC_FILE**: warc file (will be downloaded from a s3 bucket)  
**TEST_DESCRIPTION**: brief description of the recorded content  
**URL**: URL of the recorded content  
**TIME**: time (YYYYMMDDhhmmss) of the recorded content  