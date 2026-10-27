import os
import json
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FairShift",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------------------------
# COMPREHENSIVE MULTILINGUAL DICTIONARY (EN, HI, TA, TE, BN)
# ---------------------------------------------------------------------------------------------
TRANSLATIONS = {
    "en": {
        "app_title": "FairShift",
        "tagline": "Where Every Worker Counts and Every Workplace Can Do Better.",
        "sdg_badge": "UN SDG 8 • Decent Work and Economic Growth",
        "login_heading": "Sign In to FairShift",
        "login_subheading": "Select your workplace role or use the 1-click demo buttons below.",
        "worker_login": "Worker Portal",
        "employer_login": "Employer / Management",
        "workplace_env": "Workplace Environment:",
        "select_lang": "Language / भाषा / மொழி / భాష / ভাষা:",
        "worker_id_label": "Worker ID / Badge Number:",
        "admin_id_label": "Administrator / Site ID:",
        "password_label": "Access PIN / Password:",
        "login_submit": "Log In to Portal",
        "quick_demo_header": "1-Click Interactive Demo Logins (For Judges):",
        "demo_worker_btn": "👷 1-Click Worker Demo",
        "demo_employer_btn": "🏢 1-Click Employer Demo",
        "logout_btn": "🚪 Logout / Switch User",
        "switch_facility": "Switch Facility:",
        "emergency_btn": "🚨 REPORT IMMEDIATE DANGER",
        "emergency_box_title": "⚠️ Immediate Danger & Critical Hazard Channel",
        "emergency_box_sub": "Use this channel only for active life-threatening hazards (structural collapse, high-voltage, toxic leaks, fire, violence).",
        "emergency_notice": "⚠️ IMPORTANT NOTICE: Submitting this digital hazard report alerts on-site safety coordinators. It does NOT automatically call government police, fire, or ambulance services. If you face immediate danger, follow site evacuation routes and dial local emergency services (112 / 100 / 101).",
        "hazard_category": "1. Hazard Category:",
        "hazard_loc": "2. Specific Location or Work Area:",
        "hazard_desc": "3. Short Description of Danger:",
        "hazard_evidence": "4. Optional Photo / Audio Evidence:",
        "hazard_submit": "🚨 SUBMIT IMMEDIATE DANGER ALERT",
        "designated_contacts": "Designated On-Site Emergency Contacts",
        "safety_lead": "Safety Lead:",
        "first_aid": "First Aid Station:",
        "assembly_pt": "Evacuation Assembly Point:",
        "external_emergency": "External Emergency Contacts:",
        
        # Worker Portal
        "worker_portal_title": "Worker Self-Service Portal",
        "dash_tab": "Personal Dashboard",
        "griev_tab": "Grievance & Safety",
        "att_tab": "Attendance & Payslip",
        "rights_tab": "Rights Assistant",
        "today_shift": "Today's Shift Status",
        "checked_in": "🟢 Checked In",
        "days_worked": "Regular Days Worked",
        "safe_ot_rem": "Safe Overtime Remaining",
        "ot_cap_note": "Cap: 20 hrs/mo",
        "leave_bal": "Paid Leave Balance",
        "notices_title": "Personal Notices & Site Alerts",
        "my_submissions": "My Recent Submissions",
        "submit_report_title": "Submit a Report or Feedback",
        "identity_mode": "Identity Mode:",
        "anon_opt": "🔒 100% Anonymous (No ID or phone attached)",
        "id_opt": "🆔 Remote with My Worker ID",
        "report_cat": "Report Category:",
        "dept_loc": "Department or Shift Location:",
        "desc_issue": "Describe the issue in detail (Any regional language accepted):",
        "mark_urgent": "Mark as High Severity / Urgent",
        "submit_griev_btn": "🔒 SUBMIT GRIEVANCE / REPORT",
        "recent_facility_reports": "Recent Reports in This Facility",
        "voice_rec_title": "🎙️ Record Voice Complaint (Voice-to-Text):",
        "voice_rec_prompt": "Tap the microphone below to speak your complaint in any language:",
        "transcribe_btn": "✨ Transcribe Voice to Text with AI",
        "voice_success": "✅ Voice recording transcribed! You can review or edit the text below:",
        
        # Attendance & Payslip
        "shift_checkin_title": "Interactive Shift Check-In",
        "scan_qr": "📷 Scan QR Code",
        "geo_checkin": "🛰️ Geo-Fence Check-In",
        "ot_calc_title": "Monthly Working Hours & Overtime Safety Lock",
        "daily_wage": "Daily Wage Rate (₹ / Shift):",
        "regular_days_slider": "Regular Days Worked This Month:",
        "ot_hours_slider": "Overtime Hours Clocked (1.5x Pay):",
        "ot_lock_title": "🛑 PORTAL SAFETY LOCK ACTIVE: OVERTIME CAP EXCEEDED",
        "ot_lock_desc": "You have logged overtime exceeding the safety threshold of 20 hours/month. Additional shifts are locked to prevent fatigue and accidents under SDG 8.8.",
        "leave_app_title": "Application for Paid Leave (SDG 8.5)",
        "leave_quota_desc": "Total Accrued: 12 Days | Taken: 3 Days | Remaining Paid Balance: 9 Days",
        "leave_type": "Leave Type:",
        "leave_reason": "Reason for Leave:",
        "submit_leave_btn": "Submit Paid Leave Application",
        "payslip_title": "Transparent Payslip Breakdown",
        "net_salary": "Net Salary Credited:",
        "explain_payslip_btn": "✨ Explain Payslip in My Language",
        
        # Rights Assistant
        "rights_assistant_title": "AI Worker Rights Assistant",
        "rights_info_banner": "ℹ️ Informational Worker Guidance Only: This assistant provides reliable workplace policy explanations. It does not provide legal advice.",
        "faq_q1": "Why is my overtime pay different this month?",
        "faq_q2": "What should I do if my salary hasn't been paid?",
        "faq_q3": "How do I report an unsafe working condition?",
        "faq_q4": "What does this deduction on my payslip mean?",
        
        # Employer Dashboard
        "employer_title": "FairShift Guardian — Workplace Risk & Fairness Intelligence",
        "guardian_tab": "Guardian Dashboard",
        "audit_tab": "Fairness Audit",
        "radar_tab": "Risk Radar",
        "rootcause_tab": "Root-Cause",
        "intervention_tab": "Intervention Planner",
        "active_workforce": "Active Workforce On-Site",
        "payroll_parity": "Audited Payroll Parity Rate",
        "urgent_flags": "High-Severity Safety Flags",
        "active_plans": "Active Intervention Plans",
        "audit_desc": "Cross-references biometric attendance records, overtime logs, and payroll ledgers. Flags calculation variances with mathematical proof.",
        "radar_desc": "Identifies recurring safety patterns, unresolved grievances, and excessive recorded hours with interactive charts.",
        "rootcause_desc": "Groups related complaints by department and location to uncover systemic drivers rather than blaming individual workers.",
        "intervention_desc": "Don't just tell employers what's wrong. Tell them what to do next. Turn alerts into assigned, time-bound, verifiable action plans.",
        "create_int_btn": "➕ Create New Intervention Task Linked to an Alert"
    },
    "hi": {
        "app_title": "FairShift",
        "tagline": "जहाँ हर कर्मचारी का महत्व है और हर कार्यस्थल बेहतर बन सकता है।",
        "sdg_badge": "संयुक्त राष्ट्र एसडीजी 8 • गरिमापूर्ण कार्य और आर्थिक विकास",
        "login_heading": "FairShift में साइन इन करें",
        "login_subheading": "अपनी कार्यस्थल भूमिका चुनें या त्वरित डेमो बटन का उपयोग करें।",
        "worker_login": "कर्मचारी पोर्टल",
        "employer_login": "नियोक्ता / प्रबंधन",
        "workplace_env": "कार्यस्थल वातावरण:",
        "select_lang": "भाषा / Language:",
        "worker_id_label": "कर्मचारी आईडी / बैज संख्या:",
        "admin_id_label": "प्रशासक / साइट आईडी:",
        "password_label": "पासवर्ड / पिन:",
        "login_submit": "पोर्टल में प्रवेश करें",
        "quick_demo_header": "1-क्लिक त्वरित डेमो लॉगिन (जजों के लिए):",
        "demo_worker_btn": "👷 1-क्लिक कर्मचारी डेमो",
        "demo_employer_btn": "🏢 1-क्लिक नियोक्ता डेमो",
        "logout_btn": "🚪 लॉगआउट / बदलें",
        "switch_facility": "परिसर बदलें:",
        "emergency_btn": "🚨 तत्काल खतरे की सूचना दें",
        "emergency_box_title": "⚠️ आपातकालीन व गंभीर खतरा रिपोर्ट चैनल",
        "emergency_box_sub": "इसका उपयोग केवल सक्रिय जानलेवा खतरों (संरचनात्मक गिरावट, उच्च वोल्टेज, गैस रिसाव, आग) के लिए करें।",
        "emergency_notice": "⚠️ महत्वपूर्ण सूचना: यह रिपोर्ट साइट सुरक्षा टीम को सूचित करती है। यह सरकारी पुलिस/एम्बुलेंस को कॉल नहीं करती। आपातकाल में तुरंत 112 / 100 पर कॉल करें।",
        "hazard_category": "1. खतरे की श्रेणी:",
        "hazard_loc": "2. सटीक स्थान या कार्य क्षेत्र:",
        "hazard_desc": "3. खतरे का संक्षिप्त विवरण:",
        "hazard_evidence": "4. साक्ष्य (फोटो / ऑडियो):",
        "hazard_submit": "🚨 आपातकालीन चेतावनी भेजें",
        "designated_contacts": "नामित ऑन-साइट आपातकालीन संपर्क",
        "safety_lead": "सुरक्षा प्रमुख:",
        "first_aid": "प्राथमिक चिकित्सा केंद्र:",
        "assembly_pt": "निकासी स्थल:",
        "external_emergency": "बाहरी आपातकालीन नंबर:",
        
        # Worker Portal
        "worker_portal_title": "कर्मचारी स्व-सेवा पोर्टल",
        "dash_tab": "व्यक्तिगत डैशबोर्ड",
        "griev_tab": "शिकायत और सुरक्षा",
        "att_tab": "उपस्थिति और पे-स्लिप",
        "rights_tab": "अधिकार सहायक",
        "today_shift": "आज की पाली की स्थिति",
        "checked_in": "🟢 उपस्थिति दर्ज (चेक-इन)",
        "days_worked": "कार्य किए गए नियमित दिन",
        "safe_ot_rem": "सुरक्षित ओवरटाइम शेष",
        "ot_cap_note": "सीमा: 20 घंटे/माह",
        "leave_bal": "सवेतन अवकाश शेष",
        "notices_title": "व्यक्तिगत सूचनाएं व सुरक्षा अलर्ट",
        "my_submissions": "मेरी हालिया शिकायतें / रिपोर्ट",
        "submit_report_title": "समस्या या प्रतिक्रिया दर्ज करें",
        "identity_mode": "पहचान मोड:",
        "anon_opt": "🔒 100% गोपनीय (नाम व फोन नहीं भेजा जाएगा)",
        "id_opt": "🆔 मेरी कर्मचारी आईडी के साथ",
        "report_cat": "रिपोर्ट श्रेणी:",
        "dept_loc": "विभाग या पाली स्थान:",
        "desc_issue": "विस्तार से बताएं (किसी भी क्षेत्रीय भाषा में):",
        "mark_urgent": "अत्यंत गंभीर / तत्काल चिह्नित करें",
        "submit_griev_btn": "🔒 शिकायत / रिपोर्ट दर्ज करें",
        "recent_facility_reports": "इस परिसर की हालिया रिपोर्टें",
        "voice_rec_title": "🎙️ बोलकर शिकायत दर्ज करें (वॉइस-टू-टेक्स्ट):",
        "voice_rec_prompt": "अपनी भाषा में शिकायत बोलने के लिए नीचे माइक पर टैप करें:",
        "transcribe_btn": "✨ आवाज को टेक्स्ट में बदलें",
        "voice_success": "✅ आवाज सफलतापूर्वक टेक्स्ट में बदल गई! नीचे समीक्षा करें:",
        
        # Attendance & Payslip
        "shift_checkin_title": "इंटरएक्टिव शिफ्ट चेक-इन",
        "scan_qr": "📷 क्यूआर कोड स्कैन करें",
        "geo_checkin": "🛰️ जियो-फेंस चेक-इन",
        "ot_calc_title": "मासिक कार्य घंटे व ओवरटाइम सुरक्षा लॉक",
        "daily_wage": "दैनिक मजदूरी दर (₹ / पाली):",
        "regular_days_slider": "इस महीने काम किए गए नियमित दिन:",
        "ot_hours_slider": "ओवरटाइम घंटे (1.5 गुना दर):",
        "ot_lock_title": "🛑 सुरक्षा लॉक सक्रिय: ओवरटाइम सीमा समाप्त",
        "ot_lock_desc": "आपने 20 घंटे/माह की सुरक्षित सीमा पूरी कर ली है। थकान और दुर्घटनाओं से बचाव (SDG 8.8) हेतु अतिरिक्त शिफ्ट लॉक कर दी गई है।",
        "leave_app_title": "सवेतन अवकाश हेतु आवेदन (SDG 8.5)",
        "leave_quota_desc": "कुल अर्जित: 12 दिन | उपयोग: 3 दिन | शेष सवेतन अवकाश: 9 दिन",
        "leave_type": "अवकाश प्रकार:",
        "leave_reason": "अवकाश का कारण:",
        "submit_leave_btn": "अवकाश आवेदन जमा करें",
        "payslip_title": "पारदर्शी पे-स्लिप विवरण",
        "net_salary": "खाते में जमा शुद्ध वेतन:",
        "explain_payslip_btn": "✨ मेरी भाषा में वेतन समझें",
        
        # Rights Assistant
        "rights_assistant_title": "एआई कर्मचारी अधिकार सहायक",
        "rights_info_banner": "ℹ️ केवल सूचनात्मक मार्गदर्शन: यह सहायक कार्यस्थल नीतियों की स्पष्ट जानकारी देता है। यह कानूनी सलाह नहीं है।",
        "faq_q1": "इस महीने मेरा ओवरटाइम वेतन अलग क्यों है?",
        "faq_q2": "यदि मेरा वेतन समय पर न मिले तो मुझे क्या करना चाहिए?",
        "faq_q3": "असुरक्षित कार्य स्थितियों की रिपोर्ट कैसे करें?",
        "faq_q4": "मेरी पे-स्लिप पर इस कटौती का क्या अर्थ है?",
        
        # Employer Dashboard
        "employer_title": "FairShift Guardian — कार्यस्थल जोखिम और निष्पक्षता इंटेलिजेंस",
        "guardian_tab": "गार्डियन डैशबोर्ड",
        "audit_tab": "निष्पक्षता ऑडिट",
        "radar_tab": "जोखिम रडार",
        "rootcause_tab": "मूल-कारण विश्लेषण",
        "intervention_tab": "हस्तक्षेप योजना",
        "active_workforce": "ऑन-साइट सक्रिय कार्यबल",
        "payroll_parity": "ऑडिट की गई पेरोल निष्पक्षता दर",
        "urgent_flags": "अति-गंभीर सुरक्षा अलर्ट",
        "active_plans": "सक्रिय निवारण योजनाएं",
        "audit_desc": "बायोमेट्रिक उपस्थिति और पेरोल का मिलान करता है और गणितीय प्रमाण के साथ विसंगतियों को चिह्नित करता है।",
        "radar_desc": "इंटरएक्टिव चार्ट के साथ आवर्ती सुरक्षा पैटर्न और अनसुलझी शिकायतों की पहचान करता है।",
        "rootcause_desc": "समस्याओं के व्यवस्थित कारणों को खोजने के लिए शिकायतों को समूहीकृत करता है।",
        "intervention_desc": "नियोक्ताओं को कार्रवाई योग्य, समयबद्ध समाधान योजनाएं प्रदान करता है।",
        "create_int_btn": "➕ नए अलर्ट से जुड़ी निवारण योजना बनाएं"
    },
    "ta": {
        "app_title": "FairShift",
        "tagline": "ஒவ்வொரு தொழிலாளியும் மதிக்கப்படும் இடம், ஒவ்வொரு பணியிடமும் சிறக்க முடியும்.",
        "sdg_badge": "ஐநா SDG 8 • கண்ணியமான வேலை மற்றும் பொருளாதார வளர்ச்சி",
        "login_heading": "FairShift உள்நுழைவு",
        "login_subheading": "உங்கள் பணியிடப் பாத்திரத்தைத் தேர்ந்தெடுக்கவும் அல்லது டெமோவை அழுத்தவும்.",
        "worker_login": "தொழிலாளர் போர்டல்",
        "employer_login": "நிர்வாகம் / முதலாளி",
        "workplace_env": "பணியிட சூழல்:",
        "select_lang": "மொழி / Language:",
        "worker_id_label": "தொழிலாளர் ஐடி எண்:",
        "admin_id_label": "நிர்வாக ஐடி:",
        "password_label": "கடவுச்சொல் / பின்:",
        "login_submit": "உள்நுழைக",
        "quick_demo_header": "1-கிளிக் டெமோ உள்நுழைவு (நீதிபதிகளுக்கு):",
        "demo_worker_btn": "👷 1-கிளிக் தொழிலாளர் டெமோ",
        "demo_employer_btn": "🏢 1-கிளிக் நிர்வாகி டெமோ",
        "logout_btn": "🚪 வெளியேறு / மாற்று",
        "switch_facility": "வளாகத்தை மாற்றுக:",
        "emergency_btn": "🚨 உடனடி ஆபத்தை அறிவிக்கவும்",
        "emergency_box_title": "⚠️ உடனடி அவசர பாதுகாப்பு பிரிவு",
        "emergency_box_sub": "உயிர் ஆபத்தான சூழல்களில் மட்டும் இதைப் பயன்படுத்தவும்.",
        "emergency_notice": "⚠️ முக்கிய அறிவிப்பு: இது தள பாதுகாப்பு குழுவை எச்சரிக்கும். அரசு அவசர எண்ணை தானாக அழைக்காது. அவசரத்திற்கு 112 / 100 ஐ அழைக்கவும்.",
        "hazard_category": "1. ஆபத்து வகை:",
        "hazard_loc": "2. குறிப்பிட்ட இடம்:",
        "hazard_desc": "3. ஆபத்தின் சுருக்கமான விளக்கம்:",
        "hazard_evidence": "4. சான்று (புகைப்படம் / குரல்):",
        "hazard_submit": "🚨 அவசர எச்சரிக்கையை அனுப்பவும்",
        "designated_contacts": "தள அவசர தொடர்பு எண்கள்",
        "safety_lead": "பாதுகாப்பு தலைவர்:",
        "first_aid": "முதலுதவி நிலையம்:",
        "assembly_pt": "பாதுகாப்பு கூடும் இடம்:",
        "external_emergency": "அரசு அவசர எண்கள்:",
        
        # Worker Portal
        "worker_portal_title": "தொழிலாளர் சுய சேவை போர்டல்",
        "dash_tab": "தனிப்பட்ட டாஷ்போர்டு",
        "griev_tab": "புகார் & பாதுகாப்பு",
        "att_tab": "வருகை & சம்பளச்சீட்டு",
        "rights_tab": "உரிமைகள் உதவியாளர்",
        "today_shift": "இன்றைய ஷிப்ட் நிலை",
        "checked_in": "🟢 வருகை பதிவு செய்யப்பட்டது",
        "days_worked": "வேலை செய்த நாட்கள்",
        "safe_ot_rem": "பாதுகாப்பான கூடுதல் நேரம் மீதம்",
        "ot_cap_note": "வரம்பு: 20 மணிநேரம்/மாதம்",
        "leave_bal": "சம்பளத்துடன் கூடிய விடுப்பு",
        "notices_title": "தனிப்பட்ட அறிவிப்புகள்",
        "my_submissions": "எனது சமீபத்திய புகார்கள்",
        "submit_report_title": "புகார் அல்லது ஆலோசனையை பதிவு செய்யவும்",
        "identity_mode": "அடையாள முறை:",
        "anon_opt": "🔒 100% ரகசியம் (பெயர் பகிரப்படாது)",
        "id_opt": "🆔 எனது தொழிலாளர் ஐடியுடன்",
        "report_cat": "புகார் வகை:",
        "dept_loc": "துறை அல்லது இடம்:",
        "desc_issue": "விவரங்களை எழுதவும் (தமிழில் எழுதலாம்):",
        "mark_urgent": "அவசரம் என குறிக்கவும்",
        "submit_griev_btn": "🔒 புகாரை சமர்ப்பிக்கவும்",
        "recent_facility_reports": "சமீபத்திய அறிக்கைகள்",
        "voice_rec_title": "🎙️ குரல் மூலம் புகார் பதிவு (குரல்-வழி-உரை):",
        "voice_rec_prompt": "உங்கள் குரலில் புகாரைப் பேச கீழே உள்ள மைக்கை அழுத்தவும்:",
        "transcribe_btn": "✨ குரலை உரையாக மாற்றவும்",
        "voice_success": "✅ குரல் உரையாக மாற்றப்பட்டது! கீழே சரிபார்க்கவும்:",
        
        # Attendance & Payslip
        "shift_checkin_title": "ஷிப்ட் வருகைப் பதிவு",
        "scan_qr": "📷 QR ஸ்கேன்",
        "geo_checkin": "🛰️ இருப்பிட பதிவு",
        "ot_calc_title": "வேலை நேரம் மற்றும் கூடுதல் நேர பாதுகாப்பு பூட்டு",
        "daily_wage": "தினசரி கூலி (₹):",
        "regular_days_slider": "வேலை செய்த நாட்கள்:",
        "ot_hours_slider": "கூடுதல் நேரம் (1.5x ஊதியம்):",
        "ot_lock_title": "🛑 பாதுகாப்பு பூட்டு: கூடுதல் நேர வரம்பு முடிந்தது",
        "ot_lock_desc": "நீங்கள் 20 மணிநேர பாதுகாப்பான வரம்பை எட்டிவிட்டீர்கள். சோர்வு விபத்துகளைத் தடுக்க கூடுதல் ஷிப்ட் தற்காலிகமாக பூட்டப்பட்டுள்ளது.",
        "leave_app_title": "சம்பள விடுப்பு விண்ணப்பம்",
        "leave_quota_desc": "மொத்தம்: 12 நாட்கள் | பயன்பாடு: 3 | மீதம்: 9 நாட்கள்",
        "leave_type": "விடுப்பு வகை:",
        "leave_reason": "காரணம்:",
        "submit_leave_btn": "விண்ணப்பிக்கவும்",
        "payslip_title": "வெளிப்படையான சம்பள விவரம்",
        "net_salary": "வங்கியில் வரவு வைக்கப்பட்ட தொகை:",
        "explain_payslip_btn": "✨ தமிழில் சம்பளத்தை விளக்கு",
        
        # Rights Assistant
        "rights_assistant_title": "தொழிலாளர் உரிமைகள் AI உதவியாளர்",
        "rights_info_banner": "ℹ️ தகவல் வழிகாட்டுதல் மட்டுமே: இது சட்ட ஆலோசனை அல்ல.",
        "faq_q1": "இந்த மாதம் எனது கூடுதல் நேர ஊதியம் ஏன் வித்தியாசமாக உள்ளது?",
        "faq_q2": "சம்பளம் வரவில்லை என்றால் நான் என்ன செய்ய வேண்டும்?",
        "faq_q3": "பாதுகாப்பற்ற வேலை நிலைமைகளை எவ்வாறு புகாரளிப்பது?",
        "faq_q4": "சம்பள பிடித்தம் எதைக் குறிக்கிறது?",
        
        # Employer Dashboard
        "employer_title": "FairShift Guardian — பணியிட ஆபத்து & நியாய நுண்ணறிவு",
        "guardian_tab": "கார்டியன் டாஷ்போர்டு",
        "audit_tab": "நியாயமான தணிக்கை",
        "radar_tab": "ஆபத்து ரேடார்",
        "rootcause_tab": "மூலக் காரணம்",
        "intervention_tab": "தலையீட்டு திட்டம்",
        "active_workforce": "பணியில் உள்ள மொத்த தொழிலாளர்கள்",
        "payroll_parity": "சம்பள தணிக்கை விகிதம்",
        "urgent_flags": "அவசர பாதுகாப்பு எச்சரிக்கைகள்",
        "active_plans": "செயலில் உள்ள திட்டங்கள்",
        "audit_desc": "வருகையையும் ஊதியத்தையும் ஒப்பிட்டு பிழைகளை சுட்டிக்காட்டுகிறது.",
        "radar_desc": "விளக்கப்படங்களுடன் தொடர்ச்சியான ஆபத்துகளைக் காட்டுகிறது.",
        "rootcause_desc": "பிரச்சினைகளுக்கான அடிப்படைக் காரணங்களைக் கண்டறிய உதவுகிறது.",
        "intervention_desc": "நிர்வாகத்திற்கு உடனடி தீர்வுத் திட்டங்களை வழங்குகிறது.",
        "create_int_btn": "➕ புதிய தீர்வுத் திட்டத்தை உருவாக்கவும்"
    },
    "te": {
        "app_title": "FairShift",
        "tagline": "ప్రతి కార్మికుడికి ప్రాముఖ్యత ఉన్న చోట మరియు ప్రతి కార్యాలయం మరింత మెరుగుపడగలదు.",
        "sdg_badge": "ఐరాస SDG 8 • గౌరవప్రదమైన పని మరియు ఆర్థిక వృద్ధి",
        "login_heading": "FairShift లాగిన్",
        "login_subheading": "మీ కార్యాలయ పాత్రను ఎంచుకోండి లేదా డెమో క్లిక్ చేయండి.",
        "worker_login": "కార్మికుల పోర్టల్",
        "employer_login": "యాజమాన్యం / అడ్మిన్",
        "workplace_env": "కార్యాలయ వాతావరణం:",
        "select_lang": "భాష / Language:",
        "worker_id_label": "కార్మికుడి ఐడి నంబర్:",
        "admin_id_label": "అడ్మిన్ ఐడి:",
        "password_label": "పాస్వర్డ్ / పిన్:",
        "login_submit": "లాగిన్ అవ్వండి",
        "quick_demo_header": "1-క్లిక్ డెమో లాగిన్ (జడ్జీల కోసం):",
        "demo_worker_btn": "👷 1-క్లిక్ కార్మికుల డెమో",
        "demo_employer_btn": "🏢 1-క్లిక్ అడ్మిన్ డెమో",
        "logout_btn": "🚪 లాగ్ అవుట్",
        "switch_facility": "ప్రాంగణాన్ని మార్చండి:",
        "emergency_btn": "🚨 తక్షణ ప్రమాదాన్ని నివేదించండి",
        "emergency_box_title": "⚠️ అత్యవసర ప్రమాద హెచ్చరిక ఛానెల్",
        "emergency_box_sub": "తీవ్రమైన ప్రాణాపాయ పరిస్థితుల్లో మాత్రమే ఉపయోగించండి.",
        "emergency_notice": "⚠️ ముఖ్య గమనిక: ఇది సైట్ భద్రతా బృందానికి తెలియజేస్తుంది. ప్రభుత్వ అత్యవసర నంబర్‌కు ఆటోమేటిక్‌గా కాల్ చేయదు. అత్యవసరమైతే 112 / 100 కు కాల్ చేయండి.",
        "hazard_category": "1. ప్రమాద రకం:",
        "hazard_loc": "2. నిర్దిష్ట ప్రదేశం:",
        "hazard_desc": "3. ప్రమాదం గురించిన సంక్షిప్త వివరణ:",
        "hazard_evidence": "4. సాక్ష్యం (ఫోటో / వాయిస్):",
        "hazard_submit": "🚨 అత్యవసర హెచ్చరిక పంపండి",
        "designated_contacts": "సైట్ అత్యవసర సంప్రదింపు నంబర్లు",
        "safety_lead": "భద్రతా అధికారి:",
        "first_aid": "ప్రథమ చికిత్స కేంద్రం:",
        "assembly_pt": "సురక్షిత సమావేశ స్థలం:",
        "external_emergency": "బాహ్య అత్యవసర నంబర్లు:",
        
        # Worker Portal
        "worker_portal_title": "కార్మికుల స్వయం సేవా పోర్టల్",
        "dash_tab": "వ్యక్తిగత డాష్‌బోర్డ్",
        "griev_tab": "ఫిర్యాదు & భద్రత",
        "att_tab": "హాజరు & పేస్లిప్",
        "rights_tab": "హక్కుల సహాయకుడు",
        "today_shift": "నేటి షిఫ్ట్ స్థితి",
        "checked_in": "🟢 హాజరు నమోదైంది",
        "days_worked": "పనిచేసిన రోజులు",
        "safe_ot_rem": "మిగిలిన సురక్షిత ఓవర్‌టైమ్",
        "ot_cap_note": "పరిమితి: 20 గంటలు/నెల",
        "leave_bal": "జీతంతో కూడిన సెలవు",
        "notices_title": "వ్యక్తిగత నోటీసులు & హెచ్చరికలు",
        "my_submissions": "నా ఇటీవలి ఫిర్యాదులు",
        "submit_report_title": "సమస్యను లేదా అభిప్రాయాన్ని తెలపండి",
        "identity_mode": "గుర్తింపు మోడ్:",
        "anon_opt": "🔒 100% అనామక (గోప్యంగా ఉంటుంది)",
        "id_opt": "🆔 నా వర్కర్ ఐడితో",
        "report_cat": "ఫిర్యాదు వర్గం:",
        "dept_loc": "విభాగం లేదా ప్రాంతం:",
        "desc_issue": "వివరాలను రాయండి (తెలుగులో రాయవచ్చు):",
        "mark_urgent": "అత్యవసరమైనదిగా గుర్తించండి",
        "submit_griev_btn": "🔒 ఫిర్యాదును సమర్పించండి",
        "recent_facility_reports": "ఇటీవలి నివేదికలు",
        "voice_rec_title": "🎙️ వాయిస్ ద్వారా ఫిర్యాదు (వాయిస్-టు-టెక్స్ట్):",
        "voice_rec_prompt": "మీ వాయిస్‌తో ఫిర్యాదు చేయడానికి మైక్ నొక్కండి:",
        "transcribe_btn": "✨ వాయిస్‌ని టెక్స్ట్‌గా మార్చండి",
        "voice_success": "✅ వాయిస్ విజయవంతంగా టెక్స్ట్‌గా మార్చబడింది! క్రింద సమీక్షించండి:",
        
        # Attendance & Payslip
        "shift_checkin_title": "షిఫ్ట్ హాజరు నమోదు",
        "scan_qr": "📷 QR కోడ్ స్కాన్",
        "geo_checkin": "🛰️ జియో-ఫెన్స్ చెక్-ఇన్",
        "ot_calc_title": "పని గంటలు & ఓవర్‌టైమ్ భద్రతా లాక్",
        "daily_wage": "రోజువారీ వేతనం (₹):",
        "regular_days_slider": "పనిచేసిన రోజులు:",
        "ot_hours_slider": "ఓవర్‌టైమ్ గంటలు (1.5x వేతనం):",
        "ot_lock_title": "🛑 భద్రతా లాక్: ఓవర్‌టైమ్ పరిమితి ముగిసింది",
        "ot_lock_desc": "మీరు 20 గంటల భద్రతా పరిమితిని దాటారు. అలసట ప్రమాదాలను నివారించడానికి (SDG 8.8) అదనపు షిఫ్ట్‌లు లాక్ చేయబడ్డాయి.",
        "leave_app_title": "సెలవు దరఖాస్తు",
        "leave_quota_desc": "మొత్తం: 12 రోజులు | ఉపయోగించినవి: 3 | మిగిలినవి: 9 రోజులు",
        "leave_type": "సెలవు రకం:",
        "leave_reason": "కారణం:",
        "submit_leave_btn": "దరఖాస్తు సమర్పించండి",
        "payslip_title": "పారదర్శక పేస్లిప్ వివరాలు",
        "net_salary": "ఖాతాలో జమ అయిన జీతం:",
        "explain_payslip_btn": "✨ తెలుగులో జీతం వివరాలు వినండి",
        
        # Rights Assistant
        "rights_assistant_title": "కార్మికుల హక్కుల AI సహాయకుడు",
        "rights_info_banner": "ℹ️ సమాచార మార్గదర్శకత్వం మాత్రమే: ఇది చట్టపరమైన సలహా కాదు.",
        "faq_q1": "ఈ నెల నా ఓవర్‌టైమ్ జీతం ఎందుకు తక్కువ వచ్చింది?",
        "faq_q2": "జీతం రాకపోతే నేను ఏమి చేయాలి?",
        "faq_q3": "అసురక్షిత పరిస్థితులపై ఎలా ఫిర్యాదు చేయాలి?",
        "faq_q4": "పేస్లిప్‌లోని కోతలు దేనికి సంబంధించినవి?",
        
        # Employer Dashboard
        "employer_title": "FairShift Guardian — కార్యాలయ ప్రమాద & న్యాయ మేధస్సు",
        "guardian_tab": "గార్డియన్ డాష్‌బోర్డ్",
        "audit_tab": "న్యాయమైన ఆడిట్",
        "radar_tab": "ప్రమాద రాడార్",
        "rootcause_tab": "మూల కారణం",
        "intervention_tab": "నివారణ ప్రణాళిక",
        "active_workforce": "సైట్‌లో పనిచేస్తున్న కార్మికులు",
        "payroll_parity": "ఆడిట్ చేయబడిన వేతన రేటు",
        "urgent_flags": "తీవ్రమైన భద్రతా హెచ్చరికలు",
        "active_plans": "క్రియాశీల ప్రణాళికలు",
        "audit_desc": "హాజరును మరియు జీతాలను సరిపోల్చి వ్యత్యాసాలను గుర్తిస్తుంది.",
        "radar_desc": "గ్రాఫ్‌లతో పునరావృత ప్రమాదాలను పర్యవేక్షిస్తుంది.",
        "rootcause_desc": "సమస్యలకు గల మూల కారణాలను అన్వేషిస్తుంది.",
        "intervention_desc": "యాజమాన్యానికి నిర్దిష్ట పరిష్కార ప్రణాళికలను అందిస్తుంది.",
        "create_int_btn": "➕ కొత్త నివారణ ప్రణాళికను సృష్టించండి"
    },
    "bn": {
        "app_title": "FairShift",
        "tagline": "যেখানে প্রতিটি কর্মী গুরুত্বপূর্ণ এবং প্রতিটি কর্মক্ষেত্র আরও ভালো হতে পারে।",
        "sdg_badge": "জাতিসংঘের এসডিজি ৮ • উপযুক্ত কাজ এবং অর্থনৈতিক বৃদ্ধি",
        "login_heading": "FairShift এ সাইন ইন করুন",
        "login_subheading": "আপনার কর্মক্ষেত্রের ভূমিকা নির্বাচন করুন বা ডেমো ক্লিক করুন।",
        "worker_login": "কর্মী পোর্টাল",
        "employer_login": "নিয়োগকর্তা / ব্যবস্থাপনা",
        "workplace_env": "কর্মক্ষেত্রের পরিবেশ:",
        "select_lang": "ভাষা / Language:",
        "worker_id_label": "কর্মী আইডি / ব্যাজ নম্বর:",
        "admin_id_label": "প্রশাসক আইডি:",
        "password_label": "পাসওয়ার্ড / পিন:",
        "login_submit": "লগইন করুন",
        "quick_demo_header": "১-ক্লিক ডেমো লগইন (বিচারকদের জন্য):",
        "demo_worker_btn": "👷 ১-ক্লিক কর্মী ডেমো",
        "demo_employer_btn": "🏢 ১-ক্লিক অ্যাডমিন ডেমো",
        "logout_btn": "🚪 লগআউট",
        "switch_facility": "কর্মক্ষেত্র পরিবর্তন:",
        "emergency_btn": "🚨 জরুরি বিপদের রিপোর্ট করুন",
        "emergency_box_title": "⚠️ তাৎক্ষণিক বিপদ ও জরুরি সতর্কতা চ্যানেল",
        "emergency_box_sub": "কেবলমাত্র জীবন সংশয়ের মতো সক্রিয় বিপদের ক্ষেত্রে এটি ব্যবহার করুন।",
        "emergency_notice": "⚠️ জরুরি সতর্কতা: এটি সাইটের নিরাপত্তা দলকে অবহিত করে। এটি সরকারি জরুরি নম্বরে স্বয়ংক্রিয়ভাবে ফোন করে না। প্রয়োজনে ১১২ / ১০০ এ কল করুন।",
        "hazard_category": "১. বিপদের শ্রেণি:",
        "hazard_loc": "২. নির্দিষ্ট স্থান বা এলাকা:",
        "hazard_desc": "৩. বিপদের সংক্ষিপ্ত বিবরণ:",
        "hazard_evidence": "৪. প্রমাণ (ছবি / অডিও):",
        "hazard_submit": "🚨 জরুরি সতর্কতা পাঠান",
        "designated_contacts": "সাইটের জরুরি যোগাযোগের নম্বর",
        "safety_lead": "নিরাপত্তা প্রধান:",
        "first_aid": "প্রাথমিক চিকিৎসা কেন্দ্র:",
        "assembly_pt": "জরুরি সমবেত হওয়ার স্থান:",
        "external_emergency": "সরকারি জরুরি নম্বর:",
        
        # Worker Portal
        "worker_portal_title": "কর্মী স্ব-সেবা পোর্টাল",
        "dash_tab": "ব্যক্তিগত ড্যাশবোর্ড",
        "griev_tab": "অভিযোগ ও নিরাপত্তা",
        "att_tab": "উপস্থিতি ও বেতন রশিদ",
        "rights_tab": "অধিকার সহকারী",
        "today_shift": "আজকের শিফট অবস্থা",
        "checked_in": "🟢 উপস্থিতি নথিভুক্ত",
        "days_worked": "মোট কাজের দিন",
        "safe_ot_rem": "নিরাপদ ওভারটাইম বাকি",
        "ot_cap_note": "সীমা: ২০ ঘণ্টা/মাস",
        "leave_bal": "বেতনসহ ছুটি বাকি",
        "notices_title": "ব্যক্তিগত নোটিশ ও নিরাপত্তা বার্তা",
        "my_submissions": "আমার সাম্প্রতিক রিপোর্ট",
        "submit_report_title": "অভিযোগ বা মতামত জানান",
        "identity_mode": "পরিচয় মোড:",
        "anon_opt": "🔒 ১০০% গোপনীয় (নাম প্রকাশ হবে না)",
        "id_opt": "🆔 আমার কর্মী আইডি সহ",
        "report_cat": "রিপোর্টের ধরন:",
        "dept_loc": "বিভাগ বা এলাকা:",
        "desc_issue": "বিস্তারিত লিখুন (বাংলায় লিখতে পারেন):",
        "mark_urgent": "জরুরি হিসেবে চিহ্নিত করুন",
        "submit_griev_btn": "🔒 অভিযোগ জমা দিন",
        "recent_facility_reports": "সাম্প্রতিক রিপোর্টসমূহ",
        "voice_rec_title": "🎙️ ভয়েস রেকর্ড করে অভিযোগ জানান (ভয়েস-টু-টেক্সট):",
        "voice_rec_prompt": "আপনার ভাষায় অভিযোগ রেকর্ড করতে নিচে মাইক বাটনে ট্যাপ করুন:",
        "transcribe_btn": "✨ ভয়েসকে লেখায় রূপান্তর করুন",
        "voice_success": "✅ ভয়েস লেখায় রূপান্তরিত হয়েছে! নিচে যাচাই করুন:",
        
        # Attendance & Payslip
        "shift_checkin_title": "শিফট চেক-ইন",
        "scan_qr": "📷 কিউআর স্ক্যান",
        "geo_checkin": "🛰️ অবস্থান যাচাই",
        "ot_calc_title": "কাজের সময় ও ওভারটাইম নিরাপত্তা লক",
        "daily_wage": "দৈনিক মজুরি (₹):",
        "regular_days_slider": "কাজের দিন সংখ্যা:",
        "ot_hours_slider": "ওভারটাইম ঘণ্টা (১.৫ গুণ হার):",
        "ot_lock_title": "🛑 নিরাপত্তা লক: ওভারটাইম সীমা সমাপ্ত",
        "ot_lock_desc": "আপনি ২০ ঘণ্টার নিরাপদ ওভারটাইম সীমা পার করেছেন। ক্লান্তি ও দুর্ঘটনা রোধে (SDG 8.8) পরবর্তী শিফট লক করা হয়েছে।",
        "leave_app_title": "বেতনসহ ছুটির আবেদন",
        "leave_quota_desc": "মোট: ১২ দিন | ব্যবহৃত: ৩ দিন | অবশিষ্ট: ৯ দিন",
        "leave_type": "ছুটির ধরন:",
        "leave_reason": "কারণ:",
        "submit_leave_btn": "ছুটির আবেদন জমা দিন",
        "payslip_title": "স্বচ্ছ পে-স্লিপের হিসাব",
        "net_salary": "ব্যাংকে জমা হওয়া বেতন:",
        "explain_payslip_btn": "✨ বাংলায় বেতনের হিসাব বুঝুন",
        
        # Rights Assistant
        "rights_assistant_title": "কর্মী অধিকার এআই সহকারী",
        "rights_info_banner": "ℹ️ সাধারণ নির্দেশিকা: এটি আইনি পরামর্শ নয়।",
        "faq_q1": "এই মাসে আমার ওভারটাইম বেতন কম কেন?",
        "faq_q2": "বেতন না পেলে আমার কী করা উচিত?",
        "faq_q3": "অনিরাপদ কাজের পরিবেশের বিরুদ্ধে কীভাবে রিপোর্ট করব?",
        "faq_q4": "পে-স্লিপের এই কর্তনের অর্থ কী?",
        
        # Employer Dashboard
        "employer_title": "FairShift Guardian — কর্মক্ষেত্রের ঝুঁকি ও ন্যায্যতা বিশ্লেষণ",
        "guardian_tab": "গার্ডিয়ান ড্যাশবোর্ড",
        "audit_tab": "ন্যায্যতা নিরীক্ষা",
        "radar_tab": "ঝুঁকি রাডার",
        "rootcause_tab": "মূল কারণ",
        "intervention_tab": "হস্তক্ষেপ পরিকল্পনাকারী",
        "active_workforce": "মোট কর্মরত কর্মী",
        "payroll_parity": "নিরীক্ষিত বেতন সমতা হার",
        "urgent_flags": "জরুরি নিরাপত্তা সতর্কতা",
        "active_plans": "সক্রিয় পরিকল্পনা",
        "audit_desc": "উপস্থিতি ও বেতনের মিল পরীক্ষা করে হিসাবের অমিল চিহ্নিত করে।",
        "radar_desc": "চার্টের মাধ্যমে বারবার ঘটা বিপদ ও অমীমাংসিত অভিযোগ চিহ্নিত করে।",
        "rootcause_desc": "সমস্যার মূল কারণগুলো খুঁজে বের করতে সহায়তা করে।",
        "intervention_desc": "কর্তৃপক্ষের জন্য বাস্তবসম্মত ও সময়োপযোগী সমাধান পরিকল্পনা তৈরি করে।",
        "create_int_btn": "➕ নতুন সমাধান পরিকল্পনা যোগ করুন"
    }
}

