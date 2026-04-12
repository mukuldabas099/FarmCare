# """
# backend/routes/pdf.py
# Route: /generate_pdf  — builds 3-page ReportLab PDF (Soil Health Card)
# """
# import io, json, datetime, traceback, os
# from flask import Blueprint, request, jsonify, send_file

# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import cm
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.enums  import TA_RIGHT
# from reportlab.platypus   import (SimpleDocTemplate, Paragraph, Spacer, Table,
#                                    TableStyle, HRFlowable, PageBreak, Image as RLImage)
# from reportlab.graphics.shapes import Drawing, Rect
# from PIL import Image as PILImage

# from backend.utils.sensor_state import latest, lock
# from backend.utils.scoring      import health_score, classify, THRESH, get_sugs
# from backend.utils.weather      import weather_cache, weather_lock
# from backend.routes.soil        import predict_soil_from_image
# from backend.routes.optimize    import optimize_crop
# from backend.routes.fertilizer  import predict_fertilizer

# pdf_bp = Blueprint("pdf", __name__)

# # ── Palette ────────────────────────────────────────────────────
# CD   = colors.HexColor("#0d1f0d");  CLG  = colors.HexColor("#4ade80")
# CBG1 = colors.HexColor("#f0f9f0");  CBG2 = colors.HexColor("#e2f4e2")
# CBDR = colors.HexColor("#b8d8b8");  CGD  = colors.HexColor("#16a34a")
# CWN  = colors.HexColor("#d97706");  CBD  = colors.HexColor("#dc2626")
# CMT  = colors.HexColor("#6b9a6b");  CTX  = colors.HexColor("#1a2e1a")
# CBL  = colors.HexColor("#1d4ed8");  CSC  = colors.HexColor("#d4efd4")
# PAGE_W, _ = A4; MAR = 2 * cm


# def scolor(st):
#     return CGD if st == "optimal" else CWN if st == "low" else CBD if st == "high" else CMT


# def ps(n, **k):
#     return ParagraphStyle(n, **k)


# def _base_styles():
#     return {
#         "body": ps("b",  fontName="Helvetica",         fontSize=9,  textColor=CTX, spaceAfter=3, leading=14),
#         "bold": ps("bd", fontName="Helvetica-Bold",    fontSize=9,  textColor=CTX),
#         "sm":   ps("s",  fontName="Helvetica",         fontSize=8,  textColor=CMT),
#         "smi":  ps("si", fontName="Helvetica-Oblique", fontSize=7.5, textColor=CMT, leading=11),
#         "sec":  ps("sc", fontName="Helvetica-Bold",    fontSize=11, textColor=CD,
#                    backColor=CSC, spaceAfter=4, spaceBefore=10, leftIndent=6, borderPad=4),
#     }


# def _get_styles(lang):
#     """Try Hindi fonts if available, fall back to base Helvetica."""
#     try:
#         from hindi_pdf_patch import register_hindi_fonts, get_pdf_fonts
#         register_hindi_fonts()
#         return get_pdf_fonts(lang)
#     except Exception:
#         return _base_styles()


# def hdr(sub, ds, S):
#     W = PAGE_W - 2 * MAR
#     body_font = S["body"].fontName if S else "Helvetica-Bold"
#     return Table([[
#         Paragraph('<font color="#4ade80"><b>FarmCare</b></font>',
#                   ps("h1", fontName="Helvetica-Bold", fontSize=20, textColor=CLG)),
#         Paragraph(f'<font color="#a8d8a8"><b>{sub}</b></font><br/>'
#                   f'<font color="#6b9a6b" size="8">{ds}</font>',
#                   ps("h2", fontName=body_font, fontSize=11, textColor=CLG, alignment=TA_RIGHT))
#     ]], colWidths=[W - 5.5 * cm, 5.5 * cm],
#     style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CD),
#                       ("TOPPADDING", (0, 0), (-1, -1), 12),
#                       ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
#                       ("LEFTPADDING", (0, 0), (0, -1), 14),
#                       ("RIGHTPADDING", (-1, 0), (-1, -1), 14)]))


# def pbar(val, w, h=14, color=CGD):
#     d = Drawing(w, h)
#     d.add(Rect(0, 3, w, h - 6, fillColor=colors.HexColor("#c8e6c8"), strokeColor=None))
#     d.add(Rect(0, 3, max(4, w * val / 100), h - 6, fillColor=color, strokeColor=None))
#     return d


# def build_pdf(form, sensor, soil_info, img_bytes, score, sugs, opt_result, fert_r, lang="en"):
#     PDF_LABELS = {
#         "en": {
#             "title1": "SOIL HEALTH CARD", "title2": "ML ANALYSIS & RECOMMENDATIONS",
#             "title3": "WEATHER & IRRIGATION PLAN",
#             "farmer_det": "Farmer & Farm Details",
#             "farmer_name": "Farmer Name", "email": "Email",
#             "address": "Address", "gps": "GPS Location",
#             "khasra": "Khasra No.", "farm_size": "Farm Size",
#             "soil_type": "Detected Soil Type", "crop": "Selected Crop",
#             "health_score": "Overall Soil Health Score",
#             "readings": "Live Sensor Readings",
#             "param": "Parameter", "value": "Value",
#             "unit": "Unit", "opt_range": "Optimal Range", "status": "Status",
#             "action_sum": "Immediate Action Summary",
#             "soil_class": "Soil Classification (AI Model)",
#             "confidence": "Confidence", "notes": "Notes",
#             "rec_crops": "Recommended Crops",
#             "crop_opt": "Crop Optimization",
#             "param_match": "Parameter Match",
#             "your_val": "Your Value", "ideal_range": "Ideal Range",
#             "fert_rec": "Fertilizer Recommendation",
#             "soil_mapped": "Soil", "crop_mapped": "Crop",
#             "npk": "NPK Ratio", "rate": "Rate", "when": "When to Apply",
#             "curr_weather": "Current Weather Conditions",
#             "location": "Location", "condition": "Condition",
#             "temperature": "Temperature", "humidity": "Humidity",
#             "wind_speed": "Wind Speed", "rain_9h": "Rain (9h)",
#             "heat_wave": "Heat Wave", "rain_alert": "Rain Alert",
#             "irr_advice": "Irrigation Advice",
#             "forecast": "10-Day Weather Forecast",
#             "irr_guide": "Irrigation Decision Guide",
#             "soil_imp": "Soil Improvement Suggestions",
#             "best_prac": "General Best Practices for Soil Health",
#             "date": "Date", "min_c": "Min °C", "max_c": "Max °C",
#             "rain_mm": "Rain (mm)", "irrigation": "Irrigation",
#             "excellent": "Excellent", "good": "Good", "moderate": "Moderate", "poor": "Poor",
#             "skip": "Skip", "reduce": "Reduce", "normal": "Normal",
#             "yes_caution": "Yes — extreme caution", "no": "No",
#             "yes_hold": "Yes — hold irrigation",
#         },
#         "hi": {
#             "title1": "मृदा स्वास्थ्य कार्ड", "title2": "ML विश्लेषण और अनुशंसाएं",
#             "title3": "मौसम और सिंचाई योजना",
#             "farmer_det": "किसान और खेत का विवरण",
#             "farmer_name": "किसान का नाम", "email": "ईमेल",
#             "address": "पता", "gps": "GPS स्थान",
#             "khasra": "खसरा नंबर", "farm_size": "खेत का आकार",
#             "soil_type": "पहचाना गया मृदा प्रकार", "crop": "चयनित फसल",
#             "health_score": "समग्र मृदा स्वास्थ्य स्कोर",
#             "readings": "लाइव सेंसर रीडिंग",
#             "param": "पैरामीटर", "value": "मान",
#             "unit": "इकाई", "opt_range": "अनुकूल सीमा", "status": "स्थिति",
#             "action_sum": "तत्काल कार्य सारांश",
#             "soil_class": "मृदा वर्गीकरण (AI मॉडल)",
#             "confidence": "विश्वास", "notes": "नोट्स",
#             "rec_crops": "अनुशंसित फसलें",
#             "crop_opt": "फसल अनुकूलन",
#             "param_match": "पैरामीटर मिलान",
#             "your_val": "आपका मान", "ideal_range": "आदर्श सीमा",
#             "fert_rec": "उर्वरक अनुशंसा",
#             "soil_mapped": "मिट्टी", "crop_mapped": "फसल",
#             "npk": "NPK अनुपात", "rate": "दर", "when": "कब डालें",
#             "curr_weather": "वर्तमान मौसम की स्थिति",
#             "location": "स्थान", "condition": "स्थिति",
#             "temperature": "तापमान", "humidity": "आर्द्रता",
#             "wind_speed": "हवा की गति", "rain_9h": "बारिश (9 घंटे)",
#             "heat_wave": "लू", "rain_alert": "बारिश चेतावनी",
#             "irr_advice": "सिंचाई सलाह",
#             "forecast": "10 दिन का मौसम पूर्वानुमान",
#             "irr_guide": "सिंचाई निर्णय गाइड",
#             "soil_imp": "मृदा सुधार सुझाव",
#             "best_prac": "मृदा स्वास्थ्य के लिए सामान्य सर्वोत्तम प्रथाएं",
#             "date": "तारीख", "min_c": "न्यूनतम °C", "max_c": "अधिकतम °C",
#             "rain_mm": "बारिश (मिमी)", "irrigation": "सिंचाई",
#             "excellent": "उत्कृष्ट", "good": "अच्छा", "moderate": "मध्यम", "poor": "खराब",
#             "skip": "छोड़ें", "reduce": "कम करें", "normal": "सामान्य",
#             "yes_caution": "हाँ — अत्यधिक सावधानी", "no": "नहीं",
#             "yes_hold": "हाँ — सिंचाई रोकें",
#         }
#     }
#     LB = PDF_LABELS.get(lang, PDF_LABELS["en"])
#     S  = _get_styles(lang)
#     W  = PAGE_W - 2 * MAR
#     buf  = io.BytesIO()
#     doc  = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MAR, rightMargin=MAR,
#                               topMargin=1.5 * cm, bottomMargin=1.5 * cm)
#     ds    = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
#     story = []

