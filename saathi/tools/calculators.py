"""
SAATHI AI - Indian Public Utility & Financial Calculators
Provides transparent, deterministic calculations for:
1. Electricity Slab & Bill Estimator
2. Rental Security Deposit & Deduction Auditor
3. EPFO PF Advance (Form 31) Limit Estimator
"""
from typing import Dict, Any, List, Optional
from saathi.models import ProposedAction

class UtilityCalculators:
    @staticmethod
    def calculate_electricity_bill(
        units_consumed: float,
        sanctioned_load_kw: float = 2.0,
        state: str = "Standard (National Benchmark)",
        is_average_or_idf: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates electricity bill based on state-specific telescopic slab tariffs in India:
        - Delhi (DERC / TPDDL / BRPL): Lifeline 100% subsidy (0-200 units) and ₹800 subsidy (201-400 units).
        - Maharashtra (MSEDCL / Mahavitaran): 0-100 @ ₹3.36, 101-300 @ ₹7.34, 301-500 @ ₹10.37, >500 @ ₹11.86.
        - Uttar Pradesh (UPPCL): 0-100 @ ₹3.35, 101-150 @ ₹3.85, 151-300 @ ₹5.00, >300 @ ₹6.00.
        - Karnataka (BESCOM): Telescopic rates + Gruha Jyothi benefit notes.
        - Standard / National Benchmark: 0-100 @ ₹3.50, 101-200 @ ₹5.00, 201-400 @ ₹6.50, >400 @ ₹8.00.
        """
        st_lower = state.lower()
        slab_breakdown = []
        subsidy_applied = 0.0
        rem_units = units_consumed

        if "delhi" in st_lower:
            fixed_charge = 50.0 * sanctioned_load_kw if sanctioned_load_kw <= 2.0 else 100.0 * sanctioned_load_kw
            energy_charge = 0.0
            
            # Slabs: 0-200 @ 3.00, 201-400 @ 4.50, 401-800 @ 6.50, >800 @ 7.00
            u1 = min(rem_units, 200)
            if u1 > 0:
                c1 = u1 * 3.00
                energy_charge += c1
                slab_breakdown.append(f"0–200 units: {u1:.0f} units @ ₹3.00 = ₹{c1:.2f}")
                rem_units -= u1

            u2 = min(rem_units, 200)
            if u2 > 0:
                c2 = u2 * 4.50
                energy_charge += c2
                slab_breakdown.append(f"201–400 units: {u2:.0f} units @ ₹4.50 = ₹{c2:.2f}")
                rem_units -= u2

            u3 = min(rem_units, 400)
            if u3 > 0:
                c3 = u3 * 6.50
                energy_charge += c3
                slab_breakdown.append(f"401–800 units: {u3:.0f} units @ ₹6.50 = ₹{c3:.2f}")
                rem_units -= u3

            if rem_units > 0:
                c4 = rem_units * 7.00
                energy_charge += c4
                slab_breakdown.append(f">800 units: {rem_units:.0f} units @ ₹7.00 = ₹{c4:.2f}")

            # Delhi Government Subsidy Rules
            if units_consumed <= 200:
                subsidy_applied = energy_charge + fixed_charge
                slab_breakdown.append("🎁 Delhi Lifeline Subsidy (0-200 units): 100% Waiver on Energy & Fixed Charges")
            elif units_consumed <= 400:
                subsidy_applied = 800.0
                slab_breakdown.append("🎁 Delhi Government Subsidy (201-400 units): ₹800 Flat Subsidy Deducted")

            duty = max(0.0, (energy_charge + fixed_charge - subsidy_applied) * 0.05)
            total_bill = max(0.0, fixed_charge + energy_charge + duty - subsidy_applied)

        elif "maharashtra" in st_lower or "msedcl" in st_lower:
            fixed_charge = 128.0 # Standard single-phase domestic monthly fixed charge
            energy_charge = 0.0
            
            u1 = min(rem_units, 100)
            if u1 > 0:
                c1 = u1 * 3.36
                energy_charge += c1
                slab_breakdown.append(f"0–100 units: {u1:.0f} units @ ₹3.36 = ₹{c1:.2f}")
                rem_units -= u1

            u2 = min(rem_units, 200)
            if u2 > 0:
                c2 = u2 * 7.34
                energy_charge += c2
                slab_breakdown.append(f"101–300 units: {u2:.0f} units @ ₹7.34 = ₹{c2:.2f}")
                rem_units -= u2

            u3 = min(rem_units, 200)
            if u3 > 0:
                c3 = u3 * 10.37
                energy_charge += c3
                slab_breakdown.append(f"301–500 units: {u3:.0f} units @ ₹10.37 = ₹{c3:.2f}")
                rem_units -= u3

            if rem_units > 0:
                c4 = rem_units * 11.86
                energy_charge += c4
                slab_breakdown.append(f">500 units: {rem_units:.0f} units @ ₹11.86 = ₹{c4:.2f}")

            duty = (energy_charge + fixed_charge) * 0.16 # Maharashtra Electricity Duty ~16%
            total_bill = fixed_charge + energy_charge + duty

        elif "uttar pradesh" in st_lower or "uppcl" in st_lower:
            fixed_charge = sanctioned_load_kw * 110.0
            energy_charge = 0.0

            u1 = min(rem_units, 100)
            if u1 > 0:
                c1 = u1 * 3.35
                energy_charge += c1
                slab_breakdown.append(f"0–100 units: {u1:.0f} units @ ₹3.35 = ₹{c1:.2f}")
                rem_units -= u1

            u2 = min(rem_units, 50)
            if u2 > 0:
                c2 = u2 * 3.85
                energy_charge += c2
                slab_breakdown.append(f"101–150 units: {u2:.0f} units @ ₹3.85 = ₹{c2:.2f}")
                rem_units -= u2

            u3 = min(rem_units, 150)
            if u3 > 0:
                c3 = u3 * 5.00
                energy_charge += c3
                slab_breakdown.append(f"151–300 units: {u3:.0f} units @ ₹5.00 = ₹{c3:.2f}")
                rem_units -= u3

            if rem_units > 0:
                c4 = rem_units * 6.00
                energy_charge += c4
                slab_breakdown.append(f">300 units: {rem_units:.0f} units @ ₹6.00 = ₹{c4:.2f}")

            duty = (energy_charge + fixed_charge) * 0.05
            total_bill = fixed_charge + energy_charge + duty

        elif "karnataka" in st_lower or "bescom" in st_lower:
            fixed_charge = (1 * 110.0) + (max(0.0, sanctioned_load_kw - 1) * 210.0)
            energy_charge = 0.0

            u1 = min(rem_units, 100)
            if u1 > 0:
                c1 = u1 * 5.90
                energy_charge += c1
                slab_breakdown.append(f"0–100 units: {u1:.0f} units @ ₹5.90 = ₹{c1:.2f}")
                rem_units -= u1

            if rem_units > 0:
                c2 = rem_units * 7.30
                energy_charge += c2
                slab_breakdown.append(f">100 units: {rem_units:.0f} units @ ₹7.30 = ₹{c2:.2f}")

            duty = (energy_charge + fixed_charge) * 0.09
            total_bill = fixed_charge + energy_charge + duty
            if units_consumed <= 200:
                slab_breakdown.append("💡 Note: Eligible Karnataka households registered under 'Gruha Jyothi' receive zero bill up to monthly entitlement.")

        else:
            # Standard National Benchmark
            fixed_charge = sanctioned_load_kw * 75.0
            energy_charge = 0.0
            
            u1 = min(rem_units, 100)
            if u1 > 0:
                c1 = u1 * 3.50
                energy_charge += c1
                slab_breakdown.append(f"0–100 units: {u1:.0f} units @ ₹3.50 = ₹{c1:.2f}")
                rem_units -= u1
                
            u2 = min(rem_units, 100)
            if u2 > 0:
                c2 = u2 * 5.00
                energy_charge += c2
                slab_breakdown.append(f"101–200 units: {u2:.0f} units @ ₹5.00 = ₹{c2:.2f}")
                rem_units -= u2
                
            u3 = min(rem_units, 200)
            if u3 > 0:
                c3 = u3 * 6.50
                energy_charge += c3
                slab_breakdown.append(f"201–400 units: {u3:.0f} units @ ₹6.50 = ₹{c3:.2f}")
                rem_units -= u3
                
            if rem_units > 0:
                c4 = rem_units * 8.00
                energy_charge += c4
                slab_breakdown.append(f"400+ units: {rem_units:.0f} units @ ₹8.00 = ₹{c4:.2f}")
                
            duty = (energy_charge + fixed_charge) * 0.06
            total_bill = fixed_charge + energy_charge + duty

        warning = None
        if is_average_or_idf:
            warning = "⚠️ Note: Your bill is based on provisional/average assessment (IDF). You have the right to request actual meter verification to avoid overcharging."
            
        return {
            "units": units_consumed,
            "sanctioned_load_kw": sanctioned_load_kw,
            "state_discom": state,
            "fixed_charge": round(fixed_charge, 2),
            "energy_charge": round(energy_charge, 2),
            "electricity_duty": round(duty, 2),
            "subsidy_applied": round(subsidy_applied, 2),
            "total_estimated_bill": round(total_bill, 2),
            "slab_breakdown": slab_breakdown,
            "warning": warning
        }

    @staticmethod
    def audit_security_deposit_deduction(
        total_deposit: float,
        monthly_rent: float,
        unpaid_utility_bills: float = 0.0,
        painting_deduction_claimed: float = 0.0,
        structural_damage_claimed: float = 0.0,
        tenure_months: int = 11
    ) -> Dict[str, Any]:
        """
        Audits landlord deductions against Model Tenancy Guidelines:
        - Unpaid utilities: Legally deductible (must provide bill copies).
        - Structural damage: Legally deductible (beyond normal wear-and-tear).
        - Painting / Normal wear: Cannot be deducted unless specifically agreed in writing.
        """
        legitimate_deductions = unpaid_utility_bills + structural_damage_claimed
        disputed_deductions = painting_deduction_claimed
        
        legitimate_refund = total_deposit - legitimate_deductions
        
        advice = []
        if painting_deduction_claimed > 0:
            advice.append("🚫 Normal painting and fading of walls are classified as 'Normal Wear & Tear' under Model Tenancy Act and cannot be unilaterally deducted without express agreement.")
        if unpaid_utility_bills > 0:
            advice.append(f"✅ ₹{unpaid_utility_bills:.2f} for unpaid electricity/water is legitimately deductible upon producing official bill receipts.")
            
        return {
            "total_deposit": total_deposit,
            "legitimate_deductions": legitimate_deductions,
            "disputed_painting_deduction": disputed_deductions,
            "minimum_rightful_refund": max(0.0, round(legitimate_refund, 2)),
            "full_refund_if_painting_disputed": max(0.0, round(total_deposit - unpaid_utility_bills, 2)),
            "advice": advice
        }

    @staticmethod
    def calculate_security_deposit_refund(
        monthly_rent: float,
        deposit_paid: float,
        actual_damages: float = 0.0,
        unpaid_bills: float = 0.0,
        property_type: str = "residential"
    ) -> Dict[str, Any]:
        """
        Calculates legal security deposit limits and allowable deductions under Model Tenancy Act (MTA):
        - Residential max limit: 2 months rent
        - Commercial max limit: 6 months rent
        """
        legal_cap_months = 2 if property_type.lower() == "residential" else 6
        legal_max = monthly_rent * legal_cap_months
        excess_deposit = max(0.0, deposit_paid - legal_max)
        
        allowable_deductions = actual_damages + unpaid_bills
        refundable_amount = max(0.0, deposit_paid - allowable_deductions)
        
        notes = []
        if excess_deposit > 0:
            notes.append(f"⚠️ Excess Deposit: Under Model Tenancy Act, maximum deposit for {property_type} premises is capped at {legal_cap_months} months rent (₹{legal_max:,.2f}). Landlord is holding ₹{excess_deposit:,.2f} in excess.")
        if actual_damages > 0:
            notes.append(f"• Documented structural damage deduction: ₹{actual_damages:,.2f}")
        if unpaid_bills > 0:
            notes.append(f"• Unpaid utility dues deduction: ₹{unpaid_bills:,.2f}")
        notes.append("• Landlord must refund deposit within 30 days of key handover after adjusting lawful dues.")

        return {
            "legal_max_deposit": round(legal_max, 2),
            "excess_held_by_landlord": round(excess_deposit, 2),
            "total_allowable_deductions": round(allowable_deductions, 2),
            "refundable_amount": round(refundable_amount, 2),
            "statutory_deadline_days": 30,
            "notes": notes
        }


    @staticmethod
    def estimate_pf_advance_limit(
        pf_employee_share: float,
        pf_employer_share: float,
        monthly_basic_plus_da: float,
        purpose: str = "illness",
        total_service_years: float = 3.0
    ) -> Dict[str, Any]:
        """
        Estimates maximum allowable PF advance under EPFO Form 31:
        - Illness: Up to 6 months' basic+DA or total employee share (whichever is lower). No minimum service.
        - Marriage: Up to 50% of employee share (Requires 7+ years service).
        - House Purchase/Construction: Up to 36 months basic+DA or total balance (Requires 5+ years service).
        """
        purpose_lower = purpose.lower()
        max_limit = 0.0
        status = "ELIGIBLE"
        notes = []

        if "ill" in purpose_lower or "medical" in purpose_lower:
            # 6 months basic+DA or employee share
            limit_6mo = monthly_basic_plus_da * 6.0
            max_limit = min(limit_6mo, pf_employee_share)
            notes.append("Illness Advance: Available immediately without minimum service requirement.")
        elif "marri" in purpose_lower or "shadi" in purpose_lower or "vivah" in purpose_lower:
            if total_service_years < 7:
                status = "NOT_ELIGIBLE_MIN_SERVICE"
                notes.append("Marriage advance requires at least 7 years of continuous EPFO service.")
            else:
                max_limit = pf_employee_share * 0.50
                notes.append("Marriage Advance: Up to 50% of employee PF share.")
        elif "house" in purpose_lower or "ghar" in purpose_lower or "makan" in purpose_lower:
            if total_service_years < 5:
                status = "NOT_ELIGIBLE_MIN_SERVICE"
                notes.append("Housing advance requires at least 5 years of continuous EPFO service.")
            else:
                max_limit = min(monthly_basic_plus_da * 36.0, pf_employee_share + pf_employer_share)
                notes.append("Housing Advance: Up to 36 months Basic+DA or total balance.")
        else:
            # General / Special pandemic/emergency rule
            max_limit = min(monthly_basic_plus_da * 3.0, pf_employee_share * 0.75)
            notes.append("Standard Advance: 3 months Basic+DA or 75% of employee share.")

        return {
            "purpose": purpose,
            "status": status,
            "max_withdrawable_amount": round(max_limit, 2),
            "service_years_checked": total_service_years,
            "notes": notes
        }
