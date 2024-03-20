#!/bin/bash

MAIN_FOLDER="E:/Projects/Coding/Python_for_Production/Week_06/houdiniUtils/assets/"

for SUBFOLDER in "$MAIN_FOLDER"/*; do
    if [ -d "$SUBFOLDER" ]; then
        echo "Processing $SUBFOLDER"
        
        hython run_on_template.py "E:/Projects/Coding/Python_for_Production/Week_06/assetMigration_toUSD_v001.hipnc" "$SUBFOLDER"
        echo "Finished Processing!"
        sleep 2
    fi
done

