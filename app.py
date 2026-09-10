from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    send_file,
    session
)

import os
import json
import tempfile

from functools import wraps

from dotenv import load_dotenv
from openai import OpenAI

from database import (
    get_orders,
    get_order,
    get_dashboard_stats,
    create_order,
    delete_order,
    get_bookings,
    create_booking,
    get_menu,
    add_menu_item,
    update_menu_item,
    delete_menu_item,
    get_customers,
    get_customer_orders,
    get_customer_total_spending,
    delete_customer,
    update_booking_status,
    get_price,
    get_sales_report,
    get_top_pizzas,
    get_report_summary,
    get_user
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "pizza-house-secret-key"
)


# ============================================================
# OPENAI
# ============================================================

if OPENAI_API_KEY:

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

else:

    client = None


# ============================================================
# LOGIN REQUIRED
# ============================================================

def login_required(function):

    @wraps(function)
    def decorated_function(
        *args,
        **kwargs
    ):

        if not session.get(
            "logged_in"
        ):

            return redirect(
                url_for("login")
            )

        return function(
            *args,
            **kwargs
        )

    return decorated_function


# ============================================================
# ADMIN REQUIRED
# ============================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(
        *args,
        **kwargs
    ):

        if not session.get(
            "logged_in"
        ):

            return redirect(
                url_for("login")
            )

        if session.get(
            "role"
        ) != "admin":

            return redirect(
                url_for("customer_dashboard")
            )

        return function(
            *args,
            **kwargs
        )

    return decorated_function


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # --------------------------------------------------------
    # ALREADY LOGGED IN
    # --------------------------------------------------------

    if session.get(
        "logged_in"
    ):

        if session.get(
            "role"
        ) == "admin":

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("customer_dashboard")
        )


    # --------------------------------------------------------
    # LOGIN SUBMIT
    # --------------------------------------------------------

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        role = request.form.get(
            "role",
            ""
        ).strip().lower()


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not username:

            return render_template(
                "login.html",
                error="Please enter username."
            )


        if not password:

            return render_template(
                "login.html",
                error="Please enter password."
            )


        if role not in [
            "admin",
            "customer"
        ]:

            return render_template(
                "login.html",
                error="Please select a valid role."
            )


        # ----------------------------------------------------
        # CHECK USER
        # ----------------------------------------------------

        user = get_user(
            username,
            password,
            role
        )


        if not user:

            return render_template(
                "login.html",
                error="Invalid username, password or role."
            )


        # ----------------------------------------------------
        # CREATE SESSION
        # ----------------------------------------------------

        session.clear()

        session["logged_in"] = True

        session["user_id"] = user["id"]

        session["username"] = user["username"]

        session["name"] = user["name"]

        session["role"] = user["role"]

        session["mobile"] = (
            user["mobile"] or ""
        )


        # ----------------------------------------------------
        # ADMIN
        # ----------------------------------------------------

        if user["role"] == "admin":

            return redirect(
                url_for("admin")
            )


        # ----------------------------------------------------
        # CUSTOMER
        # ----------------------------------------------------

        return redirect(
            url_for("customer_dashboard")
        )


    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return redirect(
        url_for("login")
    )


# ============================================================
# CUSTOMER DASHBOARD
# ============================================================

@app.route(
    "/customer-dashboard"
)
@login_required
def customer_dashboard():

    # Only customer can open customer dashboard

    if session.get(
        "role"
    ) != "customer":

        return redirect(
            url_for("admin")
        )


    # --------------------------------------------------------
    # ALWAYS USE LOGGED-IN CUSTOMER MOBILE
    # --------------------------------------------------------

    mobile = (
        session.get(
            "mobile",
            ""
        ) or ""
    ).strip()


    orders = []

    total_spending = 0


    # --------------------------------------------------------
    # LOAD ONLY THIS CUSTOMER'S ORDERS
    # --------------------------------------------------------

    if mobile:

        orders = get_customer_orders(
            mobile
        )

        total_spending = (
            get_customer_total_spending(
                mobile
            )
        )


    return render_template(

        "customer_dashboard.html",

        name=session.get(
            "name",
            "Customer"
        ),

        mobile=mobile,

        orders=orders,

        total_spending=total_spending
    )


# ============================================================
# NORMAL ORDER
# ADMIN ONLY
# ============================================================

