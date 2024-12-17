CREATE TABLE customers (
    cust_id     INT             NOT NULL,
    cust_fname  VARCHAR(40)     NOT NULL,
    cust_lname  VARCHAR(40)     NOT NULL,
    address     VARCHAR(60)     NOT NULL,

    PRIMARY KEY (cust_id)
);
