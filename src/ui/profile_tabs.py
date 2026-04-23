import streamlit as st
import pandas as pd
import json
import plotly.express as px
from collections import Counter
from src.logic.history_manager import get_user_history, get_user_stats
from src.utils.assets import (
    ICON_CUST,
    ICON_EMPTY_BOX,
    ICON_CALENDAR,
    ICON_DISCOUNT,
    ICON_CLOCK,
    ICON_LINK_B64,
    ICON_TROPHY,
    ICON_TARGET,
    ICON_WEB_LINK
)

def render_profile_tabs(active_user, u_info):
    # --- 5. TABS ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Ανάλυση Δραστηριότητας", "Ιστορικό Προσφορών", "Χρήσιμα Links"])

    # --- ΑΝΑΚΤΗΣΗ ΔΕΔΟΜΕΝΩΝ ΑΠΟ EXCEL ---
    history_df = None
    try:
        history_df = get_user_history(active_user, u_info.get('role', ''))
    except Exception as e:
        st.error(f"Σφάλμα κατά την ανάγνωση του ιστορικού: {e}")

# --- TAB 1 : Ανάλυση Δραστηριότητας ---
    with tab1:
        if history_df is not None and not history_df.empty:
            stats = get_user_stats(active_user, u_info.get('role'))
            
            # Calculations
            total_quotes = stats.get('total_offers', 0)
            avg_value = history_df['Product_Price'].mean() if 'Product_Price' in history_df.columns else 0.0
            monthly_target_progress = 0.65

            # Top Product & Pie Data
            all_products = []
            if 'products_json' in history_df.columns:
                for json_str in history_df['products_json']:
                    try:
                        items = json.loads(json_str)
                        for item in items:
                            all_products.append(item.get('ΠΡΟΪΟΝ', item.get('Product', 'Unknown')))
                    except:
                        pass
            
            top_product_name = "N/A"
            top_product_count = 0
            
            if all_products:
                counts = Counter(all_products)
                # Top 1 for card
                most_common = counts.most_common(1)
                if most_common:
                    top_product_name = most_common[0][0]
                    top_product_count = most_common[0][1]
                
                # Top 5 for Pie
                top_5 = counts.most_common(5)
                other_count = sum(counts.values()) - sum(c for _, c in top_5)
                data = top_5
                if other_count > 0:
                    data.append(("Άλλα", other_count))
                pie_data = pd.DataFrame(data, columns=['Product', 'Count'])
            else:
                 pie_data = pd.DataFrame({'Product': ['No Data'], 'Count': [1]})

            # Line Chart Data
            if 'Date_Time' in history_df.columns:
                history_df['Month'] = history_df['Date_Time'].dt.to_period('M').astype(str)
                line_data = history_df.groupby('Month').size().reset_index(name='Quotes')
            else:
                line_data = pd.DataFrame({'Month': [], 'Quotes': []})

            # Charts
            fig_pie = px.pie(pie_data, values='Count', names='Product', title='Συχνότερα Προϊόντα', hole=0.4)
            fig_pie.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#1e293b',
                height=400,
                margin=dict(t=50, b=20, l=20, r=20)
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')

            fig_line = px.line(line_data, x='Month', y='Quotes', title='Εξέλιξη Προσφορών', markers=True)
            fig_line.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#1e293b',
                height=400,
                margin=dict(t=50, b=20, l=20, r=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
            )

            st.markdown(f"""
                <style>
                .stat-card {{
                    background: white;
                    padding: 25px;
                    border-radius: 15px;
                    border: 1px solid #f1f5f9;
                    border-left: 6px solid #3b82f6;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
                    margin-bottom: 20px;
                }}
                .stat-label {{
                    color: #6b7280;
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }}
                .stat-value {{
                    color: #111827;
                    font-size: 1.8rem;
                    font-weight: 800;
                    margin-top: 4px;
                }}
                </style>
            """, unsafe_allow_html=True)

            # --- Tier 1: Top Row (Key Metrics) ---
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class="stat-card" style="border-left-color: #3b82f6;"><div class="stat-label">Συνολο Προσφορων</div><div class="stat-value">{total_quotes}</div></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="stat-card" style="border-left-color: #f97316;"><div class="stat-label">Μεση Αξια</div><div class="stat-value">{avg_value:.2f}€</div></div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="stat-card" style="border-left-color: #10b981;"><div class="stat-label">Μοναδικοι Πελατες</div><div class="stat-value">{stats.get('unique_clients', 0)}</div></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- Tier 2: Middle Row (Insights) ---
            c4, c5 = st.columns([1.1, 0.9])
            with c4:
                st.markdown(f"""<div class="stat-card" style="border-left-color: #8b5cf6;">
                    <div style="display:flex; align-items:center; margin-bottom:10px;">
                        <img src="{ICON_TROPHY}" width="22" style="margin-right:8px; opacity: 0.6;">
                        <div class="stat-label">ΚΟΡΥΦΑΙΟ ΠΡΟΪΟΝ</div>
                    </div>
                    <div class="stat-value" style="font-size: 1.4rem;">{top_product_name}</div>
                    <div style="font-size: 0.8rem; color: #6b7280; margin-top: 4px;">Επιλέχθηκε {top_product_count} φορές</div>
                </div>""", unsafe_allow_html=True)
            with c5:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #ef4444;">
                    <div style="display:flex; align-items:center; margin-bottom:10px;">
                        <img src="{ICON_TARGET}" width="22" style="margin-right:8px; opacity: 0.6;">
                        <div class="stat-label">ΜΗΝΙΑΙΟΣ ΣΤΟΧΟΣ</div>
                    </div>
                    <div class="stat-value">{int(monthly_target_progress*100)}%</div>
                    <div style="width: 100%; background-color: #e5e7eb; border-radius: 9999px; height: 10px; margin-top: 15px;">
                        <div style="background-color: #2563eb; height: 10px; border-radius: 9999px; width: {int(monthly_target_progress*100)}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            # --- Tier 3: Bottom Row (Charts) ---
            c6, c7 = st.columns(2)
            with c6:
                st.plotly_chart(fig_pie, use_container_width=True, theme=None)
            with c7:
                st.plotly_chart(fig_line, use_container_width=True, theme=None)

        else:
            st.markdown(f"""
                <div style="text-align: center; padding: 40px; background-color: #f8fafc; border-radius: 12px; border: 2px dashed #e2e8f0;">
                    <img src="{ICON_EMPTY_BOX}" width="80" style="margin-bottom: 10px; opacity: 1;">
                    <div style="color: #64748b; font-weight: 600;">Δεν υπάρχουν στατιστικά</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Ξεκινήστε να δημιουργείτε προσφορές για να δείτε αναλύσεις.</div>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 3 : Χρήσιμα Links ---
    with tab3:
        st.markdown("""
            <style>
            .link-card {
                background: white;
                padding: 15px 20px;
                border-radius: 12px;
                border: 1px solid #f1f5f9;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .link-card:hover {
                background: #f8fafc;
                border-color: #3b82f6;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
            }
            </style>
        """, unsafe_allow_html=True)

        useful_links = [
            {"title": "Κατάλογος Προϊόντων", "url": "https://www.dropbox.com/scl/fi/dlu6g9q1z8sehm3xzze2o/2026.pdf?rlkey=g7e8n61iz10axvc6g0o5600tb&st=tg1fvnrg&dl=0"},
            {"title": "Εταιρικό Προφίλ", "url": "https://www.dropbox.com/scl/fi/h8gzyljtq61wutbwmhipq/.pdf?rlkey=tgst1qzslevwkzrmw35fz9oo3&st=kvzv8ogw&dl=0"},
            {"title": "Δελτία Δεδομένων Ασφαλείας *(MSDS)", "url": "https://www.dropbox.com/scl/fo/9hz6j9mgvh29d259v383s/AIT4vmSKKoVx21EEef3cDsc?rlkey=3vi5a1m5qh6s8fi0drp2lbi9q&st=cdqv5gnx&dl=0"},
            {"title": "Τεχνικά Φυλλάδια (TDS)", "url": "https://www.dropbox.com/scl/fo/p88z2k06n02snnd6gh9ex/ANPockYn9-73I5cR7FUVjtQ?rlkey=q841hlrgmrkoa8vkb3lfifo6i&st=20fdz5li&dl=0"},
             {"title": "Πιστοποιήσεις", "url": "https://www.dropbox.com/scl/fo/gixzrin68ock4qu3n6iam/h?rlkey=p161k1wg7vlom7ntq909nnizp&st=q1zknjc0&dl=0"},
        ]

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        for link in useful_links:
            st.markdown(f"""
                <a href="{link['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="link-card">
                        <div style="display: flex; align-items: center;">
                            <img src="{ICON_WEB_LINK}" width="20" style="margin-right: 15px; opacity: 0.7;">
                            <span style="font-weight: 600; font-size: 1rem; color: #1e293b;">{link['title']}</span>
                        </div>
                        <div style="color: #3b82f6; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center;">
                            VISIT <span style="margin-left: 5px;">→</span>
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)

