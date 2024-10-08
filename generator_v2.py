import redis
from redis_om import (JsonModel, EmbeddedJsonModel)
from pydantic import (PositiveInt, PositiveFloat, EmailStr, NonNegativeFloat)
from typing import List
from faker import Faker
import random
from jproperties import Properties
import time
from datetime import datetime


configs = Properties()
with open('./config/app-config.properties', 'rb') as config_file:
    configs.load(config_file)
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

    # class Meta:
# global_key_prefix = self.
# model_key_prefix = Customer().cif


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
    ledgerBalance: NonNegativeFloat
    availableBalance: NonNegativeFloat
    nominee: List[Nominee]

    class Meta:
        global_key_prefix = "account"
        model_key_prefix = "book2"


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
        email = fake.email()
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
        nominee = get_nominee(noOfNominee)

        cust = Customer(cif=cif, bankCode=bankCode, ifsc=ifsc,
                        name=name, address=address, virtualVault=virtualVault,
                        phone=phone, mobile=phone, email=email, pan=pan,
                        aadhaar=aadhaar, dob=dob, kycOnfile=kycOnfile)
        account = Account(cif=cif, accountNo=accountNo, accountType=accountType,
                          dormant=dormant, accountOpenDate=accountOpenDate, iBankEnabled=iBankEnabled,
                          mBankEnabled=mBankEnabled, nominee=nominee, availableBalance=availableBalance,
                          ledgerBalance=ledgerBalance)

        generateDebitCardDetails(accountNo, cif, conn)
        generateCreditCardDetails(cif, conn)
        generateLoanAccDetails(cif, conn)

        cust.save()
        account.save()


def get_nominee(no_of_nominee):
    global nominee
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


def generateLoanAccDetails(cif, conn):
    global loanAccountNo
    noOfLoanAcc = fake.pyint(min_value=0, max_value=1)
    if noOfLoanAcc == 1:
        loanAccountNo = 'LA' + fake.bban()
        loanAccount = LoanAccount(cif=cif, loanAccountNo=loanAccountNo, loanFileNo=fake.pystr(),
                                  loanType=random.choice(lnType),
                                  amount=float(fake.pricetag().replace('$', '').replace(',', '')) + 1.0,
                                  dormant=fake.boolean(chance_of_getting_true=10),
                                  issueDate=str(fake.date_between(start_date='-20y')),
                                  expiryDate=str(fake.date_between(start_date='today', end_date='+20y')),
                                  active=fake.boolean(chance_of_getting_true=65))
        loanAccount.save()


def generateCreditCardDetails(cif, conn):
    noOfCCCard = fake.pyint(min_value=0, max_value=2)
    if noOfCCCard == 1:
        creditCardNo1 = fake.credit_card_number()
        ccType1 = fake.credit_card_provider()
        ccExpiry1 = fake.credit_card_expire()
        ccCard1 = CreditCard(cif=cif, description=ccType1 + " card ending with expiry " + ccExpiry1,
                             creditCardNo=creditCardNo1, issueDate=str(fake.date_between(start_date='-4y')),
                             expiryDate=ccExpiry1, cvv=fake.credit_card_security_code(),
                             type=ccType1, active=fake.boolean(chance_of_getting_true=85))
        ccCard1.save()
    elif noOfCCCard == 2:
        creditCardNo1 = fake.credit_card_number()
        ccType1 = fake.credit_card_provider()
        ccType2 = fake.credit_card_provider()
        creditCardNo2 = fake.credit_card_number()
        ccExpiry1 = fake.credit_card_expire()
        ccExpiry2 = fake.credit_card_expire()
        ccCard1 = CreditCard(cif=cif, description=ccType1 + " card ending with expiry " + ccExpiry1,
                             creditCardNo=creditCardNo1, issueDate=str(fake.date_between(start_date='-4y')),
                             expiryDate=ccExpiry1, cvv=fake.credit_card_security_code(),
                             type=ccType1, active=fake.boolean(chance_of_getting_true=85))
        ccCard2 = CreditCard(cif=cif, description=ccType2 + " card ending with expiry " + ccExpiry2,
                             creditCardNo=creditCardNo2, issueDate=str(fake.date_between(start_date='-4y')),
                             expiryDate=ccExpiry2, cvv=fake.credit_card_security_code(),
                             type=ccType2, active=fake.boolean(chance_of_getting_true=85))
        ccCard1.save()
        ccCard2.save()


def generateDebitCardDetails(accountNo, cif, conn):
    global debitCardNo, dbCard
    noOfDebitCard = fake.pyint(min_value=0, max_value=1)
    if noOfDebitCard == 1:
        dbcExpiry = fake.credit_card_expire()
        debitCardNo = fake.credit_card_number()
        dbcType = fake.credit_card_provider()
        dbCard = DebitCard(cif=cif, accountNo=accountNo, description=dbcType + " card ending with expiry " + dbcExpiry,
                           debitCardNo=debitCardNo, issueDate=str(fake.date_between(start_date='-7y')),
                           expiryDate=fake.credit_card_expire(), type=dbcType,
                           active=fake.boolean(chance_of_getting_true=90))
        dbCard.save


if __name__ == '__main__':
    # chunk = 1
    # count = 1
    # conn = redis.Redis(host='localhost', port=6379)
    # if not conn.ping():
    #     raise Exception('Redis unavailable')
    # for x in range(chunk):
    #     try:
    #         generate_data(count, conn)
    #         print(str(x+1) + " chunk(s) of recordset generated")
    #     except Exception as inst:
    #         print(type(inst))
    #         print(inst)
    #         raise Exception('Exception occurred while generating data. Delete the corrupted data and try again')
    # print(str(chunk * count) + " recordset generated successfully")

    accountOpenDateObj = fake.date_time_between(start_date='-15y', end_date='now')
    print(accountOpenDateObj)

    unixTs = time.mktime(accountOpenDateObj.timetuple())

    print(int(unixTs))
    print(datetime.fromtimestamp(int(unixTs)).strftime(configs.get("DATE_FORMAT").data))