@app.route(
    "/order",
    methods=["GET", "POST"]
)
@admin_required
def order():

    if request.method == "POST":

        customer_name = request.form.get(
            "customer_name",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        item_name = request.form.get(
            "item_name",
            ""
        ).strip()

        size = request.form.get(
            "size",
            ""
        ).strip()

        quantity = request.form.get(
            "quantity",
            "1"
        ).strip()

        toppings = request.form.get(
            "toppings",
            ""
        ).strip()

        order_type = request.form.get(
            "order_type",
            ""
        ).strip()


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not customer_name:

            return "Customer name is required."


        if not mobile:

            return "Mobile number is required."


        if not item_name:

            return "Food item is required."


        if not size:

            return "Size is required."


        try:

            quantity = int(
                quantity
            )

        except ValueError:

            quantity = 1


        if quantity <= 0:

            quantity = 1


        # ----------------------------------------------------
        # CLEAN MOBILE
        # ----------------------------------------------------

        mobile = "".join(
            character
            for character in mobile
            if character.isdigit()
        )


        if len(mobile) != 10:

            return (
                "Please enter a valid "
                "10 digit mobile number."
            )


        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price = get_price(
            item_name,
            size
        )


        if price <= 0:

            return "Invalid pizza or size."


        # ----------------------------------------------------
        # BILL
        # ----------------------------------------------------

        subtotal = price * quantity

        gst = subtotal * 0.05

        total = subtotal + gst


        # ----------------------------------------------------
        # CREATE ORDER
        # ----------------------------------------------------

        order_id = create_order(

            customer_name=customer_name,

            mobile=mobile,

            item_name=item_name,

            size=size,

            quantity=quantity,

            price=price,

            toppings=toppings,

            order_type=order_type,

            subtotal=subtotal,

            gst=gst,

            total=total
        )


        # ----------------------------------------------------
        # INVOICE
        # ----------------------------------------------------

        return render_template(

            "order_success.html",

            order_id=order_id,

            customer_name=customer_name,

            mobile=mobile,

            item_name=item_name,

            size=size,

            quantity=quantity,

            price=price,

            toppings=toppings,

            order_type=order_type,

            subtotal=subtotal,

            gst=gst,

            total=total,

            order_date=None
        )


    # --------------------------------------------------------
    # GET ORDERS
    # --------------------------------------------------------

    orders = get_orders()

    menu = get_menu()


    return render_template(

        "orders.html",

        orders=orders,

        menu=menu
    )


# ============================================================
# DELETE ORDER
# ADMIN ONLY
# ============================================================

@app.route(
    "/order/delete/<int:order_id>",
    methods=["POST"]
)
@admin_required
def delete_order_route(
    order_id
):

    delete_order(
        order_id
    )

    return redirect(
        url_for("order")
    )


# ============================================================
# TABLE BOOKING
# ADMIN + CUSTOMER
# ============================================================

@app.route(
    "/booking",
    methods=["GET", "POST"]
)
@login_required
def booking():

    if request.method == "POST":

        customer_name = request.form.get(
            "customer_name",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        booking_date = request.form.get(
            "booking_date",
            ""
        ).strip()

        booking_time = request.form.get(
            "booking_time",
            ""
        ).strip()

        guests = request.form.get(
            "guests",
            "1"
        ).strip()

        table_number = request.form.get(
            "table_number",
            ""
        ).strip()


        # ----------------------------------------------------
        # CUSTOMER ACCOUNT DETAILS
        # ----------------------------------------------------

        if session.get(
            "role"
        ) == "customer":

            customer_name = (
                session.get(
                    "name",
                    customer_name
                ) or customer_name
            )

            mobile = (
                session.get(
                    "mobile",
                    mobile
                ) or mobile
            )


        try:

            guests = int(
                guests
            )

        except ValueError:

            guests = 1


        if guests <= 0:

            guests = 1


        # ----------------------------------------------------
        # CREATE BOOKING
        # ----------------------------------------------------

        booking_id = create_booking(

            customer_name,

            mobile,

            booking_date,

            booking_time,

            guests,

            table_number
        )


        return render_template(

            "booking_success.html",

            booking_id=booking_id,

            customer_name=customer_name,

            mobile=mobile,

            booking_date=booking_date,

            booking_time=booking_time,

            guests=guests,

            table_number=table_number
        )


    return render_template(
        "booking.html"
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin")
@admin_required
def admin():

    stats = get_dashboard_stats()

    orders = get_orders()

    bookings = get_bookings()


    return render_template(

        "admin.html",

        stats=stats,

        orders=orders,

        bookings=bookings
    )


# ============================================================
# MENU
# ADMIN + CUSTOMER
# ============================================================

@app.route("/menu")
@login_required
def menu():

    menu_items = get_menu()


    return render_template(

        "menu.html",

        menu=menu_items,

        role=session.get(
            "role"
        )
    )


# ============================================================
# MANAGE MENU
# ADMIN ONLY
# ============================================================

@app.route(
    "/menu/manage",
    methods=["GET", "POST"]
)
@admin_required
def manage_menu():

    if request.method == "POST":

        action = request.form.get(
            "action"
        )


        # ----------------------------------------------------
        # ADD MENU ITEM
        # ----------------------------------------------------

        if action == "add":

            item_name = request.form.get(
                "item_name",
                ""
            ).strip()


            try:

                small_price = float(
                    request.form.get(
                        "small_price",
                        0
                    )
                )

                medium_price = float(
                    request.form.get(
                        "medium_price",
                        0
                    )
                )

                large_price = float(
                    request.form.get(
                        "large_price",
                        0
                    )
                )

            except ValueError:

                return "Please enter valid prices."


            if not item_name:

                return "Item name is required."


            add_menu_item(

                item_name,

                small_price,

                medium_price,

                large_price
            )


        # ----------------------------------------------------
        # UPDATE MENU ITEM
        # ----------------------------------------------------

        elif action == "update":

            try:

                item_id = int(
                    request.form.get(
                        "item_id"
                    )
                )

                small_price = float(
                    request.form.get(
                        "small_price",
                        0
                    )
                )

                medium_price = float(
                    request.form.get(
                        "medium_price",
                        0
                    )
                )

                large_price = float(
                    request.form.get(
                        "large_price",
                        0
                    )
                )

            except ValueError:

                return "Invalid menu information."


            item_name = request.form.get(
                "item_name",
                ""
            ).strip()


            update_menu_item(

                item_id,

                item_name,

                small_price,

                medium_price,

                large_price
            )


        # ----------------------------------------------------
        # DELETE MENU ITEM
        # ----------------------------------------------------

        elif action == "delete":

            try:

                item_id = int(
                    request.form.get(
                        "item_id"
                    )
                )

            except ValueError:

                return "Invalid menu item."


            delete_menu_item(
                item_id
            )


        return redirect(
            url_for("manage_menu")
        )


    menu_items = get_menu()


    return render_template(

        "manage_menu.html",

        menu=menu_items
    )


# ============================================================
# CUSTOMERS
# ADMIN ONLY
# ============================================================

@app.route("/customers")
@admin_required
def customers():

    customers = get_customers()


    return render_template(

        "customers.html",

        customers=customers
    )


# ============================================================
# CUSTOMER DETAILS
# ADMIN ONLY
# ============================================================

@app.route(
    "/customer/<mobile>"
)
@admin_required
def customer_details(
    mobile
):

    orders = get_customer_orders(
        mobile
    )


    total_spending = (
        get_customer_total_spending(
            mobile
        )
    )


    customer_name = ""


    if orders:

        customer_name = orders[0][
            "customer_name"
        ]


    return render_template(

        "customer_details.html",

        orders=orders,

        total_spending=total_spending,

        customer_name=customer_name,

        mobile=mobile
    )


# ============================================================
# DELETE CUSTOMER
# ADMIN ONLY
# ============================================================

@app.route(
    "/customer/delete/<mobile>",
    methods=["POST"]
)
@admin_required
def delete_customer_route(
    mobile
):

    delete_customer(
        mobile
    )


    return redirect(
        url_for("customers")
    )


# ============================================================
# BOOKING STATUS
# ADMIN ONLY
# ============================================================

@app.route(
    "/booking/status/<int:booking_id>",
    methods=["POST"]
)
@admin_required
def booking_status(
    booking_id
):

    status = request.form.get(
        "status",
        "Pending"
    )


    update_booking_status(

        booking_id,

        status
    )


    return redirect(
        url_for("admin")
    )


# ============================================================
# REPORTS
# ADMIN ONLY
# ============================================================

@app.route("/reports")
@admin_required
def reports():

    summary = get_report_summary()

    sales_report = get_sales_report()

    top_pizzas = get_top_pizzas()


    return render_template(

        "reports.html",

        summary=summary,

        sales_report=sales_report,

        top_pizzas=top_pizzas
    )


# ============================================================
# AI ORDER PARSER
# ============================================================

def ai_parse_order(

    customer_text,

    current_order=None

):

    if not client:

        raise Exception(

            "OPENAI_API_KEY is not configured. "

            "Please add your API key to the .env file."

        )


    current_order = (

        current_order

        if current_order

        else {}

    )


    menu = get_menu()


    menu_names = []


    for item in menu:

        try:

            if isinstance(
                item,
                dict
            ):

                name = item.get(
                    "item_name",
                    ""
                )

            else:

                name = str(
                    item
                )


            if name:

                menu_names.append(
                    name
                )


        except Exception:

            pass


    if not menu_names:

        menu_names = [

            "Margherita",

            "Farmhouse",

            "Veggie Paradise",

            "Paneer Tikka",

            "Cheese Corn",

            "Pepperoni"

        ]


    prompt = f"""

You are Pizza House AI,
a friendly restaurant voice ordering assistant.

The customer is having a natural conversation with you.

Latest customer message:
{customer_text}

Information already collected:
{json.dumps(current_order)}

Available Pizza House menu:
{json.dumps(menu_names)}

Your job is to understand what the customer said
and update the order.

IMPORTANT RULES:

1. Keep information already collected.
2. Extract new information from the latest message.
3. Never invent information.
4. Customer may provide several details in one sentence.
5. Understand natural English.
6. Understand simple Indian English.
7. Understand numbers spoken as words.
8. Understand mobile numbers spoken digit-by-digit.
9. "big" means Large.
10. "parcel" means Take Away.
11. "takeaway" means Take Away.
12. "take away" means Take Away.
13. "eating here" means Dine In.
14. "dine here" means Dine In.
15. If quantity is not mentioned, use 1.
16. If toppings are not mentioned, use None.
17. Do not invent customer name.
18. Do not invent mobile number.
19. Do not invent pizza.
20. Do not invent size.
21. Do not invent order type.

Allowed pizza names:

Margherita
Farmhouse
Veggie Paradise
Paneer Tikka
Cheese Corn
Pepperoni

Allowed sizes:

Small
Medium
Large

Allowed order types:

Dine In
Take Away
Delivery

Required information:

customer_name
mobile
item_name
size
quantity
toppings
order_type

Conversation behavior:

If something important is missing,
ask for ONLY ONE missing detail.

Ask in this order when possible:

1. customer name
2. mobile number
3. pizza
4. size
5. quantity
6. toppings
7. order type

Do not ask again for something already known.

The reply should sound natural and short
because it will be spoken aloud.

When everything is available,
set complete to true.

Return ONLY valid JSON.

Use exactly:

{{
    "customer_name": "",
    "mobile": "",
    "item_name": "",
    "size": "",
    "quantity": 1,
    "toppings": "None",
    "order_type": "",
    "reply": "",
    "complete": false
}}

"""


    response = client.responses.create(

        model="gpt-5.6-luna",

        input=prompt

    )


    result = response.output_text.strip()


    if result.startswith("```"):

        result = result.replace(
            "```json",
            ""
        )

        result = result.replace(
            "```",
            ""
        )

        result = result.strip()


    return json.loads(
        result
    )


# ============================================================
# AI ORDER TEST
# ADMIN ONLY
# ============================================================

@app.route(
    "/ai-order-test",
    methods=["GET", "POST"]
)
@admin_required
def ai_order_test():

    result = None


    if request.method == "POST":

        customer_text = request.form.get(
            "customer_text",
            ""
        ).strip()


        if customer_text:

            try:

                result = ai_parse_order(
                    customer_text
                )


            except Exception as e:

                result = {

                    "error": str(e)

                }


    return render_template(

        "ai_order_test.html",

        result=result
    )


# ============================================================
# VOICE ORDER PAGE
# ADMIN + CUSTOMER
# ============================================================

@app.route("/voice-order")
@login_required
def voice_order():

    menu = get_menu()


    return render_template(

        "voice_order.html",

        menu=menu,

        user_name=session.get(
            "name",
            ""
        ),

        user_mobile=session.get(
            "mobile",
            ""
        ),

        user_role=session.get(
            "role",
            ""
        )
    )


# ============================================================
# VOICE CHAT
# ============================================================

@app.route(
    "/voice/chat",
    methods=["POST"]
)
@login_required
def voice_chat():

    if not client:

        return jsonify({

            "success": False,

            "error":
                "OPENAI_API_KEY is not configured."

        }), 500


    if "audio" not in request.files:

        return jsonify({

            "success": False,

            "error":
                "No audio file received."

        }), 400


    audio = request.files["audio"]


    if not audio.filename:

        return jsonify({

            "success": False,

            "error":
                "Audio file is empty."

        }), 400


    current_order = {}


    try:

        current_order_text = (
            request.form.get(
                "current_order",
                "{}"
            )
        )


        current_order = json.loads(
            current_order_text
        )


    except Exception:

        current_order = {}


    # --------------------------------------------------------
    # CUSTOMER ACCOUNT DETAILS
    # --------------------------------------------------------
    # For logged-in customers, account details are trusted.
    # They are added to the AI order so AI does not ask again.

    if session.get(
        "role"
    ) == "customer":

        account_name = (
            session.get(
                "name",
                ""
            ) or ""
        ).strip()

        account_mobile = (
            session.get(
                "mobile",
                ""
            ) or ""
        ).strip()


        if account_name:

            current_order[
                "customer_name"
            ] = account_name


        if account_mobile:

            current_order[
                "mobile"
            ] = account_mobile


    temp_path = None

    speech_path = None


    try:

        suffix = ".webm"


        original_ext = os.path.splitext(
            audio.filename
        )[1]


        if original_ext:

            suffix = original_ext


        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=suffix

        ) as temp_file:

            audio.save(
                temp_file.name
            )

            temp_path = temp_file.name


        # ----------------------------------------------------
        # SPEECH TO TEXT
        # ----------------------------------------------------

        with open(

            temp_path,

            "rb"

        ) as audio_file:

            transcription = (
                client.audio.transcriptions.create(

                    model="gpt-4o-transcribe",

                    file=audio_file,

                    language="en"

                )
            )


        text = transcription.text.strip()


        if not text:

            return jsonify({

                "success": False,

                "error":
                    "I could not understand your voice. "
                    "Please speak again."

            }), 400


        # ----------------------------------------------------
        # AI ORDER UNDERSTANDING
        # ----------------------------------------------------

        ai_result = ai_parse_order(

            text,

            current_order

        )


        # ----------------------------------------------------
        # IMPORTANT:
        # CUSTOMER ACCOUNT DETAILS ARE AUTHORITATIVE
        # ----------------------------------------------------

        if session.get(
            "role"
        ) == "customer":

            account_name = (
                session.get(
                    "name",
                    ""
                ) or ""
            ).strip()

            account_mobile = (
                session.get(
                    "mobile",
                    ""
                ) or ""
            ).strip()


            if account_name:

                ai_result[
                    "customer_name"
                ] = account_name


            if account_mobile:

                ai_result[
                    "mobile"
                ] = account_mobile


        reply = ai_result.get(
            "reply",
            ""
        )


        if not reply:

            reply = (
                "Please tell me the next detail "
                "for your order."
            )


        # ----------------------------------------------------
        # TEXT TO SPEECH
        # ----------------------------------------------------

        speech_file = tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".mp3"

        )


        speech_path = speech_file.name


        speech_file.close()


        speech_response = (
            client.audio.speech.create(

                model="gpt-4o-mini-tts",

                voice="coral",

                input=reply,

                response_format="mp3"

            )
        )


        speech_response.write_to_file(
            speech_path
        )


        return jsonify({

            "success": True,

            "text": text,

            "reply": reply,

            "order": ai_result,

            "complete": bool(

                ai_result.get(

                    "complete",

                    False

                )

            ),

            "audio_url":

                "/voice/reply/"

                + os.path.basename(

                    speech_path

                )

        })


    except Exception as e:

        print(

            "VOICE CHAT ERROR:",

            str(e)

        )


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


    finally:

        if (

            temp_path

            and os.path.exists(
                temp_path
            )

        ):

            try:

                os.remove(
                    temp_path
                )

            except Exception:

                pass


# ============================================================
# AI SPEAK
# ============================================================

@app.route(
    "/voice/speak",
    methods=["POST"]
)
@login_required
def voice_speak():

    if not client:

        return jsonify({

            "success": False,

            "error":
                "OPENAI_API_KEY is not configured."

        }), 500


    data = request.get_json(
        silent=True
    ) or {}


    text = data.get(
        "text",
        ""
    ).strip()


    if not text:

        return jsonify({

            "success": False,

            "error":
                "No text provided."

        }), 400


    speech_path = None


    try:

        speech_file = tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".mp3"

        )


        speech_path = speech_file.name


        speech_file.close()


        response = client.audio.speech.create(

            model="gpt-4o-mini-tts",

            voice="coral",

            input=text,

            response_format="mp3"

        )


        response.write_to_file(
            speech_path
        )


        return jsonify({

            "success": True,

            "audio_url":

                "/voice/reply/"

                + os.path.basename(
                    speech_path
                )

        })


    except Exception as e:

        print(

            "SPEECH ERROR:",

            str(e)

        )


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# AI REPLY AUDIO
# ============================================================

