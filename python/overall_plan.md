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
 - design a proper ERD for the database and decide how to connect it to the existing classes aka models 
 - add ci/cd to run the tests on pr creation 
 - extract code coverage 
 - dockerize the project
 - compose the project ( docker-compose for local implementation )
 - might need a helm chart or k8s deployment defintion , depends on the task requirments afterwards ( we will see ?)