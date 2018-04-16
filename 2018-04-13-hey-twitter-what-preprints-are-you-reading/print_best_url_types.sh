#!/bin/bash

zcat ${1} | jq -c ".arxiv_url_types|.[]" | sort | uniq -c | sort -nr