#     # ── PAGE 1: Farmer details + sensor readings ───────────────
#     story += [hdr(LB["title1"], ds, S), Spacer(1, 10)]

#     story.append(Paragraph(f"  {LB['farmer_det']}", S["sec"]))
#     labels = [[LB["farmer_name"], LB["email"], LB["address"], LB["gps"]],
#               [LB["khasra"], LB["farm_size"], LB["soil_type"], LB["crop"]]]
#     vals   = [[form.get("farmer_name", "N/A"), form.get("email", "N/A"),
#                form.get("address", "N/A"),     form.get("location", "N/A")],
#               [form.get("khasra_number", "N/A"), f"{form.get('farm_size','N/A')} sqft",
#                (soil_info or {}).get("soil_type", "—"), form.get("crop_type", "—")]]
#     rows = []
#     for i in range(2):
#         rows.append([Paragraph(labels[i][j], S["sm"]) for j in range(4)])
#         rows.append([Paragraph(f"<b>{vals[i][j]}</b>", S["body"]) for j in range(4)])
#     ft = Table(rows, colWidths=[W * 0.25] * 4)
#     ft.setStyle(TableStyle([("ROWBACKGROUNDS", (0, 0), (-1, -1), [CBG1, CBG2]),
#                              ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#                              ("TOPPADDING", (0, 0), (-1, -1), 4),
#                              ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
#                              ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
#     story += [ft, Spacer(1, 10)]

#     story.append(Paragraph(f"  {LB['health_score']}", S["sec"]))
#     sc    = CGD if score >= 70 else CWN if score >= 40 else CBD
#     vdict = LB["excellent"] if score >= 75 else LB["good"] if score >= 60 else LB["moderate"] if score >= 40 else LB["poor"]
#     story.append(Table([[pbar(score, int(W * 0.55), 16, sc),
#                          Paragraph(f'<font color="{sc.hexval()}"><b>{score}% — {vdict}</b></font>', S["body"])]],
#                         colWidths=[W * 0.57, W * 0.43]))
#     story.append(Spacer(1, 8))

#     story.append(Paragraph(f"  {LB['readings']}", S["sec"]))
#     hr = [Paragraph(f"<b>{h}</b>", S["sm"]) for h in
#           [LB["param"], LB["value"], LB["unit"], LB["opt_range"], LB["status"]]]
#     rs = [hr]
#     for dname, key in [("Temperature", "temperature"), ("Moisture", "moisture"), ("EC", "ec"),
#                         ("pH", "ph"), ("Nitrogen", "nitrogen"), ("Phosphorus", "phosphorus"),
#                         ("Potassium", "potassium")]:
#         val = sensor.get(key); st = classify(key, val); t = THRESH[key]
#         vs  = f"{val:.2f}" if isinstance(val, float) and val not in (None, -1) else \
#               str(val) if val not in (None, -1) else "ERR"
#         rs.append([Paragraph(dname, S["body"]), Paragraph(f"<b>{vs}</b>", S["body"]),
#                    Paragraph(t["unit"], S["sm"]), Paragraph(t["opt"], S["sm"]),
#                    Paragraph(f'<font color="{scolor(st).hexval()}"><b>{st.upper()}</b></font>', S["body"])])
#     st2 = Table(rs, colWidths=[W * 0.25, W * 0.15, W * 0.14, W * 0.25, W * 0.21])
#     st2.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), CD),
#                               ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
#                               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]),
#                               ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#                               ("FONTSIZE", (0, 0), (-1, -1), 8.5),
#                               ("TOPPADDING", (0, 0), (-1, -1), 5),
#                               ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
#                               ("LEFTPADDING", (0, 0), (-1, -1), 8),
#                               ("ALIGN", (1, 0), (-1, -1), "CENTER")]))
#     story += [st2, Spacer(1, 10)]

#     story.append(Paragraph(f"  {LB['action_sum']}", S["sec"]))
#     for sug in sugs[:4]:
#         icon = "🔴" if any(w in sug.lower() for w in ["critical","immediately","now"]) else \
#                "🟡" if any(w in sug.lower() for w in ["defic","low"]) else "🟢"
#         story.append(Table([[Paragraph(f"{icon}  {sug}", S["body"])]], colWidths=[W],
#             style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CBG1 if "🟢" in icon else CBG2),
#                                ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#                                ("TOPPADDING", (0, 0), (-1, -1), 5),
#                                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
#                                ("LEFTPADDING", (0, 0), (-1, -1), 10)])))
#         story.append(Spacer(1, 3))
#     story.append(Spacer(1, 8))

#     # ── PAGE 2: Soil + crop optimization + fertilizer ──────────
#     story += [PageBreak(), hdr(LB["title2"], ds, S), Spacer(1, 10)]

