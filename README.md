<h1 style="color:lightblue;">Artful Atlas : Moroccan artworks E-Commerce Platform</h1>

<p>Welcome to the Moroccan artworks E-Commerce Platform! This project aims to promote Moroccan artists by providing a robust e-commerce platform to showcase and sell their art globally.</p>


![image](https://github.com/Warrior-Player/Official-backend/assets/118373522/2c4c1be9-ca87-4cb1-b76a-e2e6de1dc280)


<h2 style="color:lightblue;">Table of Contents</h2>

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Documentation](#api-documentation)
6. [Contributing](#contributing)
7. [Contact](#contact)
8. [Perspectives](#perspectives)

<h2 id="features" style="color:lightblue;">Features</h2>

- **User Registration and Authentication:** Account creation and login, either via website's own form, or with Google and Facebook using Django Allauth.
- **Artwork & Artist Listings:** Display detailed artwork & artist listings with descriptions and images.
- **Search and Filter:** Search bar and multiple types of filters.
- **User Reviews and Ratings:** Users can leave reviews and ratings for artworks, artists and for the website itself as a testimonial.
- **Shopping Cart, Wishlist and Checkout:** Add / Remove from cart, add / remove from wishlist, secure checkout and payment processing using Paypal.
- **Maker an Offer:** Attempt to buy an artwork with a custom price that is sent with a message to the corresponding artist.
- **Order Management:** View order history and track order status, either as a buyer, or as an artist.
- **Artist Profiles:** Detailed profiles and portfolios of artists.
- **Recommendations:** Personalized artworks recommendations.
- **Security and Compliance:** Data security measures and compliance with regulations.
- **Admin Dashboard:** Manage (Add / Edit / Remove / Approve) artworks, orders, offers, and user accounts with analytics and reporting tools, using a custom template : Django Jazzmin.
- **Direct Contact with Admins:** Users can directly contact website admins using Crisp live chat integration.
- **AJAX for Dynamic Content:** Enhance user experience with dynamic page updates.
- **RESTful API:** Integration with third-party applications and services.

<h2 id="technologies-used" style="color:lightblue;">Technologies Used</h2>

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript, AJAX
- **Database:** SQLite3
- **Authentication:** Django Allauth
- **Hosting:** 
- **APIs:** Google, Facebook
- **SDK:**  Paypal

<h2 id="installation" style="color:lightblue;">Installation</h2>

<h3>Prerequisites</h3>

- Python 3.x
- Django
- Django REST Framework
- Django Allauth
- Django Jazzmin

<h3>Steps</h3>

1. Clone the repository:

    ```sh
    git clone https://github.com/Warrior-Player/Official-backend.git
    cd Official-backend
    ```

2. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```sh
    python manage.py migrate
    ```

4. Create a superuser:

    ```sh
    python manage.py createsuperuser
    ```

5. Run the server:

    ```sh
    python manage.py runserver
    ```

<h2 id="usage" style="color:lightblue;">Usage</h2>

- **Access the website:** Open your browser and go to `http://127.0.0.1:8000/`
- **Admin Panel:** Access the admin dashboard at `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.
<!-- - **API Endpoints:** Use tools like Postman to interact with the API endpoints. -->

<h2 id="api-documentation" style="color:lightblue;">API / SDK Documentation</h2>

<p>Detailed API & SDK documentations can be found here : <br> 
  - https://developers.facebook.com/docs/ <br>
  - https://developers.google.com/docs/api/reference/rest <br>
  - https://docs.djangoproject.com/en/5.0/ref/ <br>
  - https://developer.paypal.com/sdk/js/reference/ <br>
  The API follows RESTful principles for seamless integration with third-party applications.</p>

<h2 id="contributing" style="color:lightblue;">Contributing</h2>

<p>We welcome contributions! Follow these steps to contribute:</p>

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request.

<p>Please ensure your code adheres to our coding standards and include relevant tests.</p>


<h2 id="contact" style="color:lightblue;">Contact</h2>

<p>For any inquiries or feedback, please contact us at <a href="mailto:ayoubma321@gmail.com">ayoubma321@gmail.com</a>.</p>

<p>We hope this project helps promote the rich and diverse Moroccan craftsmanship to a global audience. Thank you for your support!</p>

<h2 id="perspectives">Future Directions</h2>

- **Internationalization:** Multi-language support and international shipping options.
- **Community Engagement:** Blog, newsletter, online contests, and exhibitions.
- **Performance Optimization:** Cloud computing and auto-scaling.
