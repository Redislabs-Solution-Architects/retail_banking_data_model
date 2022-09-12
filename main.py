# # This is a sample Python script.
#
# # Press ⌃R to execute it or replace it with your code.
# # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# import redis
# from redis.commands.json.path import Path
# import redis.commands.search.aggregation as aggregations
# import redis.commands.search.reducers as reducers
# from redis.commands.search.field import TextField, NumericField, TagField
# from redis.commands.search.indexDefinition import IndexDefinition, IndexType
# from redis.commands.search.query import NumericFilter, Query
# from redis_om import (JsonModel, EmbeddedJsonModel)
#
# from pydantic import (PositiveInt, PositiveFloat, AnyHttpUrl, EmailStr)
#
# from faker import Faker
# import random
# import pandas as pd
#
# # connections
# # conn = redis.Redis(host='localhost', port='6379')
# # if not conn.ping():
# #     raise Exception('Redis unavailable')
#
# Faker.seed(0)
# fake = Faker('en_IN')
# relationTypeList = ["SPOUSE", "SON", "DAUGHTER", "MOTHER", "FATHER", "SIBLING"]
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# class Nominee(EmbeddedJsonModel):
#     nomineeId: str
#     name: str
#     relation: str
#     dob: str
#     percentage: PositiveInt
#     mobile: str
#
#
# def get_nominee(no_of_nominee):
#     nominee = []
#
#     if no_of_nominee == 1:
#         nominee1 = Nominee(nomineeId=fake.pystr_format(), name=fake.name(), relation=random.choice(relationTypeList),
#                            dob=fake.date(),
#                            percentage=100, mobile="53287457324")
#         nominee = [nominee1]
#     elif no_of_nominee == 2:
#         nominee1 = Nominee(nomineeId=fake.pystr_format(), name=fake.name(), relation=random.choice(relationTypeList),
#                            dob=fake.date(),
#                            percentage=50, mobile="53287457324")
#         nominee2 = Nominee(nomineeId=fake.pystr_format(), name=fake.name(), relation=random.choice(relationTypeList),
#                            dob=fake.date(),
#                            percentage=50, mobile="53287457324")
#         nominee = [nominee1, nominee2]
#
#     return nominee
#
#
# def generate_data():
#     lnType = ["PERSONAL", "HOME", "VEHICLE", "HOME_MAINTENANCE"]  # List
#     item = random.choice(lnType)  # Chooses from list
#     print(item)
#
#     print(get_nominee(2))
#
#     #data = fake.date_between(start_date='today', end_date='+20y')
#
#     #data = fake.pyint(min_value=0, max_value=2)
#
#     #data=fake.lexify("????").upper() + str(fake.random_number(digits=6, fix_len=True))
#     #data=fake.pyfloat(positive=True, right_digits=2, max_value=10000000, min_value=0.1)
#     #data=fake.pricetag().replace('$','').replace(',','')
#     #data = [fake.name() for i in range(10)]
#     #data = [fake.last_name() for i in range(10)]
#     # data = [fake.profile() for i in range(10)]
#     # df = pd.DataFrame(data)
#
#     #data = [fake.phone_number() for i in range(10)]
#
#     #data = [fake.bban() for i in range(10)]
#
#     #data = [fake.address() for i in range(10)]
#
#     #data = [fake.free_email() for i in range(10)]
#
#     #data = [fake.ssn() for i in range(10)]
#
#     #print(data)
#
#
#
# # Press the green button in the gutter to run the script.
# def test():
#     user1 = {
#         "user": {
#             "name": "Paul John",
#             "email": "paul.john@example.com",
#             "age": 42,
#             "city": "London"
#         }
#     }
#     user2 = {
#         "user": {
#             "name": "Eden Zamir",
#             "email": "eden.zamir@example.com",
#             "age": 29,
#             "city": "Tel Aviv"
#         }
#     }
#     user3 = {
#         "user": {
#             "name": "Paul Zamir",
#             "email": "paul.zamir@example.com",
#             "age": 35,
#             "city": "Tel Aviv"
#         }
#     }
#     conn.json().set("user:1", Path.root_path(), user1)
#     conn.json().set("user:2", Path.root_path(), user2)
#     conn.json().set("user:3", Path.root_path(), user3)
#
#     schema = (TextField("$.user.name", as_name="name"),
#               TagField("$.user.city", as_name="city"),
#               NumericField("$.user.age", as_name="age"))
#     conn.ft().create_index(schema, definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON))
#
#     # Simple search
#     print(conn.ft().search("Paul"))
#
#     # Filtering search results
#     q1 = Query("Paul").add_filter(NumericFilter("age", 30, 40))
#     print(conn.ft().search(q1))
#
#     # Projecting using JSON Path expressions
#     print(conn.ft().search(Query("Paul").return_field("$.user.city", as_field="city")).docs)
#
#     # Aggregation
#     req = aggregations.AggregateRequest("Paul").sort_by("@age")
#     print(conn.ft().aggregate(req).rows)
#
#
# if __name__ == '__main__':
#     print_hi('PyCharm')
#     generate_data()
#     #test()