#     if soil_info:
#         story.append(Paragraph(f"  {LB['soil_class']}", S["sec"]))
#         left_content = [
#             Paragraph(f'<font color="{CBL.hexval()}" size="13"><b>🌍 {soil_info.get("soil_type","—")}</b></font>', S["body"]),
#             Spacer(1, 4),
#             Paragraph(f'<b>{LB["confidence"]}:</b> {soil_info.get("confidence","—")}%', S["body"]),
#             Spacer(1, 4),
#             Paragraph(f'<b>{LB["notes"]}:</b> {soil_info.get("notes","—")}', S["body"]),
#         ]
#         for c in soil_info.get("crops", []):
#             season_label = c.get("season_hi", c["season"]) if lang == "hi" else c["season"]
#             note = f' ← {c["note"]}' if c.get("note") else ""
#             left_content.append(Paragraph(f'• {c["crop"]}  ({season_label} / {c["months"]}){note}', S["body"]))
#         right = ""
#         if img_bytes:
#             try:
#                 pi = PILImage.open(io.BytesIO(img_bytes)).convert("RGB")
#                 pi.thumbnail((160, 120))
#                 tb = io.BytesIO(); pi.save(tb, "JPEG", quality=85); tb.seek(0)
#                 right = RLImage(tb, width=4 * cm, height=3 * cm)
#             except: pass
#         it = Table([[left_content, right]], colWidths=[W * 0.72, W * 0.28])
#         it.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
#                                  ("BACKGROUND", (0, 0), (-1, -1), CBG1),
#                                  ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#                                  ("LEFTPADDING", (0, 0), (-1, -1), 10),
#                                  ("TOPPADDING", (0, 0), (-1, -1), 8),
#                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
#         story += [it, Spacer(1, 10)]

#     if opt_result and "error" not in opt_result:
#         story.append(Paragraph(f"  {LB['crop_opt']} — {opt_result['crop']}", S["sec"]))
#         match_pct = opt_result.get("overall_match_pct", 0)
#         mc = CGD if match_pct >= 80 else CWN if match_pct >= 50 else CBD
#         story.append(Table([[pbar(match_pct, int(W * 0.45), 14, mc),
#                              Paragraph(f'<font color="{mc.hexval()}"><b>{LB["param_match"]}: {match_pct}%</b></font>', S["body"])]],
#                             colWidths=[W * 0.47, W * 0.53]))
#         story.append(Spacer(1, 6))
#         cmp_hdr = [Paragraph(f"<b>{h}</b>", S["sm"]) for h in
#                    [LB["param"], LB["your_val"], LB["ideal_range"], LB["unit"], LB["status"]]]
#         cmp_rows = [cmp_hdr]
#         for c in opt_result.get("comparison", []):
#             st = c["status"]
#             cmp_rows.append([
#                 Paragraph(c["param"].title(), S["body"]),
#                 Paragraph(f'<b>{c["value"]}</b>', S["body"]),
#                 Paragraph(c["ideal"], S["sm"]),
#                 Paragraph(c["unit"], S["sm"]),
#                 Paragraph(f'<font color="{scolor(st).hexval()}"><b>{st.upper()}</b></font>', S["body"]),
#             ])
#         cmp_t = Table(cmp_rows, colWidths=[W * 0.25, W * 0.18, W * 0.22, W * 0.15, W * 0.20])
#         cmp_t.setStyle(TableStyle([
#             ("BACKGROUND", (0, 0), (-1, 0), CD), ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
#             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]), ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#             ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("TOPPADDING", (0, 0), (-1, -1), 4),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 8),
#         ]))
#         story.append(cmp_t)
#         story.append(Spacer(1, 6))
#         for sug in opt_result.get("suggestions", []):
#             story.append(Paragraph(sug, S["body"]))
#         story.append(Spacer(1, 8))

#     story.append(Paragraph(f"  {LB['fert_rec']}", S["sec"]))
#     if fert_r and "error" not in fert_r:
#         rec = fert_r["recommended"]
#         story.append(Paragraph(
#             f'<font color="{CMT.hexval()}" size="8">{LB["soil_mapped"]} → <b>{fert_r["soil_type"]}</b>  |  '
#             f'{LB["crop_mapped"]} → <b>{fert_r["crop_type_mapped"]}</b></font>', S["sm"]))
#         story.append(Spacer(1, 4))
#         ft2 = Table([
#             [Paragraph(f'<font color="{CBL.hexval()}" size="14"><b>🧪 {rec["name"]}</b></font>', S["body"]),
#              Paragraph(f'<b>{LB["npk"]}:</b> <font color="{CBL.hexval()}"><b>{rec["npk"]}</b></font>', S["body"])],
#             [Paragraph(f'<b>{LB["confidence"]}:</b> {rec["confidence"]}%  |  <b>{LB["rate"]}:</b> {rec["rate"]}', S["body"]), ""],
#             [Paragraph(rec["description"], S["body"]), ""],
#             [Paragraph(f'<b>{LB["when"]}:</b> {rec["timing"]}', S["body"]), ""],
#         ], colWidths=[W * 0.55, W * 0.45],
#         style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8eef8")),
#                           ("SPAN", (0, 1), (1, 1)), ("SPAN", (0, 2), (1, 2)), ("SPAN", (0, 3), (1, 3)),
#                           ("GRID", (0, 0), (-1, -1), 0.5, CBDR), ("LEFTPADDING", (0, 0), (-1, -1), 12),
#                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
#         story += [ft2, Spacer(1, 8)]

#     # ── PAGE 3: Weather + forecast + irrigation guide ──────────
#     story += [PageBreak(), hdr(LB["title3"], ds, S), Spacer(1, 10)]

#     with weather_lock:
#         w = dict(weather_cache)

#     if w.get("temperature"):
#         story.append(Paragraph(f"  {LB['curr_weather']}", S["sec"]))
#         w_data = [
#             [Paragraph(f"<b>{LB['location']}</b>", S["sm"]),
#              Paragraph(w.get("city", "—"), S["body"]),
#              Paragraph(f"<b>{LB['condition']}</b>", S["sm"]),
#              Paragraph(w.get("description", "—"), S["body"])],
#             [Paragraph(f"<b>{LB['temperature']}</b>", S["sm"]),
#              Paragraph(f'{w["temperature"]}°C (feels {w.get("feels_like","—")}°C)', S["body"]),
#              Paragraph(f"<b>{LB['humidity']}</b>", S["sm"]),
#              Paragraph(f'{w.get("humidity","—")}%', S["body"])],
#             [Paragraph(f"<b>{LB['wind_speed']}</b>", S["sm"]),
#              Paragraph(f'{w.get("wind_speed","—")} km/h', S["body"]),
#              Paragraph(f"<b>{LB['rain_9h']}</b>", S["sm"]),
#              Paragraph(f'{w.get("rain_mm",0)} mm', S["body"])],
#             [Paragraph(f"<b>{LB['heat_wave']}</b>", S["sm"]),
#              Paragraph(LB["yes_caution"] if w.get("heat_wave") else LB["no"], S["body"]),
#              Paragraph(f"<b>{LB['rain_alert']}</b>", S["sm"]),
#              Paragraph(LB["yes_hold"] if w.get("rain_expected") else LB["no"], S["body"])],
#         ]
#         wt = Table(w_data, colWidths=[W * 0.20, W * 0.30, W * 0.20, W * 0.30])
#         wt.setStyle(TableStyle([("ROWBACKGROUNDS", (0, 0), (-1, -1), [CBG1, CBG2, CBG1, CBG2]),
#                                  ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#                                  ("TOPPADDING", (0, 0), (-1, -1), 5),
#                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
#                                  ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
#         story.append(wt); story.append(Spacer(1, 6))
#         adv_c = CBL if w.get("rain_expected") else CBD if w.get("heat_wave") else CGD
#         story.append(Table([[Paragraph(
#             f'<b>{LB["irr_advice"]}:</b>  {w.get("advice","—")}',
#             ParagraphStyle("adv", fontName="Helvetica-Bold", fontSize=10, textColor=adv_c))]],
#             colWidths=[W],
#             style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CD),
#                                ("TOPPADDING", (0, 0), (-1, -1), 10),
#                                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
#                                ("LEFTPADDING", (0, 0), (-1, -1), 14)])))
#         story.append(Spacer(1, 12))