@app.route(
    "/voice/reply/<filename>"
)
@login_required
def voice_reply(filename):

    temp_dir = tempfile.gettempdir()


    file_path = os.path.join(

        temp_dir,

        filename

    )


    if not os.path.exists(
        file_path
    ):

        return "Audio not found.", 404


    return send_file(

        file_path,

        mimetype="audio/mpeg"

    )


# ============================================================
# VOICE ORDER SUBMIT
# ============================================================

@app.route(
    "/voice-order/submit",
    methods=["POST"]
)
@login_required
def voice_order_submit():

    # --------------------------------------------------------
    # GET ORDER INFORMATION
    # --------------------------------------------------------

    customer_name = request.form.get(
        "customer_name",
        ""
    ).strip()


    mobile = request.form.get(
        "mobile",
        ""
    ).strip()


    item_name = request.form.get(
        "item_name",
        ""
    ).strip()


    size = request.form.get(
        "size",
        ""
    ).strip()


    toppings = request.form.get(
        "toppings",
        "None"
    ).strip()


    order_type = request.form.get(
        "order_type",
        ""
    ).strip()


    try:

        quantity = int(

            request.form.get(

                "quantity",

                "1"

            )

        )


    except ValueError:

        quantity = 1


    if quantity <= 0:

        quantity = 1


    # ========================================================
    # CUSTOMER ACCOUNT
    # ========================================================
    #
    # VERY IMPORTANT:
    #
    # If customer is logged in, the order ALWAYS belongs
    # to that logged-in customer's account.
    #
    # This prevents Customer A from accidentally creating
    # an order under Customer B's name.
    #
    # ========================================================

    if session.get(
        "role"
    ) == "customer":

        customer_name = (
            session.get(
                "name",
                ""
            ) or ""
        ).strip()

        mobile = (
            session.get(
                "mobile",
                ""
            ) or ""
        ).strip()


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not customer_name:

        return "Customer name is required."


    if not mobile:

        return "Mobile number is required."


    if not item_name:

        return "Pizza is required."


    if not size:

        return "Pizza size is required."


    if not order_type:

        return "Order type is required."


    # --------------------------------------------------------
    # CLEAN MOBILE
    # --------------------------------------------------------

    mobile = "".join(

        character

        for character in mobile

        if character.isdigit()

    )


    if len(mobile) != 10:

        return (

            "Please enter a valid "

            "10 digit mobile number."

        )


    # --------------------------------------------------------
    # PRICE
    # --------------------------------------------------------

    price = get_price(

        item_name,

        size

    )


    if price <= 0:

        return "Invalid pizza or size."


    # --------------------------------------------------------
    # BILL
    # --------------------------------------------------------

    subtotal = price * quantity

    gst = subtotal * 0.05

    total = subtotal + gst


    # --------------------------------------------------------
    # SAVE ORDER
    # --------------------------------------------------------

    order_id = create_order(

        customer_name=customer_name,

        mobile=mobile,

        item_name=item_name,

        size=size,

        quantity=quantity,

        price=price,

        toppings=toppings,

        order_type=order_type,

        subtotal=subtotal,

        gst=gst,

        total=total

    )


    # --------------------------------------------------------
    # INVOICE
    # --------------------------------------------------------

    return render_template(

        "order_success.html",

        order_id=order_id,

        customer_name=customer_name,

        mobile=mobile,

        item_name=item_name,

        size=size,

        quantity=quantity,

        price=price,

        toppings=toppings,

        order_type=order_type,

        subtotal=subtotal,

        gst=gst,

        total=total,

        order_date=None
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )