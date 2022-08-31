import redis
from faker import Faker
import random

Faker.seed(0)
fake = Faker('en_IN')


accTypeList = ["SAVINGS", "CURRENT"]
lnType = ["PERSONAL", "HOME", "VEHICLE", "HOME_MAINTENANCE"]
relationTypeList = ["SPOUSE", "SON", "DAUGHTER", "MOTHER", "FATHER", "SIBLING"]
bankCode = "DSI7452387423"
ifsc = "DSI6898694"


def generate_data(count, conn):
    global name, address, cif, virtualVault, aadhaar, pan, phone, mobile, email, dob, \
        accountNo, kycOnfile, iBankEnabled, mBankEnabled, accountOpenDate, dormant, accountType, \
        debitCardNo, creditCardNo, cvv, loanAccountNo, loanFileNo, loanType, amount, nominee, dbCard

    for index in range(count):
        name = fake.name()
        address = fake.building_number() + fake.address()
        cif = fake.lexify("????").upper() + str(fake.random_number(digits=6, fix_len=True)) + str(index)
        virtualVault = fake.lexify("??").upper() + str(fake.random_number(digits=7))

        aadhaar_present = fake.boolean(chance_of_getting_true=75)
        if aadhaar_present:
            aadhaar = fake.aadhaar_id()
        else:
            aadhaar = 'NA'

        pan = fake.bothify("?????####?")
        phone = fake.phone_number()
        mobile = phone
        email = fake.email().replace('@', '\\@')
        dob = fake.date(pattern="%d-%m-%Y")

        accountNo = fake.bban()
        kycOnfile = fake.boolean(chance_of_getting_true=75)
        iBankEnabled = fake.boolean(chance_of_getting_true=33)
        mBankEnabled = fake.boolean(chance_of_getting_true=25)
        accountOpenDate = str(fake.date_between(start_date='-15y', end_date='today'))
        dormant = fake.boolean(chance_of_getting_true=9)
        accountType = random.choice(accTypeList)

        availableBalance = float(fake.pricetag().replace('$', '').replace(',', ''))
        temp = fake.pyfloat(min_value=-100, max_value=1000)
        ledgerBalance = availableBalance + temp

        noOfNominee = fake.pyint(min_value=0, max_value=2)
        print(noOfNominee)
        nominee = get_nominee(noOfNominee)

        cust = {
            "cif": cif, "bankCode": bankCode,"ifsc": ifsc,
            "name": name, "address": address, "virtualVault": virtualVault,
            "phone": phone, "mobile": phone, "email": email, "pan": pan,
            "aadhaar": aadhaar, "dob": dob, "kycOnfile": kycOnfile
        }

        account = {
            "cif": cif, "accountNo": accountNo, "accountType": accountType,
            "dormant": dormant, "accountOpenDate": accountOpenDate, "iBankEnabled": iBankEnabled,
            "mBankEnabled": mBankEnabled, "nominee": nominee,
            "availableBalance": availableBalance, "ledgerBalance": ledgerBalance
        }

        generateDebitCardDetails(accountNo, cif, conn)
        generateCreditCardDetails(cif, conn)
        generateLoanAccDetails(cif, conn)

        custPrefix = "customer:" + ifsc + ":" + cif
        accPrefix = "account:" + cif + ":" + accountNo

        conn.json().set(custPrefix, "$", cust)
        conn.json().set(accPrefix, "$", account)


def get_nominee(no_of_nominee):
    global nominee
    if no_of_nominee == 1:
        nominee1 = {
                    "nomineeId": fake.pystr_format(), "name": fake.name(),
                    "relation": random.choice(relationTypeList),
                    "dob": fake.date(), "percentage": 100, "mobile": fake.phone_number()
                    }
        nominee = [nominee1]
    elif no_of_nominee == 2:
        nominee1 = {
            "nomineeId": fake.pystr_format(), "name": fake.name(),
            "relation": random.choice(relationTypeList),
            "dob": fake.date(), "percentage": 50, "mobile": fake.phone_number()
        }
        nominee2 = {
            "nomineeId": fake.pystr_format(), "name": fake.name(),
            "relation": random.choice(relationTypeList),
            "dob": fake.date(), "percentage": 50, "mobile": fake.phone_number()
        }
        nominee = [nominee1, nominee2]
    else:
        nominee = []

    return nominee


