# commerce-all

A full-stack e-commerce platform built with Django, featuring product browsing, shopping cart functionality, secure checkout, user accounts, and admin dashboard. Designed for seamless shopping experiences with comprehensive order and review management.

## Quick Start

**Live site:** <a target="_blank">https://commerce-all-7e9e664f7d53.herokuapp.com/</a>

**Local setup:**

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Requirements:** Python 3.12, PostgreSQL, Cloudinary account (for image hosting), Django allauth setup

## Deployment

<details>
<summary><strong>Detailed Deployment Instructions</strong></summary>

### Local Setup

- Install dependencies from requirements.txt
- Create Cloudinary API link
- Create instance of PostgreSQL database
- (Optional) Configure app on Google auth platform:
    - Create app
    - Define host URLs
    - Create a client
    - Define redirect URLs
- Configure environment variables:
    - Project secret key
    - Database URL
    - Cloudinary API URL
    - Email server details (host, port, TLS/SSL, user, password)
    - (For Google sign in) Google client secret key and client ID
- Ensure settings file reflects this

### Heroku Deployment

To host on Heroku, create:

- `.python-version` file with `python 3.12`
- `Procfile` with `web: gunicorn commerce.wsgi`

Environment variables must be saved on Heroku, including DB and Cloudinary links.

</details>

## Technologies

Built in python and JS using django framework. Python dependencies listed in requirements.txt: gunicorn, crispyforms. Deployed on Heroku dynos using gunicorn and image hosting on cloudinary.
Account management is handled with django allauth and Google Oauth2 SSO.

## User stories

For this project I targeted a wide user base with a focus on young adults. To achieve this I leant into a simple and playful handrawn style. This design language is prevalent in clothing markets to imply a down-to-earth, consumer-centric brand. Features and user stories were created to ensure intuitive functionality, where ease of navigation is essential for this application, so as not to introduce any barriers to a user completing a purchase.
From this project brief, I created user stories:

| User Story                  | User                | Requirement                  | Intended functionality                                                                  |
| --------------------------- | ------------------- | ---------------------------- | --------------------------------------------------------------------------------------- |
| 1) Superuser                | Staff/Admin         | Admin portal and priviledges | Admin should be able to manage site content, user accounts and perform moderation tasks |
| 2) Regular user             | User                | User dashboard               | Manage account details and view order history                                           |
| 3) Site visitor             | Visitor             | Easily navigable site        | Create a purchase order for desired items                                               |
| 4) Admin and site visitor   | Admin/Visitor       | Impactful landing page       | Retrieve and highlight products on site load to drive user engagement                   |
| 5) Regular user             | User                | Contact form                 | Submit queries to site owners for order updates and issue resolution                    |
| 6) Site admin               | Admin               | Discount management          | Add discounts to products to drive sales and create promotion periods                   |
| 7) Regular user             | User                | Shopping cart and checkout   | Add products to cart and complete purchase orders                                       |
| 8) Site visitor/Buyer/Owner | Visitor/Buyer/Owner | Product reviews              | View and add product reviews to make informed purchasing decisions                      |

## UX design

E-commerce sites are incredibly information-dense, and almost exclusively present data for the user to interactive with. To accomplish this, and allow the site to become scaleable, a logical and modular DB schema is essential.

DB Schema:
<img width="1054" height="757" alt="image" src="https://github.com/user-attachments/assets/9486ffb0-3a1c-4557-95ca-be1187deb9dc" />

Users will be able to add products to a cart and upon purchase cart details will be added to order tables and deleted from cart tables.
Users will be able to add reviews to products, and perform CRUD operations on their reviews.

I created wireframes to block out desktop and mobile layouts of the main pages, highlighting layout and responsive behaviour.

<img width="2118" height="800" alt="IFAfinal wireframe" src="https://github.com/user-attachments/assets/fa32a5a4-508f-4f1f-bef9-d4d64201d413" />

## Features

**Target features:**

- User roles implemented with registration and deletion of accounts, and user panel to view activity history.
- Users can order items, add reviews and access their order history.
- Admin can perform CRUD operations on products and user reviews, and have read-only operations on user orders.
- Implementation of Stripe payment API (stretch goal).

**Implemented features:**

