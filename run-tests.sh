#!/usr/bin/env sh

if [ "$TEST" = "pywb" ]; then
    pytest -m "pywbtest"
elif [ "$TEST" = "player" ]; then
    pytest -m "wrplayertest"
else
    pytest
fi
