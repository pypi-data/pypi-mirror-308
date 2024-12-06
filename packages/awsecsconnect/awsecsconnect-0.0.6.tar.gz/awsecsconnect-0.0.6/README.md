# awsecsconnect

https://www.notion.so/Start-a-shell-on-any-backend-container-121a349afecb803ebc33ed4d81abd953?pvs=4

Tired of typing a series of `aws` cli commands to get the arns and container name I need, when trying
to just open up a shell in that container.  

Usage: `awsecsconnect`

Dependencies: This assumes that you have AWS Profile environment variables set up already, and that you can
execute the aws cli using `aws`.  

## Notes
- This uses boto3 to get most of the details, but ultimately still depends on having the AWS CLI installed,
  because the execution of an interactive shell is a whole client unto itself.
- This package is published publicly to PYPI so that it can be conveniently installed with pip. Ultimately,
  this is not an open source project and not publicly maintained or documented (yet?).  I've registered
  this in pypi under my personal account just to keep SV1 names out of the picture. You don't REALLY need
  pypi to use this - you can just run it directly from the source - but a global package is very convenient. 

# Install
The latest tested build is available via pip:  `pip install --upgrade awsecsconnect`. 

# Build
`python -m build` will create builds in ./dist/

# Publish
Using twine with an api key, publish a new specific to pypi:
`twine upload --repository pypi dist/awsecsconnect-0.0.4*`

The build number is in the project file, and needs to be updated to create a valid downloadable pypi build.