- Product list view with price, stock status, discounts.
- Product filtering with categorization, price and sort options.
- Product detail with reviews, additional image carousels and add to cart.
- Product reviews for signed in users, with edit and delete functionality - Full CRUD operations for users own records.
- Product quantities split by sizes.
- Cart and checkout workflow, with CRUD operations for all users (create cart, add to cart, remove from cart, update quantity).
- Order creation for verified users.
- Account centre - allows users to update account information and view order history.
- Discount codes for users in cart - configured with start and end dates and usage number.
- Google account SSO
- Persistent breadcrumb and navbar for ease of navigation

**Admin specific features:**

- Admin dashboard
- CRUD of all models:
    - Product entries, Product details, Product/Category Discounts, Categories, Product images, Discount Codes, Product Reviews.
    - Discounts can be configured for products, categories or all products.
    - Discount codes can apply to all products, or restricted to specific categories.

**Post-live features to be implemented:**

- Payment API
- Tax handling for enterprise customers.
- Automated stock handling (update on order completion)

In creating this site, many more features were implemented than the original product scope. To account for this, I assigned each week as a sprint period, and reexamined the MoSCoW priority of features.

Much of the complexity of theses features came from the persistence throughout the website: any functionality change would often need reflecting through product lists, detail, cart and order functionality. To mitigate this as much as possible, I split functionality into different apps, but to allow for this database schema updates were required.

Some features were de-scoped, in particular payment was excluded from this project due to need to host site inventory on Stripe (and use webhooks to sync these). Creating product entries ended up being a large time sink, and repeating this process for stripe would have significantly impacted timelines.

It was beyond the scope of this project to create automated DB runs, but this would have streamlined a lot of features - particularly discounts. Rather than fetching discounts, and calculating price adjustments, we would be able to run an hourly executable that takes any active discounts and applies these to a product discounted price field. This would also allow for live stock updates and reserving stock for users when items are added to cart.

DB Schema updates:

- Added product image table: This allows multiple product images to be associated with one product id.
- Product Sizes: Added Product size table to allow product quantity to be tracked across multiple sizes.

### Project Hurdles/Bugs

A few features caused some issues during development, particularly cart handling, shipping and stocking different sized items.

<div style="font-size: 0.9em; line-height: 1.4;">

#### Carts:

- **Approach:** In order to store items in a cart for purchase, initially I created a cart when a user added an item to the cart, and subsequent items to this cart. In order to achieve this I wanted to tie carts to users, to ensure a 1-1 relationship.
- **Problem:** This blocked non-logged in users from adding items to a cart.
- **Solution**: I updated the view to remove this constraint.
- **Further Iteration**: This meant after completing an order, futher items would be added to the same cart and cause integrity issues when creating an order.
- **Solution:** I updated DB schema to include a cart active status, and deactivated carts after order and created a new one. I used AI to add more defensive programming, which included selecting the most recent active user cart when creating an order to enforce database constraints.

#### Shipping:

- **Approach:** Shipping should affect order total, and give the option of free shipping for orders under £50.
- **Problem:** Shipping would not be reflected either in order total or update on screen in real-time.
- **Solution:** I added a field to the Order model for shipping cost and total price, so that this could be calculated in one view and then queried for use in further view. I added javascript to update relevant fields on the front end so this is visibile to the user.

#### Sizes:

- **Approach**: Each product should be able to have multiple size options.
- **Problem:** My initial approach added size to the Product model, which meant a new product would need to be added for each size, disrupting the shopping experience by showing seemingly duplicate products and increasing the amount of data entry for staff.
- **Solution:** I added a new model 'ProductSize' to link to a product and add a size and quantity, before updating relevant views. This did cause further considerations to the cart process, as this would not group cart items by size (e.g 3x M shirt would display as 3 separate cart items); so I updated CartItem model to add size to each entry.

</div>
Overall many of these development issues could have been avoided by better understanding the scope of the project. This would allow for a larger, more comprehensize DB schema, to allow more information to persist in DB, rather than needing to be created/calculated in multiple views.

## Agile

To aid development, the project length was divided into three sprints.
User stories were added to a kanban board, and development items to achieve these were created as child objects. This enabled me to set the user stories as swimlanes to better view progress towards each issue.
I used custom labels for MoSCoW prioritisation and targeted 60% must have 30% should have, 10% could have issues for each sprint.
The development workflow was customised to add a testing and grooming status to the kanban board, which allows for issues to be developed, and then set to groom to be considered for further iteration in future sprints.

<img width="1919" height="851" alt="image" src="https://github.com/user-attachments/assets/a15073e0-27a7-41ac-8c88-487ea83e8947" />

