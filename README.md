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

#### Execute
```commandline
source venv/bin/activate
pip3 install -r requirements.txt
python3 generator.py
```
