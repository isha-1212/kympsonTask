from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/")
def products():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.name AS product_name,
            r.id,
            r.buyer_name,
            r.delivery_city,
            COUNT(q.id) AS quote_count
        FROM rfqs r
        JOIN products p ON r.product_id = p.id
        LEFT JOIN quotes q ON r.id = q.rfq_id
        GROUP BY r.id, p.name, r.buyer_name, r.delivery_city, r.created_at
        ORDER BY r.created_at DESC
    """)

    rfqs = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM products
        ORDER BY id
    """)

    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "products.html",
        products=products,
        rfqs=rfqs
    )


@app.route("/rfq/new", methods=["GET", "POST"])
def new_rfq():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM products
        ORDER BY id
    """)

    products = cursor.fetchall()

    if request.method == "POST":
        buyer_name = request.form.get("buyer_name", "").strip()
        product_id = request.form.get("product_id", "").strip()
        quantity_value = request.form.get("quantity", "").strip()
        delivery_city = request.form.get("delivery_city", "").strip()
        notes = request.form.get("notes", "").strip()

        errors = []

        # Buyer validation
        if not buyer_name:
            errors.append("Buyer name cannot be empty.")

        # City validation
        if not delivery_city:
            errors.append("Delivery city cannot be empty.")

        # Product validation
        if not product_id:
            errors.append("Please select a product.")
        else:
            try:
                product_id = int(product_id)

                cursor.execute(
                    "SELECT id FROM products WHERE id = %s",
                    (product_id,)
                )

                if not cursor.fetchone():
                    errors.append("Selected product does not exist.")

            except ValueError:
                errors.append("Invalid product selected.")

        # Quantity validation
        try:
            quantity = int(quantity_value)

            if quantity <= 0:
                errors.append("Quantity must be greater than 0.")

        except (ValueError, TypeError):
            errors.append("Quantity must be greater than 0.")

        # If validation fails
        if errors:
            cursor.close()
            db.close()

            return render_template(
                "raise_rfq.html",
                products=products,
                errors=errors,
                form=request.form
            )

        # Insert RFQ
        cursor.execute("""
            INSERT INTO rfqs
            (
                product_id,
                buyer_name,
                quantity,
                delivery_city,
                notes
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            product_id,
            buyer_name,
            quantity,
            delivery_city,
            notes
        ))

        db.commit()

        rfq_id = cursor.lastrowid

        cursor.close()
        db.close()

        # POST -> REDIRECT -> GET
        return redirect(url_for(
            "rfq_detail",
            rfq_id=rfq_id
        ))

    cursor.close()
    db.close()

    return render_template(
        "raise_rfq.html",
        products=products,
        errors=[],
        form={}
    )


@app.route("/rfq/<int:rfq_id>", methods=["GET", "POST"])
def rfq_detail(rfq_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get RFQ details first
    cursor.execute("""
        SELECT
            r.*,
            p.name AS product_name,
            p.category,
            p.unit
        FROM rfqs r
        JOIN products p
            ON r.product_id = p.id
        WHERE r.id = %s
    """, (rfq_id,))

    rfq = cursor.fetchone()

    # RFQ doesn't exist
    if not rfq:
        cursor.close()
        db.close()

        return "RFQ not found", 404

  
    # ADD SUPPLIER QUOTE
  
    if request.method == "POST":

        supplier_name = request.form.get(
            "supplier_name",
            ""
        ).strip()

        unit_price_value = request.form.get(
            "unit_price",
            ""
        ).strip()

        delivery_days_value = request.form.get(
            "delivery_days",
            ""
        ).strip()

        errors = []

        # Supplier validation
        if not supplier_name:
            errors.append(
                "Supplier name cannot be empty."
            )

        # Unit price validation
        try:
            unit_price = Decimal(unit_price_value)

            if unit_price <= 0:
                errors.append(
                    "Unit price must be greater than 0."
                )

        except (InvalidOperation, TypeError):
            errors.append(
                "Unit price must be greater than 0."
            )

        # Delivery days validation
        try:
            delivery_days = int(delivery_days_value)

            if delivery_days <= 0:
                errors.append(
                    "Delivery days must be greater than 0."
                )

        except (ValueError, TypeError):
            errors.append(
                "Delivery days must be greater than 0."
            )

      
        # VALIDATION FAILED
      
        if errors:

            cursor.execute("""
                SELECT *
                FROM quotes
                WHERE rfq_id = %s
                ORDER BY unit_price ASC
            """, (rfq_id,))

            quotes = cursor.fetchall()

            cursor.close()
            db.close()

            return render_template(
                "rfq_detail.html",
                rfq=rfq,
                quotes=quotes,
                errors=errors,
                form=request.form
            )

      
        # INSERT QUOTE
    
        cursor.execute("""
            INSERT INTO quotes
            (
                rfq_id,
                supplier_name,
                unit_price,
                delivery_days
            )
            VALUES (%s, %s, %s, %s)
        """, (
            rfq_id,
            supplier_name,
            unit_price,
            delivery_days
        ))

        db.commit()

        cursor.close()
        db.close()

     
        return redirect(url_for(
            "rfq_detail",
            rfq_id=rfq_id
        ))


    # GET RFQ QUOTES
  
    cursor.execute("""
        SELECT *
        FROM quotes
        WHERE rfq_id = %s
        ORDER BY unit_price ASC
    """, (rfq_id,))

    quotes = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "rfq_detail.html",
        rfq=rfq,
        quotes=quotes,
        errors=[],
        form={}
    )


if __name__ == "__main__":
    app.run(debug=True)