#     forecast = w.get("forecast", [])
#     if forecast:
#         story.append(Paragraph(f"  {LB['forecast']}", S["sec"]))
#         fhdr  = [Paragraph(f"<b>{h}</b>", S["sm"]) for h in
#                  [LB["date"], LB["min_c"], LB["max_c"], LB["rain_mm"], LB["condition"], LB["irrigation"]]]
#         frows = [fhdr]
#         for day in forecast:
#             rain = day.get("rain_mm", 0)
#             irr  = LB["skip"] if rain >= 5 else LB["reduce"] if rain >= 2 else LB["normal"]
#             irr_c = CBD if rain >= 5 else CWN if rain >= 2 else CGD
#             frows.append([
#                 Paragraph(day["date"], S["sm"]),
#                 Paragraph(str(day["temp_min"]), S["body"]),
#                 Paragraph(str(day["temp_max"]), S["body"]),
#                 Paragraph(f'<font color="{CBL.hexval() if rain > 2 else CGD.hexval()}"><b>{rain}</b></font>', S["body"]),
#                 Paragraph(day["description"][:20], S["sm"]),
#                 Paragraph(f'<font color="{irr_c.hexval()}"><b>{irr}</b></font>', S["body"]),
#             ])
#         ft3 = Table(frows, colWidths=[W*0.15, W*0.10, W*0.10, W*0.13, W*0.30, W*0.22])
#         ft3.setStyle(TableStyle([
#             ("BACKGROUND", (0, 0), (-1, 0), CD),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
#             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]),
#             ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#             ("FONTSIZE", (0, 0), (-1, -1), 8),
#             ("TOPPADDING", (0, 0), (-1, -1), 4),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
#             ("LEFTPADDING", (0, 0), (-1, -1), 8),
#             ("ALIGN", (1, 0), (3, -1), "CENTER"),
#         ]))
#         story += [ft3, Spacer(1, 10)]

#     irr_rules = ([
#         ["Rain > 10mm expected",   "Skip irrigation completely that day"],
#         ["Rain 2–10mm expected",   "Reduce irrigation by 50%, monitor next day"],
#         ["Soil moisture > 65%",    "Stop irrigation. Risk of waterlogging and root rot"],
#         ["Soil moisture 40–65%",   "Optimal range. No irrigation needed"],
#         ["Soil moisture 25–40%",   "Irrigate lightly within 12 hours"],
#         ["Soil moisture < 25%",    "Irrigate immediately. Crop stress risk is high"],
#         ["Temperature > 38°C",     "Irrigate in early morning or late evening only"],
#         ["EC > 800 µS/cm",         "Do NOT irrigate — salt stress. Leach soil first"],
#     ] if lang != "hi" else [
#         ["10mm से अधिक बारिश", "उस दिन सिंचाई पूरी तरह छोड़ें"],
#         ["2–10mm बारिश की उम्मीद", "सिंचाई 50% कम करें"],
#         ["मिट्टी की नमी > 65%", "सिंचाई रोकें। जलभराव का खतरा"],
#         ["मिट्टी की नमी 40–65%", "सिंचाई की जरूरत नहीं"],
#         ["मिट्टी की नमी 25–40%", "12 घंटे के भीतर हल्की सिंचाई करें"],
#         ["मिट्टी की नमी < 25%", "तुरंत सिंचाई करें"],
#         ["तापमान > 38°C", "केवल सुबह या शाम को सिंचाई करें"],
#         ["EC > 800 µS/cm", "सिंचाई न करें — पहले मिट्टी धोएं"],
#     ])
#     story.append(Paragraph(f"  {LB['irr_guide']}", S["sec"]))
#     act_lbl = "स्थिति" if lang == "hi" else "Condition"
#     rec_lbl = "अनुशंसित कार्य" if lang == "hi" else "Recommended Action"
#     irr_hdr2  = [Paragraph(f"<b>{act_lbl}</b>", S["sm"]), Paragraph(f"<b>{rec_lbl}</b>", S["sm"])]
#     irr_rows2 = [irr_hdr2] + [[Paragraph(r[0], S["bold"]), Paragraph(r[1], S["body"])] for r in irr_rules]
#     irr_t2 = Table(irr_rows2, colWidths=[W * 0.38, W * 0.62])
#     irr_t2.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), CD), ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
#         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]), ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
#         ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("TOPPADDING", (0, 0), (-1, -1), 5),
#         ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 8),
#     ]))
#     story += [irr_t2, Spacer(1, 10)]

#     story.append(Paragraph(f"  {LB['soil_imp']}", S["sec"]))
#     for i, sug in enumerate(sugs, 1):
#         story.append(Paragraph(f"<b>{i}.</b>  {sug}", S["body"]))
#     story.append(Spacer(1, 10))

#     tips = ([
#         "Test soil pH every 6 months. pH directly affects nutrient availability for crops.",
#         "Apply organic compost (2–4 tonnes/ha) annually to improve soil structure.",
#         "Use drip irrigation where possible — reduces water usage by 30–50%.",
#         "Rotate crops each season to prevent nutrient depletion.",
#         "Never apply fertilizers when rain > 10mm is expected.",
#         "Monitor EC regularly — high EC (>800 µS/cm) indicates salt build-up.",
#     ] if lang != "hi" else [
#         "हर 6 महीने में मिट्टी का pH जांचें।",
#         "वार्षिक रूप से जैविक खाद (2–4 टन/हेक्टेयर) डालें।",
#         "जहां संभव हो ड्रिप सिंचाई का उपयोग करें।",
#         "हर मौसम में फसल बदलें।",
#         "जब 10mm से अधिक बारिश की उम्मीद हो तो उर्वरक न लगाएं।",
#         "EC नियमित रूप से मॉनिटर करें।",
#     ])
#     story.append(Paragraph(f"  {LB['best_prac']}", S["sec"]))
#     for i, tip in enumerate(tips, 1):
#         story.append(Paragraph(f"<b>{i}.</b>  {tip}", S["body"]))
#     story.append(Spacer(1, 8))
#     story += [HRFlowable(width=W, thickness=0.5, color=CBDR), Spacer(1, 5),
#               Paragraph("FarmCare Automated Soil Health Monitoring System — Soil Health Card Scheme, Govt. of India", S["smi"])]

#     doc.build(story)
#     buf.seek(0)
#     return buf


# @pdf_bp.route("/generate_pdf", methods=["POST"])
# def generate_pdf():
#     try:
#         form = {k: request.form.get(k, "N/A") for k in
#                 ["farmer_name", "email", "address", "location",
#                  "khasra_number", "farm_size", "crop_type"]}
#         try:
#             sensor = json.loads(request.form.get("sensor_data", "{}"))
#         except:
#             with lock:
#                 sensor = dict(latest)

