# 1. How to design a star schema?

source: https://stackoverflow.com/questions/938318/how-to-design-a-star-schema

I am confused where should I start to design a star schema.

for example I have tables in database as follows:

~~~text
  Branch(branchNo, bStreetAddress, bCity)
  
  LoanManager(empNo, empName, phone, branchNo)
  
  Customer(custNo, custName, profession, streetAddress, city, state)
  
  Account(accNo, accType, balance, accDate, custNo)
  
  LoanContract(contractNo, loanType, amount, loanDate, empNo, custNo)
~~~

I want to design a data-warehouse to analysis the loads such as :

* The total amount of loans in 2008.

* For the type of loans with more than 10 loan contracts, 
  the type of loan and the number of contracts

## 2. Questions?

* When creating a star schema, what where should I start?

* For what I understanding, all the star schemas must have 
a center, and the center fact table, contains "Measures" 
and "Relations to other fact tables".

* So, is it that, when designing the star schema, 
we always start from the center, confirm what are 
the measure first? and then choose proper relation 
to another fact table?

* But I still have another question, what should we 
choose to be Measures? When choosing measures, what 
question should I ask myself?

## Answer

* The design of a star schema is always driven by 
the client's business needs. 

* What are the questions asked? How fine-grained should the answers be?

* In your example, interesting questions might be 
	* "Number of Contracts by Branch or LoanManager" or 
	* "Managed sum of Loans by Branch or LoanManager". 

In this case, `Branch` and LoanManager would become your 
dimensions while `Count(LoanContract)` and `Sum(LoanContract.amount)`
would be your measures. A common additional dimension is time, 
usually week or quarter.

## Schema

The schema for answering those questions could look like this:

~~~ text
   DimBranch ( branchNo )
   
   DimLoanManager ( empNo )
   
   DimQuarter ( year, qNo )  -- qNo in (1,2,3,4)
   
   DimWeek ( year, weekNo )  -- weekNo in (0..53), depending on business rules
~~~

Measures ( branchNo, empNo, year, qNo, weekNo, numContracts, sumLoans )

For the business questions you already posed in your question, the 
dimensions and measures would be such:

~~~text
   dimension: year, measure: Sum(LoanContract.amount)
   
   dimension: loanType, measure: Count(LoanContract)
~~~

Putting those two into the same star schema doesn't make much sense, 
since they neither share dimensions or measures.
