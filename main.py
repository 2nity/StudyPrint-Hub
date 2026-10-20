import random
import datetime
from pyscript import document, window, when

# --------------------------------------------------------------------------
# 1. CENTRALIZED SERVICE PRICING & CATEGORY DATA
# --------------------------------------------------------------------------
SERVICES_DATA = {
    "bw_print": {
        "name": "Black-and-White Printing",
        "price": 2.0,
        "unit": "page",
        "category": "printing",
        "keywords": "black white printing bw text page laser assignment report thesis project"
    },
    "color_print": {
        "name": "Colored Printing",
        "price": 5.0,
        "unit": "page",
        "category": "printing",
        "keywords": "colored print color chart graphic photo infographic project presentation poster"
    },
    "photocopy": {
        "name": "Photocopying",
        "price": 2.0,
        "unit": "page",
        "category": "reproduction",
        "keywords": "photocopy duplicate copy xerox notes reviewer textbook id certificate"
    },
    "scanning": {
        "name": "Document Scanning",
        "price": 5.0,
        "unit": "page",
        "category": "digital",
        "keywords": "scanning scan pdf digital image email softcopy file document"
    },
    "binding": {
        "name": "Binding",
        "price": 30.0,
        "unit": "document",
        "category": "finishing",
        "keywords": "binding comb spine cover ring book thesis manual document project"
    },
    "lamination": {
        "name": "Lamination",
        "price": 20.0,
        "unit": "sheet",
        "category": "finishing",
        "keywords": "lamination plastic laminate id certificate waterproof protective badge sheet"
    }
}

current_filter_category = "all"


# --------------------------------------------------------------------------
# 2. UTILITY & FORMATTING FUNCTIONS
# --------------------------------------------------------------------------
def format_pesos(amount):
    """Formats floating point values into Philippine Peso string (e.g. ₱20.00)."""
    return f"₱{amount:,.2f}"


def get_service_info(service_key):
    """Safely retrieves service object from dictionary with fallback."""
    return SERVICES_DATA.get(service_key, SERVICES_DATA["bw_print"])


# --------------------------------------------------------------------------
# 3. SERVICE SEARCH AND CATEGORY FILTERING
# --------------------------------------------------------------------------
def filter_services(category="all"):
    """Filters visible service cards based on category chips."""
    global current_filter_category
    current_filter_category = category
    
    # Update styling on category chip buttons
    chips = document.querySelectorAll(".cat-chip")
    for i in range(chips.length):
        chip = chips.item(i)
        chip_cat = chip.getAttribute("data-category")
        if chip_cat == category:
            chip.classList.add("bg-[#3478C7]", "text-white", "border-[#3478C7]", "active-chip")
            chip.classList.remove("bg-slate-50", "text-slate-700", "border-slate-200")
        else:
            chip.classList.remove("bg-[#3478C7]", "text-white", "border-[#3478C7]", "active-chip")
            chip.classList.add("bg-slate-50", "text-slate-700", "border-slate-200")
            
    apply_service_filters()


@when("input", "#service-search-input")
def on_search_input_change(event):
    """Handles search query changes in real time."""
    search_elem = document.getElementById("service-search-input")
    query = search_elem.value.strip() if search_elem else ""
    clear_btn = document.getElementById("clear-search-btn")
    
    if clear_btn:
        if query:
            clear_btn.classList.remove("hidden")
        else:
            clear_btn.classList.add("hidden")
            
    apply_service_filters()


@when("click", "#clear-search-btn")
def reset_service_search(event=None):
    """Clears search input and resets service list."""
    search_input = document.getElementById("service-search-input")
    if search_input:
        search_input.value = ""
    clear_btn = document.getElementById("clear-search-btn")
    if clear_btn:
        clear_btn.classList.add("hidden")
    filter_services("all")


def apply_service_filters():
    """Applies both category chip and text query filters to service cards."""
    search_elem = document.getElementById("service-search-input")
    query = search_elem.value.strip().lower() if search_elem else ""
    cards = document.querySelectorAll(".service-card")
    visible_count = 0

    for i in range(cards.length):
        card = cards.item(i)
        cat = card.getAttribute("data-category")
        keywords = card.getAttribute("data-keywords").lower() if card.getAttribute("data-keywords") else ""
        
        h3_elem = card.querySelector("h3")
        title = h3_elem.innerText.lower() if h3_elem else ""

        cat_match = (current_filter_category == "all" or cat == current_filter_category)
        search_match = (not query) or (query in keywords) or (query in title)

        if cat_match and search_match:
            card.classList.remove("hidden")
            visible_count += 1
        else:
            card.classList.add("hidden")

    counter = document.getElementById("service-search-count")
    no_res_box = document.getElementById("no-services-found")
    
    if counter:
        counter.innerText = f"Showing {visible_count} of {cards.length} available services"

    if no_res_box:
        if visible_count == 0:
            no_res_box.classList.remove("hidden")
        else:
            no_res_box.classList.add("hidden")


