# Technical Design Document

## Introduction

This document outlines the technical design for implementing the given tasks while following clean architecture and domain-driven design principles.

## Core Domain

The core domain consists of the following entities and their functionalities:

- **Managers**: Change products statuses.
- **Customers**: Order and customize their orders with several options from the catalog.
- **Orders**: Have statuses (Waiting, Preparation, Ready, Delivered) and consume locations (In-house or Take away).
- **Product**: Represents a product available in the catalog. It has properties such as name and variations.

## State Design Pattern

The Order entity in this project has been designed utilizing the State design pattern. The State design pattern is a behavioral design pattern that allows an object to alter its behavior when its internal state changes. Here are the advantages and trade-offs of using the State design pattern for the Order entity:

### Pros

- **Single Responsibility Principle**: The State design pattern organizes the code related to specific states into separate classes. Each state class is responsible for handling the behavior and transitions associated with that particular state. This promotes a clear separation of concerns and improves the maintainability of the codebase.

- **Open/Closed Principle**: The State design pattern allows for the introduction of new states without modifying existing state classes or the context. This makes the system more extensible and reduces the impact of changes in the future. New states can be easily added by implementing a new state class that adheres to the state interface.

- **Simplified Context Code**: The State design pattern simplifies the code in the context by eliminating heavy state machine conditionals. Instead of having complex conditional logic in the context to handle different states, each state class encapsulates its own behavior. This leads to cleaner and more modular code, making it easier to understand and maintain.

### Trade-offs

- **Overhead for Simple State Machines**: Applying the State design pattern might be considered overkill if the state machine has only a few states or rarely changes. If the order state machine is relatively simple and there are no plans for frequent changes or additions to the states, using the State design pattern may introduce unnecessary complexity.

I decided to use the State design pattern for the Order entity based on the possibility to easily include new status scenarios in the future.

## Application Layer

The application layer acts as an intermediary between the domain layer and the infrastructure layer.

### Use Cases

The use cases encapsulate the business logic of the application:

- **View Menu**: Retrieves the list of products from the catalog.
- **Place Order**: Handles the process of placing a new order.
- **View Order Details**: Retrieves the details of all orders.
- **Update Order**: Allows customers to update orders with the "Waiting" status.
- **Cancel Order**: Allows customers to cancel orders with the "Waiting" status.
- **Change Order Status**: Allows changing the status of an order identified by the order ID.

## Infrastructure Layer

The infrastructure layer deals with external systems, databases, and communication channels.

### Repositories

Repositories are used to provide an abstraction layer between the application's domain and the data persistence mechanism, such as a database or external APIs. They serve as a bridge that allows the application to interact with the underlying data storage without directly coupling the domain logic to specific implementation details.

For this project, in-memory repositories were utilized to allow us to focus on the core domain and avoid dealing with infrastructure details during development. This approach enabled us to rapidly prototype and iterate on the application's functionality without the need for actual databases or external systems.

However, adhering to the principles of the Clean Architecture, we have ensured that the codebase is decoupled from specific implementations. This provides us with the flexibility to easily replace these in-memory repositories with real implementations and create adapters for seamless integration with actual databases or external systems in a production environment.

By following the dependency inversion and dependency injection principles, we can abstract the data access and communication mechanisms, enabling the system to interact with various storage solutions or external services without impacting the core domain logic. This promotes maintainability, extensibility, and the ability to adapt the application to changing requirements or future enhancements.

Thus, while the in-memory repositories were suitable for the development phase, the architecture supports the seamless transition to real implementations and integration with actual databases or external systems when deploying the application to a production environment.

By leveraging the principles of the Clean Architecture, we have ensured that the system remains flexible, scalable, and future-proof, allowing for the smooth integration of various infrastructure components as needed.

### Gateways

The emails in this application are sent using the native SMTP Python library. To ensure decoupling of the library logic from the application, an adapter was created. The sender and receiver of the emails will be the same and will be defined based on the USERNAME environment variable. It is important to note that the password used for authentication must be an app password.

To create a gmail app password follow this instructions:

- Open your web browser and go to the Google Account settings page.
  Sign in to your Google Account if you haven't already.
- In the Account settings page, locate the "Security" section and click on it.
- Under the "Signing in to Google" section, find the "App Passwords" option and click on it. You may need to verify your account password again for security purposes.
- If you have enabled two-step verification, you may need to provide your verification code at this point.
- In the "App Passwords" page, scroll down to find the "Select the app and device you want to generate the app password for" section.
- From the dropdown menus, select the appropriate options for the app and device you want to generate the app password for. For example, you can choose "Mail" as the app and "Windows Computer" as the device.
- Click on the "Generate" button.
- Google will generate a unique app password for the selected app and device combination. Make sure to copy this password or keep it in a secure place as it will be displayed only once.
  -Use the generated app password in your application or device settings where you need to enter your Gmail password. Note that you won't use your regular Gmail account password for these cases.

### Brokers

Brokers are used to facilitate communication and coordination between different components or services in a distributed system. They act as intermediaries, enabling asynchronous messaging and decoupling the sender and receiver.

Using brokers in our system brings several advantages. Firstly, by enabling asynchronous message communication, brokers allow the update order status endpoint to respond faster. This is because the endpoint no longer needs to wait for the email to be sent before providing a response to the user. As a result, the overall system performance is improved.

