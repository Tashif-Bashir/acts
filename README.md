# Acts Common Tracking Software

or *A Common Tracking Software* if you do not like recursive acronyms

[![10.5281/zenodo.5141418](https://zenodo.org/badge/DOI/10.5281/zenodo.5141418.svg)](https://doi.org/10.5281/zenodo.5141418)
[![Chat on Mattermost](https://badgen.net/badge/chat/on%20mattermost/cyan)](https://mattermost.web.cern.ch/acts/)
[![codecov](https://codecov.io/gh/acts-project/acts/graph/badge.svg)](https://codecov.io/gh/acts-project/acts)
[![Latest release](https://badgen.net/github/release/acts-project/acts)](https://github.com/acts-project/acts/releases)
[![Status](https://badgen.net/github/checks/acts-project/acts/main)](https://github.com/acts-project/acts/actions)
[![Metrics](https://badgen.net/badge/metric/tracker/purple)](https://acts-project.github.io/metrics/)

Acts is an experiment-independent toolkit for (charged) particle track
reconstruction in (high energy) physics experiments implemented in modern C++.

More information can be found in the [Acts documentation](https://acts.readthedocs.io/).

## Quick start

Acts is developed in C++ and is build using [CMake](https://cmake.org). Building
the core library requires a C++17 compatible compiler,
[Boost](http://boost.org), and [Eigen](http://eigen.tuxfamily.org). The
following commands will clone the repository, configure, and build the core
library

```sh
git clone https://github.com/acts-project/acts <source>
cmake -B <build> -S <source>
cmake --build <build>
```

For more details, e.g. specific versions and additional dependencies, have a
look at the [getting started guide](docs/getting_started.md). If you find a bug,
have a feature request, or want to contribute to Acts, have a look at the
[contribution guidelines](CONTRIBUTING.rst).

## Versioning and public API

Release versions follow [semantic versioning](https://semver.org/spec/v2.0.0.html)
to indicate whether a new version contains breaking changes within the public API.
Currently, only a limited part of the visible API is considered the public API
and subject to the semantic versioning rules. The details are outlined in the
[versioning and public API documentation](docs/versioning.rst).

## Repository organization

The repository contains all code of the Acts projects, not just the core library
that a physics experiment is expected to use as part of its reconstruction code.
All optional components are disabled by default. Please see the
[getting started guide](docs/getting_started.md) on how-to enable them.

-   `Core/` contains the core library that provides functionality in the `Acts`
    namespace.
-   `Plugins/` contains plugins for core functionality that requires
    additional external packages. The functionality also resides in the `Acts`
    namespace.
-   `Fatras/` provides fast track simulation tools based on the core
    library. This is not part of the core functionality and thus resides in the
    separate `ActsFatras` namespace.
-   `Examples/` contains simulation and reconstruction examples. These are
    internal tools for manual full-chain development and tests and reside in
    the `ActsExamples` namespace.
-   `Tests/` contains automated unit tests, integration tests, and
    (micro-)benchmarks.
-   `thirdparty/` contains external dependencies that are usually not available
    through the system package manager.

## Authors and license

Contributors to the Acts project are listed in the [AUTHORS](AUTHORS) file.

The Acts project is published under the terms of the Mozilla Public License, v. 2.0.
A copy of the license can be found in the [LICENSE](LICENSE) file or at
http://mozilla.org/MPL/2.0/ .

The Acts project contains copies of the following external packages:

-   [OpenDataDetector](https://github.com/acts-project/OpenDataDetector)
    licensed under the MPLv2 license.

# Other Useful Guides
## SonarCloud Analysis Setup for C++ Repository Using GitHub Actions
This guide will help you set up SonarCloud analysis for your Acts repository on GitHub using GitHub Actions. Follow the steps below to ensure your code is analyzed for quality, bugs, vulnerabilities, and code smells.

## Step 1: Create a SonarCloud Account
Go to SonarCloud website: Open your browser and go to sonarcloud.io.
Sign up or Log in: If you don't have an account, sign up using your GitHub account for convenience.
## Step 2: Create a SonarCloud Project
Go to 'My Projects': Once logged in, click on 'My Projects' from the dashboard.
Add a New Project: Click on the 'Add new project' button.
Import your GitHub Repository: Choose 'GitHub' and select the repository you want to analyze. Authorize SonarCloud to access your GitHub account and repositories.
Set Up the Project: Follow the prompts to complete the project setup.
## Step 3: Generate a SonarCloud Token
After linking sonarcloud with your github and selecting the repository, navigate to the project on sonar cloud and click on the settings button from the side bar. 
Click on 'Analysis Method' and here you will find the Sonar Token and secret. 
## Alternatively: 
Go to Security: In your SonarCloud account, navigate to your account settings and find the 'Security' section.
Generate a New Token: Click on 'Generate Tokens', give it a name (e.g., 'GitHub Actions Token'), and click 'Generate'. Copy the token and save it for later use.

## Step 4: Add the SonarCloud Token to GitHub Secrets
Go to Your GitHub Repository: Navigate to your GitHub repository.
Open Settings: Click on the 'Settings' tab at the top of the repository page.
Access Secrets: In the left sidebar, click on 'Secrets' and then 'Actions'.
Add a New Secret: Click the 'New repository secret' button. Name it SONAR_TOKEN and paste the token you copied from SonarCloud. Click 'Add secret'.

## Step 5: Create GitHub Actions Workflow File
Open the Code Tab: In your GitHub repository, go to the 'Code' tab.
Create a New File: Click the 'Add file' button and select 'Create new file'.
Name the File: Name your file .github/workflows/sonarcloud-analysis.yml.

## Step 6: add Workflow Configuration 
Copy and paste the following YAML code into your new file:
```sh
name: Sonar Cloud

on:
  push:
  pull_request:
    branches:
      - main
      - 'release/**'
      - 'develop/**'
    paths-ignore:
      - "docs/**"

jobs:
  sonarUbuntu:
    name: Sonar-Ubuntu
    runs-on: ubuntu-latest
    env:
      SONAR_SCANNER_VERSION: 5.0
      SONAR_SERVER_URL: "https://sonarcloud.io"
      BUILD_WRAPPER_OUT_DIR: build_wrapper_output_directory # Directory where build-wrapper output will be placed
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Shallow clones should be disabled for a better relevancy of analysis
      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: 17
          distribution: 'oracle'
      - name: Set up Python 3.9 for gcovr
        uses: actions/setup-python@v4
        with:
          python-version: 3.9
      - name: Install Boost
        run: |
             sudo apt-get update
             sudo apt-get install -y libboost-all-dev
      - name: install gcovr 5.0
        run: |
          pip install gcovr==5.0 # 5.1 is not supported
      - name: Install sonar-scanner
        uses: SonarSource/sonarcloud-github-c-cpp@v2
        
      - name: Run build-wrapper
        run: |
          mkdir build-linux
          cmake -S . -B build-linux -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -D ACTS_USE_SYSTEM_BOOST=OFF -D ACTS_USE_SYSTEM_EIGEN3=OFF -D ACTS_BUILD_UNITTESTS=ON -D ACTS_BUILD_INTEGRATIONTESTS=ON -DCMAKE_CXX_FLAGS="--coverage"
    
          build-wrapper-linux-x86-64 --out-dir ${{ env.BUILD_WRAPPER_OUT_DIR }}  cmake --build build-linux --clean-first -j $(nproc)
          

      - name: Run tests to generate coverage statistics
        run: |
          find ./build-linux/bin -maxdepth 1 -name "*Test*" -executable -exec '{}' ';'
      - name: List coverage files
        run: find ./build-linux -name "*.gcda" -or -name "*.gcno"
        
      - name: Collect coverage into one XML report
        run: |
          gcovr --sonarqube > coverage.xml
          gcovr --sonarqube --root=build-linux --output=coverage.xml  --filter="^/home/runner/work/acts/acts/"
          
          
      - name: Run sonar-scanner
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: |
          sonar-scanner \
            -Dsonar.cfamily.compile-commands=/home/runner/work/acts/acts/build-linux/compile_commands.json \
            --define sonar.coverageReportPaths=coverage.xml
```


### Step 7: Create Another file named sonar-project.properties and add the following snipet: 
```sh
sonar.projectKey=
sonar.organization=


sonar.cfamily.threads=4
sonar.cfamily.compile-commands=/home/runner/work/acts/acts/build-linux/compile_commands.json
sonar.coverageReportPaths=coverage.xml
sonar.exclusions=coverage.xml
```

## Note here:
Replace Project Key: Replace YOUR_PROJECT_KEY with the project key from SonarCloud.
Replace Organization Name: Replace YOUR_ORGANIZATION_NAME with your SonarCloud organization name.

## Step 7: Customize the Workflow Configuration
Replace Project Key: Replace YOUR_PROJECT_KEY with the project key from SonarCloud.
Replace Organization Name: Replace YOUR_ORGANIZATION_NAME with your SonarCloud organization name.

## Step 8: Commit the Changes
Commit New File: Scroll down to the bottom of the page, add a commit message (e.g., "Add SonarCloud analysis workflow"), and choose 'Commit directly to the main branch'.
Commit Changes: Click 'Commit new file'.

## Step 9: Verify the Setup
Push Code to GitHub: Push any code to the main branch or create a pull request to the main branch to trigger the workflow.
Check Actions Tab: Go to the 'Actions' tab in your GitHub repository to see the workflow run. Check the details and logs to ensure everything is working correctly.

## Step 10: View SonarCloud Results
Go to SonarCloud Dashboard: Open your SonarCloud account and go to the dashboard.
Select Your Project: Click on your project to view the analysis results, including code quality, bugs, vulnerabilities, and code smells.
