import redis
from redis_om import (JsonModel, EmbeddedJsonModel)
from pydantic import (PositiveInt, PositiveFloat, AnyHttpUrl, EmailStr)
from typing import List
from faker import Faker
import random

Faker.seed(0)
fake = Faker('en_IN')


class Customer(JsonModel):
    cif: str
    bankCode: str
    ifsc: str
    name: str
    address: str
    virtualVault: str
    phone: str
    mobile: str
    pan: str
    aadhaar: str
    email: EmailStr
    dob: str
    kycOnfile: bool


class Nominee(EmbeddedJsonModel):
    nomineeId: str
    name: str
    relation: str
    dob: str
    percentage: PositiveInt
    mobile: str


class Account(JsonModel):
    cif: str
    accountNo: str
    accountType: str
    dormant: bool
    accountOpenDate: str
    iBankEnabled: bool
    mBankEnabled: bool
    nominee: List[Nominee]


class DebitCard(JsonModel):
    cif: str
    accountNo: str
    description: str
    debitCardNo: str
    issueDate: str
    expiryDate: str
    type: str
    active: bool


class CreditCard(JsonModel):
    cif: str
    description: str
    creditCardNo: str
    issueDate: str
    expiryDate: str
    cvv: str
    type: str
    active: bool


class LoanAccount(JsonModel):
    cif: str
    loanAccountNo: str
    loanFileNo: str
    loanType: str
    amount: PositiveFloat
    dormant: bool
    issueDate: str
    expiryDate: str
    active: bool


accTypeList = ["SAVINGS", "CURRENT"]
lnType = ["PERSONAL", "HOME", "VEHICLE", "HOME_MAINTENANCE"]
relationTypeList = ["SPOUSE", "SON", "DAUGHTER", "MOTHER", "FATHER", "SIBLING"]
bankCode = "DSI7452387423"
ifsc = "DSI6898694"


def get_nominee(no_of_nominee):
    nominee = []
    if no_of_nominee == 1:
        nominee1 = Nominee(nomineeId=fake.pystr_format(), name=fake.name(),
                           relation=random.choice(relationTypeList),
                           dob=fake.date(),
                           percentage=100, mobile=fake.phone_number())
        nominee = [nominee1]
    elif no_of_nominee == 2:
        nominee1 = Nominee(nomineeId=fake.pystr_format(), name=fake.name(),
                           relation=random.choice(relationTypeList),
                           dob=fake.date(),
                           percentage=50, mobile=fake.phone_number())
        nominee2 = Nominee(nomineeId=fake.pystr_format(), name=fake.name(),
                           relation=random.choice(relationTypeList),
                           dob=fake.date(),
                           percentage=50, mobile=fake.phone_number())
        nominee = [nominee1, nominee2]

    return nominee