def select_service_action(service_key):
    """Sets service selection across calculator and order form, then navigates to calculator."""
    calc_select = document.getElementById("calc-service")
    ord_select = document.getElementById("ord-service")
    
    if calc_select:
        calc_select.value = service_key
    if ord_select:
        ord_select.value = service_key
    
    calculate_price_action()
    update_order_live_summary()
    
    window.location.hash = "#calculator"


# --------------------------------------------------------------------------
# 4. PRICE CALCULATOR LOGIC
# --------------------------------------------------------------------------
def step_quantity(delta):
    """Increments or decrements quantity input in calculator."""
    qty_input = document.getElementById("calc-quantity")
    if not qty_input:
        return
    try:
        val = int(qty_input.value)
    except ValueError:
        val = 1
    new_val = max(1, min(2000, val + delta))
    qty_input.value = str(new_val)
    calculate_price_action()


@when("change", "#calc-service")
def on_calc_service_change(event):
    calculate_price_action()


@when("change", "#calc-paper-size")
def on_calc_paper_change(event):
    calculate_price_action()


@when("change", "#calc-print-side")
def on_calc_side_change(event):
    calculate_price_action()


@when("change", "#calc-rush")
def on_calc_rush_change(event):
    calculate_price_action()


@when("input", "#calc-quantity")
def on_calc_qty_input(event):
    calculate_price_action()


def calculate_price_action(event=None):
    """Executes live price calculations and updates calculator output panel."""
    error_box = document.getElementById("calc-error-box")
    if error_box:
        error_box.classList.add("hidden")
    
    service_elem = document.getElementById("calc-service")
    qty_elem = document.getElementById("calc-quantity")
    paper_elem = document.getElementById("calc-paper-size")
    side_elem = document.getElementById("calc-print-side")
    rush_elem = document.getElementById("calc-rush")

    if not service_elem or not qty_elem:
        return

    service_key = service_elem.value
    qty_str = qty_elem.value.strip()
    paper_size = paper_elem.value if paper_elem else "short"
    print_side = side_elem.value if side_elem else "single"
    is_rush = rush_elem.checked if rush_elem else False

    # Validation
    if not qty_str:
        show_calc_error("Quantity cannot be empty. Please enter a positive number.")
        return
    
    try:
        qty = int(qty_str)
    except ValueError:
        show_calc_error("Invalid quantity format. Please enter a valid whole number.")
        return

    if qty <= 0:
        show_calc_error("Quantity must be greater than 0.")
        return
    
    if qty > 2000:
        show_calc_error("For bulk print jobs exceeding 2,000 pages, please send a custom inquiry.")
        return

    # Pricing calculations
    info = get_service_info(service_key)
    unit_price = info["price"]
    subtotal = unit_price * qty
    
    paper_extra = 0.0
    if paper_size == "long" and info["category"] in ["printing", "reproduction"]:
        paper_extra = 1.0 * qty
    
    discount = 0.0
    if print_side == "double" and info["category"] in ["printing", "reproduction"]:
        discount = subtotal * 0.10
        
    rush_fee = 15.0 if is_rush else 0.0
    total = subtotal + paper_extra - discount + rush_fee

    # DOM Updates
    name_elem = document.getElementById("res-service-name")
    badge_elem = document.getElementById("res-service-badge")
    qty_res = document.getElementById("res-quantity-val")
    unit_res = document.getElementById("res-unit-price-val")
    subtotal_res = document.getElementById("res-subtotal-val")
    paper_res = document.getElementById("res-paper-val")
    discount_res = document.getElementById("res-discount-val")
    rush_res = document.getElementById("res-rush-val")
    total_res = document.getElementById("res-total-price")

    if name_elem: name_elem.innerText = info["name"]
    if badge_elem: badge_elem.innerText = f"{format_pesos(unit_price)} / {info['unit']}"
    if qty_res: qty_res.innerText = f"{qty} {info['unit']}{'s' if qty > 1 else ''}"
    if unit_res: unit_res.innerText = format_pesos(unit_price)
    if subtotal_res: subtotal_res.innerText = format_pesos(subtotal)
    if paper_res: paper_res.innerText = format_pesos(paper_extra)
    if discount_res: discount_res.innerText = f"-{format_pesos(discount)}"
    if rush_res: rush_res.innerText = f"+{format_pesos(rush_fee)}"
    if total_res: total_res.innerText = format_pesos(total)