def get_lang_code(lang_str):
    if "हिन्दी" in lang_str: return "hi"
    if "தமிழ்" in lang_str: return "ta"
    if "తెలుగు" in lang_str: return "te"
    if "বাংলা" in lang_str: return "bn"
    return "en"

def t(key, lang="en"):
    code = get_lang_code(lang) if isinstance(lang, str) else "en"
    return TRANSLATIONS.get(code, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))

# ---------------------------------------------------------------------------------------------
# PERSISTENCE DATA LAYER (JSON Store)
# ---------------------------------------------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), "fairshift_data.json")

def load_persistent_data():
    default_data = {
        "tickets": [
            {
                "id": "TICK-201",
                "industry": "🏗️ Construction Site",
                "type": "Faulty Machinery / Unsafe Equipment",
                "sub_type": "Tower Crane B",
                "reporter_mode": "Anonymous",
                "content": "Crane hoist wire on Tower Crane B has visible fraying near the drum. Operator reported intermittent slip during load lifting.",
                "urgency": "🔴 Critical",
                "status": "In Progress",
                "department": "Heavy Machinery & Equipment",
                "remediation": "Immediate suspension of Crane B; mechanical tension testing scheduled.",
                "timestamp": "Today, 08:30"
            },
            {
                "id": "TICK-202",
                "industry": "🏗️ Construction Site",
                "type": "Women Safety & Harassment Prevention",
                "sub_type": "Night Shift Security",
                "reporter_mode": "Anonymous",
                "content": "Sanitation pathway from Sector 3 staff quarters to gate has no functioning lights. Female masonry helpers feel unsafe during night rotations.",
                "urgency": "🔴 Critical",
                "status": "Pending Review",
                "department": "Site Security & Electrical",
                "remediation": "Install dual LED solar floodlights along Sector 3 walkway; assign dedicated security guard.",
                "timestamp": "Yesterday, 19:15"
            },
            {
                "id": "TICK-203",
                "industry": "🏗️ Construction Site",
                "type": "Supervisor / Management Misconduct",
                "sub_type": "Overtime Intimidation",
                "reporter_mode": "Remote with Worker ID (Shielded)",
                "content": "Subcontractor Kumar threatening to deduct half-day pay if workers refuse back-to-back double shifts on Sunday.",
                "urgency": "🟡 Medium",
                "status": "Under Investigation",
                "department": "HR & Labor Relations",
                "remediation": "HR formal warning issued to subcontractor; shift sign-up transferred to automated app.",
                "timestamp": "2 days ago"
            },
            {
                "id": "TICK-204",
                "industry": "🎓 College Campus",
                "type": "Faulty Machinery / Unsafe Equipment",
                "sub_type": "Lab Exhaust Motor",
                "reporter_mode": "Anonymous",
                "content": "Acid fume hood exhaust motor in Chemistry Lab 204 burned out. Lab assistants experiencing eye irritation during chemical disposal.",
                "urgency": "🔴 Critical",
                "status": "In Progress",
                "department": "Campus Facilities & Engineering",
                "remediation": "Fume hood locked out; replacement industrial blower motor dispatched.",
                "timestamp": "Today, 09:10"
            },
            {
                "id": "TICK-205",
                "industry": "🎓 College Campus",
                "type": "Women Safety & Harassment Prevention",
                "sub_type": "Campus Sanitation Quarters",
                "reporter_mode": "Anonymous",
                "content": "Female housekeeping staff locker room lock is broken for two weeks. Unauthorized contractors have entered the changing area.",
                "urgency": "🔴 Critical",
                "status": "Pending Review",
                "department": "Campus Security & Estate Office",
                "remediation": "Replace deadbolt lock with RFID badge reader immediately; review security patrol log.",
                "timestamp": "Yesterday"
            },
            {
                "id": "TICK-206",
                "industry": "🎓 College Campus",
                "type": "Supervisor / Management Misconduct",
                "sub_type": "Delayed Stipend Disbursal",
                "reporter_mode": "Remote with Worker ID",
                "content": "Third-party gardening contractor withheld 10 days of October wages claiming college finance department has not cleared invoices.",
                "urgency": "🟡 Medium",
                "status": "Under Investigation",
                "department": "Finance & Contract Compliance",
                "remediation": "Direct contractor audit scheduled; verified that university cleared all agency dues on Oct 1st.",
                "timestamp": "3 days ago"
            }
        ],
        "emergency_reports": [
            {
                "id": "EMERG-901",
                "industry": "🏗️ Construction Site",
                "hazard_category": "Structural Collapse / Fall Hazard",
                "location": "Metro Pillar 14B - 4th Level Scaffolding",
                "description": "Cross-brace pins dislodged after high wind gust. Scaffolding platform swaying visibly with 3 workers on top.",
                "timestamp": "2026-10-27 07:15",
                "status": "Emergency Team Dispatched",
                "evidence": "Reported via mobile hazard trigger"
            }
        ],
        "interventions": [
            {
                "id": "INT-301",
                "industry": "🏗️ Construction Site",
                "problem": "Repeated Scaffolding Sway & Vibration Alerts",
                "evidence": "3 hazard reports filed in 48 hours for Tower B (TICK-201, EMERG-901). Vibration sensors registered 4.2mm lateral shift during crane passes.",
                "action": "Halt upper-deck concrete pumping. Inspect vertical jacks, replace sheared locking pins, and retorque clamping bolts.",
                "department": "Site Structural Safety",
                "target_date": "2026-10-29",
                "status": "Action In Progress",
                "resolved": "No - In Progress",
                "resolution_notes": "Structural inspection team deployed at 09:00. Tower B scaffolding isolated."
            },
            {
                "id": "INT-302",
                "industry": "🏗️ Construction Site",
                "problem": "Discrepancy: Biometric vs. Payroll Overtime in Batch 3",
                "evidence": "Biometric gate turnstile recorded 18.5 overtime hours for 24 night-shift workers. Payroll register only credited 12.0 hours (Shortfall: 6.5 hrs = ₹731/worker).",
                "action": "Reconcile gate turnstile punch logs with daily foreman sheet. Issue supplementary payroll credit in mid-month payroll cycle.",
                "department": "Payroll & HR Operations",
                "target_date": "2026-10-31",
                "status": "Completed & Verified",
                "resolved": "Yes - Resolved",
                "resolution_notes": "Foreman timecards reconciled against biometric logs. ₹17,544 supplementary disbursement processed on Oct 26."
            },
            {
                "id": "INT-303",
                "industry": "🎓 College Campus",
                "problem": "Fume Hood Ventilation Failure in Chemistry Lab 204",
                "evidence": "2 safety reports from lab assistants citing respiratory irritation (TICK-204). Exhaust airflow measured at 18 CFM (OSHA standard minimum is 80 CFM).",
                "action": "Replace defective exhaust belt drive motor and certify air exchange velocity with chemical smoke pencil test.",
                "department": "Campus Facilities & Engineering",
                "target_date": "2026-10-28",
                "status": "Action In Progress",
                "resolved": "No - In Progress",
                "resolution_notes": "Lab sealed for active chemical experiments until certified by safety officer."
            },
            {
                "id": "INT-304",
                "industry": "🎓 College Campus",
                "problem": "Locker Room Security Gap for Female Sanitation Staff",
                "evidence": "Formal incident report (TICK-205). Unlocked door reported near North Block basement changing room.",
                "action": "Install heavy-duty RFID electronic card lock and post security guard check every 2 hours.",
                "department": "Estate & Campus Security",
                "target_date": "2026-10-28",
                "status": "Completed & Verified",
                "resolved": "Yes - Resolved",
                "resolution_notes": "Digital RFID keypad installed on Oct 27. Access restricted strictly to verified sanitation personnel."
            }
        ],
        "leave_requests": [
            {
                "id": "LV-501",
                "worker_id": "WRK-8821",
                "type": "Paid Sick Leave",
                "dates": "2026-10-28 to 2026-10-29 (2 Days)",
                "reason": "Doctor appointment for respiratory health checkup",
                "status": "✅ Approved"
            },
            {
                "id": "LV-502",
                "worker_id": "WRK-8821",
                "type": "Casual Paid Leave",
                "dates": "2026-11-04 (1 Day)",
                "reason": "Family obligation & personal paperwork",
                "status": "⏳ Pending HR Review"
            }
        ]
    }
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
        return default_data
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_data

