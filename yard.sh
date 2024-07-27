#!/bin/bash
doc_targets=(
    "app/controllers/topics_controller.rb"
    "app/models/topic.rb"
)

yard doc "${doc_targets[@]}"

yard server
