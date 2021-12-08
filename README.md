# Cohort Definition Tool

## How to Contribute

### Installation

**Python Packages**

The Cohort Definition Tool uses [pipenv](https://github.com/pypa/pipenv) to manage Python packages. In order to run an instance of the tool or to contribute to the project, users and developers must also use `pipenv`. (Packages to be installed are listed in the `Pipfile` at project root.) However, since `Pipfile.lock` created by `pipenv` contains hashes based on the operating system of the developer who last commits it, users/developers must follow the steps listed below in order to avoid package installation errors – as they potentially may have a different operating system.

```
git clone https://github.com/metaneuro/concept_query.git
cd concept_query
pipenv lock
pipenv shell
pipenv install
pipenv install -d
```

The last command (pipenv install -d) is only necessary for developers as it installs packages (for testing, linting, etc.) listed under the `dev-packages` section in the `Pipfile`.