def generateLoanAccDetails(cif, conn):
    global loanAccountNo
    noOfLoanAcc = fake.pyint(min_value=0, max_value=1)
    if noOfLoanAcc == 1:
        loanAccountNo = 'LA' + fake.bban()
        loanAccount = {
                "cif": cif, "loanAccountNo": loanAccountNo, "loanFileNo": fake.pystr(),
                "loanType": random.choice(lnType),
                "amount": float(fake.pricetag().replace('$', '').replace(',', '')) + 1.0,
                "dormant": fake.boolean(chance_of_getting_true=10),
                "issueDate": str(fake.date_between(start_date='-20y')),
                "expiryDate": str(fake.date_between(start_date='today', end_date='+20y')),
                "active": fake.boolean(chance_of_getting_true=65)
        }
        loanPrefix = "loan:" + cif + ":" + loanAccountNo
        conn.json().set(loanPrefix, "$", loanAccount)


def generateCreditCardDetails(cif, conn):
    noOfCCCard = fake.pyint(min_value=0, max_value=2)
    if noOfCCCard == 1:
        creditCardNo1 = fake.credit_card_number()
        ccType1 = fake.credit_card_provider()
        ccExpiry1 = fake.credit_card_expire()
        ccCard1 = {
            "cif": cif, "description": ccType1 + ' card ending with expiry ' + ccExpiry1,
            "creditCardNo": creditCardNo1, "issueDate": str(fake.date_between(start_date='-4y')),
            "expiryDate": ccExpiry1, "cvv": fake.credit_card_security_code(),
            "type": ccType1, "active": fake.boolean(chance_of_getting_true=85)
        }
        ccPrefix1 = "cccard:" + cif + ":" + creditCardNo1
        conn.json().set(ccPrefix1, "$", ccCard1)
    elif noOfCCCard == 2:
        creditCardNo1 = fake.credit_card_number()
        ccType1 = fake.credit_card_provider()
        ccType2 = fake.credit_card_provider()
        creditCardNo2 = fake.credit_card_number()
        ccExpiry1 = fake.credit_card_expire()
        ccExpiry2 = fake.credit_card_expire()
        ccCard1 = {
            "cif": cif, "description": ccType1 + ' card ending with expiry ' + ccExpiry1,
            "creditCardNo": creditCardNo1, "issueDate": str(fake.date_between(start_date='-4y')),
            "expiryDate": ccExpiry1, "cvv": fake.credit_card_security_code(),
            "type": ccType1, "active": fake.boolean(chance_of_getting_true=85)
        }
        ccCard2 = {
            "cif": cif, "description": ccType2 + ' card ending with expiry ' + ccExpiry2,
            "creditCardNo": creditCardNo2, "issueDate": str(fake.date_between(start_date='-4y')),
            "expiryDate": ccExpiry2, "cvv": fake.credit_card_security_code(),
            "type": ccType2, "active": fake.boolean(chance_of_getting_true=85)
        }
        ccPrefix1 = "cccard:" + cif + ":" + creditCardNo1
        ccPrefix2 = "cccard:" + cif + ":" + creditCardNo2
        conn.json().set(ccPrefix1, "$", ccCard1)
        conn.json().set(ccPrefix2, "$", ccCard2)


def generateDebitCardDetails(accountNo, cif, conn):
    global debitCardNo, dbCard
    noOfDebitCard = fake.pyint(min_value=0, max_value=1)
    if noOfDebitCard == 1:
        dbcExpiry = fake.credit_card_expire()
        debitCardNo = fake.credit_card_number()
        dbcType = fake.credit_card_provider()
        dbCard = {
            "cif": cif, "accountNo":accountNo, "description": dbcType + ' card ending with expiry ' + dbcExpiry,
            "debitCardNo": debitCardNo, "issueDate": str(fake.date_between(start_date='-7y')),
            "expiryDate": fake.credit_card_expire(), "type": dbcType,
            "active": fake.boolean(chance_of_getting_true=90)
        }
        dbcPrefix = "dbcard:" + accountNo + ":" + debitCardNo
        conn.json().set(dbcPrefix, "$", dbCard)


if __name__ == '__main__':
    chunk = 100
    count = 500
    conn = redis.Redis(host='localhost', port=6379)
    if not conn.ping():
        raise Exception('Redis unavailable')
    for x in range(chunk):
        try:
            generate_data(count, conn)
            print(str(x+1) + " chunk(s) of recordset generated")
        except Exception as inst:
            print(type(inst))
            print(inst)
            raise Exception('Exception occurred while generating data. Delete the corrupted data and try again')
    print(str(chunk * count) + " recordset generated successfully")
