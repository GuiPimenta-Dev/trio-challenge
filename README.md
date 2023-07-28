# Technical Design Document

## Introduction

This repository is dedicated to solving the challenge proposed in the link: https://trio.notion.site/Trio-Coffee-Shop-Challenge-a0b21f7d13ed489ba736973d4c165877

## Core Domain

The core domain consists of the following entities and their functionalities:

- **Managers**: Change the order status.
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

We decided to use the State design pattern for the Order entity based on the possibility to easily include new status scenarios in the future.

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

Repositories are an essential part of the application architecture, providing an abstraction layer between the domain logic and the underlying data persistence mechanism. In our project, we have embraced the concept of having a separate repository for each aggregate root.

An aggregate root is a concept from Domain-Driven Design (DDD) that represents a group of related entities treated as a single unit. It acts as a boundary for consistency and transactional boundaries within the domain model. The aggregate root encapsulates one or more entities and defines the rules and operations that govern their interactions. As a result, we have the following repositories: **CustomersRepository**, **OrdersRepository**, **ProductsRepository** and **ManagersRepository**.

These repositories serve as a bridge, enabling the application to interact with the data storage without directly coupling the domain logic to specific implementation details. They adhere to the principles of the Clean Architecture, promoting separation of concerns and decoupling the codebase from infrastructure-specific considerations.

We opted for in-memory repositories to simplify and expedite the prototyping and iteration processes. This approach allowed us to focus on the core domain while temporarily abstracting away the intricacies of working with actual databases or external systems.

However, it is crucial to note that our architecture is designed to be flexible and adaptable. We have followed the principles of dependency inversion and dependency injection to ensure that the data access and communication mechanisms can be easily replaced or integrated with real implementations as required in a production environment.

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
- Use the generated app password in your application or device settings where you need to enter your Gmail password. Note that you won't use your regular Gmail account password for these cases.

### Brokers

Brokers are used to facilitate communication and coordination between different components or services in a distributed system. They act as intermediaries, enabling asynchronous messaging and decoupling the sender and receiver.

Using brokers in our system brings several advantages. Firstly, by enabling asynchronous message communication, brokers allow the update order status endpoint to respond faster. This is because the endpoint no longer needs to wait for the email to be sent before providing a response to the user. As a result, the overall system performance is improved.

Moreover, utilizing brokers helps us adhere to the single responsibility principle. With the use of brokers, the update order status endpoint can focus solely on changing the status without the responsibility of handling email notifications. This separation of concerns enhances the maintainability and testability of our codebase.

In this project, an in-memory broker implementation was chosen for simplicity. However, it's important to note that we have the flexibility to easily create an adapter and integrate a more robust and scalable message broker like Redis or RabbitMQ. These real brokers offer additional features such as message persistence, queuing, and fault tolerance, which are crucial for handling email notifications reliably and efficiently at scale.

While it is true that including the broker introduces a certain level of complexity that might be considered overkill, the decision was driven by the necessity for improved response times in a production environment. Additionally, the inclusion of the broker eliminates the need for the update order status use case to possess knowledge about customer email details. Instead, it simply emits a domain event of Status Changed, allowing the designated event handler to take care of the email notification.

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

The project has been developed following the Test-Driven Development (TDD) approach, employing the Red-Green-Refactor methodology. This approach emphasizes the creation of unit tests prior to writing the actual code.

Throughout the development process, unit tests were implemented to achieve comprehensive coverage for both entities and use cases. By aiming for 100% test coverage, we ensured that the system's behavior and functionality were thoroughly validated. These tests played a crucial role in guaranteeing the correctness and reliability of the system, as they assessed the behavior of individual components and their interactions.

To facilitate the creation of diverse and complex test scenarios, we utilized the Test Data Builder Pattern. This pattern allowed us to conveniently generate test data with different configurations, enabling us to verify the system's behavior under various circumstances. By employing the Test Data Builder Pattern, we ensured that our test cases were comprehensive, exhaustive, and representative of real-world scenarios.

The combination of TDD and the Test Data Builder Pattern has enabled us to develop a robust and well-tested application. Through rigorous testing and adherence to best practices, we have strived to deliver a reliable and high-quality solution.

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