def show_calc_error(message):
    """Displays error message box inside price calculator."""
    error_box = document.getElementById("calc-error-box")
    error_msg = document.getElementById("calc-error-msg")
    if error_msg:
        error_msg.innerText = message
    if error_box:
        error_box.classList.remove("hidden")


def reset_calculator_action(event=None):
    """Resets all calculator inputs to defaults."""
    service_elem = document.getElementById("calc-service")
    qty_elem = document.getElementById("calc-quantity")
    paper_elem = document.getElementById("calc-paper-size")
    side_elem = document.getElementById("calc-print-side")
    rush_elem = document.getElementById("calc-rush")
    error_box = document.getElementById("calc-error-box")

    if service_elem: service_elem.value = "bw_print"
    if qty_elem: qty_elem.value = "10"
    if paper_elem: paper_elem.value = "short"
    if side_elem: side_elem.value = "single"
    if rush_elem: rush_elem.checked = False
    if error_box: error_box.classList.add("hidden")
    
    calculate_price_action()


def transfer_calc_to_order(event=None):
    """Transfers calculated values into Order Request form."""
    calc_service = document.getElementById("calc-service")
    calc_qty = document.getElementById("calc-quantity")
    calc_paper = document.getElementById("calc-paper-size")
    
    ord_service = document.getElementById("ord-service")
    ord_qty = document.getElementById("ord-quantity")
    ord_paper = document.getElementById("ord-paper-size")
    
    if calc_service and ord_service:
        ord_service.value = calc_service.value
    if calc_qty and ord_qty:
        ord_qty.value = calc_qty.value
    if calc_paper and ord_paper:
        ord_paper.value = calc_paper.value
        
    update_order_live_summary()
    window.location.hash = "#order"


# --------------------------------------------------------------------------
# 5. ORDER REQUEST FORM & DIGITAL RECEIPT MODAL LOGIC
# --------------------------------------------------------------------------
@when("change", "#ord-service")
def on_ord_service_change(event):
    update_order_live_summary()


@when("input", "#ord-quantity")
def on_ord_qty_change(event):
    update_order_live_summary()


@when("change", "#ord-paper-size")
def on_ord_paper_change(event):
    update_order_live_summary()


def update_order_live_summary():
    """Updates live calculated order summary panel next to the form."""
    service_elem = document.getElementById("ord-service")
    qty_elem = document.getElementById("ord-quantity")
    paper_elem = document.getElementById("ord-paper-size")

    if not service_elem or not qty_elem:
        return

    service_key = service_elem.value
    qty_str = qty_elem.value.strip()
    paper_size = paper_elem.value if paper_elem else "short"

    info = get_service_info(service_key)
    unit_price = info["price"]

    try:
        qty = int(qty_str)
        if qty <= 0: qty = 1
    except ValueError:
        qty = 1

    subtotal = unit_price * qty
    paper_extra = 1.0 * qty if (paper_size == "long" and info["category"] in ["printing", "reproduction"]) else 0.0
    total = subtotal + paper_extra

    name_out = document.getElementById("side-ord-service-name")
    unit_out = document.getElementById("side-ord-unit-price")
    qty_out = document.getElementById("side-ord-qty")
    total_out = document.getElementById("side-ord-total")

    if name_out: name_out.innerText = info["name"]
    if unit_out: unit_out.innerText = format_pesos(unit_price)
    if qty_out: qty_out.innerText = f"{qty} {info['unit']}{'s' if qty > 1 else ''}"
    if total_out: total_out.innerText = format_pesos(total)