#         lang = request.form.get("lang", "en")

#         img_bytes = soil_info = None
#         if "soil_image" in request.files:
#             img_bytes = request.files["soil_image"].read() or None
#             if img_bytes:
#                 soil_info = predict_soil_from_image(img_bytes)

#         crop_form = form.get("crop_type", "Rice")
#         if crop_form in ("Not selected", "N/A", ""):
#             crop_form = "Rice"

#         soil_type_str = (soil_info or {}).get("soil_type", "Alluvial")
#         score  = health_score(sensor)
#         sugs   = get_sugs(sensor)
#         opt_r  = optimize_crop(sensor, crop_form)
#         fert_r = predict_fertilizer(sensor, soil_type_str, crop_form)
#         buf    = build_pdf(form, sensor, soil_info, img_bytes, score, sugs, opt_r, fert_r, lang=lang)

#         fname = (f"SoilHealthCard_{form['farmer_name'].replace(' ', '_')}_"
#                  f"{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
#         return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name=fname)
#     except Exception:
#         traceback.print_exc()
#         return jsonify({"error": traceback.format_exc()}), 500
























































































"""
backend/routes/pdf.py
Route: /generate_pdf  — builds 3-page ReportLab PDF (Soil Health Card)
"""
import io, json, datetime, traceback, os
from flask import Blueprint, request, jsonify, send_file

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums  import TA_RIGHT
from reportlab.platypus   import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                   TableStyle, HRFlowable, PageBreak, Image as RLImage)
from reportlab.graphics.shapes import Drawing, Rect
from PIL import Image as PILImage

from backend.utils.sensor_state import latest, lock
from backend.utils.scoring      import health_score, classify, THRESH, get_sugs
from backend.utils.weather      import weather_cache, weather_lock
from backend.routes.soil        import predict_soil_from_image
from backend.routes.optimize    import optimize_crop
from backend.routes.fertilizer  import predict_fertilizer

pdf_bp = Blueprint("pdf", __name__)

# ── Palette ────────────────────────────────────────────────────
CD   = colors.HexColor("#0d1f0d");  CLG  = colors.HexColor("#4ade80")
CBG1 = colors.HexColor("#f0f9f0");  CBG2 = colors.HexColor("#e2f4e2")
CBDR = colors.HexColor("#b8d8b8");  CGD  = colors.HexColor("#16a34a")
CWN  = colors.HexColor("#d97706");  CBD  = colors.HexColor("#dc2626")
CMT  = colors.HexColor("#6b9a6b");  CTX  = colors.HexColor("#1a2e1a")
CBL  = colors.HexColor("#1d4ed8");  CSC  = colors.HexColor("#d4efd4")
PAGE_W, _ = A4; MAR = 2 * cm


def scolor(st):
    return CGD if st == "optimal" else CWN if st == "low" else CBD if st == "high" else CMT


def ps(n, **k):
    return ParagraphStyle(n, **k)


def _base_styles():
    return {
        "body": ps("b",  fontName="Helvetica",         fontSize=9,  textColor=CTX, spaceAfter=3, leading=14),
        "bold": ps("bd", fontName="Helvetica-Bold",    fontSize=9,  textColor=CTX),
        "sm":   ps("s",  fontName="Helvetica",         fontSize=8,  textColor=CMT),
        "smi":  ps("si", fontName="Helvetica-Oblique", fontSize=7.5, textColor=CMT, leading=11),
        "sec":  ps("sc", fontName="Helvetica-Bold",    fontSize=11, textColor=CD,
                   backColor=CSC, spaceAfter=4, spaceBefore=10, leftIndent=6, borderPad=4),
    }


def _get_styles(lang):
    """Try Hindi fonts if available, fall back to base Helvetica."""
    if lang != "hi":
        return _base_styles()          # English never needs merged fonts
    try:
        # hindi_pdf_patch.py lives in the project root (two levels up from here)
        import sys
        _root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        if _root not in sys.path:
            sys.path.insert(0, _root)
        from hindi_pdf_patch import get_pdf_fonts   # noqa: E402
        return get_pdf_fonts("hi")
    except FileNotFoundError as e:
        print(f"[PDF-Hindi] Font files missing — {e}")
        print("[PDF-Hindi] Run:  python3 download_hindi_fonts.py")
        return _base_styles()
    except Exception as e:
        print(f"[PDF-Hindi] Font load failed: {e}")
        return _base_styles()


def hdr(sub, ds, S):
    W = PAGE_W - 2 * MAR
    body_font = S["body"].fontName if S else "Helvetica-Bold"
    return Table([[
        Paragraph('<font color="#4ade80"><b>FarmCare</b></font>',
                  ps("h1", fontName="Helvetica-Bold", fontSize=20, textColor=CLG)),
        Paragraph(f'<font color="#a8d8a8"><b>{sub}</b></font><br/>'
                  f'<font color="#6b9a6b" size="8">{ds}</font>',
                  ps("h2", fontName=body_font, fontSize=11, textColor=CLG, alignment=TA_RIGHT))
    ]], colWidths=[W - 5.5 * cm, 5.5 * cm],
    style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CD),
                      ("TOPPADDING", (0, 0), (-1, -1), 12),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                      ("LEFTPADDING", (0, 0), (0, -1), 14),
                      ("RIGHTPADDING", (-1, 0), (-1, -1), 14)]))


def pbar(val, w, h=14, color=CGD):
    d = Drawing(w, h)
    d.add(Rect(0, 3, w, h - 6, fillColor=colors.HexColor("#c8e6c8"), strokeColor=None))
    d.add(Rect(0, 3, max(4, w * val / 100), h - 6, fillColor=color, strokeColor=None))
    return d


