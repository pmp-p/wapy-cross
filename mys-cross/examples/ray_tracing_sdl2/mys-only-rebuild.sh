#!/bin/bash

reset
rm build/app*

TARGET=wasm_1_emscripten python3.9 -u -B ../../mys-cross build ; python3.9 -m http.server