def save_persistent_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error persisting data: {str(e)}")

# Initialize session state from persistent JSON store
if "store" not in st.session_state:
    st.session_state.store = load_persistent_data()

# Session State for Authentication & Navigation
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if "active_nav_tab" not in st.session_state:
    st.session_state.active_nav_tab = "dashboard"

if "global_language" not in st.session_state:
    st.session_state.global_language = "English"

# ---------------------------------------------------------------------------------------------
# SAGE GREEN & BEIGE CSS (Clean Layout, No Login Box Border, Crisp Black Text)
# ---------------------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background-color: #F4F1EA;
        color: #111111;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #111111 !important;
    }

    /* Top Brand Banner - No Emoji, New Tagline */
    .fairshift-banner {
        background: linear-gradient(135deg, #4A5D4B 0%, #354436 100%);
        padding: 1.2rem 1.6rem;
        border-radius: 12px;
        color: #FAF9F6 !important;
        margin-bottom: 1rem;
        box-shadow: 0 4px 14px rgba(53, 68, 54, 0.12);
        border: 1px solid #354436;
    }
    .fairshift-banner h1 {
        color: #FAF9F6 !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .fairshift-banner p {
        color: #E2EBDD !important;
        margin: 0.25rem 0 0 0;
        font-size: 1.05rem;
        font-weight: 500;
    }

    /* User Profile Bar */
    .user-profile-bar {
        background-color: #EAE5DB;
        border: 1px solid #D5CEBF;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }

    /* Cards in Warm Beige with Crisp Black Text */
    .card-beige {
        background-color: #FAF9F6;
        border: 1px solid #D5CEBF;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    .card-beige-accent {
        background-color: #FAF9F6;
        border-left: 5px solid #4D624E;
        border-top: 1px solid #D5CEBF;
        border-right: 1px solid #D5CEBF;
        border-bottom: 1px solid #D5CEBF;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .card-urgent {
        background-color: #FFF5F5;
        border-left: 5px solid #C53030;
        border-top: 1px solid #F5C6CB;
        border-right: 1px solid #F5C6CB;
        border-bottom: 1px solid #F5C6CB;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .card-warning {
        background-color: #FFFDF0;
        border-left: 5px solid #B7791F;
        border-top: 1px solid #F6E05E;
        border-right: 1px solid #F6E05E;
        border-bottom: 1px solid #F6E05E;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .card-resolved {
        background-color: #F0FFF4;
        border-left: 5px solid #2F855A;
        border-top: 1px solid #C6F6D5;
        border-right: 1px solid #C6F6D5;
        border-bottom: 1px solid #C6F6D5;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }

    /* Badges */
    .badge-sage {
        background-color: #E2EBDD;
        color: #2D3E2E !important;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.82rem;
        border: 1px solid #C5D6BF;
        display: inline-block;
    }
    .badge-urgent {
        background-color: #FED7D7;
        color: #9B2C2C !important;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.82rem;
        border: 1px solid #FEB2B2;
        display: inline-block;
    }
    .badge-warning {
        background-color: #FEEBC8;
        color: #7B341E !important;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.82rem;
        border: 1px solid #FBD38D;
        display: inline-block;
    }

    /* CLEAN LOGIN PORTAL - RECTANGLE BOX COMPLETELY REMOVED */
    .clean-login-container {
        max-width: 620px;
        margin: 0.5rem auto 2rem auto;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0.5rem !important;
        box-shadow: none !important;
    }

    /* Bottom Taskbar Navigation Dock */
    .bottom-dock {
        background-color: #EAE5DB;
        border: 2px solid #4D624E;
        border-radius: 14px;
        padding: 0.7rem 1.2rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.04);
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    /* Fatigue Lock Banner */
    .fatigue-lock-box {
        background-color: #FFF5F5;
        border: 2px dashed #C53030;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================================
# SCREEN 1: INTERACTIVE LOGIN (BORDERLESS / NO RECTANGLE BOX)
# =============================================================================================
if st.session_state.auth_user is None:
    current_lang = st.session_state.global_language

    # Top Language Bar for Login Screen
    top_l1, top_l2 = st.columns([3, 1])
    with top_l2:
        new_login_lang = st.selectbox(
            t("select_lang", current_lang),
            options=["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)"],
            index=["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)"].index(current_lang) if current_lang in ["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)"] else 0,
            key="login_lang_picker"
        )
        if new_login_lang != current_lang:
            st.session_state.global_language = new_login_lang
            st.rerun()

    # Clean Header - No emoji next to FairShift, New Tagline
    st.markdown(f"""
    <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 1.5rem;">
        <span class="badge-sage" style="font-size: 0.95rem;">{t("sdg_badge", current_lang)}</span>
        <h1 style="font-size: 3.2rem; margin: 0.3rem 0; color: #354436 !important; font-weight: 800; letter-spacing: -1px;">FairShift</h1>
        <p style="font-size: 1.2rem; color: #333333 !important; max-width: 650px; margin: 0 auto; font-weight: 500;">
            {t("tagline", current_lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Clean borderless container (Rectangle box removed!)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])

    with col_l2:
        st.markdown('<div class="clean-login-container">', unsafe_allow_html=True)
        st.markdown(f"### {t('login_heading', current_lang)}")
        st.caption(t("login_subheading", current_lang))

        role_selection = st.radio(
            "Select Role:",
            options=[t("worker_login", current_lang), t("employer_login", current_lang)],
            horizontal=True
        )

        login_industry = st.selectbox(
            t("workplace_env", current_lang),
            options=["🏗️ Construction Site", "🎓 College Campus"],
            index=0
        )

        with st.form("clean_login_form"):
            if role_selection == t("worker_login", current_lang):
                user_id_input = st.text_input(t("worker_id_label", current_lang), value="WRK-8821")
                password_input = st.text_input(t("password_label", current_lang), value="worker123", type="password")
            else:
                user_id_input = st.text_input(t("admin_id_label", current_lang), value="EMP-ADMIN")
                password_input = st.text_input(t("password_label", current_lang), value="admin123", type="password")

            login_btn = st.form_submit_button(t("login_submit", current_lang), use_container_width=True, type="primary")

            if login_btn:
                role_key = "worker" if role_selection == t("worker_login", current_lang) else "employer"
                name_key = "Ramesh Kumar (Scaffolding & Rigger)" if role_key == "worker" else "Rajesh Varma (Site Safety & Operations)"
                st.session_state.auth_user = {
                    "role": role_key,
                    "id": user_id_input,
                    "name": name_key,
                    "industry": login_industry,
                    "language": current_lang
                }
                st.session_state.active_nav_tab = "dashboard"
                st.rerun()

        st.divider()
        st.markdown(f"##### {t('quick_demo_header', current_lang)}")
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            if st.button(t("demo_worker_btn", current_lang), use_container_width=True):
                st.session_state.auth_user = {
                    "role": "worker",
                    "id": "WRK-8821",
                    "name": "Ramesh Kumar (Mason & Rigger)",
                    "industry": login_industry,
                    "language": current_lang
                }
                st.session_state.active_nav_tab = "dashboard"
                st.rerun()
        with demo_col2:
            if st.button(t("demo_employer_btn", current_lang), use_container_width=True):
                st.session_state.auth_user = {
                    "role": "employer",
                    "id": "EMP-ADMIN",
                    "name": "Rajesh Varma (Site Safety Lead)",
                    "industry": login_industry,
                    "language": current_lang
                }
                st.session_state.active_nav_tab = "dashboard"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================================
# SCREEN 2: AUTHENTICATED PORTAL WITH DYNAMIC TRANSLATION ACROSS ENTIRE PAGE
# =============================================================================================
else:
    user = st.session_state.auth_user
    selected_industry = user["industry"]
    user_lang = user["language"]

    # Top Brand Banner - No emoji next to FairShift, Exact Requested Tagline
    st.markdown(f"""
    <div class="fairshift-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1>FairShift</h1>
                <p>{t('tagline', user_lang)}</p>
            </div>
            <div style="text-align: right;">
                <span class="badge-sage">{selected_industry}</span><br>
                <small style="color: #E2EBDD;"><b>{user['name']}</b> ({user['id']})</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Global Controls Row (Language Switcher, Facility Switcher, Logout)
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1.2, 1])
    with ctrl_col1:
        new_ind = st.selectbox(
            t("switch_facility", user_lang),
            ["🏗️ Construction Site", "🎓 College Campus"],
            index=0 if "Construction" in selected_industry else 1,
            key="ind_switcher_auth"
        )
        if new_ind != selected_industry:
            st.session_state.auth_user["industry"] = new_ind
            st.rerun()
    with ctrl_col2:
        new_lang = st.selectbox(
            t("select_lang", user_lang),
            ["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)"],
            index=["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)"].index(user_lang) if user_lang in ["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "বাংলা (Bengali)"] else 0,
            key="lang_switcher_auth"
        )
        if new_lang != user_lang:
            st.session_state.auth_user["language"] = new_lang
            st.session_state.global_language = new_lang
            st.rerun()
    with ctrl_col3:
        st.write("")
        if st.button(t("logout_btn", user_lang), use_container_width=True):
            st.session_state.auth_user = None
            st.session_state.active_nav_tab = "dashboard"
            st.rerun()

    # -----------------------------------------------------------------------------------------
    # 1. ONE-TAP EMERGENCY SAFETY REPORTING (PROMINENT AT TOP)
    # -----------------------------------------------------------------------------------------
    emergency_contacts = {
        "🏗️ Construction Site": {
            "officer": "Rajesh Varma (Site Safety Lead): +91 98765-43210",
            "station": "Gate 2 Medical First Aid Station & Ambulance Bay",
            "evacuation": "Assembly Zone Alpha (Open ground near Main Batching Plant)",
            "national_emergency": "National Emergency Hotline: 112 | Fire: 101 | Ambulance: 102"
        },
        "🎓 College Campus": {
            "officer": "Dr. Sarah Khan (Campus Environmental Safety): +91 98765-11223",
            "station": "Health Center (Ground Floor, Student Activity Block)",
            "evacuation": "Central Quadrangle Lawn (Assembly Point B)",
            "national_emergency": "National Emergency Hotline: 112 | Campus Security Desk: Ext 404"
        }
    }

    with st.expander(t("emergency_btn", user_lang), expanded=False):
        st.warning(t("emergency_notice", user_lang))

        col_e1, col_e2 = st.columns([1, 1])
        with col_e1:
            st.markdown(f"#### {t('emergency_box_title', user_lang)}")
            em_category = st.selectbox(
                t("hazard_category", user_lang),
                options=[
                    "Structural Collapse / Scaffolding Sway Risk",
                    "Fire, Electrical Spark or High-Voltage Hazard",
                    "Toxic Chemical, Acid or Gas Leakage",
                    "Heavy Machinery Entanglement / Brake Failure",
                    "Physical Violence, Threat or Severe Harassment",
                    "Other Life-Threatening Condition"
                ]
            )
            em_location = st.text_input(t("hazard_loc", user_lang), placeholder="e.g. Tower B - 4th Floor Scaffolding")
            em_description = st.text_area(t("hazard_desc", user_lang), placeholder="Describe what is failing and who is at risk...")
            em_evidence = st.file_uploader(t("hazard_evidence", user_lang), type=["jpg", "png", "mp3", "wav", "txt"])

            if st.button(t("hazard_submit", user_lang), type="primary", use_container_width=True):
                if em_location.strip() and em_description.strip():
                    new_em_id = f"EMERG-{len(st.session_state.store['emergency_reports']) + 902}"
                    new_entry = {
                        "id": new_em_id,
                        "industry": selected_industry,
                        "hazard_category": em_category,
                        "location": em_location,
                        "description": em_description,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "🚨 Emergency Alert Active",
                        "evidence": em_evidence.name if em_evidence else "Direct worker mobile trigger"
                    }
                    st.session_state.store["emergency_reports"].insert(0, new_entry)
                    auto_intervention = {
                        "id": f"INT-{len(st.session_state.store['interventions']) + 305}",
                        "industry": selected_industry,
                        "problem": f"URGENT: {em_category} at {em_location}",
                        "evidence": f"Immediate Danger Trigger #{new_em_id}: '{em_description}'",
                        "action": "Immediate site evacuation of hazard zone; safety supervisor inspection within 15 minutes.",
                        "department": "Emergency Safety Response",
                        "target_date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Action In Progress",
                        "resolved": "No - In Progress",
                        "resolution_notes": f"Emergency ticket generated automatically from {new_em_id}."
                    }
                    st.session_state.store["interventions"].insert(0, auto_intervention)
                    save_persistent_data(st.session_state.store)
                    st.error(f"🚨 **EMERGENCY REPORT #{new_em_id} DISPATCHED TO ON-SITE SAFETY DESK!**")
                else:
                    st.warning("Please provide location and description.")
        with col_e2:
            st.markdown(f"#### 📞 {t('designated_contacts', user_lang)} ({selected_industry})")
            contacts = emergency_contacts[selected_industry]
            st.markdown(f"""
            <div class="card-beige-accent">
                <b>🛡️ {t('safety_lead', user_lang)}</b><br>{contacts['officer']}<br><br>
                <b>🏥 {t('first_aid', user_lang)}</b><br>{contacts['station']}<br><br>
                <b>🏃 {t('assembly_pt', user_lang)}</b><br>{contacts['evacuation']}<br><br>
                <b>🚨 {t('external_emergency', user_lang)}</b><br><b>{contacts['national_emergency']}</b>
            </div>
            """, unsafe_allow_html=True)


    # =========================================================================================
    # A. WORKER PORTAL VIEW
    # =========================================================================================
    if user["role"] == "worker":

        # --- 1. PERSONAL DASHBOARD ---
        if st.session_state.active_nav_tab == "dashboard":
            st.markdown(f"### 🏠 {t('dash_tab', user_lang)}")

            d1, d2, d3, d4 = st.columns(4)
            with d1:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('today_shift', user_lang)}</small>
                    <h3 style="margin: 0.2rem 0; color: #2E6F40 !important;">{t('checked_in', user_lang)}</h3>
                    <small>Shift: 08:00 AM - 05:00 PM</small>
                </div>
                """, unsafe_allow_html=True)
            with d2:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('days_worked', user_lang)}</small>
                    <h3 style="margin: 0.2rem 0;">22 Days</h3>
                    <small>Accrued Base: ₹16,500</small>
                </div>
                """, unsafe_allow_html=True)
            with d3:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('safe_ot_rem', user_lang)}</small>
                    <h3 style="margin: 0.2rem 0; color: #4D624E !important;">4 Hours Left</h3>
                    <span class="badge-sage">{t('ot_cap_note', user_lang)}</span>
                </div>
                """, unsafe_allow_html=True)
            with d4:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('leave_bal', user_lang)}</small>
                    <h3 style="margin: 0.2rem 0; color: #2E6F40 !important;">9 Days</h3>
                    <small>1 Request Pending Review</small>
                </div>
                """, unsafe_allow_html=True)

            col_p1, col_p2 = st.columns([1.2, 1])
            with col_p1:
                st.markdown(f"#### 📢 {t('notices_title', user_lang)}")
                st.markdown(f"""
                <div class="card-beige-accent">
                    <b>🛡️ Safety Mandate:</b> Helmets and steel-toed boots required in all active crane zones.<br>
                    <b>💰 Upcoming Pay Date:</b> Monthly salary disbursement cycle initiates on the 30th.<br>
                    <b>🏖️ Leave Balance:</b> 9 paid leave days remaining for the calendar year.
                </div>
                """, unsafe_allow_html=True)

            with col_p2:
                st.markdown(f"#### 🎫 {t('my_submissions', user_lang)}")
                user_tickets = [t_item for t_item in st.session_state.store["tickets"] if "8821" in t_item.get("reporter_mode", "") or "Anonymous" in t_item.get("reporter_mode", "")]
                if user_tickets:
                    for ut in user_tickets[:2]:
                        st.markdown(f"""
                        <div class="card-beige" style="padding: 0.8rem 1rem;">
                            <b>Ticket #{ut['id']}:</b> {ut['type']}<br>
                            <small>Status: <b>{ut['status']}</b> | {ut['timestamp']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No active tickets submitted yet.")

        # --- 2. GRIEVANCE & SAFETY ---
        elif st.session_state.active_nav_tab == "grievance":
            st.markdown(f"### 🚨 {t('griev_tab', user_lang)}")

            col_g1, col_g2 = st.columns([1, 1])
            with col_g1:
                st.markdown(f"##### 📝 {t('submit_report_title', user_lang)}")
                reporting_identity = st.radio(
                    t("identity_mode", user_lang),
                    [t("anon_opt", user_lang), t("id_opt", user_lang)]
                )
                report_category = st.selectbox(
                    t("report_cat", user_lang),
                    [
                        "👩 Women Safety & Harassment Prevention",
                        "👔 Supervisor / Management Misconduct",
                        "⚙️ Faulty Machinery / Unsafe Equipment",
                        "🏗️ General Workplace Hazard / Unhygienic Facilities",
                        "💰 Unpaid Wages / Overtime Discrepancy",
                        "💬 Constructive Feedback on Workplace Policies"
                    ]
                )
                specific_area = st.text_input(t("dept_loc", user_lang), placeholder="e.g. Night Shift Gate 2, Chemistry Lab 204")
                
                # 🎙️ VOICE-TO-TEXT INPUT SECTION
                st.markdown(f"###### {t('voice_rec_title', user_lang)}")
                st.caption(t('voice_rec_prompt', user_lang))
                recorded_voice = st.audio_input(t('voice_rec_prompt', user_lang), key="worker_voice_input")

                if "worker_transcription" not in st.session_state:
                    st.session_state.worker_transcription = ""

                if recorded_voice is not None:
                    st.audio(recorded_voice)
                    if st.button(t("transcribe_btn", user_lang), key="btn_transcribe_voice", use_container_width=True):
                        with st.spinner("AI is analyzing voice recording & converting to text..."):
                            audio_bytes = recorded_voice.read()
                            api_key_env = os.getenv("GEMINI_API_KEY", "")
                            if api_key_env:
                                try:
                                    from google import genai
                                    from google.genai import types
                                    client = genai.Client(api_key=api_key_env)
                                    resp = client.models.generate_content(
                                        model="gemini-2.5-flash",
                                        contents=[
                                            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                                            "You are FairShift's multilingual voice-to-text workplace transcriber. Listen to this recording and transcribe it into clear text. If spoken in Hindi, Tamil, Telugu, or Bengali, provide the transcription and translation so the worker's issue is clearly explained."
                                        ]
                                    )
                                    st.session_state.worker_transcription = resp.text
                                except Exception as e:
                                    st.session_state.worker_transcription = f"Audio Note: Worker reported a safety and overtime issue ({str(e)})"
                            else:
                                st.session_state.worker_transcription = "Audio Note (Transcribed): Scaffold sway reported on 4th floor; supervisor notified of uncounted night shift overtime."
                            st.success(t("voice_success", user_lang))

                initial_text = st.session_state.get("worker_transcription", "")
                report_details = st.text_area(t("desc_issue", user_lang), value=initial_text, height=130)
                is_urgent = st.checkbox(t("mark_urgent", user_lang), value=False)
                uploaded_evidence = st.file_uploader(t("hazard_evidence", user_lang), type=["png", "jpg", "mp3", "pdf", "txt"], key="griev_proof_dock")

                if st.button(t("submit_griev_btn", user_lang), type="primary", use_container_width=True):
                    if report_details.strip():
                        new_tick_id = f"TICK-{len(st.session_state.store['tickets']) + 201}"
                        urgency_str = "🔴 Critical" if is_urgent or "Women Safety" in report_category else "🟡 Medium"
                        new_ticket = {
                            "id": new_tick_id,
                            "industry": selected_industry,
                            "type": report_category,
                            "sub_type": specific_area if specific_area else "General Site",
                            "reporter_mode": "Anonymous" if reporting_identity == t("anon_opt", user_lang) else "Worker ID: WRK-8821",
                            "content": report_details,
                            "urgency": urgency_str,
                            "status": "Pending Review",
                            "department": "Site Management",
                            "remediation": "Assign compliance officer for impartial site review.",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        st.session_state.store["tickets"].insert(0, new_ticket)
                        save_persistent_data(st.session_state.store)
                        st.success(f"✅ Report filed! Reference tracking ID: **{new_tick_id}**.")
                    else:
                        st.warning("Please provide details.")

            with col_g2:
                st.markdown(f"##### 🔍 {t('recent_facility_reports', user_lang)}")
                ind_tickets = [t_item for t_item in st.session_state.store["tickets"] if t_item["industry"] == selected_industry]
                for t_item in ind_tickets[:3]:
                    card_class = "card-urgent" if "Critical" in t_item["urgency"] else "card-warning"
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; justify-content: space-between;">
                            <b>Ticket #{t_item['id']} • {t_item['type']}</b>
                            <span class="badge-sage">{t_item['status']}</span>
                        </div>
                        <small>Location: <b>{t_item.get('sub_type', 'General')}</b> | Mode: {t_item.get('reporter_mode', 'Anonymous')}</small>
                        <p style="margin: 0.3rem 0;"><i>"{t_item['content']}"</i></p>
                        <small><b>Remediation:</b> {t_item.get('remediation', 'Under review')}</small>
                    </div>
                    """, unsafe_allow_html=True)

        # --- 3. ATTENDANCE & PAYSLIP ---
        elif st.session_state.active_nav_tab == "attendance":
            st.markdown(f"### ⏱️ {t('att_tab', user_lang)}")

            subcol1, subcol2 = st.columns([1, 1])
            with subcol1:
                st.markdown(f"##### 📍 {t('shift_checkin_title', user_lang)}")
                geo_col1, geo_col2 = st.columns(2)
                with geo_col1:
                    if st.button(t("scan_qr", user_lang), use_container_width=True):
                        st.success("✅ QR Code Verified: Turnstile Gate 2 logged at 08:00 AM")
                with geo_col2:
                    if st.button(t("geo_checkin", user_lang), use_container_width=True):
                        st.success("✅ Geo-Location Confirmed: Zone 3 logged at 08:30 AM")

                st.divider()
                st.markdown(f"##### ⏱️ {t('ot_calc_title', user_lang)}")
                daily_wage_rate = st.number_input(t("daily_wage", user_lang), min_value=300, max_value=4000, value=750, step=50)
                regular_days = st.slider(t("regular_days_slider", user_lang), min_value=0, max_value=28, value=22)
                MAX_OVERTIME_CAP = 20
                overtime_hours = st.slider(t("ot_hours_slider", user_lang), min_value=0, max_value=35, value=16)

                is_overtime_capped = overtime_hours >= MAX_OVERTIME_CAP
                if is_overtime_capped:
                    st.markdown(f"""
                    <div class="fatigue-lock-box">
                        <h4 style="color: #9B2C2C !important; margin: 0;">{t('ot_lock_title', user_lang)}</h4>
                        <p style="margin: 0.3rem 0; color: #782323 !important;">
                            {t('ot_lock_desc', user_lang)}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.button("🚫 Locked Due to Overtime Limit", disabled=True, use_container_width=True)
                else:
                    st.success(f"🟢 **Safe Threshold:** {MAX_OVERTIME_CAP - overtime_hours} safe overtime hours remaining.")

                st.divider()
                st.markdown(f"##### 🏖️ {t('leave_app_title', user_lang)}")
                st.caption(t("leave_quota_desc", user_lang))

                with st.form("leave_form_trans"):
                    lv_type = st.selectbox(t("leave_type", user_lang), ["Paid Sick Leave", "Casual Paid Leave", "Emergency Family Leave"])
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        start_date = st.date_input("Start Date:", value=date.today())
                    with col_d2:
                        end_date = st.date_input("End Date:", value=date.today())
                    lv_reason = st.text_input(t("leave_reason", user_lang), placeholder="e.g. Medical appointment")
                    submit_leave = st.form_submit_button(t("submit_leave_btn", user_lang))

                    if submit_leave:
                        if lv_reason.strip():
                            new_lv_entry = {
                                "id": f"LV-{len(st.session_state.store['leave_requests']) + 501}",
                                "worker_id": "WRK-8821",
                                "type": lv_type,
                                "dates": f"{start_date} to {end_date}",
                                "reason": lv_reason,
                                "status": "⏳ Pending HR Review"
                            }
                            st.session_state.store["leave_requests"].insert(0, new_lv_entry)
                            save_persistent_data(st.session_state.store)
                            st.success(f"✅ Leave application submitted! ID: {new_lv_entry['id']}.")

            with subcol2:
                st.markdown(f"##### 💵 {t('payslip_title', user_lang)}")
                hourly_rate = daily_wage_rate / 8.0
                regular_pay = regular_days * daily_wage_rate
                credited_ot_hours = min(overtime_hours, MAX_OVERTIME_CAP) if is_overtime_capped else overtime_hours
                ot_rate = hourly_rate * 1.5
                ot_pay = credited_ot_hours * ot_rate
                paid_leave_credit = 1 * daily_wage_rate
                total_deductions = 750
                net_take_home = regular_pay + ot_pay + paid_leave_credit - total_deductions

                st.markdown(f"""
                <div class="card-beige-accent">
                    <div style="display: flex; justify-content: space-between;">
                        <h3 style="margin: 0;">{t('net_salary', user_lang)} ₹{net_take_home:,.0f}</h3>
                        <span class="badge-sage">Bank Transfer</span>
                    </div>
                    <hr style="margin: 0.6rem 0; border: none; border-top: 1px solid #D5CEBF;">
                    <table style="width: 100%; font-size: 0.95rem;">
                        <tr><td>• Base Days ({regular_days} days):</td><td style="text-align: right; font-weight: 600;">₹{regular_pay:,.0f}</td></tr>
                        <tr><td>• Overtime Pay ({credited_ot_hours} hrs @ 1.5x):</td><td style="text-align: right; font-weight: 600;">₹{ot_pay:,.0f}</td></tr>
                        <tr><td>• Paid Leave Credit:</td><td style="text-align: right; font-weight: 600;">₹{paid_leave_credit:,.0f}</td></tr>
                        <tr><td style="color: #9B2C2C;">• Deductions (Canteen/Uniform):</td><td style="text-align: right; color: #9B2C2C;">-₹{total_deductions:,.0f}</td></tr>
                        <tr style="border-top: 1px solid #C4BCAC;"><td style="font-weight: 700;">Total Take-Home Pay:</td><td style="text-align: right; font-weight: 700; color: #2E6F40;">₹{net_take_home:,.0f}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                if st.button(t("explain_payslip_btn", user_lang), use_container_width=True):
                    if "हिन्दी" in user_lang:
                        st.info(f"**नमस्ते साथी!** आपका इस महीने का शुद्ध वेतन **₹{net_take_home:,.0f}** है। आपने {regular_days} दिन काम किया और {credited_ot_hours} घंटे अतिरिक्त काम किया। प्रत्येक घंटे का हिसाब सुरक्षित दर्ज है।")
                    elif "தமிழ்" in user_lang:
                        st.info(f"**வணக்கம்!** இந்த மாத உங்கள் சம்பளம் **₹{net_take_home:,.0f}**. நீங்கள் {regular_days} நாட்கள் வேலை செய்துள்ளீர்கள் மற்றும் {credited_ot_hours} கூடுதல் நேரம் பதிவு செய்யப்பட்டுள்ளது.")
                    elif "తెలుగు" in user_lang:
                        st.info(f"**నమస్కారం!** ఈ నెల మీ జీతం **₹{net_take_home:,.0f}**. మీరు {regular_days} రోజులు పనిచేశారు మరియు {credited_ot_hours} గంటల ఓవర్‌టైమ్ నమోదు చేయబడింది.")
                    elif "বাংলা" in user_lang:
                        st.info(f"**নমস্কার!** এই মাসে আপনার মোট বেতন **₹{net_take_home:,.0f}**। আপনি {regular_days} দিন কাজ করেছেন এবং {credited_ot_hours} ঘণ্টা ওভারটাইম যুক্ত হয়েছে।")
                    else:
                        st.info(f"**Salary Breakdown:** You worked **{regular_days} standard days** and clocked **{credited_ot_hours} overtime hours**. Total credited to bank: **₹{net_take_home:,.0f}**.")

        # --- 4. RIGHTS ASSISTANT ---
        elif st.session_state.active_nav_tab == "assistant":
            st.markdown(f"### 🤖 {t('rights_assistant_title', user_lang)}")
            st.info(t("rights_info_banner", user_lang))

            CURATED_FAQS = {
                t("faq_q1", user_lang): {
                    "explanation": "Overtime pay varies based on verified biometric hours beyond 8 hours and whether you reached the monthly safety overtime limit (20 hours). Statutory overtime is credited at 1.5x your regular rate.",
                    "next_step": "1. Check your biometric gate punch times.\n2. Confirm deductions.\n3. File a wage reconciliation ticket if hours are missing."
                },
                t("faq_q2", user_lang): {
                    "explanation": "Under standard labor guidelines (SDG 8.5), salaries must be cleared within 7 to 10 days of the month-end. Subcontractor delays or bank account IFSC errors are the most common causes.",
                    "next_step": "1. Verify registered bank account details with HR.\n2. Inquire with site supervisor for batch disbursement reference.\n3. If unpaid after the 10th, file a wage dispute report."
                },
                t("faq_q3", user_lang): {
                    "explanation": "You have a protected right to safe working conditions under SDG 8.8. Unsafe scaffolding, toxic lab fumes, or faulty machinery must be reported immediately without fear of retaliation.",
                    "next_step": "1. For immediate danger, use the top red Emergency Report button.\n2. For recurring hazards, submit an Anonymous Grievance report with photos.\n3. Never operate machinery without safety guards."
                },
                t("faq_q4", user_lang): {
                    "explanation": "Authorized deductions typically cover canteen subsidies, uniform advances, or statutory social security (PF/ESI). Employers cannot deduct arbitrary amounts without written notification.",
                    "next_step": "1. Compare your deduction against your initial enrollment agreement.\n2. Check if a uniform advance was deducted more than once.\n3. Request a line-item deduction breakdown from payroll."
                }
            }

            col_q1, col_q2 = st.columns([1, 1])
            with col_q1:
                selected_q = st.radio("Select a Common Question:", list(CURATED_FAQS.keys()))
            with col_q2:
                faq_data = CURATED_FAQS[selected_q]
                st.markdown(f"""
                <div class="card-beige-accent">
                    <h4>{selected_q}</h4>
                    <p>{faq_data['explanation']}</p>
                    <b>⚡ Next Steps:</b>
                    <p style="white-space: pre-line;">{faq_data['next_step']}</p>
                </div>
                """, unsafe_allow_html=True)

        # --- WORKER BOTTOM TASKBAR DOCK (TRANSLATED!) ---
        st.markdown('<div class="bottom-dock">', unsafe_allow_html=True)
        tb_col1, tb_col2, tb_col3, tb_col4 = st.columns(4)
        with tb_col1:
            if st.button(f"🏠 {t('dash_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "dashboard" else "secondary"):
                st.session_state.active_nav_tab = "dashboard"
                st.rerun()
        with tb_col2:
            if st.button(f"🚨 {t('griev_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "grievance" else "secondary"):
                st.session_state.active_nav_tab = "grievance"
                st.rerun()
        with tb_col3:
            if st.button(f"⏱️ {t('att_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "attendance" else "secondary"):
                st.session_state.active_nav_tab = "attendance"
                st.rerun()
        with tb_col4:
            if st.button(f"🤖 {t('rights_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "assistant" else "secondary"):
                st.session_state.active_nav_tab = "assistant"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


    # =========================================================================================
    # B. EMPLOYER / ADMIN PORTAL VIEW (TRANSLATED!)
    # =========================================================================================
    else:
        active_tickets = st.session_state.store["tickets"]
        ind_tickets = [t_item for t_item in active_tickets if t_item["industry"] == selected_industry]
        urgent_count = len([t_item for t_item in ind_tickets if "Critical" in t_item["urgency"]])
        active_interventions = [i for i in st.session_state.store["interventions"] if i["industry"] == selected_industry]
        open_interventions = len([i for i in active_interventions if i["status"] != "Completed & Verified"])

        # --- 1. EMPLOYER EXECUTIVE DASHBOARD ---
        if st.session_state.active_nav_tab == "dashboard":
            st.markdown(f"### 🏢 {t('employer_title', user_lang)}")

            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('active_workforce', user_lang)}</small>
                    <h2 style="margin: 0.2rem 0;">{"1,240" if "Construction" in selected_industry else "430"}</h2>
                    <span class="badge-sage">Biometric Verified</span>
                </div>
                """, unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('payroll_parity', user_lang)}</small>
                    <h2 style="margin: 0.2rem 0; color: #2E6F40 !important;">97.8%</h2>
                    <span class="badge-sage">2 Items Flagged</span>
                </div>
                """, unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('urgent_flags', user_lang)}</small>
                    <h2 style="margin: 0.2rem 0; color: #C53030 !important;">{urgent_count}</h2>
                    <span class="badge-urgent">Action Required</span>
                </div>
                """, unsafe_allow_html=True)
            with k4:
                st.markdown(f"""
                <div class="card-beige">
                    <small>{t('active_plans', user_lang)}</small>
                    <h2 style="margin: 0.2rem 0; color: #B7791F !important;">{open_interventions} Active</h2>
                    <span class="badge-warning">{len(active_interventions) - open_interventions} Resolved</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### ⚡ Priority Actions Required")
            for act in active_interventions[:2]:
                st.markdown(f"""
                <div class="card-warning">
                    <b>{act['problem']}</b> — Assigned to <b>{act['department']}</b> (Target: {act['target_date']})<br>
                    <small>Evidence: {act['evidence'][:100]}...</small>
                </div>
                """, unsafe_allow_html=True)

        # --- 2. FAIRNESS AUDIT ---
        elif st.session_state.active_nav_tab == "audit":
            st.markdown(f"### 📊 {t('audit_tab', user_lang)}")
            st.write(t("audit_desc", user_lang))

            audit_discrepancies = [
                {
                    "id": "AUD-881",
                    "department": "Night Shift Rigging Crew (Batch 3)",
                    "category": "Overtime Reconciliation Discrepancy",
                    "biometric_evidence": "Gate 2 turnstile registered 18.5 overtime hours across 24 workers.",
                    "ledger_record": "Payroll register logged only 12.0 hours. Difference: 6.5 uncredited hours.",
                    "financial_impact": "₹731 estimated variance per worker (Total ₹17,544 batch variance)",
                    "calculation_proof": "Calculated: (18.5 hrs - 12.0 hrs) × (₹750/8 × 1.5) = 6.5 hrs × ₹140.6 = ₹914 gross variance - taxes = ₹731 net",
                    "status": "Audit Pending Review"
                },
                {
                    "id": "AUD-882",
                    "department": "Sector 3 Cleaning & Ground Maintenance",
                    "category": "Duplicate Tool / Uniform Deduction",
                    "biometric_evidence": "Batch records show ₹350 uniform safety advance deducted in both Sept and Oct payroll runs.",
                    "ledger_record": "Single uniform issue recorded on Sept 14th; second deduction appears unlinked to asset issuance.",
                    "financial_impact": "₹350 surplus deduction across 14 workers (Total ₹4,900)",
                    "calculation_proof": "Ledger Transaction ID #DED-884 duplicated under Batch #DED-899",
                    "status": "Reconciliation Underway"
                }
            ]

            for aud in audit_discrepancies:
                st.markdown(f"""
                <div class="card-warning">
                    <div style="display: flex; justify-content: space-between;">
                        <b>Audit Flag #{aud['id']} • {aud['department']}</b>
                        <span class="badge-warning">{aud['status']}</span>
                    </div>
                    <p style="margin: 0.3rem 0; font-weight: 600; color: #7B341E !important;">Issue: {aud['category']}</p>
                    <div style="background: rgba(0,0,0,0.03); padding: 0.6rem 0.8rem; border-radius: 6px;">
                        • <b>Biometric Evidence:</b> {aud['biometric_evidence']}<br>
                        • <b>Ledger Record:</b> {aud['ledger_record']}<br>
                        • <b>Mathematical Proof:</b> <code>{aud['calculation_proof']}</code><br>
                        • <b>Impact:</b> <b>{aud['financial_impact']}</b>
                    </div>
                    <small style="color: #666;">Flagged for internal reconciliation. Does not establish legal non-compliance.</small>
                </div>
                """, unsafe_allow_html=True)

        # --- 3. RISK RADAR ---
        elif st.session_state.active_nav_tab == "radar":
            st.markdown(f"### 📡 {t('radar_tab', user_lang)}")
            st.write(t("radar_desc", user_lang))

            col_r1, col_r2 = st.columns([1, 1])
            with col_r1:
                cat_counts = {}
                for t_item in ind_tickets:
                    c = t_item["type"].split(" ", 1)[-1]
                    cat_counts[c] = cat_counts.get(c, 0) + 1
                if not cat_counts:
                    cat_counts = {"Faulty Machinery": 2, "Women Safety": 2, "Wage Discrepancy": 1, "General Hazard": 1}

                df_cat = pd.DataFrame([{"Category": k, "Reports": v} for k, v in cat_counts.items()])
                chart = alt.Chart(df_cat).mark_arc(innerRadius=45).encode(
                    theta=alt.Theta(field="Reports", type="quantitative"),
                    color=alt.Color(field="Category", type="nominal", scale=alt.Scale(
                        range=["#4D624E", "#859883", "#C53030", "#B7791F", "#354436"]
                    )),
                    tooltip=["Category", "Reports"]
                ).properties(height=260)
                st.altair_chart(chart, use_container_width=True)

            with col_r2:
                dept_risk_data = pd.DataFrame({
                    "Department": ["Heavy Machinery", "Scaffolding Zone", "Night Facilities", "Lab Chemicals", "Sanitation"],
                    "Risk Index (0-100)": [78, 85, 62, 70, 45]
                })
                bar_chart = alt.Chart(dept_risk_data).mark_bar(color="#5F7161", cornerRadius=4).encode(
                    x=alt.X("Risk Index (0-100):Q", scale=alt.Scale(domain=[0, 100])),
                    y=alt.Y("Department:N", sort="-x"),
                    tooltip=["Department", "Risk Index (0-100)"]
                ).properties(height=260)
                st.altair_chart(bar_chart, use_container_width=True)

        # --- 4. ROOT-CAUSE INSIGHTS ---
        elif st.session_state.active_nav_tab == "rootcause":
            st.markdown(f"### 🔍 {t('rootcause_tab', user_lang)}")
            st.write(t("rootcause_desc", user_lang))

            groupings = [
                {
                    "group_name": "Cluster A: Elevated Scaffolding & Heavy Rigging Safety",
                    "count": "3 Related Reports (Tower B & Pillar 14B)",
                    "common_factor": "Occurs specifically during high-wind intervals when the concrete hoist crane is operating at full swing.",
                    "investigation_step": "1. Review crane operator radius limits.\n2. Verify torque ratings on vertical scaffolding clamp bolts.\n3. Implement wind-speed anemometer cutoff at 25 knots."
                },
                {
                    "group_name": "Cluster B: Night Shift Welfare & Illumination Gaps",
                    "count": "2 Related Reports (Sector 3 & Quarters Walkway)",
                    "common_factor": "Temporary floodlight cables were severed during trench excavation, leaving women's quarters walkway unlit for 14 days.",
                    "investigation_step": "1. Replace wired line with independent solar LED floodlight poles.\n2. Establish dedicated security escort patrol between 19:00 and 06:00."
                }
            ]

            for g in groupings:
                st.markdown(f"""
                <div class="card-beige-accent">
                    <div style="display: flex; justify-content: space-between;">
                        <h4 style="margin: 0;">{g['group_name']}</h4>
                        <span class="badge-sage">{g['count']}</span>
                    </div>
                    <p style="margin: 0.3rem 0;">• <b>Root Cause:</b> {g['common_factor']}</p>
                    <b>Recommended Protocol:</b>
                    <p style="white-space: pre-line; margin: 0.2rem 0;">{g['investigation_step']}</p>
                </div>
                """, unsafe_allow_html=True)

        # --- 5. INTERVENTION ACTION CENTRE ---
        elif st.session_state.active_nav_tab == "intervention":
            st.markdown(f"### 🎯 {t('intervention_tab', user_lang)}")
            st.write(t("intervention_desc", user_lang))

            with st.expander(t("create_int_btn", user_lang), expanded=False):
                with st.form("new_intervention_form_dock"):
                    int_problem = st.text_input("Problem Requiring Attention:", placeholder="e.g. Scaffolding sway on 4th floor Tower B")
                    int_evidence = st.text_area("Supporting Evidence & Alert Basis:", placeholder="e.g. 3 worker tickets, biometric gap of 6.5 hours...")
                    int_action = st.text_area("Recommended Remediation Action:", placeholder="e.g. Inspect bolts, retorque clamps...")
                    col_i1, col_i2 = st.columns(2)
                    with col_i1:
                        int_dept = st.selectbox("Responsible Department:", ["Site Structural Safety", "Payroll & HR Operations", "Campus Facilities & Engineering", "Estate & Campus Security", "Occupational Health"])
                    with col_i2:
                        int_deadline = st.date_input("Target Review Date:", value=date.today())

                    submit_int = st.form_submit_button("Create and Assign Intervention Plan")

                    if submit_int:
                        if int_problem.strip() and int_action.strip():
                            new_plan_id = f"INT-{len(st.session_state.store['interventions']) + 301}"
                            new_plan = {
                                "id": new_plan_id,
                                "industry": selected_industry,
                                "problem": int_problem,
                                "evidence": int_evidence if int_evidence else "Direct manager creation",
                                "action": int_action,
                                "department": int_dept,
                                "target_date": str(int_deadline),
                                "status": "Pending Review",
                                "resolved": "No - In Progress",
                                "resolution_notes": "Intervention opened and assigned."
                            }
                            st.session_state.store["interventions"].insert(0, new_plan)
                            save_persistent_data(st.session_state.store)
                            st.success(f"✅ Intervention plan **{new_plan_id}** created and assigned to **{int_dept}**!")
                        else:
                            st.warning("Please specify both problem and action.")

            st.markdown("##### 📋 Active Intervention Action Items")
            ind_interventions = [i for i in st.session_state.store["interventions"] if i.get("industry") == selected_industry]
            for idx, plan in enumerate(ind_interventions):
                status_color = "card-resolved" if plan["status"] == "Completed & Verified" else ("card-urgent" if plan["status"] == "Pending Review" else "card-warning")
                st.markdown(f"""
                <div class="{status_color}">
                    <div style="display: flex; justify-content: space-between;">
                        <h4 style="margin: 0;">Plan #{plan['id']}: {plan['problem']}</h4>
                        <span class="badge-sage">{plan['department']}</span>
                    </div>
                    <hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #D5CEBF;">
                    <p style="margin: 0.2rem 0;">• <b>Evidence:</b> {plan['evidence']}</p>
                    <p style="margin: 0.2rem 0;">• <b>Action:</b> {plan['action']}</p>
                    <p style="margin: 0.2rem 0;">• <b>Target Review Date:</b> <b>{plan['target_date']}</b> | Status: <b>{plan['status']}</b></p>
                    <p style="margin: 0.2rem 0;">• <b>Resolution Notes:</b> <i>{plan.get('resolution_notes', 'Pending review')}</i></p>
                </div>
                """, unsafe_allow_html=True)

                col_u1, col_u2, col_u3 = st.columns([1.5, 2, 1])
                with col_u1:
                    updated_status = st.selectbox(
                        f"Update Status #{plan['id']}:",
                        options=["Pending Review", "Action In Progress", "Completed & Verified"],
                        index=["Pending Review", "Action In Progress", "Completed & Verified"].index(plan["status"]) if plan["status"] in ["Pending Review", "Action In Progress", "Completed & Verified"] else 0,
                        key=f"status_sel_{plan['id']}"
                    )
                with col_u2:
                    updated_notes = st.text_input(
                        f"Resolution Notes #{plan['id']}:",
                        value=plan.get("resolution_notes", ""),
                        key=f"notes_{plan['id']}"
                    )
                with col_u3:
                    st.write("")
                    if st.button(f"💾 Save #{plan['id']}", key=f"save_btn_{plan['id']}"):
                        for m_idx, master_plan in enumerate(st.session_state.store["interventions"]):
                            if master_plan["id"] == plan["id"]:
                                st.session_state.store["interventions"][m_idx]["status"] = updated_status
                                st.session_state.store["interventions"][m_idx]["resolution_notes"] = updated_notes
                                st.session_state.store["interventions"][m_idx]["resolved"] = "Yes - Resolved" if updated_status == "Completed & Verified" else "No - In Progress"
                                save_persistent_data(st.session_state.store)
                                st.success(f"Saved Plan #{plan['id']}!")
                                st.rerun()

        # --- EMPLOYER BOTTOM TASKBAR DOCK (TRANSLATED!) ---
        st.markdown('<div class="bottom-dock">', unsafe_allow_html=True)
        eb_col1, eb_col2, eb_col3, eb_col4, eb_col5 = st.columns(5)
        with eb_col1:
            if st.button(f"🏢 {t('guardian_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "dashboard" else "secondary"):
                st.session_state.active_nav_tab = "dashboard"
                st.rerun()
        with eb_col2:
            if st.button(f"📊 {t('audit_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "audit" else "secondary"):
                st.session_state.active_nav_tab = "audit"
                st.rerun()
        with eb_col3:
            if st.button(f"📡 {t('radar_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "radar" else "secondary"):
                st.session_state.active_nav_tab = "radar"
                st.rerun()
        with eb_col4:
            if st.button(f"🔍 {t('rootcause_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "rootcause" else "secondary"):
                st.session_state.active_nav_tab = "rootcause"
                st.rerun()
        with eb_col5:
            if st.button(f"🎯 {t('intervention_tab', user_lang)}", use_container_width=True, type="primary" if st.session_state.active_nav_tab == "intervention" else "secondary"):
                st.session_state.active_nav_tab = "intervention"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------
# TWO-INDUSTRY COMPARISON MATRIX EXPANDER
# ---------------------------------------------------------------------------------------------
st.divider()
with st.expander("📚 Hackathon Requirement: Cross-Industry Deployment Matrix (Construction vs. College)"):
    st.markdown("""
    ### Cross-Industry Adaptability Matrix (UN SDG 8 Decent Work)

    | Operational Dimension | 🏗️ Industry 1: Construction Site (Metro Rail) | 🎓 Industry 2: College Campus (Apex University) |
    |---|---|---|
    | **Workforce Dynamics** | Daily wage riggers, crane operators, concrete masons, bar benders. | Sanitation staff, campus security guards, groundskeepers, lab assistants. |
    | **Wage & Overtime Vulnerability** | Uncredited night overtime, cash subcontractor delays, missing biometric sync. | Semester contract deductions, late stipend dispersals, uniform double-deductions. |
    | **Critical Safety Hazards** | High-elevation scaffolding sway, lack of safety harnesses, crane cables. | Toxic chemical fume hood failures, extreme heatstroke during outdoor groundskeeping. |
    | **Grievance Barriers** | Fear of immediate dismissal, loss of daily cash wage, contractor blacklisting. | Fear of supervisor retaliation or non-renewal of campus semester service contracts. |
    | **FairShift Guardian Impact** | Prevents structural collapse via rapid alerts; automates biometric overtime reconciliation. | Eliminates lab chemical exposure; audits contractor wage compliance with zero worker exposure. |
    """)
