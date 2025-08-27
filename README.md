
# Indo–Lanka Power Grid Linkages: Evaluating Technical and Economic Impact

## 📌 Project Overview

This project investigates the feasibility of an **India–Sri Lanka power grid interconnection** through a High Voltage Direct Current (HVDC) link. The study evaluates **technical, operational, and economic impacts** of the link using **economic dispatch modelling, market analysis, and cost assessments**.

The interconnection aims to:

* Reduce Sri Lanka’s reliance on expensive fossil fuel generation.
* Enable **low-cost electricity imports** from India.
* Enhance **grid stability, energy security, and regional cooperation**.
* Support Sri Lanka’s transition toward a **renewable-dominated power system**.



## 🔬 Methodology

1. **Interconnection Availability** – Analyzed Indian Energy Exchange (IEX) real-time market data to determine power availability and probability of unavailability.
2. **Economic Dispatch Model** – Developed in Python using 2024 demand/generation data and monthly hydro budgets. Considered renewable penetration scenarios (45%–80%).
3. **Cost Calculations** – Incorporated link unavailability probabilities, backup plant costs, and unit prices to derive realistic system costs.
4. **Scenario Analysis** – Modeled multiple cases:

   * Scenario 1: 350 MW renewables with 500 MW link.
   * Scenario 4: 70% renewables by 2030 with 500 MW link.
   * (Other scenarios cover 45%–80% renewables and 1000 MW links).



## 📊 Key Findings

* **Cost Savings:**

  * At low renewable penetration, the link **fully displaces 500 MW thermal power**, cutting system costs.
  * At high renewable penetration (≥70%), link utilization falls but still provides **flexibility during peak demand**.

* **Unavailability Risks:**

  * Evening peak hours (18:00–22:00) in India show high unavailability probabilities (up to 0.9).
  * Imports are most reliable during **midday and midnight hours**.

* **Impact on Local Plants:**

  * Expensive thermal and some renewable plants may become **less competitive**, risking stranded assets.

* **Strategic Value:**

  * Strengthens **regional power market integration**.
  * Supports **Sri Lanka’s renewable transition**.
  * Requires **policy measures** to protect domestic generators and ensure fair cost distribution.



## ✅ Conclusion

The Indo–Lanka power grid interconnection is **technically feasible and economically beneficial**, especially for reducing thermal reliance and enhancing system reliability. However, its success depends on:

* Addressing **import availability risks**,
* Developing **backup and compensation mechanisms** for affected local plants,
* Aligning with **long-term renewable integration policies**.

If implemented with proper safeguards, the interconnection could deliver **lasting economic, environmental, and regional cooperation benefits**.



## 🚀 Future Work

* Incorporating **plant-specific parameters** (standby costs, ramping, capacity factors).
* Full-scale **IEX dataset analysis** (35,040 intervals/year).
* Estimation of **payback period & Net Present Value (NPV)**.
* Consideration of **transmission losses, geopolitical factors, and advanced scenarios**.