Moreover, utilizing brokers helps us adhere to the single responsibility principle. With the use of brokers, the update order status endpoint can focus solely on changing the status without the responsibility of handling email notifications. This separation of concerns enhances the maintainability and testability of our codebase.

In this project, an in-memory broker implementation was chosen for simplicity. However, it's important to note that we have the flexibility to easily create an adapter and to integrate a more robust and scalable message brokers like Redis or RabbitMQ. These real brokers offer additional features such as message persistence, queuing, and fault tolerance, which are crucial for handling email notifications reliably and efficiently at scale.

By leveraging brokers, we achieve improved performance, maintainable code, and the ability to scale our system seamlessly as per our requirements.

## REST API Endpoints

The application has the following endpoints:

- `GET /menu`: Retrieves the list of available products from the catalog.

        curl --request GET --url http://localhost:8000/menu

- `POST /orders`: Creates a new order with the provided details.

        curl --request POST \
        --url http://localhost:8000/orders \
        --header 'Content-Type: application/json' \
        --data '{
        "customer_id": "customer",
        "products": [
        {
        "name": "Latte",
        "variation": "Vanilla"
        }
        ],
        "location": "take-away"
        }'

- `GET /orders`: Retrieves the details of all orders.

        curl --request GET \
        --url http://localhost:8000/orders

- `PUT /orders/{order_id}`: Updates an order with the "Waiting" status.

        curl --request PUT \
        --url http://localhost:8000/orders/${ORDER_ID} \
        --header 'Content-Type: application/json' \
        --header 'manager_id: manager' \
        --data '{
            "customer_id": "customer",
            "products": [
                {
                    "name": "Latte",
                    "variation": "Hazelnut"
                }
            ],
            "location": "take-away"
        }'

- `DELETE /orders/{order_id}`: Cancels an order with the "Waiting" status.

        curl --request DELETE \
        --url http://localhost:8000/orders/${ORDER_ID}

- `POST /orders/{order_id}/status`: Changes the status of an order identified by the order ID.

        curl --request POST \
        --url http://localhost:8000/orders/${ORDER_ID}/status \
        --header 'manager_id: manager'

**Note:** The order database already contains a customer with the ID "customer" and a manager with the ID "manager".

Download the Insomnia collection clicking in the button below.

[![Run in Insomnia}](https://insomnia.rest/images/run.svg)](https://insomnia.rest/run/?label=trio-challenge&uri=)

## Test Coverage

The project has been developed with a strong focus on unit testing. Unit tests have been implemented to achieve 100% coverage for the entities and use cases. The tests ensure the correctness and reliability of the system by validating the behavior of individual components and their interactions.

The Test Data Builder Pattern was utilized to create various test scenarios and conditions. This pattern allows for the convenient creation of test data with different configurations, making it easier to verify the behavior of the system under different circumstances. By using the Test Data Builder Pattern, it becomes effortless to create complex and diverse test cases, ensuring thorough testing of the application's functionality.

| File                                            | Stmts   | Miss  | Cover    |
| ----------------------------------------------- | ------- | ----- | -------- |
| src/application/errors/bad_request.py           | 4       | 0     | 100%     |
| src/application/errors/forbidden.py             | 4       | 0     | 100%     |
| src/application/errors/not_found.py             | 4       | 0     | 100%     |
| src/application/handlers/status_changed.py      | 12      | 0     | 100%     |
| src/application/usecases/cancel_order.py        | 13      | 0     | 100%     |
| src/application/usecases/change_order_status.py | 29      | 0     | 100%     |
| src/application/usecases/place_order.py         | 42      | 0     | 100%     |
| src/application/usecases/update_order.py        | 50      | 0     | 100%     |
| src/application/usecases/view_menu.py           | 7       | 0     | 100%     |
| src/application/usecases/view_order_details.py  | 12      | 0     | 100%     |
| src/domain/entities/customer.py                 | 4       | 0     | 100%     |
| src/domain/entities/manager.py                  | 1       | 0     | 100%     |
| src/domain/entities/order.py                    | 49      | 0     | 100%     |
| src/domain/entities/product.py                  | 10      | 0     | 100%     |
| src/domain/events/status_changed.py             | 7       | 0     | 100%     |
| src/domain/service/products.py                  | 24      | 0     | 100%     |
| src/infra/broker/broker.py                      | 12      | 0     | 100%     |
| src/infra/repositories/customers.py             | 11      | 0     | 100%     |
| src/infra/repositories/managers.py              | 11      | 0     | 100%     |
| src/infra/repositories/orders.py                | 25      | 0     | 100%     |
| src/infra/repositories/products.py              | 12      | 0     | 100%     |
| **TOTAL**                                       | **343** | **0** | **100%** |

Run the tests and the coverage report with the following commands:

        $ coverage run -m pytest .
        $ coverage report

## Running the project

To run the application, you can utilize Docker and execute the following commands:

        $ docker build -t trio .
        $ docker run -d -p 8000:8000 trio

These commands build a Docker image for the application and then run a container based on that image, mapping port 8000 of the container to port 8000 of the host machine. This allows you to access the application through http://localhost:8000.

Make sure you have Docker installed and running on your system before executing these commands.

Thanks for reading!
