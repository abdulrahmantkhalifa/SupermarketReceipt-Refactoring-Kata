## Intial thoughts 
 - need to fill the tests , to have a solid base before refactoring 
 - determine a design pattern
   - the handle offers function
     - is just too complex , with too many if conditions
     - the offers are considered business logic and too intermingled with the normal logic need to seperate this somehow 
     - given the new requirement where i need to add a new discount type , need to abstract the discounts to be able to add new ones
 - price for quantity should be dynamic and not hardcoded , to allow for extesniblitly
 - class naming conventions 
 - file naming conventions 
 - unversioned package installs 
 - type hints everywhere and doc strings if needed ( last thing )

## Step 1
 - commit plan 
 - create tasks, to seperate requirements

## step 2 
 - create the test cases 

## step 3 
 - start refactor 

## step 4 
 - add new features
 - discount bundles
 - html reciepts

## Step 5 
 - clean up code ( naming conventions )
 - add type hints and proper docs 

## step 6 ( optional if i have time ) / future plans  
* **Design a proper ERD:** An Entity-Relationship Diagram formalizes the database structure, serving as the blueprint for persistence and mapping to the existing Python models.
* **Add CI/CD to run tests:** Implement automated continuous integration pipelines to execute all unit tests upon $\text{PR}$ creation, ensuring code quality and preventing regressions.
* **Extract code coverage:** Integrate a coverage tool into the testing process to measure the percentage of code that is executed by tests, highlighting areas that need better test coverage.
* **Dockerize the project:** Create a $\text{Dockerfile}$ to package the application, its dependencies, and environment into a single, isolated image for consistent execution anywhere.
* **Compose the project:** Use **Docker Compose** to define and orchestrate the multi-container environment (e.g., app, database) for easy local setup and development.
* **Helm chart or k8s deployment:** Develop a $\text{Helm}$ chart or raw $\text{Kubernetes}$ manifests to manage the deployment, scaling, and operational aspects of the application in a production cluster.
*  **Should seperate model and business** the model definition of the shopping_cart and teller and the business logic into seperate classes where the business logic is independent and should not affect the mode defintion especially if its connected to a db
*  **Using Decimal lib to consildate float calculations** the default float rounding is not consistent and not safe to use using decimal is much more persistent and concise
*  **Convert all ints to float except when not needed** float are aplicable to most int cases , use floats instead to avoid type mismatch 