# ⚖️ FairShift – Workplace Risk & Fairness Intelligence
**Theme:** UN SDG 8 – Decent Work and Economic Growth  
**Design Palette:** Sage Green (`#4D624E`, `#5F7161`) + Warm Beige (`#F4F1EA`, `#FAF9F6`) + Crisp Black Text (`#111111`)

---

## 🌟 Executive Summary

Employee-intensive organisations—such as construction sites, factories, hospitals, and university campuses—face a toxic information gap:
1. **Opaque Wages & Uncounted Overtime:** Workers don't understand how deductions are applied or whether overtime was fairly credited.
2. **Fear of Retaliation:** Workers stay silent on women's safety, harassment, and equipment hazards because they fear losing their jobs.
3. **Reactive Safety:** Management only finds out about structural flaws or toxic fumes after an accident occurs.

**FairShift** bridges this gap by combining accessible, multilingual worker tools with **FairShift Guardian**, a proactive employer intelligence engine that turns alerts into actionable, verifiable intervention plans.

---

## 👷 Worker Self-Service Portal (3 Primary Features + Rights Assistant)

### 1. 🚨 Grievance, Safety & Confidential Reporting
- **Remote or Worker ID:** Workers can file reports 100% anonymously (all device/identity metadata stripped) or with their Worker ID for direct resolution.
- **Comprehensive Scope:** Covers **Women Safety & Harassment Prevention**, **Supervisor / Management Misconduct**, **Faulty Machinery**, and **Workplace Hazards**.
- **Transparent Tracking:** Workers get a private ticket ID and can monitor management's verified remediation actions.

### 2. ⏱️ Attendance, Shift Tracking, Overtime Cap & Paid Leave
- **Interactive Check-In:** Scan on-site QR codes or verify via geo-fence.
- **🛑 Strict Safety Overtime Lock (SDG 8.8):** A mandatory safety threshold (e.g. 20 hours/month) protects workers against chronic exhaustion. **The portal automatically locks shift booking once the cap is reached**, enforcing a mandatory 48-hour recovery interval.
- **Paid Leave Application:** Live quota ledger (accrued, taken, remaining) with instant leave request tracking.
- **Transparent Payslip Breakdown:** Line-item breakdown of base days, 1.5x overtime, paid leave credits, and authorized deductions with plain-language spoken audio/text in **Hindi, Tamil, Telugu, Bengali, and English**.

### 3. 🚨 One-Tap Emergency Safety Reporting
- **Prominent Emergency Danger Button:** High-visibility hazard reporting for immediate life-threatening perils (structural collapse, high-voltage, toxic leaks, violence).
- **Instant Emergency Guidance:** Displays on-site emergency coordinators, first-aid posts, and evacuation assembly zones.
- **Mandatory Clear Disclaimer:** Submitting alerts on-site safety leads, but does not replace municipal emergency services (112 / 100 / 101).

### 4. 🤖 AI Worker Rights Assistant (Very High Priority)
- Curated, reliable workplace guidance for common questions:
  - *"Why is my overtime pay different this month?"*
  - *"What should I do if my salary hasn't been paid?"*
  - *"How do I report an unsafe working condition?"*
  - *"What does this deduction on my payslip mean?"*
- Explains standards in simple language, suggests practical next steps, and **directs the worker to the exact FairShift feature**.
- Clearly labeled as general guidance without legal jargon or invented rights.

---

## 🏢 FairShift Guardian — Employer Intelligence (4 Integrated Modules)

### Module 1: 📊 FAIRNESS AUDIT
- Compares biometric gate attendance, recorded overtime, and payroll ledgers.
- Flags mathematical variances with explicit calculation proof (e.g., *Batch 3 night shift: 18.5 biometric hours vs 12.0 ledger hours = ₹731 variance/worker*).
- Never presumes guilt; flags items for internal operational reconciliation.

### Module 2: 📡 WORKPLACE RISK RADAR
- Computes mathematical risk indicators for recurring hazards (e.g., *3 scaffolding sway reports in 48 hours*).
- **Interactive Visualizations:**
  - **Pie / Donut Chart:** Categorical distribution of grievances (Women safety, machinery, wages, general).
  - **Bar Graph:** Department risk indicator index.

### Module 3: 🔍 ROOT-CAUSE INSIGHTS
- Groups related incidents by department, shift, and physical location to find systemic drivers (e.g., crane vibration during morning high-wind periods).
- Transparent rule-based summaries out of the box, with Gemini synthesis on demand.

### Module 4: 🎯 INTERVENTION ACTION CENTRE (The FairShift Intervention Planner)
*Don't just tell employers what's wrong. Tell them what to do next.*
- For every alert, FairShift tracks:
  1. The problem requiring attention.
  2. The supporting evidence & calculations.
  3. The recommended action.
  4. The responsible department.
  5. The target review date.
  6. The current status (`Pending Review`, `Action In Progress`, `Completed & Verified`).
  7. Resolution notes & verification.
- **Full Interactivity & Persistence:** Employers can create new tasks, reassign departments, change deadlines, and record resolution notes. All updates are saved to `fairshift_data.json` and persist across page reloads.

---

## 🏗️ Cross-Industry Adaptability (Construction vs. College)

| Feature Dimension | 🏗️ Industry 1: Construction Site (Metro Rail) | 🎓 Industry 2: College Campus (Apex University) |
|---|---|---|
| **Workforce Profile** | Daily wage riggers, crane operators, concrete masons. | Janitorial & sanitation staff, campus security, lab assistants. |
| **Wage & Overtime Risk** | Uncredited night overtime, cash subcontractor delays. | Duplicate uniform deductions, late stipend dispersals. |
| **Primary Safety Hazard** | Scaffolding instability, crane hoist slippage, lack of PPE. | Toxic fume hood motor burnout, chemical exposure in labs. |
| **Women's Safety Concern** | Unlit walkway to Sector 3 staff quarters. | Broken lock on sanitation staff changing room. |
| **Intervention Target** | Structural scaffolding re-torque & biometric audit. | Lab fume hood motor replacement & RFID digital keypad lock. |

---

## 🎤 How to Demo This to Hackathon Judges (Step-by-Step)

1. **Show the Theme & Accessibility (30 seconds):**
   - Point out the soothing, accessible **Sage Green + Beige palette with crisp black text**.
   - Switch language to **हिन्दी** or **தமிழ்** and demonstrate the **AI Transparent Payslip Explainer**.

2. **Trigger the Overtime Safety Lock (30 seconds):**
   - Move the overtime slider past **20 hours**.
   - Show how the portal **locks shift booking** to protect worker health under **SDG 8.8**.

3. **Demonstrate One-Tap Emergency Danger (30 seconds):**
   - Click the top red button, submit an emergency report, and highlight the instant on-site emergency contacts and legal disclaimer.

4. **Show the AI Worker Rights Assistant (30 seconds):**
   - Click *"Why is my overtime pay different this month?"* and show how it provides practical next steps and links to the payslip tab.

5. **Switch to FairShift Guardian (Employer Dashboard) (60 seconds):**
   - Show **Fairness Audit** (biometric vs. payroll variance proof).
   - Show **Workplace Risk Radar** (interactive Altair pie chart & bar graph).
   - In the **Intervention Action Centre**, update a task from `Action In Progress` to `Completed & Verified`, add resolution notes, click **Save**, and refresh the browser to prove **100% data persistence**!