def build_pdf(form, sensor, soil_info, img_bytes, score, sugs, opt_result, fert_r, lang="en"):
    PDF_LABELS = {
        "en": {
            "title1": "SOIL HEALTH CARD", "title2": "ML ANALYSIS & RECOMMENDATIONS",
            "title3": "WEATHER & IRRIGATION PLAN",
            "farmer_det": "Farmer & Farm Details",
            "farmer_name": "Farmer Name", "email": "Email",
            "address": "Address", "gps": "GPS Location",
            "khasra": "Khasra No.", "farm_size": "Farm Size",
            "soil_type": "Detected Soil Type", "crop": "Selected Crop",
            "health_score": "Overall Soil Health Score",
            "readings": "Live Sensor Readings",
            "param": "Parameter", "value": "Value",
            "unit": "Unit", "opt_range": "Optimal Range", "status": "Status",
            "action_sum": "Immediate Action Summary",
            "soil_class": "Soil Classification (AI Model)",
            "confidence": "Confidence", "notes": "Notes",
            "rec_crops": "Recommended Crops",
            "crop_opt": "Crop Optimization",
            "param_match": "Parameter Match",
            "your_val": "Your Value", "ideal_range": "Ideal Range",
            "fert_rec": "Fertilizer Recommendation",
            "soil_mapped": "Soil", "crop_mapped": "Crop",
            "npk": "NPK Ratio", "rate": "Rate", "when": "When to Apply",
            "curr_weather": "Current Weather Conditions",
            "location": "Location", "condition": "Condition",
            "temperature": "Temperature", "humidity": "Humidity",
            "wind_speed": "Wind Speed", "rain_9h": "Rain (9h)",
            "heat_wave": "Heat Wave", "rain_alert": "Rain Alert",
            "irr_advice": "Irrigation Advice",
            "forecast": "10-Day Weather Forecast",
            "irr_guide": "Irrigation Decision Guide",
            "soil_imp": "Soil Improvement Suggestions",
            "best_prac": "General Best Practices for Soil Health",
            "date": "Date", "min_c": "Min °C", "max_c": "Max °C",
            "rain_mm": "Rain (mm)", "irrigation": "Irrigation",
            "excellent": "Excellent", "good": "Good", "moderate": "Moderate", "poor": "Poor",
            "skip": "Skip", "reduce": "Reduce", "normal": "Normal",
            "yes_caution": "Yes — extreme caution", "no": "No",
            "yes_hold": "Yes — hold irrigation",
        },
        "hi": {
            "title1": "मृदा स्वास्थ्य कार्ड", "title2": "ML विश्लेषण और अनुशंसाएं",
            "title3": "मौसम और सिंचाई योजना",
            "farmer_det": "किसान और खेत का विवरण",
            "farmer_name": "किसान का नाम", "email": "ईमेल",
            "address": "पता", "gps": "GPS स्थान",
            "khasra": "खसरा नंबर", "farm_size": "खेत का आकार",
            "soil_type": "पहचाना गया मृदा प्रकार", "crop": "चयनित फसल",
            "health_score": "समग्र मृदा स्वास्थ्य स्कोर",
            "readings": "लाइव सेंसर रीडिंग",
            "param": "पैरामीटर", "value": "मान",
            "unit": "इकाई", "opt_range": "अनुकूल सीमा", "status": "स्थिति",
            "action_sum": "तत्काल कार्य सारांश",
            "soil_class": "मृदा वर्गीकरण (AI मॉडल)",
            "confidence": "विश्वास", "notes": "नोट्स",
            "rec_crops": "अनुशंसित फसलें",
            "crop_opt": "फसल अनुकूलन",
            "param_match": "पैरामीटर मिलान",
            "your_val": "आपका मान", "ideal_range": "आदर्श सीमा",
            "fert_rec": "उर्वरक अनुशंसा",
            "soil_mapped": "मिट्टी", "crop_mapped": "फसल",
            "npk": "NPK अनुपात", "rate": "दर", "when": "कब डालें",
            "curr_weather": "वर्तमान मौसम की स्थिति",
            "location": "स्थान", "condition": "स्थिति",
            "temperature": "तापमान", "humidity": "आर्द्रता",
            "wind_speed": "हवा की गति", "rain_9h": "बारिश (9 घंटे)",
            "heat_wave": "लू", "rain_alert": "बारिश चेतावनी",
            "irr_advice": "सिंचाई सलाह",
            "forecast": "10 दिन का मौसम पूर्वानुमान",
            "irr_guide": "सिंचाई निर्णय गाइड",
            "soil_imp": "मृदा सुधार सुझाव",
            "best_prac": "मृदा स्वास्थ्य के लिए सामान्य सर्वोत्तम प्रथाएं",
            "date": "तारीख", "min_c": "न्यूनतम °C", "max_c": "अधिकतम °C",
            "rain_mm": "बारिश (मिमी)", "irrigation": "सिंचाई",
            "excellent": "उत्कृष्ट", "good": "अच्छा", "moderate": "मध्यम", "poor": "खराब",
            "skip": "छोड़ें", "reduce": "कम करें", "normal": "सामान्य",
            "yes_caution": "हाँ — अत्यधिक सावधानी", "no": "नहीं",
            "yes_hold": "हाँ — सिंचाई रोकें",
        }
    }
    LB = PDF_LABELS.get(lang, PDF_LABELS["en"])
    S  = _get_styles(lang)
    W  = PAGE_W - 2 * MAR
    buf  = io.BytesIO()
    doc  = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MAR, rightMargin=MAR,
                              topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    ds    = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
    story = []

    # ── PAGE 1: Farmer details + sensor readings ───────────────
    story += [hdr(LB["title1"], ds, S), Spacer(1, 10)]

    story.append(Paragraph(f"  {LB['farmer_det']}", S["sec"]))
    labels = [[LB["farmer_name"], LB["email"], LB["address"], LB["gps"]],
              [LB["khasra"], LB["farm_size"], LB["soil_type"], LB["crop"]]]
    vals   = [[form.get("farmer_name", "N/A"), form.get("email", "N/A"),
               form.get("address", "N/A"),     form.get("location", "N/A")],
              [form.get("khasra_number", "N/A"), f"{form.get('farm_size','N/A')} sqft",
               (soil_info or {}).get("soil_type", "—"), form.get("crop_type", "—")]]
    rows = []
    for i in range(2):
        rows.append([Paragraph(labels[i][j], S["sm"]) for j in range(4)])
        rows.append([Paragraph(f"<b>{vals[i][j]}</b>", S["body"]) for j in range(4)])
    ft = Table(rows, colWidths=[W * 0.25] * 4)
    ft.setStyle(TableStyle([("ROWBACKGROUNDS", (0, 0), (-1, -1), [CBG1, CBG2]),
                             ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
                             ("TOPPADDING", (0, 0), (-1, -1), 4),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                             ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    story += [ft, Spacer(1, 10)]

    story.append(Paragraph(f"  {LB['health_score']}", S["sec"]))
    sc    = CGD if score >= 70 else CWN if score >= 40 else CBD
    vdict = LB["excellent"] if score >= 75 else LB["good"] if score >= 60 else LB["moderate"] if score >= 40 else LB["poor"]
    story.append(Table([[pbar(score, int(W * 0.55), 16, sc),
                         Paragraph(f'<font color="{sc.hexval()}"><b>{score}% — {vdict}</b></font>', S["body"])]],
                        colWidths=[W * 0.57, W * 0.43]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(f"  {LB['readings']}", S["sec"]))
    hr = [Paragraph(f"<b>{h}</b>", S["sm"]) for h in
          [LB["param"], LB["value"], LB["unit"], LB["opt_range"], LB["status"]]]
    rs = [hr]
    for dname, key in [("Temperature", "temperature"), ("Moisture", "moisture"), ("EC", "ec"),
                        ("pH", "ph"), ("Nitrogen", "nitrogen"), ("Phosphorus", "phosphorus"),
                        ("Potassium", "potassium")]:
        val = sensor.get(key); st = classify(key, val); t = THRESH[key]
        vs  = f"{val:.2f}" if isinstance(val, float) and val not in (None, -1) else \
              str(val) if val not in (None, -1) else "ERR"
        rs.append([Paragraph(dname, S["body"]), Paragraph(f"<b>{vs}</b>", S["body"]),
                   Paragraph(t["unit"], S["sm"]), Paragraph(t["opt"], S["sm"]),
                   Paragraph(f'<font color="{scolor(st).hexval()}"><b>{st.upper()}</b></font>', S["body"])])
    st2 = Table(rs, colWidths=[W * 0.25, W * 0.15, W * 0.14, W * 0.25, W * 0.21])
    st2.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), CD),
                              ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
                              ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]),
                              ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
                              ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                              ("TOPPADDING", (0, 0), (-1, -1), 5),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8),
                              ("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    story += [st2, Spacer(1, 10)]

    story.append(Paragraph(f"  {LB['action_sum']}", S["sec"]))
    for sug in sugs[:4]:
        icon = "🔴" if any(w in sug.lower() for w in ["critical","immediately","now"]) else \
               "🟡" if any(w in sug.lower() for w in ["defic","low"]) else "🟢"
        story.append(Table([[Paragraph(f"{icon}  {sug}", S["body"])]], colWidths=[W],
            style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CBG1 if "🟢" in icon else CBG2),
                               ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
                               ("TOPPADDING", (0, 0), (-1, -1), 5),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                               ("LEFTPADDING", (0, 0), (-1, -1), 10)])))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 8))

    # ── PAGE 2: Soil + crop optimization + fertilizer ──────────
    story += [PageBreak(), hdr(LB["title2"], ds, S), Spacer(1, 10)]

    if soil_info:
        story.append(Paragraph(f"  {LB['soil_class']}", S["sec"]))
        left_content = [
            Paragraph(f'<font color="{CBL.hexval()}" size="13"><b>🌍 {soil_info.get("soil_type","—")}</b></font>', S["body"]),
            Spacer(1, 4),
            Paragraph(f'<b>{LB["confidence"]}:</b> {soil_info.get("confidence","—")}%', S["body"]),
            Spacer(1, 4),
            Paragraph(f'<b>{LB["notes"]}:</b> {soil_info.get("notes","—")}', S["body"]),
        ]
        for c in soil_info.get("crops", []):
            season_label = c.get("season_hi", c["season"]) if lang == "hi" else c["season"]
            note = f' ← {c["note"]}' if c.get("note") else ""
            left_content.append(Paragraph(f'• {c["crop"]}  ({season_label} / {c["months"]}){note}', S["body"]))
        right = ""
        if img_bytes:
            try:
                pi = PILImage.open(io.BytesIO(img_bytes)).convert("RGB")
                pi.thumbnail((160, 120))
                tb = io.BytesIO(); pi.save(tb, "JPEG", quality=85); tb.seek(0)
                right = RLImage(tb, width=4 * cm, height=3 * cm)
            except: pass
        it = Table([[left_content, right]], colWidths=[W * 0.72, W * 0.28])
        it.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                 ("BACKGROUND", (0, 0), (-1, -1), CBG1),
                                 ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 10),
                                 ("TOPPADDING", (0, 0), (-1, -1), 8),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
        story += [it, Spacer(1, 10)]

    if opt_result and "error" not in opt_result:
        story.append(Paragraph(f"  {LB['crop_opt']} — {opt_result['crop']}", S["sec"]))
        match_pct = opt_result.get("overall_match_pct", 0)
        mc = CGD if match_pct >= 80 else CWN if match_pct >= 50 else CBD
        story.append(Table([[pbar(match_pct, int(W * 0.45), 14, mc),
                             Paragraph(f'<font color="{mc.hexval()}"><b>{LB["param_match"]}: {match_pct}%</b></font>', S["body"])]],
                            colWidths=[W * 0.47, W * 0.53]))
        story.append(Spacer(1, 6))
        cmp_hdr = [Paragraph(f"<b>{h}</b>", S["sm"]) for h in
                   [LB["param"], LB["your_val"], LB["ideal_range"], LB["unit"], LB["status"]]]
        cmp_rows = [cmp_hdr]
        for c in opt_result.get("comparison", []):
            st = c["status"]
            cmp_rows.append([
                Paragraph(c["param"].title(), S["body"]),
                Paragraph(f'<b>{c["value"]}</b>', S["body"]),
                Paragraph(c["ideal"], S["sm"]),
                Paragraph(c["unit"], S["sm"]),
                Paragraph(f'<font color="{scolor(st).hexval()}"><b>{st.upper()}</b></font>', S["body"]),
            ])
        cmp_t = Table(cmp_rows, colWidths=[W * 0.25, W * 0.18, W * 0.22, W * 0.15, W * 0.20])
        cmp_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), CD), ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]), ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(cmp_t)
        story.append(Spacer(1, 6))
        for sug in opt_result.get("suggestions", []):
            story.append(Paragraph(sug, S["body"]))
        story.append(Spacer(1, 8))

    story.append(Paragraph(f"  {LB['fert_rec']}", S["sec"]))
    if fert_r and "error" not in fert_r:
        rec = fert_r["recommended"]
        story.append(Paragraph(
            f'<font color="{CMT.hexval()}" size="8">{LB["soil_mapped"]} → <b>{fert_r["soil_type"]}</b>  |  '
            f'{LB["crop_mapped"]} → <b>{fert_r["crop_type_mapped"]}</b></font>', S["sm"]))
        story.append(Spacer(1, 4))
        ft2 = Table([
            [Paragraph(f'<font color="{CBL.hexval()}" size="14"><b>🧪 {rec["name"]}</b></font>', S["body"]),
             Paragraph(f'<b>{LB["npk"]}:</b> <font color="{CBL.hexval()}"><b>{rec["npk"]}</b></font>', S["body"])],
            [Paragraph(f'<b>{LB["confidence"]}:</b> {rec["confidence"]}%  |  <b>{LB["rate"]}:</b> {rec["rate"]}', S["body"]), ""],
            [Paragraph(rec["description"], S["body"]), ""],
            [Paragraph(f'<b>{LB["when"]}:</b> {rec["timing"]}', S["body"]), ""],
        ], colWidths=[W * 0.55, W * 0.45],
        style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8eef8")),
                          ("SPAN", (0, 1), (1, 1)), ("SPAN", (0, 2), (1, 2)), ("SPAN", (0, 3), (1, 3)),
                          ("GRID", (0, 0), (-1, -1), 0.5, CBDR), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story += [ft2, Spacer(1, 8)]

    # ── PAGE 3: Weather + forecast + irrigation guide ──────────
    story += [PageBreak(), hdr(LB["title3"], ds, S), Spacer(1, 10)]

    with weather_lock:
        w = dict(weather_cache)

    if w.get("temperature"):
        story.append(Paragraph(f"  {LB['curr_weather']}", S["sec"]))
        w_data = [
            [Paragraph(f"<b>{LB['location']}</b>", S["sm"]),
             Paragraph(w.get("city", "—"), S["body"]),
             Paragraph(f"<b>{LB['condition']}</b>", S["sm"]),
             Paragraph(w.get("description", "—"), S["body"])],
            [Paragraph(f"<b>{LB['temperature']}</b>", S["sm"]),
             Paragraph(f'{w["temperature"]}°C (feels {w.get("feels_like","—")}°C)', S["body"]),
             Paragraph(f"<b>{LB['humidity']}</b>", S["sm"]),
             Paragraph(f'{w.get("humidity","—")}%', S["body"])],
            [Paragraph(f"<b>{LB['wind_speed']}</b>", S["sm"]),
             Paragraph(f'{w.get("wind_speed","—")} km/h', S["body"]),
             Paragraph(f"<b>{LB['rain_9h']}</b>", S["sm"]),
             Paragraph(f'{w.get("rain_mm",0)} mm', S["body"])],
            [Paragraph(f"<b>{LB['heat_wave']}</b>", S["sm"]),
             Paragraph(LB["yes_caution"] if w.get("heat_wave") else LB["no"], S["body"]),
             Paragraph(f"<b>{LB['rain_alert']}</b>", S["sm"]),
             Paragraph(LB["yes_hold"] if w.get("rain_expected") else LB["no"], S["body"])],
        ]
        wt = Table(w_data, colWidths=[W * 0.20, W * 0.30, W * 0.20, W * 0.30])
        wt.setStyle(TableStyle([("ROWBACKGROUNDS", (0, 0), (-1, -1), [CBG1, CBG2, CBG1, CBG2]),
                                 ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
                                 ("TOPPADDING", (0, 0), (-1, -1), 5),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
        story.append(wt); story.append(Spacer(1, 6))
        adv_c = CBL if w.get("rain_expected") else CBD if w.get("heat_wave") else CGD
        story.append(Table([[Paragraph(
            f'<b>{LB["irr_advice"]}:</b>  {w.get("advice","—")}',
            ParagraphStyle("adv", fontName="Helvetica-Bold", fontSize=10, textColor=adv_c))]],
            colWidths=[W],
            style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CD),
                               ("TOPPADDING", (0, 0), (-1, -1), 10),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                               ("LEFTPADDING", (0, 0), (-1, -1), 14)])))
        story.append(Spacer(1, 12))

    forecast = w.get("forecast", [])
    if forecast:
        story.append(Paragraph(f"  {LB['forecast']}", S["sec"]))
        fhdr  = [Paragraph(f"<b>{h}</b>", S["sm"]) for h in
                 [LB["date"], LB["min_c"], LB["max_c"], LB["rain_mm"], LB["condition"], LB["irrigation"]]]
        frows = [fhdr]
        for day in forecast:
            rain = day.get("rain_mm", 0)
            irr  = LB["skip"] if rain >= 5 else LB["reduce"] if rain >= 2 else LB["normal"]
            irr_c = CBD if rain >= 5 else CWN if rain >= 2 else CGD
            frows.append([
                Paragraph(day["date"], S["sm"]),
                Paragraph(str(day["temp_min"]), S["body"]),
                Paragraph(str(day["temp_max"]), S["body"]),
                Paragraph(f'<font color="{CBL.hexval() if rain > 2 else CGD.hexval()}"><b>{rain}</b></font>', S["body"]),
                Paragraph(day["description"][:20], S["sm"]),
                Paragraph(f'<font color="{irr_c.hexval()}"><b>{irr}</b></font>', S["body"]),
            ])
        ft3 = Table(frows, colWidths=[W*0.15, W*0.10, W*0.10, W*0.13, W*0.30, W*0.22])
        ft3.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), CD),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]),
            ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (3, -1), "CENTER"),
        ]))
        story += [ft3, Spacer(1, 10)]

    irr_rules = ([
        ["Rain > 10mm expected",   "Skip irrigation completely that day"],
        ["Rain 2–10mm expected",   "Reduce irrigation by 50%, monitor next day"],
        ["Soil moisture > 65%",    "Stop irrigation. Risk of waterlogging and root rot"],
        ["Soil moisture 40–65%",   "Optimal range. No irrigation needed"],
        ["Soil moisture 25–40%",   "Irrigate lightly within 12 hours"],
        ["Soil moisture < 25%",    "Irrigate immediately. Crop stress risk is high"],
        ["Temperature > 38°C",     "Irrigate in early morning or late evening only"],
        ["EC > 800 µS/cm",         "Do NOT irrigate — salt stress. Leach soil first"],
    ] if lang != "hi" else [
        ["10mm से अधिक बारिश", "उस दिन सिंचाई पूरी तरह छोड़ें"],
        ["2–10mm बारिश की उम्मीद", "सिंचाई 50% कम करें"],
        ["मिट्टी की नमी > 65%", "सिंचाई रोकें। जलभराव का खतरा"],
        ["मिट्टी की नमी 40–65%", "सिंचाई की जरूरत नहीं"],
        ["मिट्टी की नमी 25–40%", "12 घंटे के भीतर हल्की सिंचाई करें"],
        ["मिट्टी की नमी < 25%", "तुरंत सिंचाई करें"],
        ["तापमान > 38°C", "केवल सुबह या शाम को सिंचाई करें"],
        ["EC > 800 µS/cm", "सिंचाई न करें — पहले मिट्टी धोएं"],
    ])
    story.append(Paragraph(f"  {LB['irr_guide']}", S["sec"]))
    act_lbl = "स्थिति" if lang == "hi" else "Condition"
    rec_lbl = "अनुशंसित कार्य" if lang == "hi" else "Recommended Action"
    irr_hdr2  = [Paragraph(f"<b>{act_lbl}</b>", S["sm"]), Paragraph(f"<b>{rec_lbl}</b>", S["sm"])]
    irr_rows2 = [irr_hdr2] + [[Paragraph(r[0], S["bold"]), Paragraph(r[1], S["body"])] for r in irr_rules]
    irr_t2 = Table(irr_rows2, colWidths=[W * 0.38, W * 0.62])
    irr_t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CD), ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#c8e8c8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CBG1, CBG2]), ("GRID", (0, 0), (-1, -1), 0.5, CBDR),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [irr_t2, Spacer(1, 10)]

    story.append(Paragraph(f"  {LB['soil_imp']}", S["sec"]))
    for i, sug in enumerate(sugs, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {sug}", S["body"]))
    story.append(Spacer(1, 10))

    tips = ([
        "Test soil pH every 6 months. pH directly affects nutrient availability for crops.",
        "Apply organic compost (2–4 tonnes/ha) annually to improve soil structure.",
        "Use drip irrigation where possible — reduces water usage by 30–50%.",
        "Rotate crops each season to prevent nutrient depletion.",
        "Never apply fertilizers when rain > 10mm is expected.",
        "Monitor EC regularly — high EC (>800 µS/cm) indicates salt build-up.",
    ] if lang != "hi" else [
        "हर 6 महीने में मिट्टी का pH जांचें।",
        "वार्षिक रूप से जैविक खाद (2–4 टन/हेक्टेयर) डालें।",
        "जहां संभव हो ड्रिप सिंचाई का उपयोग करें।",
        "हर मौसम में फसल बदलें।",
        "जब 10mm से अधिक बारिश की उम्मीद हो तो उर्वरक न लगाएं।",
        "EC नियमित रूप से मॉनिटर करें।",
    ])
    story.append(Paragraph(f"  {LB['best_prac']}", S["sec"]))
    for i, tip in enumerate(tips, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {tip}", S["body"]))
    story.append(Spacer(1, 8))
    story += [HRFlowable(width=W, thickness=0.5, color=CBDR), Spacer(1, 5),
              Paragraph("FarmCare Automated Soil Health Monitoring System — Soil Health Card Scheme, Govt. of India", S["smi"])]

    doc.build(story)
    buf.seek(0)
    return buf


@pdf_bp.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    try:
        form = {k: request.form.get(k, "N/A") for k in
                ["farmer_name", "email", "address", "location",
                 "khasra_number", "farm_size", "crop_type"]}
        try:
            sensor = json.loads(request.form.get("sensor_data", "{}"))
        except:
            with lock:
                sensor = dict(latest)

        lang = request.form.get("lang", "en")

        img_bytes = soil_info = None
        if "soil_image" in request.files:
            img_bytes = request.files["soil_image"].read() or None
            if img_bytes:
                soil_info = predict_soil_from_image(img_bytes)

        crop_form = form.get("crop_type", "Rice")
        if crop_form in ("Not selected", "N/A", ""):
            crop_form = "Rice"

        soil_type_str = (soil_info or {}).get("soil_type", "Alluvial")
        score  = health_score(sensor)
        sugs   = get_sugs(sensor)
        opt_r  = optimize_crop(sensor, crop_form)
        fert_r = predict_fertilizer(sensor, soil_type_str, crop_form)
        buf    = build_pdf(form, sensor, soil_info, img_bytes, score, sugs, opt_r, fert_r, lang=lang)

        fname = (f"SoilHealthCard_{form['farmer_name'].replace(' ', '_')}_"
                 f"{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name=fname)
    except Exception:
        traceback.print_exc()
        return jsonify({"error": traceback.format_exc()}), 500