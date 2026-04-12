/* ═══════════════════════════════════════════════
   FarmCare — lang.js
   Bilingual EN/HI translations + applyT()
═══════════════════════════════════════════════ */

const TR = {
  en: {
    /* App shell */
    app_title:    'FarmCare',
    app_subtitle: 'Intelligent Soil Health Monitor',
    dept:         'Soil Health Card Scheme · Govt. of India',

    /* Module page */
    m_scheme:     'Smart Farming Programme',
    m_tagline:    'Choose Your Module',
    m_subtitle:   'Select a module to continue with your farming needs',
    m_subtitle_hi:'',
    m_divider:    'Select module / मॉड्यूल चुनें',
    m_soil_badge: 'SOIL MONITORING',
    m_soil_title: 'Soil Health Monitoring',
    m_soil_desc:  'Live sensor readings, AI soil analysis, weather forecasts, fertilizer recommendations and more.',
    m_soil_f1:    'Live sensor data from Raspberry Pi',
    m_soil_f2:    'AI soil type & crop recommendations',
    m_soil_f3:    'Weather, Mandi prices & Health Card PDF',
    m_dis_badge:  'CROP DISEASE AI',
    m_dis_title:  'Crop Disease Detection',
    m_dis_desc:   'Upload a photo of your crop — AI identifies the disease, its cause, and provides treatment solutions.',
    m_dis_f1:     'Detects 38 diseases across 14 crops',
    m_dis_f2:     'Cause, symptoms & treatment plans',
    m_dis_f3:     'Prevention tips & severity assessment',

    /* Setup page */
    connect_title: 'Enter your Pi details below',
    connect_desc:  "Enter your Pi's local IP address and port to begin real-time soil health monitoring. Your data never leaves your private network.",
    pi_ip_label:   'Raspberry Pi IP Address',
    port_label:    'Port',
    connect_btn:   '📡 Connect & Start Monitoring',
    demo_btn:      '⚡ Demo Mode — No Pi Needed',
    info1: 'Local network only — your data stays on your Pi',
    info2: 'Real-time sensor readings every 2.5 seconds',
    info3: 'Live weather + 10-day forecast included',
    info4: 'Generate official Soil Health Card PDF',
    info5: 'AI soil type + fertilizer recommendations',
    info6: 'Live mandi prices from AGMARKNET',

    /* Soil app tabs */
    tab_dashboard:   'Dashboard',
    tab_weather:     'Weather',
    tab_soil:        'Soil AI',
    tab_crops:       'Crop Optimizer',
    tab_fertilizer:  'Fertilizer',
    tab_mandi:       'Mandi Prices',
    tab_datalog:     'Data Log',
    tab_pdf:         'Health Card',

    /* Disease app */
    da_subtitle: 'Crop Disease Detection',
    da_dept:     'AI Plant Health · Govt. of India',
  },

  hi: {
    /* App shell */
    app_title:    'फार्मकेयर',
    app_subtitle: 'बुद्धिमान मृदा स्वास्थ्य मॉनिटर',
    dept:         'मृदा स्वास्थ्य कार्ड योजना · भारत सरकार',

    /* Module page */
    m_scheme:     'स्मार्ट कृषि कार्यक्रम',
    m_tagline:    'अपना मॉड्यूल चुनें',
    m_subtitle:   'अपनी कृषि आवश्यकता के अनुसार मॉड्यूल चुनें',
    m_subtitle_hi:'',
    m_divider:    'मॉड्यूल चुनें / Select module',
    m_soil_badge: 'मृदा निगरानी',
    m_soil_title: 'मृदा स्वास्थ्य निगरानी',
    m_soil_desc:  'लाइव सेंसर रीडिंग, AI मृदा विश्लेषण, मौसम पूर्वानुमान और उर्वरक सुझाव।',
    m_soil_f1:    'Raspberry Pi से लाइव सेंसर डेटा',
    m_soil_f2:    'AI मृदा प्रकार और फसल अनुशंसाएँ',
    m_soil_f3:    'मौसम, मंडी मूल्य और स्वास्थ्य कार्ड PDF',
    m_dis_badge:  'फसल रोग AI',
    m_dis_title:  'फसल रोग पहचान',
    m_dis_desc:   'फसल की फोटो अपलोड करें — AI रोग, उसका कारण और उपचार बताएगा।',
    m_dis_f1:     '14 फसलों की 38 बीमारियों की पहचान',
    m_dis_f2:     'कारण, लक्षण और उपचार योजना',
    m_dis_f3:     'रोकथाम के सुझाव और गंभीरता आकलन',

    /* Setup page */
    connect_title: 'अपना Pi विवरण नीचे दर्ज करें',
    connect_desc:  'रियल-टाइम मृदा स्वास्थ्य निगरानी शुरू करने के लिए Pi का IP पता और पोर्ट दर्ज करें।',
    pi_ip_label:   'Raspberry Pi IP पता',
    port_label:    'पोर्ट',
    connect_btn:   '📡 कनेक्ट करें और निगरानी शुरू करें',
    demo_btn:      '⚡ डेमो मोड — Pi की जरूरत नहीं',
    info1: 'केवल स्थानीय नेटवर्क — डेटा Pi पर रहता है',
    info2: 'हर 2.5 सेकंड में रियल-टाइम सेंसर रीडिंग',
    info3: 'लाइव मौसम + 10 दिन का पूर्वानुमान शामिल',
    info4: 'आधिकारिक मृदा स्वास्थ्य कार्ड PDF बनाएं',
    info5: 'AI मृदा प्रकार + उर्वरक अनुशंसाएँ',
    info6: 'AGMARKNET से लाइव मंडी मूल्य',

    /* Soil app tabs */
    tab_dashboard:   'डैशबोर्ड',
    tab_weather:     'मौसम',
    tab_soil:        'मृदा AI',
    tab_crops:       'फसल अनुकूलन',
    tab_fertilizer:  'उर्वरक',
    tab_mandi:       'मंडी मूल्य',
    tab_datalog:     'डेटा लॉग',
    tab_pdf:         'स्वास्थ्य कार्ड',

    /* Disease app */
    da_subtitle: 'फसल रोग पहचान',
    da_dept:     'AI पादप स्वास्थ्य · भारत सरकार',
  }
};

