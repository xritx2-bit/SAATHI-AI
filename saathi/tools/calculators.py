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
        Calculates electricity bill based on telescopic slab tariffs in India.
        """
        # Standard benchmark slab rates (Rs per unit)
        # 0-100 units: Rs 3.50
        # 101-200 units: Rs 5.00
        # 201-400 units: Rs 6.50
        # 400+ units: Rs 8.00
        # Fixed Charge: Rs 75 per kW of sanctioned load
        # Electricity Duty & Tax: 6% of energy charges
        
        fixed_charge = sanctioned_load_kw * 75.0
        energy_charge = 0.0
        slab_breakdown = []
        
        remaining_units = units_consumed
        
        # Slab 1: 0 - 100
        u1 = min(remaining_units, 100)
        if u1 > 0:
            c1 = u1 * 3.50
            energy_charge += c1
            slab_breakdown.append(f"0–100 units: {u1:.0f} units @ ₹3.50 = ₹{c1:.2f}")
            remaining_units -= u1
            
        # Slab 2: 101 - 200
        u2 = min(remaining_units, 100)
        if u2 > 0:
            c2 = u2 * 5.00
            energy_charge += c2
            slab_breakdown.append(f"101–200 units: {u2:.0f} units @ ₹5.00 = ₹{c2:.2f}")
            remaining_units -= u2
            
        # Slab 3: 201 - 400
        u3 = min(remaining_units, 200)
        if u3 > 0:
            c3 = u3 * 6.50
            energy_charge += c3
            slab_breakdown.append(f"201–400 units: {u3:.0f} units @ ₹6.50 = ₹{c3:.2f}")
            remaining_units -= u3
            
        # Slab 4: > 400
        u4 = remaining_units
        if u4 > 0:
            c4 = u4 * 8.00
            energy_charge += c4
            slab_breakdown.append(f"400+ units: {u4:.0f} units @ ₹8.00 = ₹{c4:.2f}")
            
        duty = (energy_charge + fixed_charge) * 0.06
        total_bill = fixed_charge + energy_charge + duty
        
        warning = None
        if is_average_or_idf:
            warning = "⚠️ Note: Your bill is based on provisional/average assessment (IDF). You have the right to request actual meter verification to avoid overcharging."
            
        return {
            "units": units_consumed,
            "sanctioned_load_kw": sanctioned_load_kw,
            "fixed_charge": round(fixed_charge, 2),
            "energy_charge": round(energy_charge, 2),
            "electricity_duty": round(duty, 2),
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
