
# Luxor Project 🚀

## Project Overview 🌟
This project was developed during my internship at **Luxor**. My role involved contributing to the development and improvement of internal software solutions aimed at automating business operations and improving overall efficiency.

The main objective of the project was to design and implement a **product management system** that allows users to:
- View and update product details stored in a database.
- Calculate the total cost of products, incorporating different pricing and tax elements.
- Generate reports for products in a standardized PDF format.
- Automate the handling of logistical and financial data across various departments.

This project helped **Luxor** streamline its processes, enabling more efficient product management, better cost tracking, and error-free tax calculations.

## Technologies Used 💻
The following technologies were used to develop the system:

- **Programming Languages:** 
  - **Python**: Main language for building the application logic and interfacing with the database.

- **Frameworks & Libraries:**
  - **PyQt5**: Used for building the desktop GUI to manage the product information.
  - **SQLAlchemy**: Object-relational mapping (ORM) for interacting with the database and managing product and tax information.

- **Tools & Platforms:**
  - **Git**: Version control to manage the project’s codebase.

- **Database:**
  - **SQLAlchemy** was used to manage the product data (e.g., product name, unit, supplier, price) and tax information (e.g., YVA and FODEC percentages).
  - Key models: 
    - `Produits` (for product details)
    - `TaxInfo` (for tax data such as VAT and other tax percentages)

## Features ✨
Here are the key features of the Luxor Product Management System:

- **Database Integration:** Seamless connection with **SQLAlchemy** for handling product data, taxes, and supplier details.
- **Product Management System:** Allows users to:
  - **Add new products** to the database with key details (e.g., name, price, quantity, supplier).
  - **Edit or delete** product entries when needed.
  - **View a product’s detailed information** such as price, tax, weight, supplier, and more.
- **Cost Calculation Automation:** Automatically calculates the total cost of a product by considering factors like:
  - **Unit price**, **quantity**, and **unit of measurement**.
  - **Taxes**: Using tax data from the **TaxInfo** table (e.g., YVA, FODEC percentages).
  - **Currency conversion**: Handles product cost in different currencies (including Tunisian Dinar - TND).
- **PDF Reporting:** Generates detailed PDF reports containing:
  - Product details with specific formatting for unit prices and taxes.
  - The logo placed symmetrically on the left and the current date on the right.
  - Customizable table formats for larger datasets.
- **Dynamic Form Inputs:** Dropdown menus populated dynamically from the database for fields like:
  - **Devise** (currency)
  - **Incoterm** (logistics term)
  - **Unité** (unit of measurement)
  - **Fournisseur** (supplier)
  - **Autorisation** (authorization status)

## Installation 🛠️
To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/luxor-project.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd luxor-project
   ```

3. **Install the required dependencies:**
   Ensure you have **Python** installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   The project requires a properly set up database. You can use the following script to initialize the database schema:
   ```bash
   python setup_database.py
   ```

5. **Run the application:**
   Once the dependencies and database are set up, you can run the application using:
   ```bash
   python main.py
   ```

## Usage 🖥️
After the application is running, you can interact with the system via the **PyQt5** GUI. Some of the main features include:

- **Login:** A secure login screen for authentication 🔐. It ensures that only authorized users can access the system.
- **Product Management:** View, add, update, or delete product details 📦. You can manage information such as product name, unit, supplier, pricing, and tax data.
- **Cost Calculation Form:** Select a product and automatically calculate the cost based on its unit price, quantity, and tax information 💰. This system ensures precise cost calculations for efficient product pricing.
- **PDF Reports:** Generate and print detailed reports in a **PDF** format. These reports contain all the relevant product details, tax calculations, and other necessary information 📄.

## Contributing 🤝
If you'd like to contribute to this project, please follow these steps:

1. **Fork the repository** to your own GitHub account.
2. **Create a new branch** for your feature or fix.
3. **Make your changes** and **commit** them.
4. **Push** your changes to your forked repository.
5. **Create a pull request** to propose your changes.

I will review your changes and merge them into the main repository if appropriate.

## License 📝
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙏
- Special thanks to **Luxor** for providing the opportunity to work on this project during my internship.
- Thanks to the development team at **Luxor** for their support and guidance throughout the project.
- The **ISO 9001 certification** for maintaining high standards of quality and efficiency.
