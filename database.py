import sqlite3
import os
from datetime import datetime


# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "pizza_house.db"
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    conn = get_connection()

    # -----------------------------------------------------
    # ORDERS TABLE
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            item_name TEXT NOT NULL,
            size TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            toppings TEXT,
            order_type TEXT NOT NULL,
            subtotal REAL NOT NULL,
            gst REAL NOT NULL,
            total REAL NOT NULL,
            order_date TEXT NOT NULL
        )
    """)

    # -----------------------------------------------------
    # MENU TABLE
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL UNIQUE,
            small_price REAL NOT NULL DEFAULT 0,
            medium_price REAL NOT NULL DEFAULT 0,
            large_price REAL NOT NULL DEFAULT 0
        )
    """)

    # -----------------------------------------------------
    # BOOKINGS TABLE
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            table_number TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            booking_date_created TEXT NOT NULL
        )
    """)

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            mobile TEXT UNIQUE
        )
    """)

    # -----------------------------------------------------
    # DEFAULT MENU
    # -----------------------------------------------------

    menu_items = [

        ("Margherita", 199, 299, 399),

        ("Farmhouse", 249, 349, 449),

        ("Veggie Paradise", 249, 349, 449),

        ("Paneer Tikka", 269, 369, 469),

        ("Cheese Corn", 229, 329, 429),

        ("Pepperoni", 299, 399, 499)

    ]

    for item in menu_items:

        conn.execute(
            """
            INSERT OR IGNORE INTO menu (
                item_name,
                small_price,
                medium_price,
                large_price
            )
            VALUES (?, ?, ?, ?)
            """,
            item
        )

    # -----------------------------------------------------
    # DEFAULT ADMIN
    # -----------------------------------------------------

    admin_exists = conn.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        ("admin",)
    ).fetchone()

    if not admin_exists:

        conn.execute(
            """
            INSERT INTO users (
                name,
                username,
                password,
                role,
                mobile
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Pizza House Admin",
                "admin",
                "admin123",
                "admin",
                None
            )
        )

    # -----------------------------------------------------
    # DEFAULT CUSTOMER
    # -----------------------------------------------------

    customer_exists = conn.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        ("customer",)
    ).fetchone()

    if not customer_exists:

        conn.execute(
            """
            INSERT INTO users (
                name,
                username,
                password,
                role,
                mobile
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Pizza House Customer",
                "customer",
                "customer123",
                "customer",
                "9999999999"
            )
        )

    conn.commit()

    conn.close()


# =========================================================
# USERS / LOGIN
# =========================================================

def get_user(username, password, role):

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
          AND password = ?
          AND role = ?
        """,
        (
            username,
            password,
            role
        )
    ).fetchone()

    conn.close()

    return user


def get_user_by_username(username):

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    conn.close()

    return user


def create_user(
    name,
    username,
    password,
    role,
    mobile=None
):

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            INSERT INTO users (
                name,
                username,
                password,
                role,
                mobile
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                username,
                password,
                role,
                mobile
            )
        )

        user_id = cursor.lastrowid

        conn.commit()

        return user_id

    except sqlite3.IntegrityError:

        return None

    finally:

        conn.close()


# =========================================================
# ORDERS
# =========================================================

def get_orders(search=""):

    conn = get_connection()

    if search:

        orders = conn.execute(
            """
            SELECT *
            FROM orders
            WHERE customer_name LIKE ?
               OR mobile LIKE ?
               OR item_name LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    else:

        orders = conn.execute(
            """
            SELECT *
            FROM orders
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return orders


def get_order(order_id):

    conn = get_connection()

    order = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    conn.close()

    return order


def create_order(
    customer_name,
    mobile,
    item_name,
    size,
    quantity,
    price,
    toppings,
    order_type,
    subtotal,
    gst,
    total,
    order_date=None
):

    if order_date is None:

        order_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO orders (
            customer_name,
            mobile,
            item_name,
            size,
            quantity,
            price,
            toppings,
            order_type,
            subtotal,
            gst,
            total,
            order_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_name,
            mobile,
            item_name,
            size,
            quantity,
            price,
            toppings,
            order_type,
            subtotal,
            gst,
            total,
            order_date
        )
    )

    order_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return order_id


def delete_order(order_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM orders
        WHERE id = ?
        """,
        (order_id,)
    )

    conn.commit()

    conn.close()


# =========================================================
# CUSTOMERS
# =========================================================

def get_customers():

    conn = get_connection()

    customers = conn.execute(
        """
        SELECT
            customer_name,
            mobile,
            COUNT(*) AS total_orders,
            COALESCE(SUM(total), 0) AS total_spending
        FROM orders
        GROUP BY customer_name, mobile
        ORDER BY customer_name
        """
    ).fetchall()

    conn.close()

    return customers


def get_customer_orders(mobile):

    conn = get_connection()

    orders = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE mobile = ?
        ORDER BY id DESC
        """,
        (mobile,)
    ).fetchall()

    conn.close()

    return orders


def get_customer_total_spending(mobile):

    conn = get_connection()

    result = conn.execute(
        """
        SELECT
            COALESCE(SUM(total), 0)
        FROM orders
        WHERE mobile = ?
        """,
        (mobile,)
    ).fetchone()

    conn.close()

    return float(result[0])


def delete_customer(mobile):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM orders
        WHERE mobile = ?
        """,
        (mobile,)
    )

    conn.commit()

    conn.close()


# =========================================================
# MENU
# =========================================================