# --- TAB 2 : Ιστορικό Προσφορών ---
    with tab2:
        # --- CSS Injection for Expanders ---
        st.markdown(f"""
            <style>
            /* Force White background and black text on all states */
            div[data-testid="stExpander"], [data-testid="stExpanderSummary"], details[open] > summary {{
                background-color: white !important;
                color: black !important;
                border: 1px solid #e2e8f0 !important;
            }}
            
            /* Product Row Separators */
            .product-row {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                color: black;
            }}

            /* Icon for Main Expander Only */
            div[data-testid="stExpander"] > details > summary p::before {{
                content: "";
                display: inline-block;
                width: 20px;
                height: 20px;
                margin-right: 10px;
                vertical-align: middle;
                background-image: url('{ICON_CUST}');
                background-size: contain;
                background-repeat: no-repeat;
            }}
            
            /* Remove icon from nested expanders */
            div[data-testid="stExpander"] div[data-testid="stExpander"] summary p::before {{
                display: none !important;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        if history_df is not None and not history_df.empty:
            display_df = history_df.copy()
            
            # --- Case-Insensitive Match ---
            user_col = 'username' if 'username' in display_df.columns else ('Username' if 'Username' in display_df.columns else None)
            if user_col:
                display_df = display_df[display_df[user_col].astype(str).str.strip().str.lower() == str(active_user).strip().lower()]

            # --- Sorting ---
            # Sort by Date_Time descending (newest first)
            if 'Date_Time' in display_df.columns:
                display_df = display_df.sort_values(by=['Date_Time'], ascending=False)

            for index, row in display_df.iterrows():
                client = row.get('Customer_Name', row.get('customer_name', 'Άγνωστος Πελάτης'))
                
                # Date
                raw_date = row.get('Date_Time', row.get('timestamp'))
                try:
                    date_str = pd.to_datetime(raw_date).strftime('%d/%m/%Y %H:%M')
                except:
                    date_str = str(raw_date)
                
                validity = row.get('Offer_Duration', row.get('duration', '-'))
                discount = float(row.get('Discount', row.get('discount', 0)))
                catalog = row.get('Catalog', row.get('catalog', ''))
                
                # JSON Processing
                products_json = row.get('products_json', '[]')
                try:
                    products = json.loads(products_json) if products_json else []
                    if not isinstance(products, list): products = []
                except:
                    products = []

                # Expander
                label = f"**{client.upper()}**  |  {date_str}"
                with st.expander(label):
                    # Grid for Date, Discount, Duration
                    st.markdown(f"""
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px;">
                            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; align-items: center;">
                                <img src="{ICON_CALENDAR}" width="20" style="margin-right:8px; vertical-align:middle;">
                                <div>
                                    <div style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">ΗΜΕΡΟΜΗΝΙΑ</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #0f172a;">{date_str}</div>
                                </div>
                            </div>
                            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; align-items: center;">
                                <img src="{ICON_DISCOUNT}" width="20" style="margin-right:8px; vertical-align:middle;">
                                <div>
                                    <div style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">ΕΚΠΤΩΣΗ</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #0f172a;">{discount}%</div>
                                </div>
                            </div>
                            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; display: flex; align-items: center;">
                                <img src="{ICON_CLOCK}" width="20" style="margin-right:8px; vertical-align:middle;">
                                <div>
                                    <div style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">ΔΙΑΡΚΕΙΑ</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #0f172a;">{validity}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Add Section Title
                    st.markdown("<p style='font-weight: bold; font-size: 0.75rem; color: #64748b; margin: 15px 0 5px 0;'>ΠΡΟΪΟΝΤΑ</p>", unsafe_allow_html=True)

                    # Product Grouping
                    grouped_products = {}
                    for p in products:
                        p_name = p.get('ΠΡΟΪΟΝ', p.get('Product', 'Unknown'))
                        if p_name not in grouped_products:
                            grouped_products[p_name] = []
                        grouped_products[p_name].append(p)

                    for p_name, variants in grouped_products.items():
                        with st.expander(p_name):
                            rows_html = ""
                            for i, p_variant in enumerate(variants):
                                price = 0.0
                                try:
                                    if 'ΤΙΜΗ_Α' in p_variant and str(catalog).upper() != 'ΛΙΑΝΙΚΗΣ':
                                        price = float(p_variant['ΤΙΜΗ_Α'])
                                    elif 'ΤΙΜΗ_Β' in p_variant and str(catalog).upper() == 'ΛΙΑΝΙΚΗΣ':
                                        price = float(p_variant['ΤΙΜΗ_Β'])
                                    else:
                                        price = float(p_variant.get('Product_Price', p_variant.get('ΤΙΜΗ', 0)))
                                except:
                                    price = 0.0
                                final_price = price * (1 - discount/100)
                                barcode = str(p_variant.get('ΚΩΔΙΚΟΣ', '-')).replace('.0', '')
                                package_size = p_variant.get('ΛΙΤΡΑ', '-')
                                
                                border_style = "border-bottom: 1px solid #f1f5f9;" if i < len(variants) - 1 else ""
                                rows_html += f"<div class='product-row' style='{border_style}'><span>{barcode}</span><span>{package_size}</span><b>{final_price:.2f}€</b></div>"

                            st.markdown(rows_html, unsafe_allow_html=True)
        else:
            # Μήνυμα όταν δεν υπάρχει ιστορικό
            st.markdown(f"""
                <div style="text-align: center; padding: 40px; background-color: #f8fafc; border-radius: 12px; border: 2px dashed #e2e8f0;">
                    <img src="{ICON_EMPTY_BOX}" width="80" style="margin-bottom: 10px; opacity: 1;">
                    <div style="color: #64748b; font-weight: 600;">Δεν υπάρχει ιστορικό προσφορών</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Δημιουργήστε την πρώτη σας προσφορά για να δείτε αναλύσεις.</div>
                </div>
            """, unsafe_allow_html=True)