def submit_order_request_action(event=None):
    """Validates form submission and renders digital demonstration receipt modal."""
    error_box = document.getElementById("ord-error-box")
    error_msg = document.getElementById("ord-error-msg")
    if error_box:
        error_box.classList.add("hidden")

    name_elem = document.getElementById("ord-name")
    contact_elem = document.getElementById("ord-contact")
    email_elem = document.getElementById("ord-email")
    cust_type_elem = document.getElementById("ord-customer-type")
    service_elem = document.getElementById("ord-service")
    qty_elem = document.getElementById("ord-quantity")
    paper_elem = document.getElementById("ord-paper-size")
    pickup_elem = document.getElementById("ord-pickup-time")

    name = name_elem.value.strip() if name_elem else ""
    contact = contact_elem.value.strip() if contact_elem else ""
    email = email_elem.value.strip() if email_elem else ""
    cust_type = cust_type_elem.value if cust_type_elem else "College Student"
    service_key = service_elem.value if service_elem else "bw_print"
    qty_str = qty_elem.value.strip() if qty_elem else "1"
    paper_size = paper_elem.value if paper_elem else "short"
    pickup = pickup_elem.value if pickup_elem else "ASAP"

    # Input Validation
    if not name or not contact or not email or not qty_str:
        if error_msg: error_msg.innerText = "Please fill in all required fields marked with *."
        if error_box: error_box.classList.remove("hidden")
        return

    try:
        qty = int(qty_str)
        if qty <= 0 or qty > 2000:
            if error_msg: error_msg.innerText = "Quantity must be a positive integer between 1 and 2,000."
            if error_box: error_box.classList.remove("hidden")
            return
    except ValueError:
        if error_msg: error_msg.innerText = "Invalid quantity number entered."
        if error_box: error_box.classList.remove("hidden")
        return

    # Receipt Calculations
    info = get_service_info(service_key)
    unit_price = info["price"]
    subtotal = unit_price * qty
    paper_extra = 1.0 * qty if (paper_size == "long" and info["category"] in ["printing", "reproduction"]) else 0.0
    total = subtotal + paper_extra

    ref_num = f"SPH-2026-{random.randint(1000, 9999)}"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update Modal
    rec_ref = document.getElementById("rec-ref-code")
    rec_time = document.getElementById("rec-timestamp")
    rec_name = document.getElementById("rec-cust-name")
    rec_type = document.getElementById("rec-cust-type")
    rec_contact = document.getElementById("rec-cust-contact")
    rec_pickup = document.getElementById("rec-cust-pickup")
    rec_service = document.getElementById("rec-service-name")
    rec_unit = document.getElementById("rec-service-unit")
    rec_qty = document.getElementById("rec-quantity")
    rec_paper = document.getElementById("rec-paper-size")
    rec_total = document.getElementById("rec-total-price")

    if rec_ref: rec_ref.innerText = ref_num
    if rec_time: rec_time.innerText = now_str
    if rec_name: rec_name.innerText = name
    if rec_type: rec_type.innerText = cust_type
    if rec_contact: rec_contact.innerText = contact
    if rec_pickup: rec_pickup.innerText = pickup
    if rec_service: rec_service.innerText = info["name"]
    if rec_unit: rec_unit.innerText = f"{format_pesos(unit_price)} / {info['unit']}"
    if rec_qty: rec_qty.innerText = f"{qty} {info['unit']}{'s' if qty > 1 else ''}"
    if rec_paper: rec_paper.innerText = paper_size.upper()
    if rec_total: rec_total.innerText = format_pesos(total)

    modal = document.getElementById("receipt-modal")
    if modal: modal.classList.remove("hidden")


def close_receipt_modal(event=None):
    """Hides digital receipt modal."""
    modal = document.getElementById("receipt-modal")
    if modal: modal.classList.add("hidden")


def reset_order_form_action(event=None):
    """Clears order form inputs."""
    name_elem = document.getElementById("ord-name")
    contact_elem = document.getElementById("ord-contact")
    email_elem = document.getElementById("ord-email")
    qty_elem = document.getElementById("ord-quantity")
    instr_elem = document.getElementById("ord-instructions")
    error_box = document.getElementById("ord-error-box")
    file_lbl = document.getElementById("file-upload-label")

    if name_elem: name_elem.value = ""
    if contact_elem: contact_elem.value = ""
    if email_elem: email_elem.value = ""
    if qty_elem: qty_elem.value = "15"
    if instr_elem: instr_elem.value = ""
    if error_box: error_box.classList.add("hidden")
    if file_lbl: file_lbl.innerHTML = "Click or drag & drop PDF / Word file here"
    
    update_order_live_summary()


# --------------------------------------------------------------------------
# 6. EXPOSE FUNCTIONS TO JS / GLOBAL SCOPE & INITIALIZE
# --------------------------------------------------------------------------
window.filter_services = filter_services
window.reset_service_search = reset_service_search
window.select_service_action = select_service_action
window.step_quantity = step_quantity
window.calculate_price_action = calculate_price_action
window.reset_calculator_action = reset_calculator_action
window.transfer_calc_to_order = transfer_calc_to_order
window.submit_order_request_action = submit_order_request_action
window.close_receipt_modal = close_receipt_modal
window.reset_order_form_action = reset_order_form_action


def init_pyscript():
    """Initializes calculations, filter states, and updates banner."""
    calculate_price_action()
    update_order_live_summary()
    apply_service_filters()
    
    status_banner = document.getElementById("pyscript-status-banner")
    if status_banner:
        status_banner.innerText = "✓ PyScript Engine Active — main.py Loaded & Ready"
        status_banner.classList.replace("bg-blue-900", "bg-emerald-900")

init_pyscript()