def get_menu():

    conn = get_connection()

    menu = conn.execute(
        """
        SELECT *
        FROM menu
        ORDER BY item_name
        """
    ).fetchall()

    conn.close()

    return menu


def get_menu_item(item_name):

    conn = get_connection()

    item = conn.execute(
        """
        SELECT *
        FROM menu
        WHERE item_name = ?
        """,
        (item_name,)
    ).fetchone()

    conn.close()

    return item


def get_price(item_name, size):

    item = get_menu_item(item_name)

    if not item:

        return 0

    size = size.lower()

    if size == "small":

        return float(
            item["small_price"]
        )

    if size == "medium":

        return float(
            item["medium_price"]
        )

    if size == "large":

        return float(
            item["large_price"]
        )

    return 0


def add_menu_item(
    item_name,
    small_price,
    medium_price,
    large_price
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO menu (
            item_name,
            small_price,
            medium_price,
            large_price
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            item_name,
            small_price,
            medium_price,
            large_price
        )
    )

    conn.commit()

    conn.close()


def update_menu_item(
    item_id,
    item_name,
    small_price,
    medium_price,
    large_price
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE menu
        SET
            item_name = ?,
            small_price = ?,
            medium_price = ?,
            large_price = ?
        WHERE id = ?
        """,
        (
            item_name,
            small_price,
            medium_price,
            large_price,
            item_id
        )
    )

    conn.commit()

    conn.close()


def delete_menu_item(item_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM menu
        WHERE id = ?
        """,
        (item_id,)
    )

    conn.commit()

    conn.close()


# =========================================================
# BOOKINGS
# =========================================================

def create_booking(
    customer_name,
    mobile,
    booking_date,
    booking_time,
    guests,
    table_number="",
    status="Pending"
):

    created_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO bookings (
            customer_name,
            mobile,
            booking_date,
            booking_time,
            guests,
            table_number,
            status,
            booking_date_created
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_name,
            mobile,
            booking_date,
            booking_time,
            guests,
            table_number,
            status,
            created_date
        )
    )

    booking_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return booking_id


def get_bookings():

    conn = get_connection()

    bookings = conn.execute(
        """
        SELECT *
        FROM bookings
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return bookings


def update_booking_status(
    booking_id,
    status
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE bookings
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            booking_id
        )
    )

    conn.commit()

    conn.close()


# =========================================================
# DASHBOARD
# =========================================================

def get_dashboard_stats():

    conn = get_connection()

    total_orders = conn.execute(
        """
        SELECT COUNT(*)
        FROM orders
        """
    ).fetchone()[0]

    total_sales = conn.execute(
        """
        SELECT COALESCE(SUM(total), 0)
        FROM orders
        """
    ).fetchone()[0]

    customers = conn.execute(
        """
        SELECT COUNT(DISTINCT mobile)
        FROM orders
        """
    ).fetchone()[0]

    total_gst = conn.execute(
        """
        SELECT COALESCE(SUM(gst), 0)
        FROM orders
        """
    ).fetchone()[0]

    total_bookings = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        """
    ).fetchone()[0]

    pending_bookings = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        WHERE status = 'Pending'
        """
    ).fetchone()[0]

    conn.close()

    return {
        "total_orders": total_orders,
        "total_sales": float(total_sales),
        "customers": customers,
        "total_gst": float(total_gst),
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings
    }


# =========================================================
# REPORTS
# =========================================================

def get_sales_report():

    conn = get_connection()

    report = conn.execute(
        """
        SELECT
            DATE(order_date) AS sale_date,
            COUNT(*) AS total_orders,
            COALESCE(SUM(subtotal), 0) AS subtotal,
            COALESCE(SUM(gst), 0) AS gst,
            COALESCE(SUM(total), 0) AS total_sales
        FROM orders
        GROUP BY DATE(order_date)
        ORDER BY sale_date DESC
        """
    ).fetchall()

    conn.close()

    return report


def get_top_pizzas():

    conn = get_connection()

    pizzas = conn.execute(
        """
        SELECT
            item_name,
            SUM(quantity) AS total_quantity,
            COUNT(*) AS total_orders,
            COALESCE(SUM(total), 0) AS total_sales
        FROM orders
        GROUP BY item_name
        ORDER BY total_quantity DESC
        """
    ).fetchall()

    conn.close()

    return pizzas


def get_report_summary():

    conn = get_connection()

    total_orders = conn.execute(
        """
        SELECT COUNT(*)
        FROM orders
        """
    ).fetchone()[0]

    total_sales = conn.execute(
        """
        SELECT COALESCE(SUM(total), 0)
        FROM orders
        """
    ).fetchone()[0]

    total_gst = conn.execute(
        """
        SELECT COALESCE(SUM(gst), 0)
        FROM orders
        """
    ).fetchone()[0]

    total_subtotal = conn.execute(
        """
        SELECT COALESCE(SUM(subtotal), 0)
        FROM orders
        """
    ).fetchone()[0]

    total_customers = conn.execute(
        """
        SELECT COUNT(DISTINCT mobile)
        FROM orders
        """
    ).fetchone()[0]

    total_bookings = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        """
    ).fetchone()[0]

    conn.close()

    return {
        "total_orders": total_orders,
        "total_sales": float(total_sales),
        "total_gst": float(total_gst),
        "total_subtotal": float(total_subtotal),
        "total_customers": total_customers,
        "total_bookings": total_bookings
    }


# =========================================================
# START DATABASE
# =========================================================

init_db()