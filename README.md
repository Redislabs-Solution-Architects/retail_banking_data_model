# Sample retail banking data model

Following data models are used:
<li> BankBranch
<li> Customer
<li> Account
<li> DebitCard
<li> CreditCard
<li> LoanAccount

#### ER diagram

TBD

#### Sample JSON objects
Customer
```json
 {
  "bankCode":"DSI7452387423",
  "ifsc":"DSI6898694",
  "cif": "UYO9786898",
  "name": "B Suresh",
  "address": "B2, Greater Kailash, New Delhi, 110001",
  "virtualVault":"VBM5472364NM",
  "phone": "0116472388",
  "mobile": "9869546732",
  "pan": "BTY643768",
  "aadhaar": "321478659801",
  "dob": "cif",
  "email": "bsuresh.gmail.com",
  "kycOnfile": true
}
```
Account
```json
{
  "cif": "UYO9786898",
  "accountNo": "123498572345",
  "accountType": "SAVINGS",
  "dormant": false,
  "accountOpenDate": "2015-02-23T00:00:00.000Z",
  "iBankEnabled": true,
  "mBankEnabled": false,
  "nominee": [
    {
      "nomineeId": "N4234324",
      "name": "Kirti S",
      "relation": "SPOUSE",
      "dob": "1981-01-01T00:00:00.000Z",
      "percentage": 50,
      "mobile": "9642342432"
    },
    {
      "nomineeId": "N4234322",
      "name": "Deepak",
      "relation": "SON",
      "dob": "2000-11-01T00:00:00.000Z",
      "percentage": 50
    }
  ]
}
```

DebitCard
```json
{
  "cif": "UYO9786898",
  "accountNo": "123498572345",
  "description": "Millennium shopping card",
  "debitCardNo": "123486570989",
  "issueDate": "2015-03-07T00:00:00.000Z",
  "expiryDate": "2025-03-07T00:00:00.000Z",
  "type": "VISA",
  "active": true
}
```

CreditCard
```json
{
  "cif": "UYO9786898",
  "description": "Millennium credit card",
  "creditCardNo": "453486570923",
  "issueDate": "2017-08-07T00:00:00.000Z",
  "expiryDate": "2027-08-07T00:00:00.000Z",
  "cvv": "973",
  "type": "VISA",
  "active": true
}

```

LoanAccount
```json
{
  "cif": "UYO9786898,",
  "loanAccountNo": "123498572345,",
  "loanFileNo": "LF3498572300,",
  "loanType": "PERSONAL",
  "amount": "200000",
  "dormant": "false,",
  "issueDate": "2019-02-23T00:00:00.000Z",
  "expiryDate": "2012-02-23T00:00:00.000Z",
  "active": true
}
```

#### Running the data loader
```commandline
source venv/bin/activate
pip3 install -r requirements.txt
python3 generator.py
```

#### Indexes
```
FT.CREATE idx_customer on JSON PREFIX 1 customer: SCHEMA $.cif as cif TEXT $.name as name TEXT $.mobile as mobile TEXT $.pan as pan TEXT $.aadhaar as aadhaar TEXT $.email as email TEXT
FT.CREATE idx_account on JSON PREFIX 1 account: SCHEMA $.cif as cif TEXT $.accountNo as accountNo TEXT $.accountType as accountType TAG $.dormant as dormant TAG $.iBankEnabled as iBankEnabled TAG $.nominee.nomineeId as nomineeId TEXT 
FT.CREATE idx_dbcard on JSON PREFIX 1 dbcard: SCHEMA $.cif as cif TEXT $.accountNo as accountNo TEXT $.type as type TAG 
FT.CREATE idx_cccard on JSON PREFIX 1 cccard: SCHEMA $.cif as cif TEXT $.creditCardNo as creditCardNo TEXT $.expiryDate as expiryDate TEXT $.type as type TAG $.active as active TAG 
FT.CREATE idx_loan on JSON PREFIX 1 loan: SCHEMA $.cif as cif TEXT $.amount as amount NUMERIC SORTABLE $.loanType as loanType TAG
```

#### Queries
1. Get customer:
    - by email
           - FT.SEARCH idx_customer '@email:(tiwarimishti\@example.org)'
    - by cif 
           - FT.SEARCH idx_customer '@cif:ICKU814154312'
    - by uid(aadhaar) 
           - FT.SEARCH idx_customer '@aadhaar:(551747310375)'
2. Fetch the nominee details of an account 
          - FT.SEARCH idx_account "@cif:(BEPS620487198)" return 1 $.nominee
3. Get all credit cards by customer id 
          - FT.SEARCH idx_cccard '@cif:(QEOE110093342)' return 2 creditCardNo type
4. Get maximum loan by loanTypes 
          - FT.AGGREGATE idx_loan '@amount:[0 +inf]' groupby 1 @loanType  REDUCE MAX 1 @amount as loanmount 
          - FT.AGGREGATE idx_loan * groupby 1 @loanType  REDUCE MAX 1 @amount as loanmount 
5. Get total loan liabilities by loanTypes
          - FT.AGGREGATE idx_loan *  groupby 1 @loanType  REDUCE SUM 1 @amount as loanmount
6. Get total loan given as a HOME loan
          - FT.AGGREGATE idx_loan '@loanType:{HOME}'  groupby 1 @loanType  REDUCE SUM 1 @amount as loanmount
7. Get total number of different types of credit cards issued to customers
          - FT.AGGREGATE idx_cccard * groupby 1 @type REDUCE COUNT 0 as ccTypes
8. Get total number of inactive credit cards 
          - FT.AGGREGATE idx_cccard '@active:{false}' groupby 1 @active REDUCE COUNT 0 as inactiveCards
9. Get the number of different types of accounts, customers are holding in the bank 
          - FT.AGGREGATE idx_account * groupBy 1 @accountType REDUCE COUNT 0 as count
10. Search customer by name
          - FT.SEARCH idx_customer '@name: srivastava'