function t(k) {
  return (TR[FC.lang] || TR.en)[k] || (TR.en)[k] || k;
}

function applyT() {
  /* Map: element-id → translation-key */
  const MAP = {
    /* Setup */
    S_subtitle:      'app_subtitle',
    S_connect_title: 'connect_title',
    S_connect_desc:  'connect_desc',
    S_pi_ip_label:   'pi_ip_label',
    S_port_label:    'port_label',
    S_connect_btn:   'connect_btn',
    S_demo_btn:      'demo_btn',
    S_info1: 'info1', S_info2: 'info2',
    S_info3: 'info3', S_info4: 'info4',
    S_info5: 'info5', S_info6: 'info6',

    /* Module page */
    M_scheme_label: 'm_scheme',
    M_tagline:      'm_tagline',
    M_subtitle:     'm_subtitle',
    M_divider:      'm_divider',
    M_soil_badge:   'm_soil_badge',
    M_soil_title:   'm_soil_title',
    M_soil_desc:    'm_soil_desc',
    M_soil_f1:      'm_soil_f1',
    M_soil_f2:      'm_soil_f2',
    M_soil_f3:      'm_soil_f3',
    M_dis_badge:    'm_dis_badge',
    M_dis_title:    'm_dis_title',
    M_dis_desc:     'm_dis_desc',
    M_dis_f1:       'm_dis_f1',
    M_dis_f2:       'm_dis_f2',
    M_dis_f3:       'm_dis_f3',

    /* Soil app header */
    A_title:    'app_title',
    A_subtitle: 'app_subtitle',
    A_dept:     'dept',

    /* Soil app tabs */
    T_dashboard:  'tab_dashboard',
    T_weather:    'tab_weather',
    T_soil:       'tab_soil',
    T_crops:      'tab_crops',
    T_fertilizer: 'tab_fertilizer',
    T_mandi:      'tab_mandi',
    T_datalog:    'tab_datalog',
    T_pdf:        'tab_pdf',

    /* Disease app */
    DA_subtitle: 'da_subtitle',
    DA_dept:     'da_dept',
  };

  Object.entries(MAP).forEach(([id, key]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = t(key);
  });

  /* Language labels */
  const lbl = FC.lang.toUpperCase();
  ['langLabel', 'langLabel2', 'langLabel3'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = lbl;
  });

  /* Push lang change into iframes */
  FC.broadcastLang(FC.lang);

  /* Also push into disease iframe specifically */
  try {
    const df = document.getElementById('if-crop-disease');
    if (df && df.contentWindow && df.contentWindow.onLangChange) {
      df.contentWindow.onLangChange(FC.lang);
    }
  } catch(e) {}
}

function toggleLang() {
  FC.lang = FC.lang === 'en' ? 'hi' : 'en';
  applyT();
}
