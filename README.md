# commerce-all

Commerce-all is a sleek, navigable e-commerce website built with django designed for end users and site administrators.

Deployed link:

## UX design

E-commerce sites are incredibly information-dense, and almost exclusively present data for the user to interactive with. Ease of navigation is essential for this application, so as not to introduce any barriers to a user completing a transaction.
To accomplish this, and allow the site to become scaleable, a logical and modular DB schema is essential.

DB Schema:
<img width="1054" height="757" alt="image" src="https://github.com/user-attachments/assets/9486ffb0-3a1c-4557-95ca-be1187deb9dc" />

Users will be able to add products to a cart and upon purchase cart details will be added to order tables and deleted from cart tables.
Users will be able to add reviews to products, and perform CRUD operations on their reviews.


## Features

Target features:
- User roles implemented with registration and deletion of accounts, and user panel to view activity history.
- Users can order items, add reviews and access their order history.
- Admin can perform CRUD operations on products and user reviews, and have read-only operations on user orders.
- Implementation of Stripe payment API (stretch goal).

Implemented features:
- Product list view with price, stock status, discounts.
- Product filtering with categorization, price and sort options
- Product detail view with reviews, additional image carousels and add to cart
- Product reviews for signed in users, with edit and delete functionality - Full CRUD operations for users own records
- Cart and checkout workflow, with CRUD operations for all users (create cart, add to cart, remove from cart, update quantity).
- Order creation for verified users.
- Account centre - allows users to update account information and view order history
- Discount codes for users in cart - configured with start and end dates and usage number.

Admin specific features:
- Admin dashboard
- CRUD of all models:
  - Product entries, Product details, Product/Category Discounts, Categories, Product images, Discount Codes, Product Reviews.
 Discounts can be configured for products, categories or all products. Discount codes can apply to all products, or restricted to specific categories.

In creating this site, many more features were implemented than the original product scope. To account for this, I assigned each week as a sprint period, and reexamined the MoSCoW priority of features. 
Much of the complexity of theses features came from the persistence throughout the website: any functionality change would often need reflecting through product lists, detail, cart and order functionality. To mitigate this as much as possible, I split functionality into different apps, but to allow for this database schema updates were required. In future I would allow for a larger, more comprehensize DB schema, to allow more information to persist in DB, rather than needing to be created/calculated in multiple views.

## Technologies

Built in python and JS using django framework. Python dependencies listed in requirements.txt: gunicorn, crispyforms. Deployed on Heroku dynos using gunicorn and image hosting on cloudinary.

## Testing

## Deployment

## AI retrospective

To aid development, I created a custom copilot agent inspired by u/burkeholland 's gpt beastmode agent. The aim of this was to increase the contextual understanding of free and less-than-premium usage models (which often struggle with more complex and persistent conversations due to a reduced context window) to allow for greater usage within my premium requests budget. To achieve this, I defined three main goals: be opinionated, break down tasks into to-do lists, ask for user input before moving to next steps.
It's worth noting that using custom agents with premium request models will drastically increase the rate at which context window is filled due to additional tool definitions.

I used AI to create a project checklist to ensure I had considered all bases, to debug, discuss functionality and for light code creation.
I created initial HTML boilerplates from wireframes, thought this did require manual intervention.

Test pack creation was augmented - I defined a test suite and asked AI to expand coverage: to create tests for missed edge cases; alongside validating the created tests were behaving as expected.

## References

u/burkeholland/minibeast.md