For initial creation of the minimum viable project, no git workflow was utilised, but following deployment of the MVP this repo will use a gitflow approach for further release and feature development.

## Testing

**Testing approach:** Automated unit tests for models, views, and forms built with django test module. Manual UX testing with user group feedback. Lighthouse performance audits; WCAG 2.1 accessibility compliance via WAVE (webAIM browser extension).
HTML, CSS and JS validated with w3schools, jigsaw and https://validatejavascript.com/.
A few html errors persist, but these are false-positive screen reader errors around bootstrap modals. After checking the documentation and checking with AI, I'm confident that this has the intended behaviour on screen readers.<img width="1130" height="98" alt="image" src="https://github.com/user-attachments/assets/f97d301f-108f-4b8f-bca2-439b5c5895d0" />
One CSS issue was raised: that font-optical-auto is an invalid property, however after checking the support for this on caniuse, it has widespread browser support and I have elected to leave this in.
<img width="783" height="171" alt="image" src="https://github.com/user-attachments/assets/e70329f5-ecbf-497e-aad4-306714d72886" />
<img width="1384" height="818" alt="image" src="https://github.com/user-attachments/assets/135c17e3-139c-40fa-afaf-dc32025d395e" />


**Unit test results:** 316 automated tests with 100% pass rate and 95% code coverage. Coverage was calculated against number of lines in views/models etc that were called in unit test suite.

| Component    | Tests | Coverage | Pass rate |
| ------------ | ----- | -------- | --------- |
| About App    | 50    | 100%     | 100%      |
| Cart App     | 114   | 85%      | 100%      |
| Dashboard    | 42    | 100%     | 100%      |
| Enter App    | 16    | 100%     | 100%      |
| Products App | 94    | 93%      | 100%      |

For detailed unit test breakdown and coverage analysis, see [TESTING_EXIT_REPORT.md](TESTING_EXIT_REPORT.md).

| User Story                  | Expected functionality                                                                  | Actual Functionality                                                                                                                 | Pass/Fail |
| --------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| 1) Superuser                | Admin should be able to manage site content, user accounts and perform moderation tasks | Admin panel has full CRUD operations over all models. Reviews require admin approval.                                                | Pass      |
| 2) Regular user             | Manage account details and view order history                                           | Account centre displays order history and quick links to change password, email, username                                            | Pass      |
| 3) Site visitor             | Create a purchase order for desired items                                               | Checkout workflow creates order, confirms and adds to order history in account centre                                                | Pass      |
| 4) Admin and site visitor   | Retrieve and highlight products on site load to drive user engagement                   | No shop highlights/featured products were implemented                                                                                | Fail      |
| 5) Regular user             | Submit queries to site owners for order updates and issue resolution                    | Order contact form and email server saves user queries to admin panel and marks as read/unread for Categorizing                      | Pass      |
| 6) Site admin               | Add discounts to products to drive sales and create promotion periods                   | Discounts can be applied to product, category and have specified timeframe.                                                          | Pass      |
| 7) Regular user             | Add products to cart and complete purchase orders                                       | User can create cart add products and checkout. Carts are stored in user session to retain products when revisiting site.            | Pass      |
| 8) Site visitor/Buyer/Owner | View and add product reviews to make informed purchasing decisions                      | Product reviews visible to all. Authenticated users can leave and edit/delete reviews. Admin can approve and see unapproved reviews. | Pass      |

**Accessibility:** All pages achieve WCAG AAA compliance with Lighthouse scores ≥9.6/10.
Initial Google lighthouse testing largely revealed issues with third party cookies and insecure photo delivery, associated with cloudiary - this was easily remidied by enforcing 'secure = true' in cloudinary SDK config. In future I would prompt user to accept these for site function or seek an alternative hosting provider <img width="851" height="449" alt="image" src="https://github.com/user-attachments/assets/5f9609d9-2626-4c5c-b33b-de5ea45393dd" />

**Responsivity:** All pages are fully responsive across mobile, tablet, and desktop viewports with consistent layouts and navigation.

