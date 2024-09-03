import redis
from faker import Faker
import random
from jproperties import Properties
import time
from datetime import datetime

Faker.seed(0)
fake = Faker('en_IN')
configs = Properties()
with open('./config/app-config.properties', 'rb') as config_file:
    configs.load(config_file)

accTypeList = ["SAVINGS", "CURRENT"]
lnType = ["PERSONAL", "HOME", "VEHICLE", "HOME_MAINTENANCE"]
relationTypeList = ["SPOUSE", "SON", "DAUGHTER", "MOTHER", "FATHER", "SIBLING"]
bankCode = configs.get("SAMPLE_BANK_CODE").data
ifsc = configs.get("SAMPLE_IFSC").data


def generate_data(count, conn, conn2):
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
        accountOpenDateObj = fake.date_time_between(start_date='-15y', end_date='now')
        accountOpenDate = int(time.mktime(accountOpenDateObj.timetuple()))
        dormant = fake.boolean(chance_of_getting_true=9)
        accountType = random.choice(accTypeList)

        availableBalance = float(fake.pricetag().replace('$', '').replace(',', ''))
        temp = fake.pyfloat(min_value=-100, max_value=1000)
        ledgerBalance = availableBalance + temp

        noOfNominee = fake.pyint(min_value=0, max_value=2)
        nominee = get_nominee(noOfNominee)

        cust = {
            "cif": cif, "bankCode": bankCode,"ifsc": ifsc,
            "name": name, "address": address, "virtualVault": virtualVault,
            "phone": phone, "mobile": phone, "email": email, "pan": pan,
            "aadhaar": aadhaar, "dob": dob, "kycOnfile": kycOnfile
        }

        account = {
            "cif": cif, "accountNo": accountNo, "accountType": accountType,
            "dormant": dormant, "accountOpenDate": accountOpenDate, "accountOpenDateStr": str(accountOpenDateObj),
            "iBankEnabled": iBankEnabled, "mBankEnabled": mBankEnabled, "nominee": nominee,
            "availableBalance": availableBalance, "ledgerBalance": ledgerBalance
        }

        generateDebitCardDetails(accountNo, cif, conn, conn2)
        generateCreditCardDetails(cif, conn, conn2)
        generateLoanAccDetails(cif, conn, conn2)

        custPrefix = "customer:" + ifsc + ":" + cif
        accPrefix = "account:" + cif + ":" + accountNo

        conn.json().set(custPrefix, "$", cust)
        conn.json().set(accPrefix, "$", account)

        conn2.json().set(custPrefix, "$", cust)
        conn2.json().set(accPrefix, "$", account)


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


def generateLoanAccDetails(cif, conn, conn2):
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
        conn2.json().set(loanPrefix, "$", loanAccount)


def generateCreditCardDetails(cif, conn, conn2):
    noOfCCCard = fake.pyint(min_value=0, max_value=2)
    if noOfCCCard == 1:
        creditCardNo1 = fake.credit_card_number()
        ccType1 = fake.credit_card_provider()

        issueDateObj = fake.date_time_between(start_date='-6y', end_date='-2y')
        issueDate = int(time.mktime(issueDateObj.timetuple()))

        ccExpiry1Obj = fake.date_time_between(start_date='-2y', end_date='+6y')
        ccExpiry1 = int(time.mktime(ccExpiry1Obj.timetuple()))

        ccCard1 = {
            "cif": cif, "description": ccType1 + ' card ending with expiry ' + str(ccExpiry1Obj),
            "creditCardNo": creditCardNo1, "issueDate": issueDate, "issueDateStr": str(issueDateObj),
            "expiryDate": ccExpiry1, "expiryDateStr": str(ccExpiry1Obj), "cvv": fake.credit_card_security_code(),
            "type": ccType1, "active": fake.boolean(chance_of_getting_true=85)
        }
        ccPrefix1 = "cccard:" + cif + ":" + creditCardNo1
        conn.json().set(ccPrefix1, "$", ccCard1)
        conn2.json().set(ccPrefix1, "$", ccCard1)
    elif noOfCCCard == 2:
        creditCardNo1 = fake.credit_card_number()
        ccType1 = fake.credit_card_provider()
        ccType2 = fake.credit_card_provider()
        creditCardNo2 = fake.credit_card_number()

        issueDateObj1 = fake.date_time_between(start_date='-6y', end_date='-2y')
        issueDate1 = int(time.mktime(issueDateObj1.timetuple()))
        issueDateObj2 = fake.date_time_between(start_date='-6y', end_date='-2y')
        issueDate2 = int(time.mktime(issueDateObj2.timetuple()))

        ccExpiry1Obj = fake.date_time_between(start_date='-2y', end_date='+6y')
        ccExpiry1 = int(time.mktime(ccExpiry1Obj.timetuple()))
        ccExpiry2Obj = fake.date_time_between(start_date='-2y', end_date='+6y')
        ccExpiry2 = int(time.mktime(ccExpiry2Obj.timetuple()))

        ccCard1 = {
            "cif": cif, "description": ccType1 + ' card ending with expiry ' + str(ccExpiry1Obj),
            "creditCardNo": creditCardNo1, "issueDate": issueDate1, "issueDateStr": str(issueDateObj1),
            "expiryDate": ccExpiry1, "expiryDateStr": str(ccExpiry1Obj), "cvv": fake.credit_card_security_code(),
            "type": ccType1, "active": fake.boolean(chance_of_getting_true=85)
        }
        ccCard2 = {
            "cif": cif, "description": ccType2 + ' card ending with expiry ' + str(ccExpiry2Obj),
            "creditCardNo": creditCardNo2, "issueDate": issueDate2, "issueDateStr": str(issueDateObj2),
            "expiryDate": ccExpiry2, "expiryDateStr": str(ccExpiry2Obj), "cvv": fake.credit_card_security_code(),
            "type": ccType2, "active": fake.boolean(chance_of_getting_true=85)
        }
        ccPrefix1 = "cccard:" + cif + ":" + creditCardNo1
        ccPrefix2 = "cccard:" + cif + ":" + creditCardNo2
        conn.json().set(ccPrefix1, "$", ccCard1)
        conn.json().set(ccPrefix2, "$", ccCard2)
        conn2.json().set(ccPrefix1, "$", ccCard1)
        conn2.json().set(ccPrefix2, "$", ccCard2)


def generateDebitCardDetails(accountNo, cif, conn, conn2):
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
        conn2.json().set(dbcPrefix, "$", dbCard)


if __name__ == '__main__':
    chunk = 100
    count = 500
    conn = redis.Redis(host=configs.get("HOST").data, port=configs.get("PORT").data)
    conn2 = redis.Redis(host="redis-10748.c21283.ap-south-1-1.ec2.cloud.rlrcp.com", port=10748, password="mOxcxZlBBb9LZXsBrbqibqEGkGfUcyEQ")
    if not conn.ping():
        raise Exception('Redis unavailable')
    for x in range(chunk):
        try:
            generate_data(count, conn, conn2)
            print(str(x+1) + " chunk(s) of recordset generated")
        except Exception as inst:
            print(type(inst))
            print(inst)
            raise Exception('Exception occurred while generating data. Delete the corrupted data and try again')
    print(str(chunk * count) + " recordset generated successfully")
