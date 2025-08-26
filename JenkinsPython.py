from locust import task, SequentialTaskSet, HttpUser, constant

class JpetStore(SequentialTaskSet):

    def __init__(self,parent):
        super().__init__(parent)
        self.Animal=""
        self.productId=""
        self.ItemId=""
        self.orderId = ""

    @task
    def launch(self):
        expected_Response = "Welcome to JPetStore 6"
        endpoint= ""
        method = "GET"
        with self.client.get(endpoint, name = "Launch", catch_response = True) as response:
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

class JpetUser(HttpUser):
    host = "https://petstore.octoperf.com/"
    tasks = [JpetStore]
    wait_time = constant(1)