| Page               | Phone                                                                                                                                                  | Tablet                                                                                                                                                 | Desktop                                                                                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shop               | <img width="363" height="640" alt="Shop mobile view" src="https://github.com/user-attachments/assets/a6d93a3d-a839-454c-a31c-63a53273892f" />          | <img width="532" height="755" alt="Shop tablet view" src="https://github.com/user-attachments/assets/773a0b7c-a3c3-4979-80db-6c7182ba3e92" />          | <img width="1208" height="686" alt="Shop desktop view" src="https://github.com/user-attachments/assets/47f2ff65-6515-4d8d-a9d9-d28b1c3370cc" />          |
| Item Detail        | <img width="497" height="797" alt="Item detail mobile" src="https://github.com/user-attachments/assets/387b8b77-9b82-44fb-b984-667af4e356a3" />        | <img width="531" height="756" alt="Item detail tablet" src="https://github.com/user-attachments/assets/0dfd5bcf-9512-4021-b291-28c937d63696" />        | <img width="1386" height="782" alt="Item detail desktop" src="https://github.com/user-attachments/assets/39aa48ff-a040-406c-9df7-a9d60ae2e78d" />        |
| Cart               | <img width="366" height="639" alt="Cart mobile" src="https://github.com/user-attachments/assets/4d1e6088-acc7-4d96-bf7d-0ab58a627f17" />               | <img width="471" height="676" alt="Cart tablet" src="https://github.com/user-attachments/assets/7023b524-6fa8-4d68-8ee7-68516b109aa0" />               | <img width="1209" height="683" alt="Cart desktop" src="https://github.com/user-attachments/assets/8ae55541-eaed-4b74-9d32-b7fc314d9ad6" />               |
| Checkout           | <img width="360" height="633" alt="Checkout mobile" src="https://github.com/user-attachments/assets/f9208a18-5de7-405a-8870-0b36aeadca2c" />           | <img width="522" height="747" alt="Checkout tablet" src="https://github.com/user-attachments/assets/ed5dfbfe-4a72-43a2-bd8f-b694472de929" />           | <img width="1209" height="684" alt="Checkout desktop" src="https://github.com/user-attachments/assets/c0f2ead9-80d1-49d2-8215-51e736629630" />           |
| Order Confirmation | <img width="362" height="639" alt="Order confirmation mobile" src="https://github.com/user-attachments/assets/eba13542-c2a3-4d53-9819-f0b5f5fe51c0" /> | <img width="527" height="751" alt="Order confirmation tablet" src="https://github.com/user-attachments/assets/bd0a8fb4-5219-4518-9a4d-e4df4b4cc0a8" /> | <img width="1213" height="687" alt="Order confirmation desktop" src="https://github.com/user-attachments/assets/3088a9cb-dba2-4117-bf34-2454e410e905" /> |

## AI retrospective

**Main use cases**:

- Project planning and organisation tooling
- Code creation (for simple, easy to define use cases)
- Debugging
- Test pack creation

To aid development, I created a custom copilot agent inspired by u/burkeholland 's gpt beastmode agent. The aim of this was to standardise the approach of free and less-than-premium usage models (which often struggle with more complex and persistent conversations due to a reduced context window) to give repeateable, more viable results to allow for greater usage within my premium requests budget.
To achieve this, I defined three main goals: be opinionated (don't pander to user), break down tasks into to-do lists, ask for user input before moving to next steps.

I used AI to create a project checklist to ensure I had considered all bases, and serve as a project status checker.
I created initial HTML boilerplates with AI by attaching wireframes. This streamlined development, though did require manual intervention, as this created a large amount of redundant functionality that could be present on an e-commerce website, but was not needed for the scope of my project.

Test pack creation was augmented with AI - I defined a test suite and implemented initial unit tests for models, views, and forms; before using Claude Haiku to expand coverage and create tests for missed edge cases, including minor stress testing.
Again using Claude, I created a testing exit summary report to better describe the scope and success of the test suite. This mimicked working with an external QA team, who have separation from code creation and can be more analytical and penetrative when creating test suites.

In future I would continue to use custom agent prompts, and boilerplate creation. I would ensure that any feature creation would include the full workspace in requests and use premium request models to ensure the largest amount of context and reduce code that doesn't interact well with the existing codebase.

Unit test creation through AI was a very impactful addition, and greatly increased coverage as there were many cases I had not thought to test. It is worth noting that it would create unused variables and sometimes invalid tests, so in future I will place hard limits on the number of generated tests (e.g 50 tests per app) to reduce the amount of manual intervention needed.

## References

u/burkeholland/minibeast.md: https://gist.github.com/burkeholland/1366d67f8d59247e098b6df3c6a6e38 <br>
Design: https://www.ssense.com/en-gb/, https://london.doverstreetmarket.com/
