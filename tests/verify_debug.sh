#!/bin/bash
# Check the variable's value
if [ "$DEBUG" != "True" ]; then
  echo "Error: Debug is not set to True."
  exit 1
fi