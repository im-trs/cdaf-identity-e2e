![Test Automation Process](o2c_test_flow.png)

---

# Allure Report

## _Installation Notes_
> Install Allure framework
```sh
pip install allure-behave
```

> Execute the regression pack and create the Allure Report into the folder './output/allure'
```sh
behave -f allure_behave.formatter:AllureFormatter -o output/allure ./features/regression
```
> Start the web-server to see the allure report
```sh
allure serve ./output/allure
```


---

# Behave & Allure sample runs
## _Execution Notes_

> Example: `Passing a tag`

```sh
behave -f plain --tags="@regression" features/regression
```

> Example: `filtering for file name and writing the output into output/allure`

```sh
behave -f allure_behave.formatter:AllureFormatter -o output/allure ./features/regression/496504*
```

> Example: `running formatting "pretty" to check the advancement whilst it run`

```sh
behave -f allure_behave.formatter:AllureFormatter -o output/allure ./features/regression/ -f pretty
```
