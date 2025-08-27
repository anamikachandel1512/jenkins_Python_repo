from locust import task, SequentialTaskSet, HttpUser, constant
from csvRead import csvRead
import re, random

class JpetStoreClass(SequentialTaskSet):

    def __init__(self,parent):
        super().__init__(parent)
        self.Animal=""
        self.productId=""
        self.ItemId=""
        self.orderId = ""

    @task
    def launch(self):
        # Assertion
        expected_Response = "Welcome to JPetStore 6"
        endpoint= ""
        method = "GET"
        with self.client.get(endpoint, name = "Launch", catch_response = True) as response:

            # Condition to chk whether we are getting proper data or not
            if response.status_code == 200 and expected_Response in response.text:
                print("JPetStore launched")
                response.success()

            else:
                response.failure("Launch failed")

    @task
    def EnterStore(self):
        expected_Response = "Sign In"
        with self.client.get("/actions/Catalog.action", name = "EnterStore", catch_response = True) as response:
            if response.status_code == 200 and expected_Response in response.text:
                print("JPetStore -> enter Store")
                response.success()
            else:
                response.failure("EnterStore failed")

    @task
    def SignIn(self):
        expected_Response = "Please enter your username and password."
        with self.client.get("/actions/Account.action?signonForm=", name="SignInClicked", catch_response=True) as response:
            if response.status_code == 200 and expected_Response in response.text:
                print("Sign In clicked successfully")
                response.success()
            else:
                response.failure("Sign In clicked failed")

    @task
    def EnterCred(self):

        #  csvRead class will read data from Data.csv file and store it in testdata variable
        testdata = csvRead("Data.csv").read()
        expected_Response = "Welcome "

        # Parametrization in the form dictionary
        data = {"username": testdata["username"], "password": testdata["password"], "signon": "Login", "_sourcePage": "MEKDozV5Ktr0Bsc9_4N8omQkvClDMAVwTyg8H0bI7uAJ1bVwkQOO9IXEea5AByuvXehvcGkpO7Rs83jiT--pvZvKzIo-yO3IGbT0Vci5hPI=", "__fp": "0-lQOV14iFaeah6r_OH24pZApv7wAz3IWdIHpWvKeuEm6c9caALcn0InN0hZ9apQ"}

        with self.client.post("/actions/Account.action", data = data, name="EnterCred", catch_response=True) as response:
            print("Enter Cred Status code ", response.status_code)
            if expected_Response in response.text:
                print("Enter cred successfully")
                response.success()
            else:
                print("Enter cred failed")
                response.failure("Enter cred failed")

            try:
                # findall and search function are used for searching particular text in response. Used for Co-relation
                # It will make use of Regular expression
                animal = re.findall(r"categoryId=(.*?)\"><img src=",response.text)

                # Randomly select animal from the list. Store Result in self.animal var.
                self.Animal = random.choice(animal)
                print("Pet Selected ",self.Animal)

            except AttributeError:
                self.Animal = ""
    @task
    def SelectPet(self):

        # Using Corelated variable
        name = "Select " + str(self.Animal)
        url = "/actions/Catalog.action?viewCategory=&categoryId="+str(self.Animal)
        # productId=FI-FW-01">
        with self.client.get(url, name = name, catch_response = True) as response:
            if response.status_code == 200 and "Product ID" in response.text:
                try:
                    productId = re.findall(r"productId=(.*?)\">",response.text)
                    self.productId= random.choice(productId)
                    print("Product Id fetched ",self.productId)
                    response.success()
                except AttributeError:
                    self.productId = ""
            else:
                response.failure("Either Select Pet didn't load or corelation failed")

    @task
    def SelectProductId(self):
        name = "Select " + str(self.Animal) +" " + str(self.productId)
        url = "/actions/Catalog.action?viewProduct=&productId=" + str(self.productId)
        # itemId=EST-18">
        with self.client.get(url, name=name, catch_response=True) as response:
            if response.status_code == 200 and "Description" in response.text:
                try:
                    ItemId = re.findall(r"itemId=(.*?)\">", response.text)
                    self.ItemId = random.choice(ItemId)
                    print("Item Id Selected ", self.ItemId)
                    response.success()
                except AttributeError:
                    self.ItemId = ""
            else:
                response.failure("Either ProductId page didn't load or corelation failed")

    @task
    def SelectItemId(self):
        name = "Select " + str(self.Animal) + " " + str(self.ItemId)
        url = "/actions/Catalog.action?viewItem=&itemId=" + str(self.ItemId)

        with self.client.get(url, name=name, catch_response=True) as response:
            if response.status_code == 200 and "Add to Cart" in response.text:
                print("Select Item Id paased")
                response.success()
            else:
                response.failure("Item Id page didn't load")

    @task
    def AddtoCart(self):
        name = "AddToCart"
        url = "/actions/Cart.action?addItemToCart=&workingItemId=" + str(self.ItemId)
        with self.client.get(url, name=name, catch_response=True) as response:
            if response.status_code == 200 and "Update Cart" in response.text:
                print("Add to cart successfully")
                response.success()
            else:
                response.failure("Add tp cart didn't load")

    @task
    def ProceedtoCheckout(self):
        name = "ProceedtoCheckout"
        url = "/actions/Order.action?newOrderForm="
        with self.client.get(url, name=name, catch_response=True) as response:
            if response.status_code == 200 and "Payment Details" in response.text:
                print("Proceed to checkout passed")
                response.success()
            else:
                response.failure("Proceed to checkout didn't load")

    @task
    def PaymentDetails_Continue(self):
        name = "PaymentDetails_Continue"
        url = "/actions/Order.action"
        data = {
            "order.cardType": "Visa",
            "order.creditCard": "999 9999 9999 9999",
            "order.expiryDate": "12/03",
            "order.billToFirstName": "ion",
            "order.billToLastName": "pop",
            "order.billAddress1": "qweQEW",
            "order.billAddress2": "qwd",
            "order.billCity": "dqawd",
            "order.billState": "1",
            "order.billZip": "233111",
            "order.billCountry": "asd",
            "newOrder": "Continue",
            "_sourcePage": "iQUQF2uDZ6BYgc9osTYuVDZ726lK-sm5xYndoUNoxxaq-hFqMC7_GzML9ILSqSe6DHRGr11bsPIVEe55TJVYzIePlnzsNtYeFjQoNLHWB1g="
        }
        with self.client.post(url, name=name, data=data, catch_response=True) as response:
            if response.status_code == 200 and "Please confirm the information" in response.text:
                print("PaymentDetails_Continue passed")
                response.success()
            else:
                response.failure("PaymentDetails_Continue didn't load")

    @task
    def ClickedContinue_PaymentDetails(self):
        name = "ClickedContinue_PaymentDetails"
        url = "/actions/Order.action?newOrder=&confirmed=true"
        # Order #35265
        with self.client.get(url, name=name, catch_response=True) as response:
            if response.status_code == 200 and "Thank you, your order has been submitted." in response.text:
                print("Thank you, your order has been submitted.")
                response.success()
            else:
                response.failure(" ClickedContinue_PaymentDetails didn't load")
            try:
                orderId= re.search(r"Order #([0-9]{5})", response.text)
                self.orderId = orderId.group(1)
                print("Order Id", self.orderId)
            except AttributeError:
                self.orderId=""




    @task
    def SignOut(self):
        expected_Response = "Sign In"
        with self.client.get("/actions/Account.action?signoff=", name="SignOutClicked",
                             catch_response=True) as response:
            if expected_Response in response.text:
                print(response.status_code)
                print("SignOutClicked successfully")
                response.success()
            else:
                response.failure("SignOutClicked failed")

class JpetUserMain(HttpUser):
    host = "https://petstore.octoperf.com/"
    tasks = [JpetStoreClass]
    wait_time = constant(1)

