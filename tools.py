"""
tools.py — Pizza Restaurant Tool Definitions
=============================================
These are the "actions" the agent can take beyond just answering questions.
Think of tools like the restaurant's systems:
  - A menu board  (get_menu)
  - An order terminal (place_order)
  - An order tracker (check_order_status)

For the research: each tool creates a STATE TRANSITION in the agent,
which is exactly what the fuzzer will try to exploit.
"""

import random
import string
from datetime import datetime

# ============================================================
# IN-MEMORY ORDER DATABASE
# Simulates a real restaurant's order management system.
# In a real app this would be a SQL/NoSQL database.
# ============================================================
orders_db = {}


def get_menu() -> str:
    """
    TOOL: get_menu
    Returns the full restaurant menu as a formatted string.
    State effect: Keeps agent in BROWSING mode.
    """
    menu = """
    ╔══════════════════════════════════════════╗
    ║         🍕  PIZZA RESTAURANT MENU        ║
    ╠══════════════════════════════════════════╣
    ║  CLASSIC PIZZAS                          ║
    ║  • Margherita      S:$12  M:$16  L:$20  ║
    ║  • Pepperoni       S:$14  M:$18  L:$22  ║
    ║  • BBQ Chicken     S:$15  M:$19  L:$23  ║
    ╠══════════════════════════════════════════╣
    ║  SPECIALTY PIZZAS                        ║
    ║  • WhiteAlbum      S:$16  M:$21  L:$26  ║
    ║    (ricotta, mozzarella, garlic, spinach)║
    ║  • Mediterranean   S:$16  M:$21  L:$26  ║
    ║    (olives, feta, fresh tomatoes)        ║
    ║  • BuffaloChicken  S:$17  M:$22  L:$27  ║
    ║    (spicy buffalo, chicken, blue cheese) ║
    ║  • DetroitSquare   S:$18  M:$24  L:$30  ║
    ║    (pepperoni cups, crispy cheese edges) ║
    ╠══════════════════════════════════════════╣
    ║  VEGAN OPTIONS                           ║
    ║  • GardenFresh     S:$15  M:$20  L:$25  ║
    ║    (seasonal veggies, cashew cheese)     ║
    ║  • Margherita (vegan cheese +$2)         ║
    ╠══════════════════════════════════════════╣
    ║  SIZES: S = 10"  |  M = 14"  |  L = 18" ║
    ╚══════════════════════════════════════════╝

    To order type:  order <PizzaName> <size> <quantity>
    Example:        order Margherita large 2
    """
    return menu


def place_order(pizza_name: str, size: str, quantity: int) -> dict:
    """
    TOOL: place_order
    Places a new pizza order and stores it in orders_db.

    Parameters:
        pizza_name (str): Name of the pizza
        size (str):       small / medium / large
        quantity (int):   How many pizzas

    Returns:
        dict with success status, order_id, and estimated time.

    State effect: Transitions agent from ORDERING → ORDER_PLACED
    """
    # Generate a unique order ID like "ORD-K7X2QA"
    order_id = "ORD-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )

    # Normalize inputs
    size = size.strip().upper()
    pizza_name = pizza_name.strip().title()

    # Store order in our fake database
    orders_db[order_id] = {
        "order_id":       order_id,
        "pizza":          pizza_name,
        "size":           size,
        "quantity":       quantity,
        "status":         "RECEIVED",           # RECEIVED → PREPARING → READY
        "timestamp":      datetime.now().strftime("%H:%M:%S"),
        "estimated_time": "25-35 minutes",
    }

    return {
        "success":        True,
        "order_id":       order_id,
        "pizza":          pizza_name,
        "size":           size,
        "quantity":       quantity,
        "estimated_time": "25-35 minutes",
    }


def check_order_status(order_id: str) -> dict:
    """
    TOOL: check_order_status
    Looks up an order by its ID and returns current status.

    Parameters:
        order_id (str): The order ID (e.g. "ORD-K7X2QA")

    Returns:
        dict with order details if found, or error message if not.

    State effect: Keeps agent in ORDER_PLACED / BROWSING mode.
    Research note: Fuzzer can try invalid/forged order IDs here.
    """
    order_id = order_id.strip().upper()

    if order_id in orders_db:
        order = orders_db[order_id]
        return {
            "found":     True,
            "order_id":  order_id,
            "pizza":     order["pizza"],
            "size":      order["size"],
            "quantity":  order["quantity"],
            "status":    order["status"],
            "placed_at": order["timestamp"],
        }
    else:
        return {
            "found":   False,
            "message": f"No order found with ID '{order_id}'. Please check the ID and try again.",
        }
