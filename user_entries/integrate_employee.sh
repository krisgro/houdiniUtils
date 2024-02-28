#!/bin/bash

#system_integration step
python system_integration.py

#create user data package
python create_package_json.py

#copy package file into Houdini 
cp packages/company_vars.json C:/Users/Kris/Documents/houdini20.0/packages

echo "All steps done!"