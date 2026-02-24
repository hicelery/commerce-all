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
- Product filtering with categorization, price and sort options.
- Product detail view with reviews, additional image carousels and add to cart.
- Product reviews for signed in users, with edit and delete functionality - Full CRUD operations for users own records.
- Product quantities split by sizes.
- Cart and checkout workflow, with CRUD operations for all users (create cart, add to cart, remove from cart, update quantity).
- Order creation for verified users.
- Account centre - allows users to update account information and view order history.
- Discount codes for users in cart - configured with start and end dates and usage number.
- Google account SSO

Admin specific features:

- Admin dashboard
- CRUD of all models:
    - Product entries, Product details, Product/Category Discounts, Categories, Product images, Discount Codes, Product Reviews.
      Discounts can be configured for products, categories or all products. Discount codes can apply to all products, or restricted to specific categories.

Post-live features to be implemented:

- Payment API
- Tax handling for enterprise customers.
- Automated stock handling (update on order completion)

In creating this site, many more features were implemented than the original product scope. To account for this, I assigned each week as a sprint period, and reexamined the MoSCoW priority of features.
Much of the complexity of theses features came from the persistence throughout the website: any functionality change would often need reflecting through product lists, detail, cart and order functionality. To mitigate this as much as possible, I split functionality into different apps, but to allow for this database schema updates were required. In future I would allow for a larger, more comprehensize DB schema, to allow more information to persist in DB, rather than needing to be created/calculated in multiple views.
It was beyond the scope of this project to create automated DB runs, but this would have streamlined a lot of features - particularly discounts. Rather than fetching discounts, and calculating price adjustments, we would be able to run an hourly executable that takes any active discounts and applies these to a product discounted price field. This would also allow for live stock updates and reserving stock for users when items are added to cart.

DB Schema updates:

- Added product image table: This allows multiple product images to be associated with one product id.
- Product Sizes: Added Product size table to allow product quantity to be tracked across multiple sizes.

## Technologies

Built in python and JS using django framework. Python dependencies listed in requirements.txt: gunicorn, crispyforms. Deployed on Heroku dynos using gunicorn and image hosting on cloudinary.
Account management is handled with django allauth and Google Oauth2 SSO.

## Testing

Automated tests were created upon MVP deployment, and kept as a regression test suite for future feature implementation. General UX testing was conducted following site maps and distributing the site to a prospective user group to provide feedback and bugs; which greatly increased testing coverage.

I created initial unit tests for models, views, and forms, before using Claude Haiku to expand coverage and create tests for edge cases I may have missed, including minor stress testing; before creating a coverage summary report to better describe the scope of the test suite. This mimicked working with an external QA team, who have separation from code creation and can be more analytical and penetrative when creating test suites.

Lighthouse testing was conducted for performance and high-level accessibility/security testing. WCAG testing utilized WAVE(WebAIM) browser extension.

### Test Suite Exit Report

#### Dashboard Tests: 42 Tests

##### `TestProfileViewAccountCentre` (11 tests)

Tests for the account centre which displays user orders:

- **Login Requirements**: Tests authentication redirects for unauthenticated users
- **Access Control**: Verifies only authenticated users can access the view
- **Order Display**: Tests correct template usage (`account_centre.html`) and context variables
- **Data Filtering**: Ensures users only see their own orders, not other users' orders
- **Sorting**: Validates orders are sorted by `updated_at` in descending order
- **Item Counting**: Tests automatic item count calculation and aggregation per order
- **Edge Cases**: No orders, many orders (50+), orders with various item counts (0-100)

##### `TestProfilePageView` (8 tests)

Tests for the profile page view (GET profile form):

- **Authentication**: Validates login requirement
- **Form Handling**: Unbound form with user data pre-populated correctly
- **Template Verification**: Correct template usage (`profile.html`)
- **Field Validation**: All expected fields present (`first_name`, `last_name`, `username`)
- **HTTP Methods**: Tests both GET and POST request handling

##### `TestProfileUpdateView` (15 tests)

Tests for the profile update view (POST profile updates):

- **Valid Updates**: Successful profile modifications with success message display
- **Partial Updates**: Updating individual fields (`first_name`, `last_name`) independently
- **Data Persistence**: Verifies non-profile fields are preserved (email, password, etc.)
- **Invalid Data**: Tests with missing required fields and duplicate username attempts
- **Edge Cases**: Empty fields, case-sensitive username handling
- **Form Validation**: Warning messages displayed on invalid submissions
- **HTTP Methods**: GET returns unbound form, POST processes updates

##### `TestDashboardEdgeCases` (8 tests)

Edge case and boundary condition tests:

- **Special Characters,  Unicode Support**: Names with hyphens, apostrophes and accents
- **Length Limits**: Very long names (30+ characters), whitespace-only values
- **Data Isolation**: Verifies session persistence across multiple operations
- **Stress Tests**: 50 orders per user, 100 items per order

#### About & Products Tests: 13 Tests

Comprehensive tests for:

- Contact form submission
- Product listing and filtering
- Product detail views
- Product reviews and ratings
- Category and product relationships

#### Accessibility

All pages tested manually with WAVE and lighthouse and have no WCAG errors. All pages have AIM score of or above 9.6/10  <img width="600" aspect-ratio="1/1" alt="image" src="https://github.com/user-attachments/assets/f1e56a47-b66d-4308-95f5-96af00128396" />


## Deployment

## AI retrospective

To aid development, I created a custom copilot agent inspired by u/burkeholland 's gpt beastmode agent. The aim of this was to increase the contextual understanding of free and less-than-premium usage models (which often struggle with more complex and persistent conversations due to a reduced context window) to allow for greater usage within my premium requests budget. To achieve this, I defined three main goals: be opinionated, break down tasks into to-do lists, ask for user input before moving to next steps.

I used AI to create a project checklist to ensure I had considered all bases, and serve as a project status checker.
I created initial HTML boilerplates from wireframes, thought this did require manual intervention, as this created a large amount of redundant functionality that could be present on an e-commerce website, but was not needed for the scope of my project.

Test pack creation was augmented - I defined a test suite and asked AI to expand coverage: to create tests for missed edge cases; alongside validating the created tests were behaving as expected.

In future I would continue to use custom agent prompts, and boilerplate creation. I would ensure that any feature creation would include the full workspace in requests and use premium request models to ensure the largest amount of context and reduce code that doesn't interact well with the existing codebase.

## References

u/burkeholland/minibeast.md
