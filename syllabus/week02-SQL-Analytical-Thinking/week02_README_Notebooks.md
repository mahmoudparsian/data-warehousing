Given the following data:

% head insurance
head: insurance: No such file or directory
example_1_insurance (main *) % head insurance.csv
age,gender,bmi,children,smoker,region,charges
19,female,27.9,0,yes,southwest,16884.924
18,male,33.77,1,no,southeast,1725.5523
28,male,33,3,no,southeast,4449.462
33,male,22.705,0,no,northwest,21984.47061
32,male,28.88,0,no,northwest,3866.8552
31,female,25.74,0,no,southeast,3756.6216
46,female,33.44,1,no,southeast,8240.5896
37,female,27.74,3,no,northwest,7281.5056
37,male,29.83,2,no,northeast,6406.4107


Create a Jupyter notebook with the following cells:

1. create a duckdb connection

2. read insurance.csv and create a table called insurance

3. # TODO: write query for top 3 per region

4. 2) Compare to Regional Average

5. ## 3) Above-Average Customers

6. % of Total Contribution

7. Running Total by Age

8. Do smokers pay more for insurance?

9. Does BMI impact insurance charges

10. Are smokers related to high BMI?

