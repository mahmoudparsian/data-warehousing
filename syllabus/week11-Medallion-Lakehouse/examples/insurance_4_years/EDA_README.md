Consider the following test data for teaching purposes.

% ls -lR data
drwxr-xr-x@ 6 max  staff  192 Mar  3 15:17 bronze

data/bronze:
-rw-r--r--@ 1 max  staff  50185 Mar  3 23:08 insurance.2021.csv
-rw-r--r--@ 1 max  staff  50250 Mar  3 23:08 insurance.2022.csv
-rw-r--r--@ 1 max  staff  50161 Mar  3 23:08 insurance.2023.csv
-rw-r--r--@ 1 max  staff  50246 Mar  3 23:08 insurance.2024.csv

% wc -l data/bronze/*
    1301 data/bronze/insurance.2021.csv
    1301 data/bronze/insurance.2022.csv
    1301 data/bronze/insurance.2023.csv
    1301 data/bronze/insurance.2024.csv
    5204 total

% head data/bronze/insurance.2021.csv
age,gender,bmi,children,smoker,region,charges
22,female,23.2,1,no,northwest,5605.93
54,male,30.6,0,no,northeast,7118.87
48,male,31.31,0,yes,southwest,40381.51
38,female,27.49,0,yes,southwest,21178.05
38,male,33.1,0,no,northwest,12829.41
58,female,25.56,1,no,northeast,12468.18
22,male,33.56,1,no,northwest,6807.32
50,female,33.82,0,yes,northeast,25883.3
27,male,15.5,0,no,southwest,5068.98

With this data, please provide a
complete EDA in Jupyter notebook,
shall we use DuckDB?

Your notebook is ready.

Download it here:

Download the notebook￼

You can place it in your project folder and run it with:

jupyter notebook

or

jupyter lab

It assumes your directory structure is:

data/
   bronze/
      insurance.2021.csv
      insurance.2022.csv
      insurance.2023.csv
      insurance.2024.csv

The notebook demonstrates:
	•	DuckDB reading multiple CSV files
	•	dataset inspection
	•	descriptive statistics
	•	visual EDA
	•	SQL + Python integration
	•	preparation for Bronze → Silver → Gold

If you want, I can also create a much richer teaching version with:
	•	10 SQL insight queries
	•	better visualizations
	•	clearer teaching explanations
	•	a transition to the Silver layer

which works extremely well in graduate Data Warehousing / Lakehouse courses. ￼

