"""
SAATHI AI - Utility & Citizen Calculators API Routes
"""
from fastapi import APIRouter
from api.schemas import (
    ElectricityCalcRequest, ElectricityCalcResponse,
    TenancyCalcRequest, TenancyCalcResponse,
    PFAdvanceCalcRequest, PFAdvanceCalcResponse
)
from saathi.tools.calculators import UtilityCalculators

router = APIRouter(prefix="/tools", tags=["Utility & Citizen Calculators"])

@router.post("/calculate-electricity", response_model=ElectricityCalcResponse, summary="Audit Electricity Bill & Telescopic Slab Tariffs")
async def calculate_electricity(req: ElectricityCalcRequest):
    """
    Computes telescopic slab energy charges, fixed demand tariffs, and state duty under Indian DERC/DISCOM regulations.
    Detects IDF / Defective Meter estimated provisional billing.
    """
    res = UtilityCalculators.calculate_electricity_bill(
        units_consumed=req.units_consumed,
        sanctioned_load_kw=req.sanctioned_load_kw,
        is_average_or_idf=req.is_average_or_idf
    )
    return ElectricityCalcResponse(
        units=res["units"],
        sanctioned_load_kw=res["sanctioned_load_kw"],
        energy_charge=res["energy_charge"],
        fixed_charge=res["fixed_charge"],
        electricity_duty=res["electricity_duty"],
        total_estimated_bill=res["total_estimated_bill"],
        slab_breakdown=res["slab_breakdown"],
        is_average_or_idf=req.is_average_or_idf,
        warning=res["warning"]
    )

@router.post("/calculate-tenancy-deposit", response_model=TenancyCalcResponse, summary="Audit Rental Security Deposit & Model Tenancy Deductions")
async def calculate_tenancy(req: TenancyCalcRequest):
    """
    Audits security deposit refunds under the Model Tenancy Act (MTA) & Indian tenancy norms:
    - Caps residential deposit at max 2 months rent.
    - Bars illegal routine painting deductions.
    - Computes net refundable amount with statutory 30-day timeline.
    """
    res = UtilityCalculators.calculate_security_deposit_refund(
        monthly_rent=req.monthly_rent,
        deposit_paid=req.security_deposit_paid,
        actual_damages=req.actual_damages,
        unpaid_bills=req.unpaid_bills,
        property_type=req.property_type
    )
    return TenancyCalcResponse(
        legal_max_deposit=res["legal_max_deposit"],
        excess_held_by_landlord=res["excess_held_by_landlord"],
        total_allowable_deductions=res["total_allowable_deductions"],
        refundable_amount=res["refundable_amount"],
        statutory_deadline_days=res["statutory_deadline_days"],
        notes=res["notes"]
    )

@router.post("/calculate-pf-advance", response_model=PFAdvanceCalcResponse, summary="Estimate EPFO Form 31 Online PF Advance Withdrawable Limit")
async def calculate_pf_advance(req: PFAdvanceCalcRequest):
    """
    Estimates maximum allowable non-refundable PF advance under EPFO Paragraph 68B/68H/68K regulations.
    """
    res = UtilityCalculators.estimate_pf_advance_limit(
        pf_employee_share=req.employee_pf_share,
        pf_employer_share=req.employer_pf_share,
        monthly_basic_plus_da=req.basic_plus_da,
        purpose=req.purpose,
        total_service_years=req.service_years
    )
    return PFAdvanceCalcResponse(
        max_withdrawable_amount=res["max_withdrawable_amount"],
        status=res["status"],
        purpose=res["purpose"],
        notes=res["notes"]
    )