def generate_data(count, conn):
    global name, address, cif, virtualVault, aadhaar, pan, phone, mobile, email, dob, \
        accountNo, kycOnfile, iBankEnabled, mBankEnabled, accountOpenDate, dormant, accountType, \
        debitCardNo, creditCardNo, cvv, loanAccountNo, loanFileNo, loanType, amount, nominee

    for index in range(count):
        name = fake.name()
        address = fake.building_number() + fake.address()
        cif = fake.lexify("????").upper() + str(fake.random_number(digits=6, fix_len=True)) + str(index)
        virtualVault = fake.lexify("??").upper() + str(fake.random_number(digits=7))
        aadhaar = fake.aadhaar_id()
        pan = fake.bothify("?????####?")
        phone = fake.phone_number()
        mobile = phone
        email = fake.email()
        dob = fake.date(pattern="%d-%m-%Y")

        accountNo = fake.bban()
        kycOnfile = fake.boolean(chance_of_getting_true=75)
        iBankEnabled = fake.boolean(chance_of_getting_true=33)
        mBankEnabled = fake.boolean(chance_of_getting_true=25)
        accountOpenDate = str(fake.date_between(start_date='-15y', end_date='today'))
        dormant = fake.boolean(chance_of_getting_true=9)
        accountType = random.choice(accTypeList)

        dbcExpiry = fake.credit_card_expire();
        debitCardNo = fake.credit_card_number()
        dbcType = fake.credit_card_provider()
        dbdescription = dbcType + " card ending with expiry " + dbcExpiry
        dbactive = fake.boolean(chance_of_getting_true=90)
        dbissueDate = str(fake.date_between(start_date='-7y'))

        ccExpiry = fake.credit_card_expire();
        creditCardNo = fake.credit_card_number()
        ccType = fake.credit_card_provider()
        cvv = fake.credit_card_security_code()
        ccActive = fake.boolean(chance_of_getting_true=85)
        ccdescription = ccType + " card ending with expiry " + ccExpiry
        ccissueDate = str(fake.date_between(start_date='-4y'))

        loanAccountNo = 'LA' + fake.bban()
        loanFileNo = fake.pystr()
        loanType = random.choice(lnType)
        amount = float(fake.pricetag().replace('$', '').replace(',', '')) + 1.0
        loanDormant = fake.boolean(chance_of_getting_true=10)
        loanIssueDate = str(fake.date_between(start_date='-20y'))
        loanExpiryDate = str(fake.date_between(start_date='today', end_date='+20y'))
        loanActive = fake.boolean(chance_of_getting_true=65)

        noOfNominee = fake.pyint(min_value=0, max_value=2)
        nominee = get_nominee(noOfNominee)

        cust = Customer(cif=cif, bankCode=bankCode, ifsc=ifsc,
                        name=name, address=address, virtualVault=virtualVault,
                        phone=phone, mobile=phone, email=email, pan=pan,
                        aadhaar=aadhaar, dob=dob, kycOnfile=kycOnfile)
        account = Account(cif=cif, accountNo=accountNo, accountType=accountType,
                          dormant=dormant, accountOpenDate=accountOpenDate, iBankEnabled=iBankEnabled,
                          mBankEnabled=mBankEnabled, nominee=nominee)
        dbCard = DebitCard(cif=cif, accountNo=accountNo, description=dbdescription,
                           debitCardNo=debitCardNo, issueDate=dbissueDate, expiryDate=dbcExpiry,
                           type=dbcType, active=dbactive)
        ccCard = CreditCard(cif=cif, description=ccdescription, creditCardNo=creditCardNo,
                            issueDate=ccissueDate, expiryDate=ccExpiry,
                            cvv=cvv, type=ccType, active=ccActive)
        loanAccount = LoanAccount(cif=cif, loanAccountNo=loanAccountNo, loanFileNo=loanFileNo,
                                   loanType=loanType, amount=amount, dormant=loanDormant,
                                   issueDate=loanIssueDate, expiryDate=loanExpiryDate, active=loanActive)

        custPrefix = "customer:" + ifsc + ":" + cif
        accPrefix = "account:" + cif + ":" + accountNo
        ccPrefix = "cccard:" + cif + ":" + creditCardNo
        loanPrefix = "loan:" + cif + ":" + loanAccountNo
        dbcPrefix = "dbcard:" + accountNo + ":" + debitCardNo

        conn.json().set(custPrefix, "$", cust.json())
        conn.json().set(accPrefix, "$", account.json())
        conn.json().set(ccPrefix, "$", ccCard.json())
        conn.json().set(loanPrefix, "$", loanAccount.json())
        conn.json().set(dbcPrefix, "$", dbCard.json())


if __name__ == '__main__':
    chunk = 100
    count = 1000
    conn = redis.Redis(host='localhost', port='6379')
    if not conn.ping():
        raise Exception('Redis unavailable')
    for x in range(chunk):
        generate_data(count, conn)
        print(" chunks of recordset generated")
    #print(str(20)+" records generated successfully")
