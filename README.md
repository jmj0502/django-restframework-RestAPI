# Django-Restframework-RestAPI
A fully featured RestAPI built with Django Restframework. The API provides Income/Expense tracking services, and its propected with token based authentication.

## Project Structure
This project takes advantage of Django's hexagonal architecture to handle the whole app bussiness logic. The app is structured as follows:
* Authenticacion: This module contains an user model, a custom authentication model, their corresponding serializers and an email verification service written using Restframework and built-in packages.
* Income: This module handles the income bussiness logic. It contains an Income model, it's correnponding serializers and views.
* Expense: This module handles the expenses bussiness logic. It contains an Expense model, it's corresponding serializers and views.

I built the API in order to learn how to deal with techologies I use on a day-to-day basis in a different stack and context. The API also contains swagger integration, since it provides an efficient way to document and test every endpoint.
