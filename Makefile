init:
    pip install -r requirements.txt

test:
    py.test main

.PHONY: init main